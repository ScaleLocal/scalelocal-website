/* TNJ Custom Contact Launcher — handles the floating button & 4-action panel.
   Opens, closes, and hands off "Chat with us" to the embedded GHL widget. */
(function(){
  function $(s,r){return (r||document).querySelector(s);}

  // Strategies to open the GHL chat. Tried in order. Each returns true if it succeeded.
  function tryOpenGHL(){
    // 1) Public LeadConnector API if it exists
    try{
      if(window.LeadConnector && typeof window.LeadConnector.openChat === 'function'){
        window.LeadConnector.openChat();
        return true;
      }
    }catch(e){}

    // 2) Postmessage to the GHL widget iframe (works for newer AIO widgets)
    try{
      var ifr = document.querySelector('iframe[src*="leadconnectorhq.com/chat-widget"]');
      if(ifr && ifr.contentWindow){
        ifr.contentWindow.postMessage({type:'openChat'},'*');
        ifr.setAttribute('data-tnj-active','true');
        return true;
      }
    }catch(e){}

    // 3) Find the lc-chat-widget custom element and call its open method or click it
    try{
      var wc = document.querySelector('lc-chat-widget');
      if(wc){
        // Make it visible briefly and click its bubble button
        wc.style.cssText = 'display:block !important;visibility:visible !important;';
        var bubble = wc.shadowRoot && wc.shadowRoot.querySelector('button, [role="button"], .chat-bubble, .lc-chat-bubble');
        if(bubble && bubble.click){ bubble.click(); return true; }
        if(typeof wc.open === 'function'){ wc.open(); return true; }
        if(typeof wc.click === 'function'){ wc.click(); return true; }
      }
    }catch(e){}

    // 4) Last-ditch: temporarily un-hide the GHL widget so the user can use its native bubble
    try{
      var st = document.getElementById('tnj-ghl-bubble-hide');
      if(st){
        st.disabled = true;
        // Re-enable the hider after 30s if user didn't engage
        setTimeout(function(){ try{ st.disabled = false; }catch(e){} }, 30000);
        return true;
      }
    }catch(e){}

    return false;
  }

  function openGHLChat(){
    if(tryOpenGHL()) return;
    // Fallback: scroll to estimate form / nav to contact
    var f = document.getElementById('estimate');
    if(f){ f.scrollIntoView({behavior:'smooth',block:'start'}); return; }
    window.location.href = 'contact.html#estimate';
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
  // Use a small retry to attach handlers either way.
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
