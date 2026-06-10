/* Santos & Sons — hero carousel, mobile nav, gallery viewer */
(function () {
  /* Mobile nav toggle */
  var toggle = document.querySelector('.menu-toggle');
  var menu = document.getElementById('navmenu');
  if (toggle && menu) {
    toggle.addEventListener('click', function () {
      menu.classList.toggle('open');
      toggle.classList.toggle('active');
    });
  }

  /* Hero carousel */
  var hero = document.querySelector('.hero-carousel');
  if (hero) {
    var slides = hero.querySelectorAll('.hero-slide');
    var dots = hero.querySelectorAll('.hero-dot');
    var idx = 0, timer = null, INTERVAL = 6000;

    var hh = document.getElementById('hero-h');
    var hp = document.getElementById('hero-p');

    function go(n) {
      slides[idx].classList.remove('active');
      if (dots[idx]) dots[idx].classList.remove('active');
      idx = (n + slides.length) % slides.length;
      slides[idx].classList.add('active');
      if (dots[idx]) dots[idx].classList.add('active');
      /* swap overlay headline/copy from the active slide's data attrs */
      var s = slides[idx];
      if (hh && s.dataset.h) {
        hh.style.opacity = 0; if (hp) hp.style.opacity = 0;
        setTimeout(function () {
          hh.innerHTML = s.dataset.h;
          if (hp && s.dataset.p) hp.innerHTML = s.dataset.p;
          hh.style.opacity = 1; if (hp) hp.style.opacity = 1;
        }, 280);
      }
    }
    if (hh) { hh.style.transition = 'opacity .28s'; }
    if (hp) { hp.style.transition = 'opacity .28s'; }
    function start() { stop(); timer = setInterval(function () { go(idx + 1); }, INTERVAL); }
    function stop() { if (timer) clearInterval(timer); }

    dots.forEach(function (d, i) {
      d.addEventListener('click', function () { go(i); start(); });
    });
    var prev = hero.querySelector('.hero-arrow.prev');
    var next = hero.querySelector('.hero-arrow.next');
    if (prev) prev.addEventListener('click', function () { go(idx - 1); start(); });
    if (next) next.addEventListener('click', function () { go(idx + 1); start(); });
    hero.addEventListener('mouseenter', stop);
    hero.addEventListener('mouseleave', start);
    start();
  }

  /* Gallery viewer (click to enlarge) */
  var items = document.querySelectorAll('[data-gallery] .g-item img');
  if (items.length) {
    var overlay = document.createElement('div');
    overlay.className = 'g-overlay';
    overlay.innerHTML = '<button class="g-close" aria-label="Close">&times;</button><img alt="">';
    document.body.appendChild(overlay);
    var big = overlay.querySelector('img');
    items.forEach(function (img) {
      img.parentElement.addEventListener('click', function () {
        big.src = img.src; big.alt = img.alt;
        overlay.classList.add('open');
      });
    });
    overlay.addEventListener('click', function () { overlay.classList.remove('open'); });
  }

  /* Footer year */
  var y = document.querySelector('[data-year]');
  if (y) y.textContent = new Date().getFullYear();
})();
