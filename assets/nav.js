/*!
 * LOVII DS — сквозная навигация (assets/nav.js)
 * Канон: lovii-design. Подключать последним перед </body>:
 *   <script src="assets/nav.js" defer></script>            (страницы в корне)
 *   <script src="../assets/nav.js" defer></script>         (страницы в examples/)
 * Сам находит хедер (.app-header / .gs-head-right) и добавляет кнопку «☰»;
 * если хедера нет — рисует плавающую кнопку. Шит — по канону docs/07 §9.
 */
(function () {
  'use strict';
  if (window.__lvnav) return; window.__lvnav = true;

  /* ---------- база репо от URL самого скрипта ---------- */
  var base = new URL('../', (document.currentScript && document.currentScript.src) || location.href);
  function u(p) { return new URL(p, base).href; }

  var ITEMS = [
    { p: 'index.html',                      t: 'Хаб дизайн-системы', s: 'точка входа',      c: 'var(--lv-ink)' },
    { p: 'style-guide.html',                t: 'Живой style-guide',  s: 'все токены и компоненты', c: 'var(--lv-pink)' },
    { p: 'examples/01-client-store.html',   t: 'Витрина · клиент',   s: 'референс-экран',   c: 'var(--lv-pink)' },
    { p: 'examples/02-business-dashboard.html', t: 'Дашборд · бизнес', s: 'референс-экран', c: 'var(--lv-tiffany)' },
    { p: 'examples/03-partner-portal.html', t: 'Портал · партнёр',   s: 'референс-экран',   c: 'var(--lv-gold)' },
    { p: 'examples/04-ambassador-program.html', t: 'Амбассадор',     s: 'референс-экран',   c: 'var(--lv-pink)' },
    { p: 'examples/05-investor-overview.html',  t: 'Инвестор',       s: 'референс-экран',   c: 'var(--lv-dim)' }
  ];
  var GH = 'https://github.com/bestdeejay-design/lovii-design';

  /* ---------- стили (scoped, канон токенов) ---------- */
  var css = [
    '.lvnav-btn{width:36px;height:36px;border-radius:999px;border:0;flex:none;cursor:pointer;',
      'background:var(--lv-surface);color:var(--lv-ink);display:flex;align-items:center;justify-content:center;',
      'transition:transform .15s ease,background .2s ease;margin-left:8px;padding:0}',
    '.lvnav-btn:hover{background:var(--lv-soft-pink)}',
    '.lvnav-btn:active{transform:scale(.95)}',
    '.lvnav-btn svg{width:18px;height:18px;display:block}',
    '.lvnav-btn.lvnav-float{position:fixed;right:16px;bottom:calc(var(--lv-nav-h,64px) + 16px + env(safe-area-inset-bottom,0px));z-index:70;',
      'box-shadow:var(--lv-shadow-lift);margin:0;background:var(--lv-card)}',
    '.lvnav-overlay{position:fixed;inset:0;z-index:80;background:rgba(0,0,0,.4);opacity:0;transition:opacity .3s ease}',
    '.lvnav-sheet{position:fixed;left:50%;bottom:0;z-index:85;transform:translate(-50%,100%);',
      'width:100%;max-width:var(--lv-container,480px);max-height:82vh;overflow:auto;',
      'background:var(--lv-card);border-radius:24px 24px 0 0;',
      'padding:8px 16px calc(20px + env(safe-area-inset-bottom,0px));',
      'transition:transform .4s cubic-bezier(.32,.72,0,1);box-shadow:var(--lv-shadow-lift)}',
    '.lvnav-open .lvnav-overlay{opacity:1}',
    '.lvnav-open .lvnav-sheet{transform:translate(-50%,0)}',
    '.lvnav-handle{width:36px;height:4px;border-radius:999px;background:var(--lv-grey-soft);margin:4px auto 14px}',
    '.lvnav-title{font-size:13px;font-weight:800;letter-spacing:-.01em;color:var(--lv-dim);',
      'text-transform:uppercase;letter-spacing:.08em;font-size:11px;margin:0 4px 10px}',
    '.lvnav-list{list-style:none;margin:0;padding:0}',
    '.lvnav-item a{display:flex;align-items:center;gap:12px;padding:12px 12px;border-radius:12px;',
      'text-decoration:none;color:var(--lv-ink);transition:background .15s ease}',
    '.lvnav-item a:hover{background:var(--lv-surface)}',
    '.lvnav-item.here a{background:var(--lv-soft-pink)}',
    '.lvnav-dot{width:10px;height:10px;border-radius:999px;flex:none;background:var(--c,var(--lv-pink))}',
    '.lvnav-txt{display:flex;flex-direction:column;min-width:0}',
    '.lvnav-t{font-size:15px;font-weight:600;line-height:1.2}',
    '.lvnav-item.here .lvnav-t{color:var(--lv-pink);font-weight:700}',
    '.lvnav-s{font-size:12px;color:var(--lv-dim);line-height:1.4;margin-top:2px}',
    '.lvnav-gh{margin-top:10px;border-top:1px solid var(--lv-hairline);padding-top:12px}',
    '.lvnav-gh a{display:flex;align-items:center;justify-content:space-between;gap:12px;',
      'padding:12px;border-radius:12px;text-decoration:none;font-size:14px;font-weight:600;',
      'color:var(--lv-tiffany);transition:background .15s ease}',
    '.lvnav-gh a:hover{background:var(--lv-surface)}',
    '@media (prefers-reduced-motion:reduce){.lvnav-overlay,.lvnav-sheet{transition:none}}'
  ].join('');

  /* ---------- DOM ---------- */
  var style = document.createElement('style'); style.textContent = css;
  document.head.appendChild(style);

  var btn = document.createElement('button');
  btn.className = 'lvnav-btn'; btn.type = 'button';
  btn.setAttribute('aria-label', 'Открыть навигацию'); btn.setAttribute('title', 'Навигация по дизайн-системе');
  btn.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16"/><path d="M4 12h16"/><path d="M4 17h16"/></svg>';

  var host = document.querySelector('.gs-head-right') ||
             document.querySelector('.app-header');
  if (host) { host.appendChild(btn); }
  else { btn.classList.add('lvnav-float'); document.body.appendChild(btn); }

  var ov = document.createElement('div'); ov.className = 'lvnav-overlay'; ov.hidden = true;
  var sheet = document.createElement('div'); sheet.className = 'lvnav-sheet';
  sheet.setAttribute('role', 'dialog'); sheet.setAttribute('aria-modal', 'true');
  sheet.setAttribute('aria-label', 'Навигация по дизайн-системе LOVII'); sheet.hidden = true;

  /* активный пункт: сверяем путь без index.html и с ним */
  var here = location.pathname.replace(/\/+$/, '');
  var hereFile = here.replace(/\/([^/]*)$/, '$1');
  function isHere(item) {
    var target = new URL(item.p, base).pathname.replace(/\/+$/, '');
    var active = here === target || hereFile === target.replace(/\/([^/]*)$/, '$1');
    if (!active && (here === '' || hereFile === '') && item.p === 'index.html') active = true;
    return active;
  }

  var rows = ITEMS.map(function (it) {
    var li = document.createElement('li');
    li.className = 'lvnav-item' + (isHere(it) ? ' here' : '');
    var a = document.createElement('a'); a.href = u(it.p);
    if (isHere(it)) a.setAttribute('aria-current', 'page');
    a.innerHTML = '<span class="lvnav-dot" style="--c:' + it.c + '"></span>' +
      '<span class="lvnav-txt"><span class="lvnav-t">' + it.t + '</span>' +
      '<span class="lvnav-s">' + (isHere(it) ? 'вы здесь · ' : '') + it.s + '</span></span>';
    li.appendChild(a); return li;
  });

  var gh = document.createElement('div'); gh.className = 'lvnav-gh';
  gh.innerHTML = '<a href="' + GH + '" target="_blank" rel="noopener">Документация на GitHub' +
    '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17 17 7"/><path d="M8 7h9v9"/></svg></a>';

  sheet.innerHTML = '<div class="lvnav-handle"></div><p class="lvnav-title">Навигация · ДС LOVII</p>';
  var ul = document.createElement('ul'); ul.className = 'lvnav-list';
  rows.forEach(function (li) { ul.appendChild(li); });
  sheet.appendChild(ul); sheet.appendChild(gh);

  /* ---------- поведение (канон docs/07 §9) ---------- */
  var lastFocus = null;
  function open() {
    lastFocus = document.activeElement;
    ov.hidden = sheet.hidden = false;
    document.body.style.overflow = 'hidden';
    requestAnimationFrame(function () {
      document.documentElement.classList.add('lvnav-open');
      var first = sheet.querySelector('a'); if (first) first.focus({ preventScroll: true });
    });
  }
  function close() {
    document.documentElement.classList.remove('lvnav-open');
    document.body.style.overflow = '';
    ov.hidden = sheet.hidden = true;
    if (lastFocus && lastFocus.focus) lastFocus.focus({ preventScroll: true });
  }
  btn.addEventListener('click', open);
  ov.addEventListener('click', close);
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && !sheet.hidden) close();
  });
  document.body.appendChild(ov); document.body.appendChild(sheet);
})();
