# 05 · Темы: технический контракт

> Система тем едина для всех продуктов LOVII. Реализация намеренно stateless на стороне JS/React: состояние живёт в `data-theme` на `<html>` + `localStorage`, видимость логотипов и иконок управляется чистым CSS. Это даёт нулевую вспышку темы при загрузке и гидратации.

## Контракт

| Элемент | Канон |
|---|---|
| Атрибут | `data-theme="light" \| "dark"` на `<html>`; отсутствие = light |
| Хранилище | `localStorage['lovii_theme']`; валидны только `'dark'`/`'light'`, прочее/отсутствие → системная |
| Определение стартовой | явный выбор → `prefers-color-scheme` → light |
| Anti-FOUC | инлайн-скрипт в `<head>` **до** подключения CSS |
| meta theme-color | light `#f64a8a` · dark `#171219`; обновлять при переключении (`id="meta-theme"`) |
| color-scheme | `light`/`dark` на `:root`/`[data-theme="dark"]` (нативные скроллбары/контролы) |
| Ключ токенов | значения тем описаны только в tokens.css; логика переключения не знает конкретных цветов |

## Anti-FOUC скрипт (копировать как есть)

```html
<script>
  (function () {
    try {
      var t = localStorage.getItem('lovii_theme');
      if (t !== 'dark' && t !== 'light') {
        t = window.matchMedia && matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
      }
      document.documentElement.dataset.theme = t;
    } catch (e) { document.documentElement.dataset.theme = 'light'; }
  })();
</script>
```

`try/catch` обязателен: приватный режим Safari кидает исключение на localStorage.

## Переключение (канон app.js)

```js
const THEME_KEY = 'lovii_theme';
const THEME_META = { light: '#f64a8a', dark: '#171219' };

function currentTheme() {
  return document.documentElement.dataset.theme === 'dark' ? 'dark' : 'light';
}
function applyTheme(t) {
  document.documentElement.dataset.theme = t;
  const meta = document.getElementById('meta-theme');
  if (meta) meta.setAttribute('content', THEME_META[t]);
}
function toggleTheme() {
  const t = currentTheme() === 'dark' ? 'light' : 'dark';
  try { localStorage.setItem(THEME_KEY, t); } catch { /* приватный режим */ }
  applyTheme(t);
}
```

## Логотипы и иконки — CSS, без JS-состояния

Оба логотипа и обе иконки всегда в DOM; видимость переключает атрибут:

```css
.logo .logo-dark-img { display: none; }
[data-theme="dark"] .logo .logo-dark-img { display: block; }
[data-theme="dark"] .logo .logo-light-img { display: none; }

.icon-btn .theme-ico-sun { display: none; }        /* луна видна в светлой */
[data-theme="dark"] .icon-btn .theme-ico-sun { display: block; }
[data-theme="dark"] .icon-btn .theme-ico-moon { display: none; }
```

Файлы логотипов (канон):

- Светлая тема: `assets/lovii-logo-light.svg`
- Тёмная тема: `assets/logo-dark.svg` — **канон, md5 `145731d888e5d913ce85de3a9789d097`**, побайтово идентичен `assets/lovii-logo-black.svg`. Это авторский логотип из коммита `a902cf7` репо lovii_demo.
- ⚠️ Файл `assets/lovii-logo-dark.svg` (кремовые штрихи #f3ebf0) — удалён из канона 2026-09-04 (был высветленным дублем). Не использовать и не восстанавливать.

Размеры: `height: 32px` (≤360px — 28px), `width: auto`.

## Кастомный вариант Tailwind-проекта (lovii-site)

- Тёмный вариант: `@custom-variant dark (&:where([data-theme="dark"], [data-theme="dark"] *));` — привязка к data-theme, не к медиа.
- Тот же инлайн-anti-FOUC в `layout.tsx`; кнопка темы без useState — просто onClick с toggleTheme + прямой DOM-апдейт.
- React-гидрация не должна трогать `data-theme` (иначе вспышка) — только инлайн-скрипт в head.

## Do

- Всегда анти-FOUC до CSS; всегда `try/catch`.
- Всегда обновлять meta theme-color вместе с data-theme.
- Тестировать: холодный старт в обеих темах, системная тема, приватный режим, PWA-старт.
- SW/PWA: при изменении набора темовых ассетов поднимать версию кэша.

## Don't

- ❌ Не хранить тему в React-state/cookies/URL — только data-theme + localStorage.
- ❌ Не решать видимость логотипа JS'ом (мерцает при гидратации).
- ❌ Не ставить `data-theme` на body/контейнеры — только `<html>`.
- ❌ Не использовать инверсию `filter: invert` для тёмной темы.
- ❌ Не забывать `color-scheme` (ломает нативные контролы и скроллбары).

## Чек-лист раздела

- [ ] Anti-FOUC инлайн в head, localStorage с try/catch, валидация значения
- [ ] meta theme-color обновляется; color-scheme задан для обеих тем
- [ ] Логотипы/иконки переключаются CSS-ом; в DOM оба варианта
- [ ] Тёмный логотип — канон `assets/logo-dark.svg` (md5 145731d8…)
- [ ] Нет вспышки при загрузке и при гидратации (проверено на медленном 3G + cold start)
