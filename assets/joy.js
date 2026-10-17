(function (root) {
  // PLACEHOLDER: made-up starting number for the "ripples of joy" counter.
  // Replace with real data later; nothing is stored between visits.
  var PLACEHOLDER_START_COUNT = 1284;

  var IDEAS = [
    "Give someone a sincere compliment.",
    "Tell someone you're glad they're here.",
    "Send a \"thinking of you\" message.",
    "Notice someone's effort and let them know.",
    "Ask someone how they're doing, then really listen.",
    "Celebrate someone's accomplishment, big or small.",
    "Thank someone whose work often goes unnoticed.",
    "Introduce yourself to someone new.",
    "Check in on someone you haven't heard from lately.",
    "Offer a specific helping hand: \"I can bring dinner.\""
  ];

  function formatCount(n) {
    return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
  }

  function createCounter(start) {
    var n = start;
    return {
      value: function () { return n; },
      tap: function () { n += 1; return n; }
    };
  }

  function shuffled(items, rng) {
    var a = items.slice();
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(rng() * (i + 1));
      var t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a;
  }

  function createShuffler(items, rng) {
    rng = rng || Math.random;
    var queue = [];
    var last = null;
    return {
      next: function () {
        if (items.length === 1) return items[0];
        if (queue.length === 0) {
          queue = shuffled(items, rng);
          // keep a new cycle from opening with the previous cycle's last item
          if (queue[0] === last) {
            var swap = queue.length - 1;
            var t = queue[0]; queue[0] = queue[swap]; queue[swap] = t;
          }
        }
        last = queue.shift();
        return last;
      }
    };
  }

  var Joy = {
    PLACEHOLDER_START_COUNT: PLACEHOLDER_START_COUNT,
    IDEAS: IDEAS,
    formatCount: formatCount,
    createCounter: createCounter,
    createShuffler: createShuffler
  };

  if (typeof module !== 'undefined' && module.exports) module.exports = Joy;
  root.Joy = Joy;
})(typeof window !== 'undefined' ? window : globalThis);
