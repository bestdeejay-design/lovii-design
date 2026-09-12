# 10 · UX-паттерны: scroll, адаптив, PWA, hash-роутинг

> Version: 1.4.0 · Updated: 2026-09-04 · Живая лаборатория: `examples/06-ux-lab.html` · Каркас: docs/04 · Сниппеты компонентов: docs/07
> v3 роадмэпа. Всё, что живёт **вокруг** компонентов: как экран открывается по ссылке, скроллится, перестраивается по ширине, ставится как приложение и адресуется хешем.

Компоненты (docs/09) отвечают на вопрос «как выглядит», UX-паттерны — «как себя ведёт». Все четыре раздела ниже проверены живьём в `examples/06-ux-lab.html`: там работают настоящие якоря с `scroll-margin-top`, кнопка «наверх», индикатор брейкпоинта, честный `beforeinstallprompt` и hash-роутер на `#/…`. Новый экран собирай так: каркас роли из `examples/01…05` + поведение по этому документу.

---

## 1. Якоря и scroll

### 1.1 Sticky-слои и scroll-margin-top

Канонический каркас — sticky-хедер 56px (`--lv-header-h`), иногда + подшапка «назад» 48px (`--lv-subheader-h`). Нативный прыжок по якорю прижимает цель к верху окна **под** шапкой. Правило: каждой якорной цели задаётся `scroll-margin-top` из токенов каркаса — никаких магических чисел в отступе.

```css
/* Канон: якорная цель не прячется под sticky-хедером */
section[id] { scroll-margin-top: calc(var(--lv-header-h) + 12px); }
/* Если на экране есть подшапка «назад» — суммарно:
   scroll-margin-top: calc(var(--lv-header-h) + var(--lv-subheader-h) + 12px); */
```

Smooth-скролл включается на `<html>` per-page (`html { scroll-behavior:smooth; }`) и **обязан** отключаться при reduce-motion — `tokens.css` глушит анимации, но `scroll-behavior` не является анимацией, поэтому отключается отдельно:

```css
@media (prefers-reduced-motion: reduce) { html { scroll-behavior:auto; } }
```

### 1.2 Внешний вход по якорю (deep link)

Ссылки вида `страница.html#блок` из писем, соцсетей и хаба — частый вход. Проблема: если контент рендерится или сдвигается после загрузки (шрифты, картинки, роутер), браузер успевает прыгнуть по якорю **до** отрисовки, и пользователь попадает не туда. Канон: повторить позиционирование после `load` (или двойного `requestAnimationFrame`).

```js
addEventListener('load', function () {
  var h = location.hash;
  if (h && h.indexOf('#/') !== 0) {          // якорь (роуты #/… — см. §4)
    var t = document.querySelector(h);
    if (t) t.scrollIntoView({ block: 'start' }); // scroll-margin-top учтётся
  }
});
```

### 1.3 Кнопка «наверх» (back-to-top)

Появляется после прокрутки ≈480px (2–3 экрана контента), у правого края над нижней навигацией, в зоне, свободной от nav.js-кнопки (та левее по потоку футера или в хедере). Канон: капсула 48px, `gradient-brand`, иконка `i-arrow-up` 20px `on-brand`, тень покоя `shadow-lift`.

```css
.to-top { position:fixed; right:16px; bottom:calc(var(--lv-nav-h,64px) + 16px + env(safe-area-inset-bottom,0px));
  z-index:70; width:48px; height:48px; border-radius:999px; border:0; cursor:pointer;
  background-image:var(--lv-gradient-brand); color:var(--lv-on-brand);
  display:flex; align-items:center; justify-content:center; box-shadow:var(--lv-shadow-lift);
  opacity:0; pointer-events:none; transform:translateY(8px);
  transition:opacity .2s ease, transform .2s ease; }
.to-top.show { opacity:1; pointer-events:auto; transform:translateY(0); }
.to-top .ico { width:20px; height:20px; }
```

```js
var toTop = document.getElementById('toTop');
addEventListener('scroll', function () {
  toTop.classList.toggle('show', scrollY > 480);
}, { passive: true });
toTop.addEventListener('click', function () { scrollTo({ top: 0, behavior: 'smooth' }); });
```

