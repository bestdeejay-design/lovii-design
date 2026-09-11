# 12 · Библиотека компонентов: полный набор

> Version: 1.7.0 · Updated: 2026-09-04 · Живая библиотека: `examples/08-components.html` · Анатомия и состояния: `docs/09-components.md` · Сниппеты copy-paste: `docs/07-patterns.md` · Значения: `tokens/tokens.css`

Полный набор компонентов ДС «Лови». Собран по итогам v5 роадмэпа: владелец делегировал подбор состава агенту, дальше смотрит библиотеку живьём и решает, чего не хватает и с чем работать. Каждый компонент собран **только** из канонических токенов; если новому компоненту нужно значение, которого нет — сначала токен (рецепт Р3), потом компонент.

Живая подача: **https://bestdeejay-design.github.io/lovii-design/examples/08-components.html** — каждая группа демонстрируется вживую, со состояниями, в обеих темах. Гайд `style-guide.html` показывает базовые образцы и палитру; библиотека — расширенный и полный набор.

---

## 1. Реестр набора

Статус: **✓** — в библиотеке живьём · **○** — описан в docs/07/09, в библиотеку не вынесен (паттерн-композиция).

### Группа 1 · Кнопки (`#buttons`)

| Компонент | Варианты | Состояния |
|---|---|---|
| `cta-btn` (primary) | 32 / 36 / 48, с иконкой 16px | hover lift · active scale .95 · focus-visible · disabled · loading |
| `cta-btn.plain` (secondary) | 36 | те же |
| `ghost-btn` | 40 / 32, с иконкой | hover: розовый бордер и текст |
| `link-btn` | текст + шеврон 16 | hover: gap растёт |
| `pill-btn` | иконка 16 pink + текст 14 | hover: soft-pink |
| `icon-btn` | 36×36, иконка 18 | hover · active · с `count-badge` |
| `count-badge` | счётчик на icon-btn | gradient-brand, бордер card 2px |

### Группа 2 · Чипы, статусы, бейджи (`#chips`)

| Компонент | Варианты | Правило |
|---|---|---|
| `stat-pill` | pink / tiffany / gold / grey | h28, 12px/600, soft-пара |
| `badge-pill` | hit / new / sale / eco | h20, 10px/700, фикс-подложки badge-* |
| `status-pill` | + `lv-dot` с пульсом | h24, статус процесса |
| `st-chip` | gold / grey | h22, модерация/пауза |
| `walk-pill` | с `i-map-pin` 13px | h24, tiffany-пара |
| `open-pill` | on / off | h20, точка 6px |
| `filter-chip` | интерактивная | h36, active = gradient-brand + `aria-pressed` |

### Группа 3 · Поля и контролы (`#fields`)

| Компонент | Варианты | Состояния |
|---|---|---|
| `search-bar` | капсула h44, иконка 16 | focus-within: `ring-search` |
| `f-field` input | text / tel | focus: pink + `ring-field`; **error**: pink-бордер + подпись 11px без вины |
| `f-field` select / textarea | радиус 14 | те же |
| `check-row` + `cbx` | 20px, галочка 12px stroke 3 | checked: gradient-brand; focus-visible на `cbx` |
| `switch` | 42×24, knob 20 | checked: gradient-brand; только transform |
| `seg` (сегмент) | h30 в капсуле surface | active: card + shadow-float, `aria-selected` |
| `stepper` | − / значение / + | 1..9, tabular-nums |

### Группа 4 · Карточки (`#cards`)

| Компонент | Состав |
|---|---|
| `btn-card` товарная | cover 80 на `tile-*` + бейдж 8/8 + name/sub + футер: рейтинг или цена (+`price-old`) или `quick-btn` 36 |
| `quick-btn` | 36, gradient-brand, `i-plus` 16 |
| `promo-card` | tone-pink / tone-gold: mini-капсула + title 16/800 + desc |
| `kpi` (+ `.accent`) | label caps 10.5 + value 19/800 tabular + дельта ▲▼ |

### Группа 5 · Списки и строки (`#lists`)

| Компонент | Состав |
|---|---|
| `list-card` | контейнер строк с разделителями `line-2` |
| `row` | `row-icon` 36px (soft-пара, иконка 17) + `row-main` (title 14/600 + sub 12 dim) + справа pill / `open-pill` / шеврон 16 dim; вариант `.danger` |
| `district-row` | h56, selectable: active = pink-бордер + soft-pink + pill «Выбран» |
| Разделители | `line-2` (строки) · `hairline` (юр.блок) — демо-капы |

### Группа 6 · Навигация (`#nav`)

| Компонент | Параметры |
|---|---|
| `app-header` | sticky glass 56px, лого-пара, theme-btn |
| Subheader «назад» | 48px, back-кнопка 32px (`i-arrow-left`) |
| `app-nav-in` (bottom nav) | 5 точек, иконка 22, active: pink + `top-ind` 32×2 |
| `tabs` | h40, active: pink-dark + underline 32×2, `aria-selected` |
| z-карта | overlay 50 · sheet 51 · toast 60 · nav 70–85 (см. nav.js) |

### Группа 7 · Обратная связь (`#feedback`)

