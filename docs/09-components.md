# 09 · Компоненты: анатомия и состояния

> Version: 1.3.0 · Updated: 2026-09-04 · Канон: `style-guide.html` (собран из tokens) · Референсы: `examples/`
> v2 роадмэпа. Сниппеты copy-paste — `docs/07-patterns.md`; значения — `tokens/tokens.css`.

Компонент ДС собирается **только** из канонических значений: высоты, радиусы, шрифты, тени и цвета берутся из tokens. Если компоненту нужно новое значение — сначала токен (рецепт Р3), потом компонент. Ниже — анатомия четырёх базовых семейств (кнопки, чипы, карточки, шиты) и общая сетка состояний.

---

## 1. Иконки — SVG-спрайт, эмодзи запрещены

**Эмоджи в UI запрещены** (решение владельца, v1.3): они рендерятся по-разному на платформах, ломают монохромную палитру и выглядят несолидно. Единственный источник иконок — спрайт `assets/icons.svg`.

### Подключение

```html
<!-- контурная иконка: цвет = currentColor -->
<svg class="ico" aria-hidden="true"><use href="assets/icons.svg#i-heart"/></svg>
```
```css
.ico { width:20px; height:20px; fill:none; stroke:currentColor; stroke-width:2;
       stroke-linecap:round; stroke-linejoin:round; }
```

На страницах в `examples/` путь `../assets/icons.svg`; в style-guide спрайт инлайнится сборщиком (ссылки `#i-*` без пути).

### Канонические размеры

| Контекст | Размер | Комментарий |
|---|---|---|
| Кнопка/иконка в хедере (theme, ☰) | 16px | stroke 2 |
| row-icon в списках | 17px | stroke 2 |
| Нижняя навигация | 22px | stroke 2 |
| Плитка `tile-*` | 26px | stroke 2, `color:var(--lv-on-tile)` |
| Медаль уровня | 26px | stroke 2 |
| Обложка товара `cover` | 46px | stroke 1.8 — тоньше на крупном |
| Чекбокс | 12px | stroke 3 |
| Звезда рейтинга `i-star` | 12px | заливная: `fill:var(--lv-gold)`, без stroke |

### Цвет иконки (currentColor)

| Фон | Цвет |
|---|---|
| card / surface / bg | `var(--lv-ink)` / `var(--lv-dim)` — как текст |
| Плитка `tile-*` (светлая в обеих темах) | `var(--lv-on-tile)` |
| `cv-hero` (светлая обложка) | `var(--lv-pink-dark)` |
| `gradient-ink` / `gradient-brand` (тёмная заливка) | `#ffffff` |
| Рейтинг | `var(--lv-gold)` |

### Как добавить новую иконку

1. Нарисовать 24×24, stroke 2 (крупные обложки допускают 1.8), round caps/joins, `currentColor`, без встроенных цветов.
2. Добавить `<symbol id="i-имя">` в `assets/icons.svg` (алфавитный порядок не обязателен, префикс `i-` обязателен).
3. Использовать на странице через `<use>`; в style-guide иконка появится после пересборки (`python3 tools/build-style-guide.py`).
4. Новая иконка = коммит в lovii-design, затем использования.

Текущий набор (v2, 1.4.0): `moon, sun, heart, gift, gem, mail, bear, flame, choco, flower, ring, camera, shapes, award, crown, check, x, bot, star, coffee, salad, copy, clock, arrow-up, download, share`.

---

## 2. Кнопки

### Анатомия

| Параметр | Значение | Токен/шкала |
|---|---|---|
| Высоты | 32 (sm) · 36 (base) · 48 (big) | фикс-шкала |
| Padding | 0 12px (sm) · 0 16px (base) · 0 24px (big) | — |
| Радиус | 999px (капсула) | — |
| Шрифт | 12px/700 (sm, base) · 14px/700 (big) | Inter |
| Иконка в кнопке | 16px, gap 6px | stroke 2 |
| Фон primary | `linear-gradient(135deg, #f64a8a 0%, #c92a6a 100%)` | = `--lv-gradient-brand` |
| Текст primary | `--lv-on-brand` | — |
| Фон secondary (plain) | `--lv-surface`, текст `--lv-ink` | — |

```html
<button class="cta-btn"><svg class="ico" aria-hidden="true"><use href="assets/icons.svg#i-gift"/></svg>В подарок</button>
```
```css
.cta-btn { height:36px; padding:0 16px; border-radius:999px; color:var(--lv-on-brand);
  font-size:12px; font-weight:700; transition:all .2s; display:inline-flex; align-items:center;
  justify-content:center; gap:6px; background-image:var(--lv-gradient-brand); }
.cta-btn .ico { width:16px; height:16px; }
```

### Состояния кнопки

| Состояние | Эффект | Код |
|---|---|---|
| hover (desktop) | `box-shadow:var(--lv-shadow-lift)` | `.cta-btn:hover` |
| active | `transform:scale(.95)` | `.cta-btn:active` |
| focus-visible | розовое кольцо 2px, offset 2px | канон tokens `:focus-visible` |
| disabled | `opacity:.5; pointer-events:none` | `.cta-btn.disabled` |
| loading | спиннер-иконка вместо контента, текст «Отправляем…» | см. ниже |

```css
/* Loading: вращение — transform, поэтому безопасно для reduce-motion */
.cta-btn.loading { opacity:.7; pointer-events:none; }
.cta-btn.loading .spinner { width:14px; height:14px; border-radius:999px;
  border:2px solid rgba(255,255,255,.4); border-top-color:#fff; animation:spin .8s linear infinite; }
@keyframes spin { to { transform:rotate(360deg); } }
```

