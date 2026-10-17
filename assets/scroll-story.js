(function (root) {
  function clamp(v, a, b) { return Math.min(b, Math.max(a, v)); }

  // Pure maths for the pinned story. `progress` is 0..1 through the tall section,
  // `count` is the number of photos/lines. Returns what each photo and line should look like.
  function storyState(progress, count, reduce) {
    var p = clamp(progress, 0, 1);
    var seg = p * count * 0.999;
    var index = Math.min(count - 1, Math.floor(seg));
    var local = seg - index;
    var frames = [];
    var lines = [];
    for (var i = 0; i < count; i++) {
      // each photo stays opaque once shown; the next one fades in over the last 22% of the current segment
      var opacity = i <= index ? 1 : (i === index + 1 ? clamp((local - 0.78) / 0.22, 0, 1) : 0);
      // each photo settles from slightly zoomed-in to normal size
      var scale = reduce ? 1 : 1.12 - 0.12 * clamp((seg - (i - 0.3)) / 0.7, 0, 1);
      frames.push({ opacity: opacity, scale: scale });

      var d = seg - (i + 0.42);
      lines.push({
        opacity: reduce ? (i === index ? 1 : 0) : clamp(1 - Math.abs(d) * 2.3, 0, 1),
        shift: reduce ? 0 : -d * 36
      });
    }
    return { index: index, frames: frames, lines: lines };
  }

  function initStory(doc, win) {
    var story = doc.getElementById('story');
    if (!story) return;

    var reduce = !!(win.matchMedia && win.matchMedia('(prefers-reduced-motion: reduce)').matches);
    var card = doc.getElementById('heroCard');
    var frames = Array.prototype.slice.call(story.querySelectorAll('.frame'));
    var lines = Array.prototype.slice.call(story.querySelectorAll('.line'));
    var dots = Array.prototype.slice.call(story.querySelectorAll('.dots i'));

    // fade things in as they scroll into view
    if ('IntersectionObserver' in win) {
      var io = new win.IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
        });
      }, { threshold: 0.2 });
      Array.prototype.forEach.call(doc.querySelectorAll('.reveal'), function (el) { io.observe(el); });
    } else {
      Array.prototype.forEach.call(doc.querySelectorAll('.reveal'), function (el) { el.classList.add('in'); });
    }

    function tick() {
      var y = win.scrollY, vh = win.innerHeight;

      if (card && !reduce) {
        // the hero photo grows from 90% to full size as you scroll away
        card.style.transform = 'scale(' + (0.9 + 0.1 * clamp(y / (vh * 0.7), 0, 1)) + ')';
      }

      var span = story.offsetHeight - vh;
      var state = storyState(span > 0 ? (y - story.offsetTop) / span : 0, frames.length, reduce);
      frames.forEach(function (f, i) {
        f.style.opacity = state.frames[i].opacity;
        f.style.transform = 'scale(' + state.frames[i].scale + ')';
      });
      lines.forEach(function (l, i) {
        l.style.opacity = state.lines[i].opacity;
        l.style.transform = 'translateY(' + state.lines[i].shift + 'px)';
      });
      dots.forEach(function (d, i) { d.classList.toggle('on', i === state.index); });
    }

    var ticking = false;
    win.addEventListener('scroll', function () {
      if (!ticking) {
        ticking = true;
        win.requestAnimationFrame(function () { tick(); ticking = false; });
      }
    }, { passive: true });
    win.addEventListener('resize', tick);
    tick();
  }

  // Cards row: a mouse can drag the row sideways (touch already scrolls natively)
  function initCards(doc) {
    var row = doc.getElementById('cards');
    if (!row) return;
    var down = false, moved = false, startX = 0, startLeft = 0;
    row.addEventListener('pointerdown', function (e) {
      if (e.pointerType !== 'mouse') return;
      down = true; moved = false; startX = e.clientX; startLeft = row.scrollLeft;
    });
    doc.addEventListener('pointermove', function (e) {
      if (!down) return;
      var dx = e.clientX - startX;
      if (Math.abs(dx) > 5) { moved = true; row.classList.add('dragging'); }
      if (moved) row.scrollLeft = startLeft - dx;
    });
    doc.addEventListener('pointerup', function () {
      if (!down) return;
      down = false; row.classList.remove('dragging');
    });
    // a drag should not count as a click on the card underneath
    row.addEventListener('click', function (e) {
      if (moved) { e.preventDefault(); e.stopPropagation(); moved = false; }
    }, true);
    row.addEventListener('dragstart', function (e) { e.preventDefault(); });
  }

  // Apple-style bar: tucks away while you scroll down, comes back as soon as you scroll up.
  function headerHidden(prevY, y, wasHidden) {
    if (y < 80) return false;
    if (y > prevY + 4) return true;
    if (y < prevY - 8) return false;
    return wasHidden;
  }

  function initHeader(doc, win) {
    var bar = doc.querySelector('.site-header');
    if (!bar) return;
    var prev = win.scrollY, hidden = false;
    win.addEventListener('scroll', function () {
      var y = win.scrollY;
      var next = headerHidden(prev, y, hidden);
      if (next !== hidden) { hidden = next; bar.classList.toggle('tucked', hidden); }
      prev = y;
    }, { passive: true });
  }

  var api = { storyState: storyState, initStory: initStory, initCards: initCards, headerHidden: headerHidden, initHeader: initHeader };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  if (typeof document !== 'undefined' && typeof window !== 'undefined') {
    root.StoryScroll = api;
    initStory(document, window);
    initCards(document);
    initHeader(document, window);
  }
})(typeof window !== 'undefined' ? window : globalThis);
