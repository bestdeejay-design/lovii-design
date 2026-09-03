# LOVII Design System

Дизайн-система бренда **«Лови» (LOVII)** — единый источник истины для всех клиентских продуктов: витрины-приложения [lovii.mobiap.com](https://lovii.mobiap.com), посадочной страницы [lovii-site](https://bestdeejay-design.github.io/lovii-site/) и будущих продовых экранов для всех ролей (клиент · бизнес · партнёр · амбассадор · инвестор).

Документация написана для **людей и ИИ-агентов**: у каждого раздела есть значения, правила Do/Don't и чек-лист приёмки.

**Version 1.1.0** · канон: lovii.mobiap.com · обновлено 2026-09-04 · [CHANGELOG](CHANGELOG.md)

---

## Быстрый старт

```html
<!-- 1. Подключить токены -->
<link rel="stylesheet" href="tokens/tokens.css">

<!-- 2. Anti-FOUC скрипт в <head> ДО CSS (канон docs/05-theming.md) -->
<script>(function(){try{var t=localStorage.getItem('lovii_theme');
if(t!=='dark'&&t!=='light'){t=matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light';}
document.documentElement.dataset.theme=t;}catch(e){document.documentElement.dataset.theme='light';}})();</script>
```

```css
/* 3. Использовать ТОЛЬКО токены */
.btn { background-image: var(--lv-gradient-brand); border-radius: 999px; color: var(--lv-on-brand); }
```

ИИ-агентам и контрибьюторам: начать с [AGENTS.md](AGENTS.md) → [docs/01-principles.md](docs/01-principles.md) → [docs/checklist.md](docs/checklist.md).

## Состав репозитория

| Путь | Что это |
|---|---|
| `style-guide.html` | **Живой гайд** — самодостаточная страница: обе темы, свотчи, типографика, кнопки, пилюли, формы, карточки, шиты, тосты. Открыть в браузере |
| `tokens/tokens.css` | Канонические CSS-переменные (`--lv-*`) + базовые стили + анимации |
| `tokens/design-tokens.json` | Те же токены машинночитаемо (упрощённый W3C Design Tokens) |
| `docs/01-principles.md` | Принципы системы, иерархия источников |
| `docs/02-color.md` | Палитра, soft-пары, правила контраста |
| `docs/03-typography.md` | Inter, шкала размеров, веса, интерлиньяж |
| `docs/04-space-shape-motion.md` | Отступы, каркас, радиусы, тени, движение, иконки, брейкпоинты |
| `docs/05-theming.md` | Технический контракт тем: data-theme, anti-FOUC, localStorage, логотипы |
| `docs/06-application.md` | Применение в lovii_demo и lovii-site, маппинг имён, таблица расхождений |
| `docs/07-patterns.md` | **Библиотека copy-paste сниппетов**: тема, каркас, кнопки, пилюли, карточки, формы, шит, тост, навигация + антипаттерны |
| `docs/08-recipes.md` | **Рецепты для агента**: сборка экрана, новый токен/компонент, подключение ДС в репо, приёмка, перенос из легаси |
| `examples/` | **Референс-экраны по ролям**: 01 клиент · 02 бизнес · 03 партнёр · 04 амбассадор · 05 инвестор (готовые HTML, обе темы) |
| `docs/checklist.md` | Чек-лист приёмки вёрстки перед деплоем |
| `AGENTS.md` | Правила для ИИ-агентов, работающих с любым репо LOVII |
| `SKILL.md` | Скил «дизайн-система LOVII» для агента-дизайнера (готов к установке) |
| `assets/` | Канонические логотипы (light + dark, md5 зафиксирован) |
| `tools/` | Сборщик style-guide (`build-style-guide.py` + шаблон) |

## Канон и иерархия

1. **tokens/** — канон значений (изменение значения начинается здесь)
2. **docs/** — канон правил применения
3. **style-guide.html** — канон визуальной подачи
4. **lovii_demo** (lovii.mobiap.com) — эталонная реализация
5. **lovii-site** — вторая реализация, подтягивается под канон

Порядок изменения стиля: `lovii-design` → `lovii_demo` → `lovii-site` → проверка обоих продов. Известные расхождения фиксируются в [docs/06-application.md](docs/06-application.md) (таблица «Расхождения»), а не молча выбираются.

## Roadmap

- **v1.0 (готова)** — токены: цвет, типографика, пространство/форма/движение, темы, применение
- **v1.1 (готова)** — библиотека паттернов (docs/07), рецепты агента (docs/08), референс-экраны всех 5 ролей (examples/), скил v2
- **v1.2** — решение по таблице расхождений (dark-альфы soft-токенов, dark-тени)
- **v2** — компоненты: анатомия кнопок/чипов/карточек/шитов, состояния
- **v3** — UX-паттерны: якоря и scroll, адаптив, PWA-установка, hash-роутинг
- **v4** — бренд и тон: голос, тексты, юр.блок, иллюстрации

## Контакты

Владелец системы: Sergey (bestdeejay) · сопровождение: ИИ-агент проекта LOVII.
