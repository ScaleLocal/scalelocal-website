/* HVAC Pro Beast — shared partials. Injects the 4-action launcher on every page.
   window.HPB_ROOT is set per-page ('' at root, '../' in subfolders). */

/* <!-- HVAC Pro Beast AIO Chat Widget (Preview Slot N) — clone of Slot 1 (Superior Sealcoat 69d9496fc41f60a7fa93719d) trained on HVAC Pro Beast. Once cloned in GHL, replace this comment with the <script> embed and remove the launcher chat fallback note. --> */

(function(){
  var R = window.HPB_ROOT || '';
  var LAUNCHER_HTML = '<div class="hpb-launcher" role="dialog" aria-label="Contact options">'
    + '<div class="hpb-launcher-panel"><div class="hpb-launcher-head"><h4>How can we help?</h4><p>Tom answers around the clock. 24/7 emergency service.</p></div>'
    + '<a href="sms:7813508141?body=Urgent%20refrigeration%2FHVAC%20issue%20at%20" class="hpb-launcher-action"><div class="hpb-action-icon red"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg></div><div class="hpb-action-text"><p class="t">Urgent — text Tom now</p><p class="s">Walk-in down? Ice machine out?</p></div></a>'
    + '<button class="hpb-launcher-action" data-hpb-action="chat"><div class="hpb-action-icon purple"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/></svg></div><div class="hpb-action-text"><p class="t">Chat with us</p><p class="s">Instant answers about our services</p></div></button>'
    + '<button class="hpb-launcher-action" data-hpb-action="book"><div class="hpb-action-icon teal"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg></div><div class="hpb-action-text"><p class="t">Request a free estimate</p><p class="s">Tell us about your equipment</p></div></button>'
    + '<a href="tel:7813508141" class="hpb-launcher-action"><div class="hpb-action-icon blue"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07 19.5 19.5 0 01-6-6 19.79 19.79 0 01-3.07-8.67A2 2 0 014.11 2h3a2 2 0 012 1.72 12.84 12.84 0 00.7 2.81 2 2 0 01-.45 2.11L8.09 9.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45 12.84 12.84 0 002.81.7A2 2 0 0122 16.92z"/></svg></div><div class="hpb-action-text"><p class="t">(781) 350-8141</p><p class="s">Open now — 24/7, every day</p></div></a>'
    + '<div class="hpb-launcher-foot">Powered by ScaleLocal</div></div>'
    + '<button class="hpb-launcher-btn" aria-label="Open contact options"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 11.5a8.38 8.38 0 01-.9 3.8 8.5 8.5 0 01-7.6 4.7 8.38 8.38 0 01-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 01-.9-3.8 8.5 8.5 0 014.7-7.6 8.38 8.38 0 013.8-.9h.5a8.48 8.48 0 018 8v.5z"/></svg><span class="hpb-launcher-badge">4</span></button></div>';
  function inject(){
    if(document.querySelector('.hpb-launcher')) return;
    var d=document.createElement('div'); d.innerHTML=LAUNCHER_HTML;
    document.body.appendChild(d.firstChild);
  }
  if(document.readyState==='loading'){ document.addEventListener('DOMContentLoaded',inject); } else { inject(); }
})();