Do: одна primary-кнопка на экран; secondary — `plain`; иконка в кнопке — только одна, слева.
Don't: тень в покое у primary (только hover); свои высоты вне 32/36/48; текст капсом.

---

## 3. Чипы и пилюли

### Анатомия

| Параметр | Значение |
|---|---|
| Высота | 24–28px (текстовые), 36px (интерактивные-фильтры) |
| Padding | 4px 10px · 6px 12px |
| Радиус | 999px |
| Шрифт | 11–12px / 600–700 |
| Иконка | 12–14px, gap 4–6px, `vertical-align:-2px` в строке |
| Фон/пара | строго soft-парой: `soft-pink`+`pink-dark` · `soft-tiffany`+`tiffany-text` · `soft-gold`+`gold-text` · `grey-soft`+`#999` |

```html
<span class="chip"><svg class="ico" aria-hidden="true"><use href="assets/icons.svg#i-clock"/></svg>Ожидание</span>
```
```css
.chip { display:inline-flex; align-items:center; gap:5px; padding:5px 11px; border-radius:999px;
  font-size:12px; font-weight:600; background:var(--lv-soft-tiffany); color:var(--lv-tiffany-text); }
.chip .ico { width:13px; height:13px; }
```

Do: одна soft-пара на чип; иконка наследует цвет текста чипа.
Don't: смешивать пары (например `soft-gold` + `pink-dark`); класть чип на чип.

---

## 4. Карточки

### Анатомия

| Зона | Параметры |
|---|---|
| Контейнер | `border-radius:16px`; фон `--lv-card`; бордер 1px `--lv-line`; тень покоя `--lv-shadow-soft` |
| Медиа (`cover`) | высота 120px; `cv-hero` = градиент `hero-top → card`; `cv-ink` = `gradient-ink`; иконка 46px; бейдж абсолютом 8px/8px |
| Заголовок | 15px / 700, `letter-spacing:-.01em`; 1–2 строки, ellipsis |
| Мета | 12px / 400, `--lv-dim` |
| Цифры (цена) | 16px / 800; зачёркнутая старая — 12px / dim |
| Футер карточки | flex, `justify-content:space-between`, padding-top 8px, гэп 8px |
| Действие | quick-кнопка 36px капсула (`gradient-brand`, иконка 16px) |
| Паддинг тела | 12px (grid 390px) – 16px (wide) |

### Состояния

| Состояние | Эффект |
|---|---|
| hover (desktop) | `box-shadow:var(--lv-shadow-lift)`; трансформ не обязателен |
| active (tap) | `transform:scale(.97)` |
| enter | `.lv-enter` каскад: opacity+translateY(10px), шаг 0.06s |
| выбранная | бордер 2px `--lv-pink` или soft-подложка — по макету роли |

Do: вся карточка кликабельна (обёртка `<a>`/`<button>`); бейдж поверх медиа.
Don't: тени-подъём в покое; радиусы ≠16px; кликабельная зона меньше карточки.

---

## 5. Bottom-sheet

Полный сниппет — `docs/07` §9. Анатомия: контейнер `radius 24px 24px 0 0`, фон `--lv-card`, `max-height:82vh`, `max-width:var(--lv-container)`; хендл 36×4 `grey-soft`; паддинг `8px 16px calc(20px + safe-area)`; оверлей `rgba(0,0,0,.4)`; z-index 50/55 (nav 70–85, toast 60 — см. nav.js). Анимация входа `.4s cubic-bezier(.32,.72,0,1)` только transform. Закрытие: оверлей, Escape, кнопка-действие. При открытии — `body { overflow:hidden }`.

Do: заголовок 18px/800 + крестик/готово справа; первичное действие — big-кнопка 48px внизу шита.
Don't: шиты уже капсулы или шире; вложенные шиты; анимация height/top.

---

## 6. Общая сетка состояний

| Состояние | Правило | Проверка |
|---|---|---|
| default | покой: `shadow-soft`, без трансформов | скрин в гайде |
| hover | только desktop-обязательный: lift-тень (кнопки/карточки), фон `surface→soft-pink` (иконки-кнопки) | эмуляция hover |
| active / tap | `scale(.95)` мелкие контролы, `.97` карточки; только transform | тап-тест |
| focus-visible | розовое кольцо 2px / offset 2px (кнопки), `ring-field` 4px (поля), `ring-search` 2px (поиск) — токены shadow | Tab-тест |
| disabled | `opacity:.5` + `pointer-events:none`; текст не менять | — |
| loading | спиннер (transform-анимация) или скелетон `grey-soft`; кнопка блокируется | — |
| empty | `docs/07` §11: иконка 44px dim + заголовок 18/800 + текст dim + CTA | — |
| enter | `.lv-enter(-1..4)` каскад 0.06s; отключается при `prefers-reduced-motion` | — |

**Железное правило движения:** анимируются только `transform` и `opacity` (исключение — сворачивание через `grid-template-rows`). `prefers-reduced-motion: reduce` обязателен к поддержке.

---

## 7. Чек-лист нового компонента

- [ ] Все значения — из tokens (нет «случайных» px/hex/секунд)
- [ ] Иконки — из `assets/icons.svg`; эмоджи не использованы
- [ ] Все состояния из §6, где применимо; reduce-motion не сломан
- [ ] Работает в обеих темах (проверка переключением)
- [ ] Сниппет добавлен в `docs/07` (если переиспользуемый)
- [ ] Присутствует в живом style-guide (пересборка Р8)
- [ ] Чек-лист приёмки `docs/checklist.md` пройден
