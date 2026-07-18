/* ============================================================
   Maine General Contractors — site.js
   Vanilla JS. Mobile nav, contact launcher widget, estimate
   form (mailto), footer year. NO GHL, no third-party trackers.
   ============================================================ */
(function () {
    'use strict';

    /* ---- CONFIG: single place to update contact details ----
       Phone verified from the business's public Houzz profile.
       EMAIL is a placeholder — confirm from GBP before go-live.
       CALENDAR_URL: paste the booking link (Calendly/Google etc.)
       when ready; until then the Book button shows a note. */
    var CONFIG = {
        PHONE_DISPLAY: '(207) 272-4923',
        PHONE_E164: '+12072724923',
        EMAIL: 'info@mainegcs.com',
        CALENDAR_URL: ''
    };

    /* Wire every element carrying data-contact attributes. */
    document.querySelectorAll('[data-call]').forEach(function (el) {
        el.setAttribute('href', 'tel:' + CONFIG.PHONE_E164);
        if (el.hasAttribute('data-show-number')) { el.textContent = CONFIG.PHONE_DISPLAY; }
    });
    document.querySelectorAll('[data-text]').forEach(function (el) {
        el.setAttribute('href', 'sms:' + CONFIG.PHONE_E164);
    });
    document.querySelectorAll('[data-email]').forEach(function (el) {
        el.setAttribute('href', 'mailto:' + CONFIG.EMAIL);
    });

    /* ---- Mobile nav ---- */
    var toggle = document.querySelector('.nav-toggle');
    var nav = document.querySelector('.site-nav');
    if (toggle && nav) {
        toggle.addEventListener('click', function () {
            var open = nav.classList.toggle('open');
            toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
        });
    }

    /* ---- Contact launcher widget ---- */
    var launcher = document.querySelector('.mgc-launcher');
    if (launcher) {
        var lbtn = launcher.querySelector('.mgc-launcher-btn');
        lbtn.addEventListener('click', function (e) {
            e.stopPropagation();
            var open = launcher.classList.toggle('open');
            lbtn.setAttribute('aria-expanded', open ? 'true' : 'false');
        });
        document.addEventListener('click', function (e) {
            if (!launcher.contains(e.target)) { launcher.classList.remove('open'); }
        });
        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape') { launcher.classList.remove('open'); }
        });

    }

    /* ---- Book an appointment (all pages): use the calendar link when
       configured; until then, fall back gracefully — launcher button shows
       a note, inline links become a call. */
    document.querySelectorAll('[data-book]').forEach(function (bookBtn) {
        if (CONFIG.CALENDAR_URL) {
            bookBtn.setAttribute('href', CONFIG.CALENDAR_URL);
            bookBtn.setAttribute('target', '_blank');
            bookBtn.setAttribute('rel', 'noopener');
        } else if (launcher && launcher.contains(bookBtn)) {
            bookBtn.addEventListener('click', function (e) {
                e.preventDefault();
                var note = launcher.querySelector('.mgc-note');
                if (note) {
                    note.textContent = 'Online booking is coming soon — call or text and we’ll get you on the schedule today.';
                }
            });
        } else {
            bookBtn.setAttribute('href', 'tel:' + CONFIG.PHONE_E164);
        }
    });

    /* ---- Estimate form (contact page): composes an email ---- */
    var form = document.getElementById('estimateForm');
    if (form) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            var v = function (id) {
                var el = document.getElementById(id);
                return el ? el.value.trim() : '';
            };
            var subject = 'Project Inquiry - ' + (v('ef-name') || 'Website Visitor');
            var lines = [
                'Name: ' + v('ef-name'),
                'Phone: ' + v('ef-phone'),
                'Email: ' + v('ef-email'),
                'Town: ' + v('ef-town'),
                'Project type: ' + v('ef-service'),
                '',
                'Project details:',
                v('ef-message')
            ];
            window.location.href = 'mailto:' + CONFIG.EMAIL
                + '?subject=' + encodeURIComponent(subject)
                + '&body=' + encodeURIComponent(lines.join('\n'));
        });
    }

    /* ---- Footer year ---- */
    var yearEl = document.getElementById('footerYear');
    if (yearEl) { yearEl.textContent = String(new Date().getFullYear()); }
})();
