/* ============================================================
   LawnWize — site.js
   Vanilla JS only. Hero carousel, mobile nav, estimate form.
   ============================================================ */
(function () {
    'use strict';

    /* ---- Mobile nav toggle ---- */
    var toggle = document.querySelector('.nav-toggle');
    var nav = document.querySelector('.site-nav');
    if (toggle && nav) {
        toggle.addEventListener('click', function () {
            var open = nav.classList.toggle('open');
            toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
        });
    }

    /* ---- Hero carousel (homepage only) ----
       Slides container holds N real slides plus a clone of slide 1
       at the end, so the loop wraps without a visible jump. */
    var slides = document.getElementById('heroSlides');
    var dotsWrap = document.getElementById('heroDots');
    if (slides && dotsWrap) {
        var realCount = slides.children.length;
        var clone = slides.children[0].cloneNode(true);
        slides.appendChild(clone);

        var dots = dotsWrap.querySelectorAll('.hero-dot');
        var current = 0;
        var timer = null;

        function render(instant) {
            slides.style.transition = instant ? 'none' : 'transform 0.9s ease';
            slides.style.transform = 'translateX(-' + (current * 100) + '%)';
            dots.forEach(function (d, i) {
                d.classList.toggle('active', i === (current % realCount));
            });
        }

        function next() {
            current += 1;
            render(false);
            if (current === realCount) {
                /* After sliding onto the clone, snap back to the real
                   first slide once the transition finishes. */
                setTimeout(function () {
                    current = 0;
                    render(true);
                }, 950);
            }
        }

        function goTo(i) {
            current = i;
            render(false);
            restart();
        }

        function restart() {
            if (timer) { clearInterval(timer); }
            timer = setInterval(next, 5000);
        }

        dots.forEach(function (d, i) {
            d.addEventListener('click', function () { goTo(i); });
        });

        restart();
    }

    /* ---- Estimate form (contact page) ----
       Static build: submitting composes an email to LawnWize in the
       visitor's mail app. To wire a form provider instead, see the
       comment block in contact.html. */
    var form = document.getElementById('estimateForm');
    if (form) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            var v = function (id) {
                var el = document.getElementById(id);
                return el ? el.value.trim() : '';
            };
            var subject = 'Estimate Request - ' + (v('ef-name') || 'Website Visitor');
            var lines = [
                'Name: ' + v('ef-name'),
                'Phone: ' + v('ef-phone'),
                'Email: ' + v('ef-email'),
                'Town: ' + v('ef-town'),
                'Service: ' + v('ef-service'),
                '',
                'Details:',
                v('ef-message')
            ];
            window.location.href = 'mailto:info@lawnwize.com'
                + '?subject=' + encodeURIComponent(subject)
                + '&body=' + encodeURIComponent(lines.join('\n'));
        });
    }

    /* ---- Footer year ---- */
    var yearEl = document.getElementById('footerYear');
    if (yearEl) { yearEl.textContent = String(new Date().getFullYear()); }
})();