| Компонент | Параметры |
|---|---|
| `toast` (+`.d`) | ink↔card, radius 16, `shadow-toast`; тексты — матрица тона docs/11 |
| `sheet` | radius 24 24 0 0, `cubic-bezier(.32,.72,0,1)`, закрытие: оверлей/Escape/действие |
| Skeleton | `grey-soft` блоки, shimmer 1.4s (opacity-градиент) |
| `empty-state` | формула: иконка 44 dim + заголовок 16/800 + тело с перспективой + CTA; маскот `i-bear` — только дружелюбные сцены |
| Progress | track h6 `grey-soft` + fill `gradient-brand`, meta tabular-nums |
| `spinner` | в кнопке 14px / отдельный 20px, transform-вращение |

### Группа 8 · Контентные блоки (`#blocks`)

| Компонент | Состав |
|---|---|
| `section-head` | заголовок 16/800 + `link-btn` «Все» |
| `tile-*` (×5) | radius 12, иконка 26 + подпись 11/600, `on-tile` |
| `glass-demo` | `gradient-ink` + `glass-chip` (white .1), gold/tiffany-акценты |
| `stars-row` | `star-ico` заливной gold 16px, off = `grey-soft`; мета 12px |
| `avatar` | 40px, инициалы или иконка, soft-пара |
| `timeline` | `hairline` рельса; `done` = tiffany, `now` = pink-пульс, будущее = dim |
| `promo-code` | dashed line-бордер, код градиентным текстом, `copy-mini` 36 |
| `legal` | hairline-top, dim 12px, ссылки pink-dark, полные даты, без маркетинга |

### Группа 9 · Состояния (`#states`)

Живая сетка docs/09 §6: default / hover / active / focus-visible / disabled / loading / empty / enter — на одной кнопке и одном поле. Железное правило: анимируются только `transform` и `opacity`; `prefers-reduced-motion: reduce` поддерживается везде (глобально в tokens.css).

---

### Группа 11 · LOVII PAY (`#clubpay`)

| Компонент | Варианты | Правило |
|---|---|---|
| `paycard` (+ `pay-face` front/back) | лицевая / оборот | gradient-ink · flip по тапу · tilt по курсору · номер 4-4-4-4 Visa/Мир · префикс 9643 |
| `pay-badge` / `pay-head` | бейдж уровня в хедере | gold-капсула с crown |
| `acct-card` | счёт LOVII PAY | баланс 30/800 · 3 метрики · h44 капсулы-действия |
| `tx-tabs` / `tx-row` | Все / Начисления / Покупки / Списания | группы дней · иконка 36×36 soft-пара по типу |
| `tier-card` / `tier-levels` / `tier-bar` | уровни LOVII PAY→PASS→VIP | полоска уровней · прогресс gradient-gold · перки-чипы |
| `priv-card` | gold / pink / tiffany | плитка 168px в ленте hscroll |
| `msp-fav` | сердце soft-pink | 40×40, active scale .9 |

## 2. Иконки библиотеки

Спрайт `assets/icons.svg` (v6, 51 символ): контентные (heart, gift, gem, bear, coffee…) + **системные v1.7.0**: `search, chevron-right, arrow-left, plus, minus, bell, dots, home, user, bag, edit, trash, map-pin, filter, phone, calendar, info` + **LOVII PAY v1.13.0**: `i-wallet i-qr i-rotate i-percent i-send i-arrow-down-left` + **v1.13.1**: `i-ticket` (мероприятия) + **бренд-маскот v1.9.1**: `i-lo` (голубь Ло — fill-знак 512, единственное исключение из stroke-системы). Все 24px, stroke 2, round, currentColor; `star` — заливной gold. Размеры по контекстам — docs/09 §1. Эмоджи запрещены (AGENTS пр.11).

---

## 3. Как расширять набор (порядок жёсткий)

1. **Значения** — если нужен новый px/цвет/тень: сначала токен в `tokens/tokens.css` (+ `design-tokens.json`, sync-правило Р3).
2. **Сниппет** — переиспользуемый паттерн описать в `docs/07-patterns.md` (copy-paste).
3. **Анатомия** — новый базовый компонент (высоты, зоны, состояния) — в `docs/09-components.md`.
4. **Библиотека** — живое демо в `examples/08-components.html` в подходящую группу (+ новая группа по правилам ниже).
5. **Стражи** — `tools/check-sync.py` и `scripts/check_examples.py` обязаны быть зелёными; реестр §1 дополнить строкой.
6. **Приёмка** — чек-лист `docs/checklist.md`: обе темы, 390px без h-scroll, консоль чистая.

### Новая группа в библиотеке

- Добавить чип в `.anchor-rail` (иконка из спрайта) и `section[id]`.
- Название группы — существительное во множественном числе («Поля и контролы»).
- В каждой панели — `.spec` со значениями токенов (моно 10.5px, dim).
- Не копировать значения токенов в CSS панели — только `var(--lv-*)`.

### Чего в наборе НЕТ (и не должно быть без решения владельца)

Модальные диалоги по центру экрана (в каноне — bottom-sheet), dropdown-меню (в каноне — шиты и rows), таблицы данных (в каноне — KPI-карточки и строки), даты-календарь как виджет. Эти паттерны противоречат мобильной капсуле 480px; запрос — через владельца. Исключение: таблицы данных разрешены в лонгриде/на сайте продукта по паттерну `.data-table` (docs/13 §3) — там класс артефакта иной.