На широких экранах с плавающей капсулой навигации `--lv-nav-h` продолжает работать: формула `bottom` уже содержит safe-area. `z-index:70` — один слой с nav.js-кнопкой, ниже шита (80–85) и тоста (60 — тост всегда поверх по центру).

### 1.4 Индикатор позиции (опционально)

Для длинных служебных экранов (чек-листы, документация) допустима пилюля «где я» — `position:fixed`, `surface`-фон, `dim`-текст 12px. Обновление — в том же scroll-листенере, что и «наверх», только через `requestAnimationFrame`-троттлинг.

Do: `scroll-margin-top` на всех `section[id]`; passive-листенеры; reduce-motion отключает smooth.
Don't: анимировать `top/height` при скролле; вешать scroll-логику без `{ passive:true }`; ставить «наверх» в левый угол (там жест «назад» на iOS).

---

## 2. Адаптив: брейкпоинты и каркас

### 2.1 Карта брейкпоинтов

| Диапазон | Каркас | Что меняется |
|---|---|---|
| 0–639 | капсула `--lv-container` 480px, `--lv-pad-x` 16px | bottom-nav 64px, сетки 2 колонки, hero 26px, лого 28px (≤360px — 26px) |
| 640–899 | широкий поток `--lv-container-wide` 1120px / линейный `--lv-container-narrow` 760px | full width, сетки 3–4 колонки, hero 32px, view `padding-bottom:96px` |
| ≥900 | широкий поток | **bottom-nav → плавающая десктоп-капсула 60px** по центру, тень `shadow-nav` |

Брейкпоинты — **литералы 640 / 900** (в `@media` нельзя использовать `var()`, поэтому это не токены, а задокументированные константы каркаса). Тест-ширина мобильного — 390px: горизонтального скролла не существует ни на одной странице ДС.

### 2.2 Правила

- Сетки и контейнеры — от `--lv-container*`-токенов; колонки меняются только на 640/900.
- Нижние бары и плавающие кнопки всегда учитывают `env(safe-area-inset-bottom)`; `<meta viewport>` — с `viewport-fit=cover`.
- Трансформация bottom-nav → капсула: сниппет в `examples/01` (секция `.bottom-nav`, media ≥900 превращает бар в `position:fixed; left:50%; transform:translateX(-50%)` капсулу). Тень меняется с `shadow-nav` на `shadow-lift`.
- Никаких собственных промежуточных брейкпоинтов (480/768/1024 — запрещены): два порога + токены каркаса покрывают всё. 1024 исторически упоминается только как синоним «десктоп-теста».
- Горизонтальные ленты — `overflow-x:auto` + `.no-scrollbar` + `lv-edge-fade` (маска краёв из tokens.css).

### 2.3 3D-карта в карусели: вертикальный запас

Горизонтальная карусель (`overflow-x: auto`) по спецификации CSS клиппит и по вертикали
(`visible` во второй оси вычисляется в `auto`). При flip/tilt перспектива выносит углы карты
за плоский бокс. Замер (демо, `perspective: 1100px`, tilt-max ±4°): мобильная карта — самая
большая (390 → 386×243), на 90° флипа проекция уходит вверх до ~41px — карта подрезается
«окном» карусели. Канон: `padding-block: 46px` на карусели (clip-box = padding-box) +
компенсация ритма `margin-block: -42px` — заголовок и соседние блоки не сдвигаются
(сверху/снизу остаётся по 4px, как до правки). Запас проверен на 390/674/1440: на всех углах
флипа с tilt-max углы карты не касаются краёв, вертикального скролла внутри карусели нет
(`scrollHeight ≤ clientHeight`).

Do: запас на карусели-контейнере. Don't: `overflow: hidden` на обёртках карты; запас меньше
проекции на широких вьюпортах.

