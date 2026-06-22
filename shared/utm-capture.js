(function(){
  // UTM Capture & Persistence — runs on every page
  // Captures UTM params from URL, persists to sessionStorage, exposes via window.__sl_utms
  var params = new URLSearchParams(location.search);
  var utmKeys = ['utm_source','utm_medium','utm_campaign','utm_term','utm_content','gclid','fbclid','msclkid'];
  var captured = {};
  var hasNew = false;
  utmKeys.forEach(function(k){
    var v = params.get(k);
    if (v) { captured[k] = v; hasNew = true; }
  });
  
  // Read prior session UTMs
  var stored = {};
  try { stored = JSON.parse(sessionStorage.getItem('sl_utms') || '{}'); } catch(e){}
  
  // If we have new UTMs in URL, write them (overwriting). Otherwise keep stored.
  var final = hasNew ? captured : stored;
  if (hasNew) {
    try { sessionStorage.setItem('sl_utms', JSON.stringify(final)); } catch(e){}
  }
  
  // Also capture document.referrer on first page (if not already stored)
  if (!sessionStorage.getItem('sl_referrer') && document.referrer) {
    try { sessionStorage.setItem('sl_referrer', document.referrer); } catch(e){}
  }
  
  // Capture landing page (first page of session)
  if (!sessionStorage.getItem('sl_landing')) {
    try { sessionStorage.setItem('sl_landing', location.pathname + location.search); } catch(e){}
  }
  
  // Expose globally
  window.__sl_utms = final;
  window.__sl_referrer = sessionStorage.getItem('sl_referrer') || '';
  window.__sl_landing = sessionStorage.getItem('sl_landing') || location.pathname;
  
  // Push to dataLayer for GTM tags to pick up
  window.dataLayer = window.dataLayer || [];
  var dlEvent = { event: 'attribution_loaded' };
  Object.keys(final).forEach(function(k){ dlEvent[k] = final[k]; });
  dlEvent.referrer = window.__sl_referrer;
  dlEvent.landing_page = window.__sl_landing;
  window.dataLayer.push(dlEvent);
  
  // Auto-inject hidden fields into any form on the page
  // Runs at DOMContentLoaded (or immediately if document is already ready)
  function injectFormFields(){
    var forms = document.querySelectorAll('form');
    forms.forEach(function(form){
      utmKeys.forEach(function(k){
        if (final[k] && !form.querySelector('input[name="'+k+'"]')) {
          var inp = document.createElement('input');
          inp.type = 'hidden';
          inp.name = k;
          inp.value = final[k];
          form.appendChild(inp);
        }
      });
      // Also referrer + landing
      if (window.__sl_referrer && !form.querySelector('input[name="referrer"]')) {
        var r = document.createElement('input');
        r.type = 'hidden'; r.name = 'referrer'; r.value = window.__sl_referrer;
        form.appendChild(r);
      }
      if (window.__sl_landing && !form.querySelector('input[name="landing_page"]')) {
        var l = document.createElement('input');
        l.type = 'hidden'; l.name = 'landing_page'; l.value = window.__sl_landing;
        form.appendChild(l);
      }
    });
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', injectFormFields);
  } else {
    injectFormFields();
  }
})();