(function (root) {
  // The one place the Give address is written for the floating pill (same as GIVE_URL in build.py).
  var GIVE_URL = 'https://givebutter.com/SpreadJoyCollective';

  // The pill is always in the corner, except while a Give band is already on screen.
  function givePillVisible(band, vh) {
    return !(band && band.top < vh && band.bottom > 0);
  }

  // Everything is looked up on each update: Squarespace re-draws blocks after load.
  function initGive(doc, win) {
    function update() {
      var pill = doc.getElementById('sj-give-pill');
      if (!pill) {
        pill = doc.createElement('a');
        pill.id = 'sj-give-pill';
        pill.className = 'sj-give-pill';
        pill.textContent = 'Give ♥';
        pill.setAttribute('href', GIVE_URL);
        pill.setAttribute('target', '_blank');
        pill.setAttribute('rel', 'noopener');
        doc.body.appendChild(pill);
      }
      var band = doc.getElementById('sj-give');
      var r = band ? band.getBoundingClientRect() : null;
      pill.classList.toggle('on', givePillVisible(r, win.innerHeight));
    }
    win.addEventListener('scroll', update, { passive: true });
    win.addEventListener('resize', update);
    update();
    win.setTimeout && [100, 1000, 2500].forEach(function (ms) { win.setTimeout(update, ms); });
  }

  var api = { GIVE_URL: GIVE_URL, givePillVisible: givePillVisible, initGive: initGive };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  if (typeof document !== 'undefined' && typeof window !== 'undefined') {
    root.GivePill = api;
    // run once the page body exists; the footer injection already runs after it
    if (document.body) initGive(document, window);
    else document.addEventListener('DOMContentLoaded', function () { initGive(document, window); });
  }
})(typeof window !== 'undefined' ? window : globalThis);
