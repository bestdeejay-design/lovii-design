# AGENTS.md — правила для ИИ-агентов проекта LOVII

Этот файл читают любые ИИ-агенты (Claude, Codex, opencode, собственные боты), работающие с клиентским кодом LOVII: `lovii_demo`, `lovii-site`, будущие продовые репозитории. Прочитай его **до** первой правки стилей.

## 1. Карта мира

| Продукт | Репо | Ветка | URL | Роль |
|---|---|---|---|---|
| Дизайн-система | `bestdeejay-design/lovii-design` | main | — (style-guide.html локально) | Источник истины |
| Витрина-приложение | `bestdeejay-design/lovii_demo` | master | https://lovii.mobiap.com | Эталон реализации, канон стилей |
| Посадочная страница | `bestdeejay-design/lovii-site` | main | https://bestdeejay-design.github.io/lovii-site/ | Информационная витрина |

Клиентские роли LOVII (для новых экранов): **клиент** · **бизнес** · **партнёр** · **амбассадор** · **инвестор**. Референс-экраны каждой роли — `examples/01…05.html` (см. `examples/README.md`); собирать новый экран начинай с каркаса референса.

- Канон стилей — **lovii.mobiap.com**. Токены канона — `tokens/tokens.css` и `tokens/design-tokens.json` в этом репозитории.
- lovii-site — Next.js static export в `site-src/` (Tailwind 4, хеш-роуты `#/…`, деплой GitHub Actions).
- lovii_demo — ванильный HTML/CSS/JS + service worker `sw.js` (кэш `lovii-vN`), ветка master деплоится напрямую.

## 2. Железные правила (нарушать нельзя)

1. **Никакого хардкода стилей.** Цвет — только `var(--lv-*)`, тень/радиус/длительность — из шкалы. Новое значение = сначала коммит в lovii-design, потом использование.
2. **Иерархия изменений:** lovii-design → lovii_demo → lovii-site → проверка обоих продов. Прямые правки стилей реализаций в обход ДС запрещены.
3. **Канон — lovii.mobiap.com.** При расхождении реализаций правится та, что ниже по иерархии, а не токен. Расхождения фиксируй в docs/06-application.md, не прячь.
4. **Темы.** Управление: `data-theme="light|dark"` на `<html>`, хранение `localStorage['lovii_theme']`, anti-FOUC инлайн-скрипт до CSS. Не хранить тему в React-state/cookies. Не использовать `filter: invert`. Логотипы/иконки — оба в DOM, видимость через CSS.
5. **Логотип.** Тёмный канон — `assets/lovii-logo-dark.svg` (md5 `145731d888e5d913ce85de3a9789d097`, идентичен `lovii-logo-black.svg`). Высветленный `lovii-logo-dark.svg` удалён из канона 2026-09-04 — не восстанавливать.
6. **Soft-пары.** `soft-pink→pink-dark`, `soft-tiffany→tiffany-text`, `soft-gold→gold-text`, `grey-soft→#999`. Не смешивать тоны.
7. **Тексты на градиентах** — только `--lv-on-brand` (вторичные — `rgba(255,255,255,.65–.7)`).
8. **Кэш демки.** Любое изменение статики демки = поднять `?v=N` в index.html и `CACHE lovii-vN` в sw.js (иначе PWA-пользователи застрянут на старом).
9. **Пуш-дисциплина.** Коммиты по одному смыслу, сообщение — тип(область): суть. Не форс-пушить master/main.
10. **Навигация ДС.** Страницы дизайн-системы (хаб, style-guide, examples) подключают `assets/nav.js` перед `</body>` — единое меню «☰». Список страниц меняется только в `assets/nav.js`.
10. **Секреты.** Токены доступа GitHub никогда не попадают в файлы — только переменные окружения/разовые команды.

## 3. Как применять (порядок работы агента)

1. Прочитай `docs/01-principles.md` — принципы и приоритет источников.
2. Для нового экрана: определи роль → возьми каркас из `examples/` (01 клиент · 02 бизнес · 03 партнёр · 04 амбассадор · 05 инвестор).
3. Компоненты собирай готовыми сниппетами из `docs/07-patterns.md`; для цвета/текста/геометрии — сверяйся с `tokens/tokens.css` (значения) и docs/02–04 (правила).
4. Для тем — docs/05 (контракт) + копируй anti-FOUC/applyTheme как есть (есть и в SKILL.md, и в docs/07 §1).
5. Типовые процедуры (новый токен, приёмка, перенос из легаси) — по рецептам `docs/08-recipes.md`.
6. Перед завершением задачи прогони `docs/checklist.md` — это приёмка.
7. Если нужного токена нет — предложи токен (имя `--lv-*` по аналогии), внеси в tokens.css + design-tokens.json + style-guide (пересборка: `python3 tools/build-style-guide.py`), и только потом используй.
8. Зафиксируй изменения: CHANGELOG.md (semver) + таблица расхождений (если затронута).

## 4. Маппинг имён (легаси ↔ канон)

- демка `css/lovii.css`: `--pink→--lv-pink`, `--ink→--lv-ink`, `--bg→--lv-bg`, `--card→--lv-card`, `--surface→--lv-surface`, `--soft-*→--lv-soft-*`, `--*-text→--lv-*-text` и т.д. (полный список docs/06).
- lovii-site `globals.css`: Tailwind `--color-lovii-*` и shadcn-слой — вторичны, выводятся из канона; классы `bg-lovii-pink`/`text-lovii-dim` использовать вместо сырых значений.
- Утилити-классы канона: `.brand-gradient`, `.shadow-soft`, `.shadow-lift`, `.lv-enter`, `.lv-float`, `.lv-dot`, `.lv-edge-fade`, `.no-scrollbar`.

## 5. Что читать дальше

- Значения и правила: docs/02-color · 03-typography · 04-space-shape-motion
- Темы: docs/05-theming
- Интеграция и расхождения: docs/06-application
- Компоненты (сниппеты): docs/07-patterns
- Рецепты типовых задач: docs/08-recipes
- Референсы по ролям: examples/README.md
- Приёмка: docs/checklist.md
- Визуально: style-guide.html (обе темы)
