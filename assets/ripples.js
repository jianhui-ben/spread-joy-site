(function (root) {
  // The "ripples of joy" heart and counter. This file is self-contained: the hero Code Block carries it
  // on its own (see home-page/3-hero-block.html), so no site-wide or footer script is needed for it.
  //
  // PLACEHOLDER: this number is made up, not a real count. There is no server, so it is worked out from the
  // clock: it starts at PLACEHOLDER_START_COUNT on EPOCH_MS, goes up by one every TICK_MS for everyone, and
  // goes back to 0 at WRAP_AT (ten million). A visitor's own taps are added on top and remembered in this
  // browser (localStorage, key below). Replace all of it with real data later.
  var PLACEHOLDER_START_COUNT = 1284;
  var EPOCH_MS = Date.UTC(2026, 9, 17); // 17 October 2026, the day the placeholder was made up
  var TICK_MS = 10000;                  // one more ripple every 10 seconds
  var WRAP_AT = 10000000;               // ten million, then back to 0
  var STORAGE_KEY = 'sj-ripples';
  var MAX_RINGS = 6;
  var MAX_FLOATS = 12;
  var CONFETTI_EVERY = 10;
  var CONFETTI_BITS = 14;

  function formatCount(n) {
    return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
  }

  // With a clock (a function returning milliseconds, normally Date.now) the number rises on its own from
  // EPOCH_MS. With a storage object (localStorage) the visitor's own taps are remembered between visits.
  // Storage can be missing or blocked (private windows); the counter then just works for this visit.
  function createCounter(start, storage, now) {
    var own = 0;
    try {
      var saved = parseInt(storage && storage.getItem(STORAGE_KEY), 10);
      if (saved > 0) own = saved;
    } catch (e) {}
    function total() {
      var ticks = now ? Math.floor((now() - EPOCH_MS) / TICK_MS) : 0;
      return (start + (ticks > 0 ? ticks : 0) + own) % WRAP_AT;
    }
    return {
      value: total,
      tap: function () {
        own += 1;
        try { if (storage) storage.setItem(STORAGE_KEY, String(own)); } catch (e) {}
        return total();
      }
    };
  }

  function reducedMotion(doc) {
    var view = doc.defaultView;
    return !!(view && view.matchMedia && view.matchMedia('(prefers-reduced-motion: reduce)').matches);
  }

  function closestWithId(node, id) {
    while (node) {
      if (node.id === id) return node;
      node = node.parentNode;
    }
    return null;
  }

  // The click listener is on the whole document and elements are looked up at click time, because
  // Squarespace re-draws a Code Block's HTML after load. Running this again (the block was re-drawn and
  // its script ran twice) only refreshes the number; it never adds a second listener.
  function initRipples(doc, storage, now) {
    var html = doc.documentElement;
    var counter = createCounter(PLACEHOLDER_START_COUNT, storage, now);
    var taps = 0;

    function show() {
      var number = doc.getElementById('sj-count');
      var text = formatCount(counter.value());
      if (number && number.textContent !== text) number.textContent = text;
    }
    show();

    if (html && html.classList.contains('sj-ripples-on')) return;
    if (html) html.classList.add('sj-ripples-on');

    // Other scripts on the page may write their own number later; put ours back once the page has loaded.
    var view = doc.defaultView;
    if (view && view.addEventListener) view.addEventListener('load', show);
    // the number rises on its own, so look again every second (it only changes every TICK_MS)
    if (now && view && view.setInterval) view.setInterval(show, 1000);

    // a heart that floats up from the button, and a burst of confetti on every tenth tap
    function playful(fx) {
      taps += 1;
      var heart = doc.createElement('span');
      heart.classList.add('float');
      heart.textContent = '♥';
      heart.style.setProperty('--x', Math.round((Math.random() - 0.5) * 120) + 'px');
      heart.addEventListener('animationend', function () { heart.remove(); });
      fx.appendChild(heart);
      // children is a live HTMLCollection in browsers (no filter/shift), so copy it into an array first
      var floats = Array.prototype.filter.call(fx.children, function (c) { return c.classList.contains('float'); });
      while (floats.length > MAX_FLOATS) fx.removeChild(floats.shift());

      if (taps % CONFETTI_EVERY === 0) {
        for (var i = 0; i < CONFETTI_BITS; i++) {
          var bit = doc.createElement('i');
          bit.classList.add('bit');
          var angle = (i / CONFETTI_BITS) * Math.PI * 2;
          var dist = 70 + Math.random() * 60;
          bit.style.setProperty('--dx', Math.round(Math.cos(angle) * dist) + 'px');
          bit.style.setProperty('--dy', Math.round(Math.sin(angle) * dist - 40) + 'px');
          bit.style.setProperty('--c', i % 3 === 0 ? '#fdcd17' : i % 3 === 1 ? '#ffffff' : '#231f20');
          bit.addEventListener('animationend', function (b) { return function () { b.remove(); }; }(bit));
          fx.appendChild(bit);
        }
      }
    }

    function tap() {
      var heart = doc.getElementById('sj-heart');
      var rings = doc.getElementById('sj-rings');
      var number = doc.getElementById('sj-count');
      if (!heart || !rings || !number) return;

      number.textContent = formatCount(counter.tap());

      if (reducedMotion(doc)) {
        heart.classList.add('pulse');
        setTimeout(function () { heart.classList.remove('pulse'); }, 300);
        return;
      }

      var fx = doc.getElementById('sj-fx');
      if (fx) playful(fx);
      number.classList.add('bump');
      setTimeout(function () { number.classList.remove('bump'); }, 250);

      var ring = doc.createElement('span');
      ring.classList.add('ring');
      ring.addEventListener('animationend', function () { ring.remove(); });
      rings.appendChild(ring);
      while (rings.children.length > MAX_RINGS) rings.removeChild(rings.children[0]);
    }

    // Capture phase, and the tap is claimed here so no other script on the page counts it a second time.
    doc.addEventListener('click', function (e) {
      if (!closestWithId(e.target, 'sj-heart')) return;
      if (e.stopPropagation) e.stopPropagation();
      tap();
    }, true);
  }

  // Reading localStorage can throw (blocked cookies, some private windows), so ask for it carefully.
  function browserStorage() {
    try { return root.localStorage || null; } catch (e) { return null; }
  }

  var Ripples = {
    PLACEHOLDER_START_COUNT: PLACEHOLDER_START_COUNT,
    EPOCH_MS: EPOCH_MS,
    TICK_MS: TICK_MS,
    WRAP_AT: WRAP_AT,
    formatCount: formatCount,
    createCounter: createCounter,
    initRipples: initRipples
  };

  if (typeof module !== 'undefined' && module.exports) module.exports = Ripples;
  root.Ripples = Ripples;

  if (typeof document !== 'undefined') {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', function () { initRipples(document, browserStorage(), Date.now); });
    } else {
      initRipples(document, browserStorage(), Date.now);
    }
  }
})(typeof window !== 'undefined' ? window : globalThis);
