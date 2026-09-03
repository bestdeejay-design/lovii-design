# 06 · Применение в репозиториях LOVII

> Как подключать токены в каждой реализации и как соотносятся имена токенов дизайн-системы, демки и lovii-site. Канон — lovii.mobiap.com (lovii_demo).

## Карта продуктов

| Продукт | Репозиторий | URL | Технология | Роль |
|---|---|---|---|---|
| Витрина-приложение | `bestdeejay-design/lovii_demo` (master) | https://lovii.mobiap.com | Ванильный HTML/CSS/JS + SW (PWA) | **Эталон реализации**, канон стилей |
| Посадочная страница | `bestdeejay-design/lovii-site` (main) | https://bestdeejay-design.github.io/lovii-site/ | Next.js static export + Tailwind 4 (в `site-src/`) | Информационная витрина, будущий lovii.ru |
| Дизайн-система | `bestdeejay-design/lovii-design` | — | Токены + docs + style-guide | Источник истины |

Процесс изменения стиля: **lovii-design** (токен/правило) → lovii_demo → lovii-site → проверка обоих продов. Обратный порядок запрещён (см. docs/01 §Иерархия).

## lovii_demo (ванильный CSS)

- Канонический файл: `css/lovii.css` — в нём живут значения, дублирующие tokens.css. При обновлении токена правится и tokens.css, и lovii.css (до полного перехода демки на внешние токены).
- Маппинг имён: канонный `--lv-*` ↔ легаси демки: `--pink→--lv-pink`, `--pink-dark→--lv-pink-dark`, `--ink→--lv-ink`, `--dim→--lv-dim`, `--bg→--lv-bg`, `--page→--lv-page`, `--card→--lv-card`, `--surface→--lv-surface`, `--glass→--lv-glass`, `--line→--lv-line`, `--line-2→--lv-line-2`, `--hairline→--lv-hairline`, `--soft-pink→--lv-soft-pink`, `--mist-pink→--lv-mist-pink`, `--soft-tiffany→--lv-soft-tiffany`, `--soft-gold→--lv-soft-gold`, `--sand-soft→--lv-sand-soft`, `--grey-soft→--lv-grey-soft`, `--gold-text→--lv-gold-text`, `--tiffany-text→--lv-tiffany-text`, `--green-text→--lv-green-text`, `--green-soft→--lv-green-soft`, `--hero-top→--lv-hero-top`, `--kpi-soft→--lv-kpi-soft`, `--on-brand→--lv-on-brand`.
- Без префикса в каноне остаются только утилити-классы: `.brand-gradient` (= `background-image: var(--lv-gradient-brand)`), `.shadow-soft`, `.shadow-lift`, `.lv-enter`, `.lv-float`, `.lv-dot`, `.no-scrollbar`.
- Кэш: правки CSS → `index.html?css/lovii.css?v=N` и `sw.js CACHE lovii-vN` (сейчас v17) — иначе пользователи PWA останутся на старом.

## lovii-site (Tailwind 4)

- `site-src/src/app/globals.css` содержит `@theme inline` слой: `--color-lovii-*` проброшены в Tailwind-палитру (классы `bg-lovii-pink`, `text-lovii-dim` и т.п.), темовые `--lv-*` объявлены в `:root`/`[data-theme="dark"]`.
- Маппинг: `--color-lovii-pink→--lv-pink`, `-pink-dark→--lv-pink-dark`, `-pink-soft→--lv-soft-pink`, `-pink-mist→--lv-mist-pink`, `-tiffany(-soft/-mist)`, `-gold(-soft/-mist)`, `-chiffon` (спец), `-sand→--lv-sand`, `-ink→--lv-ink`, `-dim→--lv-dim`, `-surface→--lv-surface`.
- shadcn-слой (`--primary`, `--background`, `--card`, `--border`, `--ring`…) вторичен: его значения выведены из канона и не должны редактироваться отдельно от токенов.
- Спец-слой lovii-site: `--header-h: 4rem` (64px) и `scroll-margin-top: calc(var(--header-h) + 1px)` для якорных секций — это параметры посадочной, не противоречат канону (у витрины хедер 56px).
- Анимации канона продублированы: `.lv-enter(-1..4)`, `.lv-float(-slow)`, `.lv-dot`, `.edge-fade-x`, `:focus-visible` розовый, reduce-motion — не удалять при рефакторинге.

