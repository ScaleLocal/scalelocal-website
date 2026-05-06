(function(){
  function $(s,r){return (r||document).querySelector(s);}
  function openGHLChat(){
    var tried=false;
    try{if(window.LeadConnector&&typeof window.LeadConnector.openChat==='function'){window.LeadConnector.openChat();tried=true;}}catch(e){}
    if(!tried){var b=document.querySelector('lc-chat-widget')||document.querySelector('iframe[src*="leadconnectorhq"]');if(b&&b.click){try{b.click();tried=true;}catch(e){}}}
    if(!tried){var f=document.getElementById('estimate');if(f)f.scrollIntoView({behavior:'smooth',block:'start'});else window.location.href='contact.html#estimate';}
  }
  function bookEstimate(){var f=document.getElementById('estimate');if(f){f.scrollIntoView({behavior:'smooth',block:'start'});return;}window.location.href='contact.html#estimate';}
  document.addEventListener('DOMContentLoaded',function(){
    var l=$('.tnj-launcher');if(!l)return;
    var b=$('.tnj-launcher-btn',l);
    b.addEventListener('click',function(e){e.stopPropagation();l.classList.toggle('open');});
    document.addEventListener('click',function(e){if(!l.contains(e.target))l.classList.remove('open');});
    var c=$('[data-tnj-action="chat"]',l);if(c)c.addEventListener('click',function(e){e.preventDefault();openGHLChat();l.classList.remove('open');});
    var bk=$('[data-tnj-action="book"]',l);if(bk)bk.addEventListener('click',function(e){e.preventDefault();bookEstimate();l.classList.remove('open');});
  });
})();
