/* ============================================================
   Fitzgerald General Contracting — site.js
   - Hero carousel (4 slides, auto-advance + dots)
   - Mobile nav toggle
   - Active nav state
   - Reviews carousel
   - Injects the custom four-action launcher on every page
   - Chat widget: PLACEHOLDER ONLY. No GHL Preview Slot assigned yet,
     so we do NOT load a live widget. The injectGHLWidget() function is
     written and ready but intentionally NOT called — see the labeled
     HTML comment near </body> on each page. Once Matt confirms the slot
     and clones the AIO widget, set GHL_WIDGET_ID below and call
     injectGHLWidget() inside init().
   ============================================================ */
(function () {
  'use strict';

  /* ---- Hero carousel ---- */
  function initHero() {
    var slides = document.querySelectorAll('.hero-slide');
    var dotsWrap = document.querySelector('.hero-dots');
    if (slides.length < 2) return;
    var idx = 0;
    // build dots
    if (dotsWrap) {
      dotsWrap.innerHTML = '';
      for (var i = 0; i < slides.length; i++) {
        var d = document.createElement('button');
        d.className = 'hero-dot' + (i === 0 ? ' is-active' : '');
        d.setAttribute('aria-label', 'Go to slide ' + (i + 1));
        d.dataset.i = i;
        dotsWrap.appendChild(d);
      }
      dotsWrap.addEventListener('click', function (e) {
        if (e.target.classList.contains('hero-dot')) {
          go(parseInt(e.target.dataset.i, 10));
          restart();
        }
      });
    }
    function go(n) {
      slides[idx].classList.remove('is-active');
      var dots = dotsWrap ? dotsWrap.querySelectorAll('.hero-dot') : [];
      if (dots[idx]) dots[idx].classList.remove('is-active');
      idx = (n + slides.length) % slides.length;
      slides[idx].classList.add('is-active');
      if (dots[idx]) dots[idx].classList.add('is-active');
    }
    var timer;
    function restart() { clearInterval(timer); timer = setInterval(function () { go(idx + 1); }, 6000); }
    restart();
    var hero = document.querySelector('.hero');
    if (hero) {
      hero.addEventListener('mouseenter', function () { clearInterval(timer); });
      hero.addEventListener('mouseleave', restart);
    }
  }

  /* ---- Mobile nav ---- */
  function initNav() {
    var toggle = document.querySelector('.menu-toggle');
    var menu = document.getElementById('navmenu');
    if (toggle && menu) {
      toggle.addEventListener('click', function () { menu.classList.toggle('open'); });
    }
    // active state by filename
    var p = window.location.pathname.split('/').pop() || 'index.html';
    document.querySelectorAll('nav a').forEach(function (a) {
      var h = a.getAttribute('href'); if (!h) return;
      if (h.split('/').pop() === p) a.classList.add('active');
    });
  }

  /* ---- Reviews carousel ---- */
  function initReviews() {
    var track = document.querySelector('.rv-track');
    var cards = document.querySelectorAll('.rv-card');
    var prev = document.querySelector('.rv-prev');
    var next = document.querySelector('.rv-next');
    var dots = document.querySelector('.rv-dots');
    if (!track || cards.length === 0) return;
    function visibleCount() { return window.innerWidth < 720 ? 1 : (window.innerWidth < 1080 ? 2 : 3); }
    var idx = 0;
    function update() {
      var n = visibleCount();
      var maxIdx = Math.max(0, cards.length - n);
      if (idx > maxIdx) idx = maxIdx;
      if (idx < 0) idx = 0;
      var cw = cards[0].getBoundingClientRect().width + 24;
      track.style.transform = 'translateX(-' + (idx * cw) + 'px)';
      if (dots) {
        var dotCount = maxIdx + 1; dots.innerHTML = '';
        for (var i = 0; i < dotCount; i++) {
          var d = document.createElement('button');
          d.className = 'rv-dot' + (i === idx ? ' is-active' : '');
          d.setAttribute('aria-label', 'Go to review ' + (i + 1));
          d.dataset.i = i; dots.appendChild(d);
        }
      }
    }
    if (prev) prev.addEventListener('click', function () { idx--; update(); });
    if (next) next.addEventListener('click', function () { idx++; update(); });
    if (dots) dots.addEventListener('click', function (e) {
      if (e.target.classList.contains('rv-dot')) { idx = parseInt(e.target.dataset.i, 10); update(); }
    });
    window.addEventListener('resize', update);
    update();
    var timer = setInterval(function () {
      var n = visibleCount(); var maxIdx = Math.max(0, cards.length - n);
      idx = (idx >= maxIdx) ? 0 : idx + 1; update();
    }, 7000);
    var car = document.querySelector('.rv-carousel');
    if (car) car.addEventListener('mouseenter', function () { clearInterval(timer); });
  }

  /* ---- Custom four-action launcher (injected on every page) ---- */
  var LAUNCHER_HTML =
    '<div class="fitz-launcher" role="dialog" aria-label="Get in touch">'
    + '<div class="fitz-launcher-panel"><div class="fitz-launcher-head"><h4>How can we help?</h4><p>Talk to the Fitzgerald crew &mdash; we answer fast.</p></div>'
    + '<a href="sms:9784089390?body=Hi%20Fitzgerald%20GC%2C%20I%20have%20an%20urgent%20question%20about%20" class="fitz-launcher-action"><div class="fitz-action-icon red"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg></div><div class="fitz-action-text"><p class="t">Urgent &mdash; text us</p><p class="s">Storm damage, leaks, fast questions</p></div></a>'
    + '<button class="fitz-launcher-action" data-fitz-action="chat"><div class="fitz-action-icon green"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/></svg></div><div class="fitz-action-text"><p class="t">Chat with us</p><p class="s">Questions about your project</p></div></button>'
    + '<button class="fitz-launcher-action" data-fitz-action="book"><div class="fitz-action-icon gold"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg></div><div class="fitz-action-text"><p class="t">Request a free estimate</p><p class="s">Tell us about your project</p></div></button>'
    + '<a href="tel:9784089390" class="fitz-launcher-action"><div class="fitz-action-icon blue"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07 19.5 19.5 0 01-6-6 19.79 19.79 0 01-3.07-8.67A2 2 0 014.11 2h3a2 2 0 012 1.72 12.84 12.84 0 00.7 2.81 2 2 0 01-.45 2.11L8.09 9.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45 12.84 12.84 0 002.81.7A2 2 0 0122 16.92z"/></svg></div><div class="fitz-action-text"><p class="t">(978) 408-9390</p><p class="s">Mon &ndash; Fri 8a&ndash;6p</p></div></a>'
    + '<div class="fitz-launcher-foot">Powered by ScaleLocal</div></div>'
    + '<button class="fitz-launcher-btn" aria-label="Open contact options"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 11.5a8.38 8.38 0 01-.9 3.8 8.5 8.5 0 01-7.6 4.7 8.38 8.38 0 01-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 01-.9-3.8 8.5 8.5 0 014.7-7.6 8.38 8.38 0 013.8-.9h.5a8.48 8.48 0 018 8v.5z"/></svg><span class="fitz-launcher-badge">3</span></button></div>';

  function injectLauncher() {
    if (document.querySelector('.fitz-launcher')) return;
    var div = document.createElement('div');
    div.innerHTML = LAUNCHER_HTML;
    document.body.appendChild(div.firstChild);
  }

  /* ---- GHL AIO chat widget loader — READY BUT NOT CALLED ----
     Preview Slot is TBD. Once Matt assigns a slot and clones the AIO
     widget (see GHL_SETUP_FITZGERALD_GC.md), set GHL_WIDGET_ID and call
     injectGHLWidget() from init(). The custom launcher's "Chat" action
     will then hand off to it automatically (see launcher.js).            */
  var GHL_WIDGET_ID = ''; // <-- paste cloned Fitzgerald AIO widget ID here
  function injectGHLWidget() {
    if (!GHL_WIDGET_ID) return;
    if (document.querySelector('script[data-widget-id="' + GHL_WIDGET_ID + '"]')) return;
    var s = document.createElement('script');
    s.src = 'https://widgets.leadconnectorhq.com/loader.js';
    s.setAttribute('data-resources-url', 'https://widgets.leadconnectorhq.com/chat-widget/loader.js');
    s.setAttribute('data-widget-id', GHL_WIDGET_ID);
    document.body.appendChild(s);
  }

  function init() {
    initHero();
    initNav();
    initReviews();
    injectLauncher();
    // injectGHLWidget();  // <-- uncomment once GHL_WIDGET_ID is set
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else { init(); }
})();