## Известные расхождения (фиксируем открыто)

| # | Токен/область | Канон (демка) | lovii-site | Статус |
|---|---|---|---|---|
| 1 | dark `soft-pink/tiffany/gold` | α .12 / .12 / .16 | α .20 / .18 / .20 (×~1.6 «иначе теряют контраст») | ✅ Решено v1.2 (2026-09-04): A/B-тест в тёмной теме — значения site читаемее; **приняты в канон**: .20 / .18 / .20. Разноска: демка — в ближайшем стилевом цикле (с бампом css ?v и SW) |
| 2 | dark `mist-pink` | .06 | .10 | ✅ Решено v1.2 аналогично #1: **канон = .10** |
| 3 | dark тени soft/lift | те же, что light | `rgba(0,0,0,.45)/.55` (глубже) | ✅ Решено v1.2: **канон = `rgba(0,0,0,.45)` / `lift rgba(0,0,0,.55)`** (и nav). «Сливовая» тень на тёмном фоне не читается; нейтральная глубокая даёт настоящий подъём. См. также `$dark`-поля в design-tokens.json §shadow |
| 4 | `--lv-scroll-thumb` | rgba(26,26,26,.15) / rgba(255,255,255,.18) | тот же | ✅ Совпадает (токен родился в site) |
| 5 | Хедер | 56px (витрина) | 64px (посадка) | ✅ Не расхождение: разные продукты |
| 6 | Логотип тёмной темы | `assets/logo-dark.svg` md5 `145731d8…` | `logo-dark.svg` md5 `145731d8…` (после revert 6b62bf9) | ✅ Канон синхронизирован (Task 23) |
| 7 | light `--lv-bg` (+`line/line-2` в тон) | `#f7f2f4` (розоватый) | свой фон посадки | ✅ Решено v1.3 (2026-09-04, решение владельца «слишком розовый»): канон = `#f8f5f0` — тёплый бежевый; `line` → `#ece5da`, `line-2` → `#f6f1e8`. Разноска в демку — ближайший стилевой цикл |
| 8 | Иконки в контенте | эмодзи (витрина: товары/категории) | не замечено | ✅ Решено v1.3 (решение владельца «эмоджи — по-детски»): эмоджи в UI запрещены, только SVG-спрайт `assets/icons.svg` (docs/09 §1). Контент демки — очередь разноски при следующем контентном изменении |

Правило работы с таблицей: любое обнаруженное новое расписание сюда же, со статусом ⚠, датой и автором. Решение фиксируется коммитом в lovii-design, затем разносится по репозиториям.

Решение v1.2 (2026-09-04): по п.1–3 канон приведён к значениям lovii-site (A/B-скриншот в тёмной теме: чипы .20/.18/.20 читаемее, нейтральная глубокая тень даёт подъём карточек, тогда как .12 и «сливовая» .22 визуально теряются). lovii-site уже соответствует; **lovii_demo — очередь на разноску**: обновить dark-блок css/lovii.css в ближайшем стилевом изменении (бамп `?v=N` и SW CACHE обязательны). До разноски демка продолжает выглядеть по-старому — это не баг.

## Чек-лист раздела

- [ ] Новый стиль сначала внесён в lovii-design (tokens + docs), потом в реализации
- [ ] Имена в реализации соответствуют маппингу, дублей-«синонимов» не плодим
- [ ] Кэш-версии подняты (css ?v=N, SW CACHE) при каждом изменении стилей демки
- [ ] Таблица расхождений актуальна; новые — задокументированы
