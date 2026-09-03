# Changelog

Все значимые изменения дизайн-системы LOVII. Формат — Keep a Changelog, версионирование — SemVer.
Изменение значений токенов: backward-compatible — MINOR, ломающее — MAJOR, правки правил/опечаток — PATCH.

## [1.0.0] — 2026-09-04

### Added
- Токены: `tokens/tokens.css` (канонические CSS-переменные `--lv-*`, обе темы, анимации, базовые стили) и `tokens/design-tokens.json` (машиночитаемая версия, упрощённый W3C Design Tokens).
- Документация: принципы (01), цвет (02), типографика (03), пространство/форма/движение (04), контракт тем (05), применение в репозиториях + таблица расхождений (06), чек-лист приёмки (checklist).
- Живой style-guide: `style-guide.html` — самодостаточная страница с обеими темами (сборка `tools/build-style-guide.py`; логотипы и токены инлайнятся из канона).
- Канон-ассеты: `assets/lovii-logo-light.svg`, `assets/lovii-logo-dark.svg` (md5 `145731d888e5d913ce85de3a9789d097`, идентичен `lovii-logo-black.svg`).
- Правила для ИИ-агентов: `AGENTS.md` (карта репозиториев, железные правила, порядок работы) и заготовка скила `SKILL.md`.

### Fixed
- Синхронизация логотипа тёмной темы с каноном lovii.mobiap.com (высветленный `lovii-logo-dark.svg` удалён из демки в коммите 38dc7b1 lovii_demo, логотип lovii-site откачен к канону в 6b62bf9 lovii-site; зафиксировано в docs/05 и docs/06).

### Known divergences
- Зафиксированы в docs/06-application.md: dark-альфы soft-токенов (канон .12/.12/.16 vs lovii-site .20/.18/.20), dark-тени soft/lift, mist-pink. Статус: ⚠ требует решения (v1.1).
