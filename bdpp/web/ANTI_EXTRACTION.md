# BD++ Sniper Anti-Extraction Strategy

Browser-based protection is **deterrence, not security**. The ceiling is "stops casual copying by non-technical users." Anything rendered in a browser can be extracted by a determined actor — the goal is friction, not prevention.

This document catalogs the techniques that work, the tricks that look impressive but accomplish nothing, and the limits you must communicate to stakeholders.

---

## 1. CSS `user-select` disable

```css
.no-select,
.no-select * {
  -webkit-user-select: none;  /* Safari, old Chrome */
  -khtml-user-select: none;   /* Konqueror */
  -moz-user-select: none;     /* Firefox */
  -ms-user-select: none;      /* IE / old Edge */
  user-select: none;          /* standard */
  -webkit-touch-callout: none; /* iOS long-press menu */
}
```

## 2. Right-click context menu blocking

Inline:
```html
<body oncontextmenu="return false;">
```

Programmatic:
```js
document.addEventListener('contextmenu', (e) => {
  e.preventDefault();
  return false;
}, { capture: true });
```

## 3. Keyboard shortcut blocking

```js
document.addEventListener('keydown', (e) => {
  const k = e.key.toLowerCase();
  const mod = e.ctrlKey || e.metaKey; // Ctrl on Win/Linux, Cmd on Mac

  // Copy/cut/paste/save/print/select-all/view-source
  if (mod && ['c', 'x', 'v', 's', 'p', 'a', 'u'].includes(k)) {
    e.preventDefault(); return false;
  }
  // F12 devtools
  if (e.key === 'F12') { e.preventDefault(); return false; }
  // Ctrl/Cmd + Shift + I / J / C (devtools, console, inspector)
  if (mod && e.shiftKey && ['i', 'j', 'c'].includes(k)) {
    e.preventDefault(); return false;
  }
}, { capture: true });

// Also block copy/cut/paste at the event level
['copy', 'cut', 'paste'].forEach(ev =>
  document.addEventListener(ev, e => e.preventDefault(), { capture: true })
);
```

## 4. DevTools detection

**Window dimension delta** — docked devtools shrinks the inner viewport:
```js
setInterval(() => {
  const wThresh = window.outerWidth  - window.innerWidth  > 160;
  const hThresh = window.outerHeight - window.innerHeight > 160;
  if (wThresh || hThresh) onDevToolsOpen();
}, 1000);
```

**Debugger timing trick** — `debugger` pauses execution only when devtools is open:
```js
setInterval(() => {
  const t0 = performance.now();
  // eslint-disable-next-line no-debugger
  debugger;
  if (performance.now() - t0 > 100) onDevToolsOpen();
}, 2000);
```

Limits:
- Dimension trick **misses undocked devtools** (separate window).
- Debugger trick **doesn't fire if devtools opened before script loads**.
- Neither detects **remote debugging, browser extensions, or proxy interception**.

## 5. Drag-drop blocking

```js
document.addEventListener('dragstart', e => e.preventDefault(), { capture: true });
document.addEventListener('drop',      e => e.preventDefault(), { capture: true });
```

## 6. Print blocking

```css
@media print {
  body { display: none !important; }
  html::before {
    content: "Printing disabled.";
    display: block;
  }
}
```

## 7. Window-blur blur (screenshot deterrence)

```css
body.window-blurred {
  filter: blur(20px);
  transition: filter 0.1s;
}
```
```js
window.addEventListener('blur',  () => document.body.classList.add('window-blurred'));
window.addEventListener('focus', () => document.body.classList.remove('window-blurred'));
```
Stops naive "screenshot the whole desktop" workflows where the user alt-tabs to the snipping tool — the page is blurred the moment focus leaves.

## 8. Dynamic watermark overlay

Diagonal repeating SVG with user ID + ISO timestamp, redrawn every 5 seconds.

```html
<div id="wm" style="
  position: fixed; inset: 0; pointer-events: none;
  z-index: 2147483647; opacity: 0.12;
  mix-blend-mode: difference;"></div>
```
```js
function paintWatermark(userId) {
  const stamp = `${userId} | ${new Date().toISOString()}`;
  const svg = `
    <svg xmlns="http://www.w3.org/2000/svg" width="400" height="200">
      <text x="0" y="100" transform="rotate(-30 200 100)"
            font-family="monospace" font-size="14" fill="#000">${stamp}</text>
    </svg>`;
  const url = `url("data:image/svg+xml;utf8,${encodeURIComponent(svg)}")`;
  document.getElementById('wm').style.backgroundImage = url;
}
paintWatermark(window.USER_ID);
setInterval(() => paintWatermark(window.USER_ID), 5000);
```

## 9. Screenshot deterrence on iOS/Android

```html
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="format-detection" content="telephone=no">
```

**There is no web API to block OS-level screenshots.** `screen-capture-protected` is **not a web standard** — it exists only in native Android (`FLAG_SECURE`) and iOS native APIs. A browser-rendered page **cannot** invoke it. Mobile users will always be able to screenshot.

## 10. What it cannot stop

- **OS screenshot tools** — macOS `Cmd+Shift+5`, Windows Snipping Tool, `PrtSc`.
- **Phone camera pointed at the screen.** Zero defense.
- **Screen recorders / OBS / Loom / Teams sharing** — they capture the framebuffer.
- **Browser extensions** that strip protection scripts or re-enable selection.
- **DevTools opened *before* the page loads** — your detection script never runs.
- **JavaScript disabled** — all keyboard/menu/devtools handlers are gone.
- **Proxy interception** (mitmproxy, Burp, Fiddler) stripping the protection bundle in flight.
- **View Source via `view-source:` URL prefix** — bypasses `Ctrl+U` block entirely.
- **Headless browsers** (Puppeteer, Playwright) ignoring your event handlers.
- **Accessibility tools** reading the DOM directly.

---

**Honest recommendation — this stack stops 95% of casual copying. It will not stop a determined actor. For information that absolutely must not leak, do not put it in a web app.**
