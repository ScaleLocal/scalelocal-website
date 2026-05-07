/* TNJ — Shared partials. Loads on every page.
   - Sets active nav state
   - Injects the custom contact launcher (with GHL chat handoff) if not already present
   - Loads the GHL AIO chat widget (hidden bubble — opens via custom launcher)
   - Injects CSS to hide the GHL native bubble (we use the custom launcher as the
     visible UX). Verified: the GHL widget renders as <chat-widget> with the
     bubble drawn by its shadow DOM. Hiding the host element hides the bubble;
     the open chat panel is positioned by the same component, so when we call
     leadConnector.chatWidget.openWidget() we temporarily allow visibility.
   ============================================================ */
(function(){
  var GHL_WIDGET_ID = '69fcd6a6d663de65e9565ab7';

  var LAUNCHER_HTML = '<div class="tnj-launcher" role="dialog" aria-label="Get help">'
    + '<div class="tnj-launcher-panel"><div class="tnj-launcher-head"><h4>How can we help?</h4><p>Thomas responds personally &mdash; usually within an hour.</p></div>'
    + '<a href="sms:7818440482?body=Emergency%20at%20" class="tnj-launcher-action"><div class="tnj-action-icon red"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg></div><div class="tnj-action-text"><p class="t">Urgent &mdash; text Thomas</p><p class="s">Direct line to the owner</p></div></a>'
    + '<button class="tnj-launcher-action" data-tnj-action="chat"><div class="tnj-action-icon purple"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/></svg></div><div class="tnj-action-text"><p class="t">Chat with us</p><p class="s">Instant answers about our work</p></div></button>'
    + '<button class="tnj-launcher-action" data-tnj-action="book"><div class="tnj-action-icon teal"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg></div><div class="tnj-action-text"><p class="t">Schedule a free estimate</p><p class="s">Pick a time that works</p></div></button>'
    + '<a href="tel:7818440482" class="tnj-launcher-action"><div class="tnj-action-icon blue"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07 19.5 19.5 0 01-6-6 19.79 19.79 0 01-3.07-8.67A2 2 0 014.11 2h3a2 2 0 012 1.72 12.84 12.84 0 00.7 2.81 2 2 0 01-.45 2.11L8.09 9.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45 12.84 12.84 0 002.81.7A2 2 0 0122 16.92z"/></svg></div><div class="tnj-action-text"><p class="t">781-844-0482</p><p class="s">Open now &middot; Mon &ndash; Sat 7a&ndash;6p</p></div></a>'
    + '<div class="tnj-launcher-foot">Powered by ScaleLocal</div></div>'
    + '<button class="tnj-launcher-btn" aria-label="Open contact options"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 11.5a8.38 8.38 0 01-.9 3.8 8.5 8.5 0 01-7.6 4.7 8.38 8.38 0 01-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 01-.9-3.8 8.5 8.5 0 014.7-7.6 8.38 8.38 0 013.8-.9h.5a8.48 8.48 0 018 8v.5z"/></svg><span class="tnj-launcher-badge">3</span></button></div>';

  // CSS hides the GHL bubble by default. When we open the widget programmatically
  // we add data-tnj-chat-open=true on documentElement, which switches visibility on.
  // Defense-in-depth: hide GHL bubble entirely most of the time. Even if a
  // flash slips through during script load, force the GHL widget's host
  // element behind the custom launcher and shrink any bubble inside its
  // shadow DOM by re-styling chat-widget to occupy the same corner but with
  // very low z-index. When we explicitly open the chat, html[data-tnj-chat-open]
  // is set and we restore display + raise z-index so the open panel renders.
  var HIDE_GHL_BUBBLE_CSS = ''
    + 'chat-widget{position:fixed !important;right:24px !important;bottom:24px !important;width:0 !important;height:0 !important;opacity:0 !important;pointer-events:none !important;z-index:1 !important;overflow:hidden !important;}'
    + 'html[data-tnj-chat-open="true"] chat-widget{width:auto !important;height:auto !important;opacity:1 !important;pointer-events:auto !important;z-index:9999 !important;overflow:visible !important;}';

  function injectStyles(){
    if(document.getElementById('tnj-ghl-bubble-hide'))return;
    var s=document.createElement('style');
    s.id='tnj-ghl-bubble-hide';
    s.textContent=HIDE_GHL_BUBBLE_CSS;
    document.head.appendChild(s);
  }

  function injectLauncher(){
    if(document.querySelector('.tnj-launcher'))return; // already in HTML
    var div=document.createElement('div');
    div.innerHTML=LAUNCHER_HTML;
    document.body.appendChild(div.firstChild);
  }

  function injectGHLWidget(){
    if(document.querySelector('script[data-widget-id="'+GHL_WIDGET_ID+'"]'))return;
    var s=document.createElement('script');
    s.src='https://widgets.leadconnectorhq.com/loader.js';
    s.setAttribute('data-resources-url','https://widgets.leadconnectorhq.com/chat-widget/loader.js');
    s.setAttribute('data-widget-id',GHL_WIDGET_ID);
    document.body.appendChild(s);
  }

  function setActiveNav(){
    var p=window.location.pathname.split('/').pop()||'index.html';
    document.querySelectorAll('nav a').forEach(function(a){
      var h=a.getAttribute('href');if(!h)return;
      var hf=h.split('/').pop();
      if(hf===p)a.classList.add('active');
    });
  }

  function init(){
    injectStyles();
    injectLauncher();
    injectGHLWidget();
    setActiveNav();
  }

  if(document.readyState==='loading'){
    document.addEventListener('DOMContentLoaded',init);
  } else {
    init();
  }
})();