**Горизонталь — карта не full-bleed (v1.16.1, фидбек владельца «карта липнет к краям экрана,
вне блока получилась»):** вертикальный запас расширяет clip-box и по горизонтали тоже — если
не дать карте боковую вставку, она визуально прилипает к краям экрана и выпадает из общего
контент-блока. Канон: `padding-inline: 16px` на карусели — карта живёт в блоке экрана, как
хедер и секции (на 390 это 358px, не 386). В двухколонной раскладке ≥640 колонка уже даёт
свои 16px — там `padding-inline: 0` на карусели (иначе двойная вставка 32px). Бонус: карта
358×226 вместо 386×243 уменьшает проекцию флипа — запас клипа растёт с ~5px до ~24px.

---

## 3. PWA-установка

### 3.1 Манифест и требования

| Поле | Канон |
|---|---|
| `name` / `short_name` | «Лови» / «Лови» |
| `start_url` | `/` (вход в витрину) |
| `display` | `standalone` |
| `background_color` | светлый `--lv-bg` → `#f8f5f0` |
| `theme_color` | бренд `#f64a8a` (= meta theme-color светлой) |
| `icons` | 192 + 512, PNG; иконка 512 помечена `"purpose":"maskable"` |

`meta theme-color` остаётся парой `#f64a8a / #171219` и обновляется темой (docs/05) — он красит системный UI и в standalone-режиме.

### 3.2 Service worker и кэш

SW демки кэширует ядро (HTML, `tokens.css`, лого, `icons.svg`, манифест). Железные правила кэша — AGENTS.md №8: **любое** изменение статики демки = поднять `?v=N` у ссылок в `index.html` **и** `CACHE lovii-vN` в `sw.js`, иначе PWA-пользователи застрянут на старом. Новый ассет (например, манифест или иконка установки) добавляется в precache-список ядра тем же коммитом.

### 3.3 Кнопка установки (canonical flow)

Свою кнопку показываем только когда браузер отдал `beforeinstallprompt`; внутри уже установленного приложения — скрываем всё установочное (состояние `standalone`); iOS в prompt не участвует — показываем инструкцию «Поделиться → На экран „Домой“» с иконкой `i-share`.

```js
var deferred = null, btn = document.getElementById('installBtn'),
    isIOS = /iphone|ipad|ipod/i.test(navigator.userAgent),
    standalone = matchMedia('(display-mode: standalone)').matches || navigator.standalone === true;

addEventListener('beforeinstallprompt', function (e) {
  e.preventDefault(); deferred = e;
  btn.hidden = false;                       // 36–48px, gradient-brand, i-download
});
btn.addEventListener('click', function () {
  if (!deferred) return;
  deferred.prompt();
  deferred.userChoice.then(function (res) {
    showToast(res.outcome === 'accepted' ? 'Устанавливаем…' : 'Установка отменена');
    deferred = null; btn.hidden = true;
  });
});
addEventListener('appinstalled', function () { showToast('Приложение установлено'); });
if (standalone || isIOS) { /* standalone → чип «Уже установлено»; iOS → инструкция */ }
```

Состояния карты установки (все реализованы в `examples/06`): `standalone` → tiffany-чип «Уже установлено»; iOS → карточка-инструкция; prompt доступен → кнопка; иначе → dim-подпись «недоступно в этом браузере». Do: одна точка установки на экран, состояние проверяется на каждом входе. Don't: показывать кнопку в standalone; агрессировать (баннеры/модалки «установи»); рендерить кнопку до `beforeinstallprompt`.

---

## 4. Hash-роутинг

### 4.1 Канон

Хеш-роуты lovii-site — `#/…`. Это единственный формат, дающий deep links без сервера: ссылка `lovii-site…/#/gifts` открывает экран сразу. Правила:

1. Роут — только из `location.hash`, рендер по `hashchange` **и** на старте (внешний вход!). Неизвестный роут → дефолтный, никогда не пустой экран.
2. Якоря страницы — простые `#блок`, роуты — `#/путь`. Роутер обязан игнорировать хеши без префикса `#/`, якорный код — хеши с ним.
3. Смена роута = верх страницы: `history.scrollRestoration = 'manual'` + `scrollTo({top:0, behavior:'smooth'})` (reduce-motion гасит smooth — см. §1.1).
4. Назад/вперёд работают бесплатно — `hashchange` и есть история. Ничего не пишем в `history.pushState` вручную.
5. Тема не зависит от роута: anti-FOUC и `meta theme-color` — один раз на входе (docs/05).

