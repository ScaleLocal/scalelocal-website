/* TNJ Custom Contact Launcher — handles the floating button & 4-action panel.
   Opens, closes, and hands off "Chat with us" to the embedded GHL widget.

   GHL widget API (verified live, May 2026):
     window.leadConnector.chatWidget.openWidget()
     window.leadConnector.chatWidget.closeWidget()
     window.leadConnector.chatWidget.isLoaded
     window.leadConnector.chatWidget.isActive
   ============================================================ */
(function(){
  function $(s,r){return (r||document).querySelector(s);}

  function ghlReady(){
    return !!(window.leadConnector
              && window.leadConnector.chatWidget
              && typeof window.leadConnector.chatWidget.openWidget === 'function'
              && window.leadConnector.chatWidget.isLoaded);
  }

  function showWidget(){
    document.documentElement.setAttribute('data-tnj-chat-open', 'true');
  }
  function hideWidget(){
    document.documentElement.removeAttribute('data-tnj-chat-open');
  }

  function openGHLChat(retries){
    retries = (retries == null) ? 25 : retries; // ~5s of polling
    if(ghlReady()){
      showWidget();
      try{ window.leadConnector.chatWidget.openWidget(); }catch(e){}
      // Watch for chat close so we can re-hide the host element afterward
      var poll = setInterval(function(){
        try{
          if(window.leadConnector && window.leadConnector.chatWidget
             && window.leadConnector.chatWidget.isActive === false){
            clearInterval(poll);
            hideWidget();
          }
        }catch(e){ clearInterval(poll); hideWidget(); }
      }, 500);
      // Safety: hide again after 10 minutes regardless
      setTimeout(function(){ try{ clearInterval(poll); }catch(e){} }, 10*60*1000);
      return;
    }
    if(retries <= 0){
      // GHL widget didn't load — fallback to estimate form
      var f = document.getElementById('estimate');
      if(f){ f.scrollIntoView({behavior:'smooth',block:'start'}); return; }
      window.location.href = 'contact.html#estimate';
      return;
    }
    setTimeout(function(){ openGHLChat(retries - 1); }, 200);
  }

  function bookEstimate(){
    var f = document.getElementById('estimate');
    if(f){ f.scrollIntoView({behavior:'smooth',block:'start'}); return; }
    window.location.href = 'contact.html#estimate';
  }

  function bind(){
    var l = $('.tnj-launcher');
    if(!l) return;

    var b = $('.tnj-launcher-btn', l);
    if(b){
      b.addEventListener('click', function(e){
        e.stopPropagation();
        l.classList.toggle('open');
      });
    }

    document.addEventListener('click', function(e){
      if(!l.contains(e.target)) l.classList.remove('open');
    });

    var c = $('[data-tnj-action="chat"]', l);
    if(c) c.addEventListener('click', function(e){
      e.preventDefault();
      openGHLChat();
      l.classList.remove('open');
    });

    var bk = $('[data-tnj-action="book"]', l);
    if(bk) bk.addEventListener('click', function(e){
      e.preventDefault();
      bookEstimate();
      l.classList.remove('open');
    });
  }

  // _partials.js may inject the launcher AFTER DOMContentLoaded.
  function attempt(retries){
    if($('.tnj-launcher')){ bind(); return; }
    if(retries <= 0) return;
    setTimeout(function(){ attempt(retries-1); }, 60);
  }

  if(document.readyState==='loading'){
    document.addEventListener('DOMContentLoaded', function(){ attempt(20); });
  } else {
    attempt(20);
  }
})();
