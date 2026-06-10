/* Santos & Sons — custom four-action contact launcher (bottom-right).
   Pattern: TNJ build. Injects its own markup, binds actions, and hands
   "Chat with us" off to the GHL AIO widget once that script is embedded
   (Preview Slot TBD). Until then, Chat falls back to the estimate form.

   GHL widget API (verified on TNJ, May 2026):
     window.leadConnector.chatWidget.openWidget()
     window.leadConnector.chatWidget.isLoaded / .isActive
   ============================================================ */
(function () {
  var PHONE_DISPLAY = '(978) 888-4638';
  var PHONE_RAW = '9788884638';

  var ICON = {
    text: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
    chat: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/></svg>',
    book: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>',
    call: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07 19.5 19.5 0 01-6-6 19.79 19.79 0 01-3.07-8.67A2 2 0 014.11 2h3a2 2 0 012 1.72 12.84 12.84 0 00.7 2.81 2 2 0 01-.45 2.11L8.09 9.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45 12.84 12.84 0 002.81.7A2 2 0 0122 16.92z"/></svg>',
    open: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 11.5a8.38 8.38 0 01-.9 3.8 8.5 8.5 0 01-7.6 4.7 8.38 8.38 0 01-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 01-.9-3.8 8.5 8.5 0 014.7-7.6 8.38 8.38 0 013.8-.9h.5a8.48 8.48 0 018 8v.5z"/></svg>'
  };

  var HTML =
    '<div class="ss-launcher" role="dialog" aria-label="Get in touch">' +
      '<div class="ss-launcher-panel">' +
        '<div class="ss-launcher-head"><h4>How can we help?</h4><p>Derek answers personally &mdash; usually the same day.</p></div>' +
        '<a href="sms:' + PHONE_RAW + '?body=Urgent%20fence%20question%20%E2%80%94%20" class="ss-launcher-action"><div class="ss-action-icon red">' + ICON.text + '</div><div class="ss-action-text"><p class="t">Urgent &mdash; text Derek</p><p class="s">Straight to the owner’s phone</p></div></a>' +
        '<button type="button" class="ss-launcher-action" data-ss-action="chat"><div class="ss-action-icon green">' + ICON.chat + '</div><div class="ss-action-text"><p class="t">Chat with us</p><p class="s">Quick answers about our work</p></div></button>' +
        '<button type="button" class="ss-launcher-action" data-ss-action="book"><div class="ss-action-icon gold">' + ICON.book + '</div><div class="ss-action-text"><p class="t">Book a free estimate</p><p class="s">Tell us about your project</p></div></button>' +
        '<a href="tel:' + PHONE_RAW + '" class="ss-launcher-action"><div class="ss-action-icon dark">' + ICON.call + '</div><div class="ss-action-text"><p class="t">' + PHONE_DISPLAY + '</p><p class="s">Mon&ndash;Sat &middot; 8a&ndash;5p</p></div></a>' +
        '<div class="ss-launcher-foot">Powered by ScaleLocal</div>' +
      '</div>' +
      '<button type="button" class="ss-launcher-btn" aria-label="Open contact options">' + ICON.open + '<span class="ss-launcher-badge" aria-hidden="true"></span></button>' +
    '</div>';

  /* --- GHL widget integration (no-op until the Slot widget is embedded) --- */
  var SHADOW_HIDE_CSS =
    '#lc_text-widget--btn,.lc_text-widget--bubble,.lc_chat-bubble,.lc_chat-prompt,.lc_chat-prompt--container,' +
    '[class*="bubble"]:not([class*="message"]):not([class*="agent"]):not([class*="visitor"]),[id*="bubble"]' +
    '{display:none!important;visibility:hidden!important;opacity:0!important;pointer-events:none!important;width:0!important;height:0!important;}' +
    '#lc_text-widget,#lc_text-widget--box,#lc_text-widget--box.active{max-height:443px!important;height:443px!important;}' +
    '.lc_text-widget--formContainer{max-height:336px!important;}';

  function injectShadowCSS() {
    var cw = document.querySelector('chat-widget');
    if (!cw || !cw.shadowRoot) return false;
    if (cw.shadowRoot.querySelector('#ss-shadow-hide')) return true;
    var s = document.createElement('style');
    s.id = 'ss-shadow-hide';
    s.textContent = SHADOW_HIDE_CSS;
    cw.shadowRoot.appendChild(s);
    return true;
  }

  function ghlReady() {
    return !!(window.leadConnector && window.leadConnector.chatWidget &&
      typeof window.leadConnector.chatWidget.openWidget === 'function' &&
      window.leadConnector.chatWidget.isLoaded);
  }

  function bookEstimate() {
    var f = document.getElementById('estimate');
    if (f) { f.scrollIntoView({ behavior: 'smooth', block: 'start' }); return; }
    window.location.href = 'contact.html#estimate';
  }

  function openGHLChat(retries) {
    retries = (retries == null) ? 15 : retries; /* ~3s — short, then graceful fallback */
    if (ghlReady()) {
      injectShadowCSS();
      try { window.leadConnector.chatWidget.openWidget(); } catch (e) {}
      var poll = setInterval(function () {
        try {
          if (window.leadConnector.chatWidget.isActive === false) { clearInterval(poll); }
        } catch (e) { clearInterval(poll); }
      }, 500);
      setTimeout(function () { try { clearInterval(poll); } catch (e) {} }, 600000);
      return;
    }
    if (retries <= 0) { bookEstimate(); return; }
    setTimeout(function () { openGHLChat(retries - 1); }, 200);
  }

  function init() {
    if (document.querySelector('.ss-launcher')) return;
    var host = document.createElement('div');
    host.innerHTML = HTML;
    document.body.appendChild(host.firstChild);

    var l = document.querySelector('.ss-launcher');
    var btn = l.querySelector('.ss-launcher-btn');
    btn.addEventListener('click', function (e) { e.stopPropagation(); l.classList.toggle('open'); });
    document.addEventListener('click', function (e) { if (!l.contains(e.target)) l.classList.remove('open'); });

    l.querySelector('[data-ss-action="chat"]').addEventListener('click', function (e) {
      e.preventDefault(); l.classList.remove('open');
      /* If the GHL widget is on the page (script embedded), keep retrying briefly;
         if it was never embedded, fall back to the estimate form immediately. */
      openGHLChat(document.querySelector('chat-widget') ? 15 : 0);
    });
    l.querySelector('[data-ss-action="book"]').addEventListener('click', function (e) {
      e.preventDefault(); l.classList.remove('open'); bookEstimate();
    });

    /* Pre-hide GHL bubble whenever the widget eventually loads */
    var tries = 0;
    var t = setInterval(function () {
      if (injectShadowCSS() || ++tries > 120) clearInterval(t);
    }, 1000);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