### 4.2 Мини-роутер (canonical snippet)

```js
var ROUTES = ['#/obzor', '#/nagrad', '#/istoriya'], DEFAULT_ROUTE = ROUTES[0];
var lastRoute = null;
function renderRoute() {
  var h = location.hash;
  if (h.indexOf('#/') !== 0) {                       // это якорь — не наш случай
    if (!(h === '' && lastRoute)) return;            // назад из роута в «начало» — сброс на дефолт
    h = DEFAULT_ROUTE;
  }
  if (ROUTES.indexOf(h) < 0) h = DEFAULT_ROUTE;      // неизвестный → дефолт
  document.querySelectorAll('[data-route]').forEach(function (p) {
    p.hidden = p.getAttribute('data-route') !== h;
  });
  document.querySelectorAll('[data-tab]').forEach(function (t) {
    t.classList.toggle('active', t.getAttribute('data-tab') === h);
  });
  lastRoute = h;
  scrollTo({ top: 0, behavior: 'smooth' });
}
addEventListener('hashchange', renderRoute);
renderRoute();                                       // внешний вход по #/…
```

Правило «назад в начало»: без него кнопка «назад» из первого роута возвращает URL без хеша, а панели остаются в прошлом состоянии — найдено при приёмке лаборатории (v1.4.0).

Таб — `<a href="#/obzor" data-tab="#/obzor">`: ссылка, а не кнопка, чтобы работали средний клик и «открыть в новой вкладке» (та же ссылка = тот же роут). Панели — `[data-route]`, переключение `hidden` без анимаций DOM-порядка; вход панелей — `.lv-enter`, если нужен каскад.

Do: дефолтный роут; вкладки-ссылки; scroll top при смене. Don't: пушить историю вручную; мешать `#anchor` и `#/route` в одном парсере; прятать контент до JS (панель дефолтного роута должна быть видна и без скрипта — прогрессивное улучшение).

---

## 5. OTP-ввод с авто-подстановкой (SMS · WebOTP)

> Паттерн един для всех продуктов платформы: клиентское приложение, B2B-кабинет, будущие формы.
> Две обязательные половины: поле с правильными атрибутами (§5.1) + хук WebOTP (§5.2); третья —
> формат SMS на бэкенде (§5.4). Одна половина без остальных авто-подстановку не даёт.

### 5.1 Анатомия поля (обязательные атрибуты)

| Атрибут | Значение | Зачем |
|---|---|---|
| `type` | `text` | `number` даёт спиннеры и ломает вставку из буфера |
| `inputmode` | `numeric` | цифровая клавиатура на тач-устройствах |
| `autocomplete` | `one-time-code` | iOS: системная подстановка кода из SMS в сфокусированное поле |
| `name` | `otp` | стабильное имя для автозаполнения ОС |
| `maxlength` | длина кода (`otp.code_length`) | единый источник длины — конфиг бэкенда |
| фокус | `autofocus` / `focus()` при монтировании | подстановка работает только в сфокусированное поле |

ОДИН инпут, не 4 отдельные ячейки: split-ячейки ломают автоподстановку — код приходит одним
значением в одно поле. Визуальная маска `####` допустима. Автосабмит при достижении длины — канон.

### 5.2 WebOTP API (Android · Chrome; где не поддержано — тихий фолбэк)

```js
// Хук: запускать при монтировании экрана ввода кода; вернуть cancel() для размонтирования.
async function bindOtpAutofill(input, { length = 4, timeoutMs = 120000 } = {}) {
  if (!('OTPCredential' in window) || !input) return () => {};
  const ac = new AbortController();
  const timer = setTimeout(() => ac.abort(), timeoutMs); // не держим приёмник вечно
  try {
    const { code } = await navigator.credentials.get({ otp: { transport: ['sms'] }, signal: ac.signal });
    if (code && input.isConnected) {
      input.value = code.slice(0, length);
      input.dispatchEvent(new Event('input', { bubbles: true })); // автосабмит на длине
    }
  } catch { /* AbortError / NotAllowed — тихо: поле остаётся ручным */ }
  clearTimeout(timer);
  return () => ac.abort();
}
```

