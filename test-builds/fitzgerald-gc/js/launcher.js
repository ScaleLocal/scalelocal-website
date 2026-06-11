/* ============================================================
   Fitzgerald GC — custom four-action launcher behavior.
   Opens/closes the panel and wires the "Chat" + "Book" actions.

   "Chat with us" hands off to the GHL AIO chat widget IF it's loaded.
   Until a Preview Slot is assigned and the widget is embedded (see
   site.js GHL_WIDGET_ID + the placeholder comment on each page), the
   GHL widget is NOT present, so "Chat" gracefully falls back to the
   estimate form / contact page. No broken behavior in the demo state.

   GHL widget API (verified live, ScaleLocal builds 2026):
     window.leadConnector.chatWidget.openWidget()
     window.leadConnector.chatWidget.isLoaded
     window.leadConnector.chatWidget.isActive
   ============================================================ */
(function () {
  'use strict';
  function $(s, r) { return (r || document).querySelector(s); }

  function ghlReady() {
    return !!(window.leadConnector
      && window.leadConnector.chatWidget
      && typeof window.leadConnector.chatWidget.openWidget === 'function'
      && window.leadConnector.chatWidget.isLoaded);
  }

  function bookEstimate() {
    var f = document.getElementById('estimate');
    if (f) { f.scrollIntoView({ behavior: 'smooth', block: 'start' }); return; }
    window.location.href = 'contact.html#estimate';
  }

  function openChat(retries) {
    retries = (retries == null) ? 12 : retries; // ~2.4s of polling
    if (ghlReady()) {
      try { window.leadConnector.chatWidget.openWidget(); } catch (e) {}
      return;
    }
    if (retries <= 0) { bookEstimate(); return; } // demo fallback: no widget yet
    setTimeout(function () { openChat(retries - 1); }, 200);
  }

  function bind() {
    var l = $('.fitz-launcher');
    if (!l) return;
    var b = $('.fitz-launcher-btn', l);
    if (b) b.addEventListener('click', function (e) {
      e.stopPropagation();
      l.classList.toggle('open');
    });
    document.addEventListener('click', function (e) {
      if (!l.contains(e.target)) l.classList.remove('open');
    });
    var c = $('[data-fitz-action="chat"]', l);
    if (c) c.addEventListener('click', function (e) {
      e.preventDefault(); openChat(); l.classList.remove('open');
    });
    var bk = $('[data-fitz-action="book"]', l);
    if (bk) bk.addEventListener('click', function (e) {
      e.preventDefault(); bookEstimate(); l.classList.remove('open');
    });
  }

  // site.js injects the launcher (possibly after DOMContentLoaded), so poll briefly.
  function attempt(retries) {
    if ($('.fitz-launcher')) { bind(); return; }
    if (retries <= 0) return;
    setTimeout(function () { attempt(retries - 1); }, 60);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { attempt(25); });
  } else { attempt(25); }
})();
