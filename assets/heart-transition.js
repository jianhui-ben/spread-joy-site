(function (root) {
  // Page-open effect on the landing page: a yellow heart-shaped cover shrinks away to reveal the page,
  // and a heart stays behind the headline. Added by a teammate on the Squarespace master; the styles are
  // in assets/heart-transition.css. Like the heart counter, the hero Code Block carries it on its own.
  var DURATION = 750;
  var DURATION_REDUCED = 150;

  // The landing page is "/" or "/home" on Squarespace, and "/index.html" in the local preview.
  function isHomePath(path) {
    var p = path.replace(/\/$/, '');
    return p === '' || p === '/home' || p === '/index.html';
  }

  function initHeartTransition(doc, win) {
    if (win.self !== win.top) return; // not inside the editor's preview frame

    var container = doc.querySelector('.sj-home');
    if (!container || container.querySelector('#heart-transition')) return;
    if (!isHomePath(win.location.pathname)) return;

    var duration = win.matchMedia('(prefers-reduced-motion: reduce)').matches ? DURATION_REDUCED : DURATION;

    var heart = doc.createElement('div');
    heart.id = 'heart-transition';
    heart.setAttribute('aria-hidden', 'true');
    container.insertBefore(heart, container.firstChild);

    // start fully covered with no animation, then let it shrink on the next painted frame
    heart.style.setProperty('--heart-duration', '0ms');
    heart.classList.add('visible', 'cover');
    win.requestAnimationFrame(function () {
      win.requestAnimationFrame(function () {
        heart.style.setProperty('--heart-duration', duration + 'ms');
        heart.classList.remove('cover');
        heart.classList.add('persistent');
      });
    });
  }

  var api = { initHeartTransition: initHeartTransition, isHomePath: isHomePath };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;

  if (typeof document !== 'undefined' && typeof window !== 'undefined') {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', function () { initHeartTransition(document, window); }, { once: true });
    } else {
      initHeartTransition(document, window);
    }
  }
})(typeof window !== 'undefined' ? window : globalThis);