Правила: вызов при монтировании экрана кода; отмена на размонтировании и по таймауту;
ошибки — тихо (ручной ввод остаётся); требует HTTPS.

### 5.3 Диагностика «код не вставляется»

| Симптом | Причина | Лечение |
|---|---|---|
| iOS: код не предлагается | поле не в фокусе при получении SMS; нет атрибута | фокус при монтировании + `autocomplete="one-time-code"` |
| Android: ничего не происходит | нет вызова WebOTP | хук §5.2 |
| WebOTP не срабатывает, всё верно | в SMS нет привязки домена | формат §5.4 |
| В браузере работает, в PWA нет | нет привязки приложения к домену | `web-app-origin-association` / assetlinks §5.5 |

### 5.4 Формат SMS (бэкенд — обязательная часть паттерна)

Без привязки домена Android не считает SMS адресованным сайту — WebOTP молчит:

```
LOVII: код 1234 для входа. Никому его не сообщайте.

@lovii.mobiap.com #1234
```

- последняя строка строго `@домен #код`, домен = точный хост страницы ввода;
- у каждого окружения свой хост (staging ≠ prod), иначе код «уходит не туда»;
- длина кода — из `otp.code_length`, тот же источник, что `maxlength` поля.

### 5.5 Каналы и PWA

| Канал | Авто-подстановка | Что нужно |
|---|---|---|
| SMS | полная (iOS + Android) | §5.1 + §5.2 + §5.4 |
| MAX / Telegram / VK | web-стандарта нет | фокус + кнопка «Вставить код» (clipboard) + автосабмит; код в тексте бота — отдельной строкой |
| PWA (installed) | как у браузера + привязка | `web-app-origin-association` (web) / assetlinks (Android-пакет) |

Мессенджерные каналы в стандарт автоподстановки не входят: код копируется вручную —
UX компенсирует (автофокус, паст-кнопка, автосабмит на длине).

### 5.6 B2B-кабинет

Тот же компонент без вариаций: анатомия §5.1, хук §5.2, свой домен в §5.4
(`@b2b.<домен>`), длина из `otp.code_length`. Локальные вариации поля запрещены.

---

## 6. Антипаттерны (симптом → причина → как надо)

| Симптом | Причина | Как надо |
|---|---|---|
| Якорный заголовок ушёл под шапку | нет `scroll-margin-top` | §1.1 — `calc(var(--lv-header-h) + 12px)` |
| Внешняя ссылка `…#/gifts` открыла «Обзор» | роутер не вызван на старте | §4.2 — `renderRoute()` сразу после объявления |
| Браузер «прыгает» при смене таба | нет `scrollRestoration` + `scrollTo` | §4.1 п.3 |
| Кнопка установки видна внутри PWA | нет проверки `display-mode: standalone` | §3.3 |
| На iOS показывается пустой prompt-флоу | iOS не поддерживает `beforeinstallprompt` | §3.3 — инструкция с `i-share` |
| Горизонтальный скролл на 390px | фиксированная ширина > `--lv-container`, минусы в grid | §2.2 — только токены каркаса |
| Smooth-скролл при reduce-motion | отключали только анимации | §1.1 — `scroll-behavior:auto` в media |

---

## 7. Чек-лист UX-приёмки

- [ ] Якоря не прячутся под sticky-слоями (`scroll-margin-top` от токенов каркаса)
- [ ] Внешний вход работает: `…#блок` попадает в блок, `…#/роут` — в роут (тест: открыть ссылку в новой вкладке)
- [ ] Назад/вперёд браузера меняют роуты и якоря без перезагрузки
- [ ] 390px — нет горизонтального скролла; ≥900px — навигация-капсула; safe-area на нижних барах
- [ ] Кнопка «наверх» появляется после ~480px и не перекрывает тост/nav
- [ ] Установка: в standalone установочный UI скрыт; на iOS — инструкция; кэш-бамп `?v=N` + `CACHE lovii-vN` для новой статики
- [ ] `prefers-reduced-motion`: smooth-скролл и все переходы отключены
- [ ] Живое поведение сверено с `examples/06-ux-lab.html`
