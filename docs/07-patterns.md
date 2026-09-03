# 07 · Библиотека паттернов (copy-paste сниппеты)

> Готовые фрагменты кода, из которых собираются все экраны LOVII. Каждый сниппет уже написан на токенах — копируй как есть и меняй только контент/классы. Живые версии — в `style-guide.html` и `examples/01…05.html`. Правила применения — docs/02–04.

## Содержание

1. [Тема: подключение и переключение](#1-тема)
2. [Каркас экрана](#2-каркас)
3. [Хедер и подшапка](#3-хедер)
4. [Кнопки](#4-кнопки)
5. [Пилюли и статусы](#5-пилюли)
6. [Карточки](#6-карточки)
7. [Формы и поиск](#7-формы)
8. [Сегменты-фильтры](#8-сегменты)
9. [Bottom-sheet](#9-bottom-sheet)
10. [Toast](#10-toast)
11. [Пустое состояние](#11-пустое-состояние)
12. [Нижняя навигация](#12-навигация)
13. [Антипаттерны](#13-антипаттерны)

---

## 1. Тема

### Подключение (в `<head>`, порядок строгий)

```html
<!-- 1) Anti-FOUC: ДО любого CSS -->
<script>
(function(){try{var t=localStorage.getItem('lovii_theme');
if(!t){t=matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light';}
document.documentElement.setAttribute('data-theme',t);}catch(e){}})();
</script>
<!-- 2) Шрифт -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<!-- 3) Токены -->
<link rel="stylesheet" href="tokens/tokens.css">
<!-- 4) meta theme-color обновляется из applyTheme -->
<meta name="theme-color" id="metaTheme" content="#f64a8a">
```

### Логотипы: оба в DOM, видимость через CSS

```html
<img src="assets/lovii-logo-light.svg" class="logo-light-img" alt="Лови">
<img src="assets/lovii-logo-dark.svg"  class="logo-dark-img"  alt="Лови">
```
```css
img.logo-dark-img, img.logo-light-img { display:block; height:28px; width:auto; }
html[data-theme="light"] img.logo-dark-img { display:none; }
html[data-theme="dark"]  img.logo-light-img { display:none; }
```
⚠️ Специфичность: селектор с `html[data-theme=…]` бьёт простые классы. Если логотип вложен в блок со своими правилами (`img.xxx-logo`), правило скрытия должно быть не слабее — см. баг из style-guide (`.gs-header img.gs-logo` перебивал скрытие).

### applyTheme (канон)

```js
function applyTheme(t){
  document.documentElement.setAttribute('data-theme', t);
  try{ localStorage.setItem('lovii_theme', t); }catch(e){}
  var m = document.getElementById('metaTheme');
  if(m) m.content = t === 'dark' ? '#171219' : '#f64a8a';
}
```
Do: `data-theme` только на `<html>`; ключ `lovii_theme`; try/catch вокруг localStorage.
Don't: React-state, cookie, `filter: invert`, хранить тему в CSS-классе на body.

---

## 2. Каркас

### Капсула 480px → wide

```css
.view { max-width:var(--lv-container); margin:0 auto; padding-bottom:calc(var(--lv-nav-h) + 32px + env(safe-area-inset-bottom,0px)); }
@media (min-width:640px){ .view { max-width:var(--lv-container-wide); padding-bottom:96px; } }
/* Линейные экраны (партнёр, инвестор): */
/* @media (min-width:640px){ .view { max-width:var(--lv-container-narrow); } } */
```

### Секция: 20px сверху, 12px до контента

```html
<section class="section">
  <div class="section-head">
    <h2 class="section-title">Заголовок</h2>
    <a class="section-link" href="#">Все</a>
  </div>
  <!-- контент -->
</section>
```
```css
.section { margin-top:20px; }
.section-head { display:flex; align-items:baseline; justify-content:space-between; padding:0 16px; margin-bottom:12px; }
.section-title { font-size:20px; font-weight:800; letter-spacing:-.02em; }
.section-link { font-size:13px; font-weight:600; color:var(--lv-pink); text-decoration:none; }
```

---

## 3. Хедер

### Sticky glass 56px

```css
.app-header {
  position:sticky; top:0; z-index:40; height:var(--lv-header-h);
  display:flex; align-items:center; gap:12px; padding:0 var(--lv-pad-x);
  background:var(--lv-glass); backdrop-filter:blur(16px); -webkit-backdrop-filter:blur(16px);
}
```
Do: z-index 40–45 для sticky-слоёв, toast 60, sheet 50.
Don't: непрозрачный фон вместо glass; отрицательные отступы для «прилипания».

---

## 4. Кнопки

### Полный набор

```html
<button class="btn btn-primary">Добавить</button>
<button class="btn btn-ghost">Отмена</button>
<button class="btn btn-soft" disabled>Недоступно</button>
```
```css
.btn {
  height:48px; padding:0 28px; border:0; cursor:pointer; border-radius:999px;
  font-family:inherit; font-size:15px; font-weight:700;
  display:inline-flex; align-items:center; justify-content:center; gap:8px;
  transition:transform .15s ease, box-shadow .2s ease, background .2s ease;
}
.btn:active { transform:scale(.96); }
.btn-primary { background-image:var(--lv-gradient-brand); color:var(--lv-on-brand); box-shadow:var(--lv-shadow-lift); }
.btn-primary:hover { box-shadow:var(--lv-shadow-toast); }
.btn-ghost { background:var(--lv-surface); color:var(--lv-ink); }
.btn-ghost:hover { background:var(--lv-grey-soft); }
.btn-soft { background:var(--lv-grey-soft); color:#999; cursor:default; }
```
Do: пилюля 999px; hover — усиление розовой тени; нажатие scale .96 за 0.15s.
Don't: квадратные кнопки; тень black на brand; текст `--lv-ink` на градиенте.

### Кнопка-иконка (круглая)

```css
.icon-btn { width:36px; height:36px; border-radius:999px; background:var(--lv-surface);
  display:flex; align-items:center; justify-content:center; border:0; cursor:pointer;
  transition:transform .15s ease; }
.icon-btn:active { transform:scale(.95); }
```
aria-label обязателен (цель ≥36px).

---

## 5. Пилюли

### Статусы: soft-пары (не смешивать!)

```html
<span class="pill p-pink">Акция</span>
<span class="pill p-tiffany"><span class="lv-dot"></span>В наличии</span>
<span class="pill p-gold">Премиум</span>
<span class="pill p-grey">Черновик</span>
```
```css
.pill { display:inline-flex; align-items:center; gap:6px; padding:6px 12px; border-radius:999px; font-size:12px; font-weight:600; }
.pill .lv-dot { background:currentColor; }
.p-pink    { background:var(--lv-soft-pink);    color:var(--lv-pink-dark); }
.p-tiffany { background:var(--lv-soft-tiffany); color:var(--lv-tiffany-text); }
.p-gold    { background:var(--lv-soft-gold);    color:var(--lv-gold-text); }
.p-grey    { background:var(--lv-grey-soft);    color:#999; }
```

### Бейджи на обложках (фиксированные светлые подложки — не зависят от темы)

```html
<span class="badge b-hit">Хит</span>  <!-- badge-hit → pink-dark -->
<span class="badge b-new">Новинка</span>  <!-- badge-new → tiffany-text -->
<span class="badge b-sale">−20%</span>  <!-- badge-sale → gold-text -->
```
```css
.badge { position:absolute; top:10px; left:10px; padding:4px 10px; border-radius:999px;
  font-size:10px; font-weight:700; letter-spacing:.06em; text-transform:uppercase; }
.b-hit { background:var(--lv-badge-hit); color:var(--lv-pink-dark); }
.b-new { background:var(--lv-badge-new); color:var(--lv-tiffany-text); }
.b-sale { background:var(--lv-badge-sale); color:var(--lv-gold-text); }
```
Don't: бейдж на `soft-*` в тёмной теме — подложки `badge-*` фиксированно светлые и в паре со своими тёмными текстами смотрятся верно всегда.

---

## 6. Карточки

### Базовая карточка

```css
.card {
  background:var(--lv-card); border:1px solid var(--lv-line); border-radius:16px;
  box-shadow:var(--lv-shadow-soft); overflow:hidden;
  transition:transform .15s ease, box-shadow .2s ease;
}
.card:hover { box-shadow:var(--lv-shadow-lift); }
.card:active { transform:scale(.97); }
```

### Плитки категорий и уровней (фиксированно светлые подложки)

```html
<a class="tile t-pink" href="#"><span class="emoji">💝</span><span class="name">Для неё</span></a>
```
```css
.tile { border-radius:12px; padding:14px 8px 10px; text-align:center; text-decoration:none; transition:transform .15s ease; }
.tile:active { transform:scale(.96); }
.tile .name { font-size:11px; font-weight:600; color:var(--lv-on-tile); } /* НЕ --lv-ink! */
.t-pink { background-image:var(--lv-tile-pink); }
```
⚠️ Плитки `tile-*` остаются светлыми в обеих темах, поэтому их текст — только `--lv-on-tile` / `--lv-on-tile-dim`, чипы на плитке — `--lv-tile-chip` + `--lv-on-tile-dim`. Темовые `ink/dim` в тёмной теме станут светлыми и растворятся.

### Карточка товара

```html
<article class="card">
  <div class="cover cv-hero"><span>🧸</span><span class="badge b-hit">Хит</span></div>
  <div class="card-body">
    <div class="card-title">Название товара</div>
    <div class="card-sub">40 см · плюш</div>
    <div class="card-row">
      <span class="price">1 890 ₽ <small>990 ₽</small></span>
      <button class="btn-add" aria-label="Добавить в корзину">+</button>
    </div>
  </div>
</article>
```
```css
.cover { position:relative; height:120px; display:flex; align-items:center; justify-content:center; }
.cv-hero { background:linear-gradient(180deg, var(--lv-hero-top), var(--lv-card)); }
.cv-ink  { background-image:var(--lv-gradient-ink); }   /* акцентная обложка */
.card-body { padding:12px 14px 14px; }
.card-title { font-size:14px; font-weight:600; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.card-sub { margin-top:2px; font-size:11px; color:var(--lv-dim); }
.price { font-size:16px; font-weight:800; letter-spacing:-.02em; }
.price small { font-size:11px; font-weight:600; color:var(--lv-dim); text-decoration:line-through; }
```

### KPI-карточка (бизнес/инвестор)

```css
.kpi { background:var(--lv-card); border:1px solid var(--lv-line); border-radius:16px; padding:16px; box-shadow:var(--lv-shadow-soft); }
.kpi.accent { background:var(--lv-kpi-soft); border-color:transparent; }
.kpi.accent .value {   /* градиентный текст — вместо градиентной заливки */
  background-image:var(--lv-gradient-brand); -webkit-background-clip:text; background-clip:text; color:transparent; }
```

---

## 7. Формы

### Инпут и поиск-пилюля

```css
.field {
  height:44px; padding:0 14px; border-radius:999px; border:1px solid var(--lv-line);
  background:var(--lv-surface); color:var(--lv-ink); font-size:14px; font-family:inherit; width:100%;
}
.field::placeholder { color:var(--lv-dim); }
.field:focus { outline:none; border-color:transparent; box-shadow:var(--lv-ring-field); }
.field[aria-invalid="true"] { border-color:var(--lv-pink); }
```
```html
<input class="field" type="email" placeholder="you@mail.ru" autocomplete="email">
```
Do: фокус — `ring-field` (розовый ореол 4px), не стандартный outline браузера.
Don't: фон `--lv-bg` у поля (сольётся с фоном страницы); бордер `--lv-pink` по умолчанию (только ошибка/фокус).

---

## 8. Сегменты

```html
<div class="segments" role="tablist" aria-label="Период">
  <button class="segment active" role="tab" aria-selected="true">Неделя</button>
  <button class="segment" role="tab">Месяц</button>
</div>
```
```css
.segments { display:inline-flex; padding:4px; gap:4px; border-radius:999px; background:var(--lv-surface); }
.segment { border:0; cursor:pointer; padding:8px 18px; border-radius:999px; font-size:13px; font-weight:600;
  color:var(--lv-dim); background:transparent; transition:all .2s ease; font-family:inherit; }
.segment.active { background:var(--lv-card); color:var(--lv-ink); box-shadow:var(--lv-shadow-soft); }
```

---

## 9. Bottom-sheet

```html
<div class="sheet-overlay" id="ov" hidden></div>
<div class="sheet" id="sheet" role="dialog" aria-modal="true" aria-label="Оформление" hidden>
  <div class="sheet-handle"></div>
  <!-- контент -->
</div>
```
```css
.sheet-overlay { position:fixed; inset:0; z-index:50; background:rgba(0,0,0,.4); }
.sheet {
  position:fixed; left:50%; bottom:0; z-index:55; transform:translateX(-50%);
  width:100%; max-width:var(--lv-container); max-height:82vh; overflow:auto;
  background:var(--lv-card); border-radius:24px 24px 0 0; padding:8px 16px calc(20px + env(safe-area-inset-bottom,0px));
  animation:sheet-in .4s cubic-bezier(.32,.72,0,1) both;
}
.sheet-handle { width:36px; height:4px; border-radius:999px; background:var(--lv-grey-soft); margin:4px auto 14px; }
@keyframes sheet-in { from { transform:translate(-50%,100%); } to { transform:translate(-50%,0); } }
```
```js
function openSheet(){ ov.hidden = sheet.hidden = false; document.body.style.overflow = 'hidden'; }
function closeSheet(){ ov.hidden = sheet.hidden = true; document.body.style.overflow = ''; }
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeSheet(); });
ov.addEventListener('click', closeSheet);
```
Do: кривая `cubic-bezier(.32,.72,0,1)`; хендл; закрытие по оверлею/Escape; блок скролла body.
Don't: ширина больше капсулы; радиус верхних углов ≠ 24px; анимация left/top.

---

## 10. Toast

```html
<div class="toast" id="toast" role="status" aria-live="polite"></div>
```
```css
.toast {
  position:fixed; left:50%; bottom:calc(var(--lv-nav-h) + 16px + env(safe-area-inset-bottom,0px)); z-index:60;
  transform:translateX(-50%) translateY(16px); opacity:0; pointer-events:none;
  max-width:min(420px, calc(100vw - 32px)); padding:12px 18px; border-radius:999px;
  background-image:var(--lv-gradient-brand); color:var(--lv-on-brand);
  box-shadow:var(--lv-shadow-toast); font-size:14px; font-weight:600; text-align:center;
  transition:opacity .25s ease, transform .25s cubic-bezier(.32,.72,0,1);
}
.toast.show { opacity:1; transform:translateX(-50%) translateY(0); }
```
```js
var toastTimer;
function showToast(text){
  var el = document.getElementById('toast');
  el.textContent = text; el.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => el.classList.remove('show'), 2400);
}
```
Do: один переиспользуемый элемент; на брендовом градиенте вторичный текст `--lv-toast-d`.
Don't: несколько тостов одновременно; белый текст `#fff` вместо `--lv-on-brand`; тост без таймера.

---

## 11. Пустое состояние

```html
<div class="empty">
  <span class="empty-emoji">💌</span>
  <div class="empty-title">Пока пусто</div>
  <p class="empty-text">Здесь появятся заказы — оформите первый подарок.</p>
  <button class="btn btn-primary">В каталог</button>
</div>
```
```css
.empty { text-align:center; padding:48px 24px; }
.empty-emoji { font-size:40px; animation:lv-float 5s ease-in-out infinite; display:inline-block; }
.empty-title { margin-top:12px; font-size:18px; font-weight:800; }
.empty-text { margin:6px auto 16px; font-size:14px; color:var(--lv-dim); line-height:1.6; max-width:32ch; }
```

---

## 12. Навигация

### Нижняя навигация (мобайл) → плавающая капсула (≥900px)

См. полный код в `examples/01-client-store.html`. Ключевое:

```css
.bottom-nav { position:fixed; bottom:0; left:0; right:0; z-index:45;
  height:calc(var(--lv-nav-h) + env(safe-area-inset-bottom,0px));
  padding-bottom:env(safe-area-inset-bottom,0px);
  background:var(--lv-glass); backdrop-filter:blur(16px); box-shadow:var(--lv-shadow-nav); }
@media (min-width:900px){
  .bottom-nav { left:50%; right:auto; transform:translateX(-50%); bottom:16px;
    height:60px; padding:0 8px; border-radius:999px; width:min(420px,90vw); }
}
.nav-item { color:var(--lv-dim); font-size:10px; font-weight:600; }
.nav-item.active { color:var(--lv-pink); }
```
Do: safe-area; у активного пункта розовый цвет; иконки — inline SVG `stroke="currentColor"`.
Don't: цвет активного пункта из soft-пары (слабый контраст); фикс. высота без safe-area.

### Лента с растворением краёв

```html
<div class="rail no-scrollbar lv-edge-fade"><!-- карточки --></div>
```
```css
.rail { display:flex; gap:12px; overflow-x:auto; padding:2px 16px 6px; scroll-snap-type:x proximity; }
.rail .card { flex:0 0 150px; scroll-snap-align:start; }
```
`.lv-edge-fade` и `.no-scrollbar` уже в tokens.css — не дублировать.

---

## 13. Антипаттерны

Сводка запретов с быстрым поиском проблемы:

| Симптом | Причина | Как надо |
|---|---|---|
| Текст «светится» на тёмном | `#fff`/`#000` в тексте | `--lv-ink` / `--lv-dim`; на градиентах — `--lv-on-brand` |
| Пилюля нечитаема в тёмной теме | смешана пара: soft одного тона + текст другого | только канонические пары: `soft-pink→pink-dark`, `soft-tiffany→tiffany-text`, `soft-gold→gold-text`, `grey-soft→#999` |
| Карточка «вспыхивает» при hover | резкая тень | тени только `shadow-soft ↔ shadow-lift`, transition .2s |
| Кнопка квадратная в фокусе | стандартный outline | `:focus-visible` розовый 2px offset 2px (уже в tokens.css) |
| Мигание темы при загрузке | скрипт темы после CSS | anti-FOUC инлайн **до** линков CSS |
| Скроллится под шитом | body не заблокирован | `document.body.style.overflow='hidden'` на открытие |
| Лента вылезает за капсулу | отрицательные margins | паддинги 16px внутри ленты + `.lv-edge-fade` |
| Текст на плитке нечитаем в тёмной теме | на `tile-*` использован темовый `ink/dim` | только `--lv-on-tile` / `--lv-on-tile-dim` / `--lv-tile-chip` (плитки фиксированно светлые) |
| Анимация «дёргается» | анимируются width/height/margin | только transform/opacity |
| У пользователя PWA старый CSS | не поднят кэш | `?v=N` в index.html + `CACHE lovii-vN` в sw.js (демка) |
