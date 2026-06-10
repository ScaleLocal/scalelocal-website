/* HVAC Pro Beast — Custom Contact Launcher (pattern: TNJ build, verified May 2026).
   Handles the floating button & 4-action panel. "Chat" hands off to the GHL AIO
   widget once it is embedded (see placeholder comment in _partials.js). Until the
   widget is cloned into the assigned Preview Slot, Chat falls back to the
   estimate form. */
(function(){
  function $(s,r){return (r||document).querySelector(s);}
  function ghlReady(){
    return !!(window.leadConnector && window.leadConnector.chatWidget
      && typeof window.leadConnector.chatWidget.openWidget === 'function'
      && window.leadConnector.chatWidget.isLoaded);
  }
  function showWidget(){ document.documentElement.setAttribute('data-hpb-chat-open','true'); }
  function hideWidget(){ document.documentElement.removeAttribute('data-hpb-chat-open'); }
  function openGHLChat(retries){
    retries = (retries==null)?15:retries;
    if(ghlReady()){
      showWidget();
      try{ window.leadConnector.chatWidget.openWidget(); }catch(e){}
      var poll=setInterval(function(){
        try{
          if(window.leadConnector && window.leadConnector.chatWidget
             && window.leadConnector.chatWidget.isActive===false){ clearInterval(poll); hideWidget(); }
        }catch(e){ clearInterval(poll); hideWidget(); }
      },500);
      setTimeout(function(){ try{ clearInterval(poll); }catch(e){} },10*60*1000);
      return;
    }
    if(retries<=0){
      var f=document.getElementById('estimate');
      if(f){ f.scrollIntoView({behavior:'smooth',block:'start'}); return; }
      window.location.href=(window.HPB_ROOT||'')+'contact.html#estimate';
      return;
    }
    setTimeout(function(){ openGHLChat(retries-1); },200);
  }
  function bookEstimate(){
    var f=document.getElementById('estimate');
    if(f){ f.scrollIntoView({behavior:'smooth',block:'start'}); return; }
    window.location.href=(window.HPB_ROOT||'')+'contact.html#estimate';
  }
  function bind(){
    var l=$('.hpb-launcher'); if(!l) return;
    var b=$('.hpb-launcher-btn',l);
    if(b){ b.addEventListener('click',function(e){ e.stopPropagation(); l.classList.toggle('open'); }); }
    document.addEventListener('click',function(e){ if(!l.contains(e.target)) l.classList.remove('open'); });
    var c=$('[data-hpb-action="chat"]',l);
    if(c) c.addEventListener('click',function(e){ e.preventDefault(); openGHLChat(); l.classList.remove('open'); });
    var bk=$('[data-hpb-action="book"]',l);
    if(bk) bk.addEventListener('click',function(e){ e.preventDefault(); bookEstimate(); l.classList.remove('open'); });
  }
  function attempt(retries){
    if($('.hpb-launcher')){ bind(); return; }
    if(retries<=0) return;
    setTimeout(function(){ attempt(retries-1); },60);
  }
  if(document.readyState==='loading'){ document.addEventListener('DOMContentLoaded',function(){ attempt(20); }); }
  else{ attempt(20); }
})();
