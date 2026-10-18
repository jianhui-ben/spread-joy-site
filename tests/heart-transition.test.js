const test = require('node:test');
const assert = require('node:assert/strict');
const { initHeartTransition, isHomePath } = require('../assets/heart-transition.js');

// A tiny fake page: one .sj-home container, a window with a path, frames and queued animation frames.
const rect = (top, bottom) => ({ top, bottom, height: bottom - top });
const LAYOUT = { container: rect(0, 900), h1: rect(56, 150), sub: rect(168, 220), card: rect(260, 900) };

function setup({ path = '/', framed = false, reduceMotion = false, hasContainer = true, layout = LAYOUT } = {}) {
  const frames = [];
  const makeEl = () => ({
    id: '',
    attrs: {},
    style: { setProperty(k, v) { this[k] = v; } },
    classes: new Set(),
    classList: null,
    children: [],
    setAttribute(k, v) { this.attrs[k] = v; },
    querySelector(sel) {
      if (sel === '#heart-transition') return this.children.find((c) => c.id === 'heart-transition') || null;
      const r = layout && { '.hero h1': layout.h1, '.hero .sub': layout.sub, '.hero-card': layout.card }[sel];
      return r ? { getBoundingClientRect: () => r } : null;
    },
    getBoundingClientRect() { return layout ? layout.container : rect(0, 0); },
    insertBefore(child) { this.children.unshift(child); },
    get firstChild() { return this.children[0] || null; },
  });
  const container = makeEl();
  const mk = () => {
    const el = makeEl();
    el.classList = { add: (...c) => c.forEach((x) => el.classes.add(x)), remove: (...c) => c.forEach((x) => el.classes.delete(x)), contains: (c) => el.classes.has(c) };
    return el;
  };
  container.classList = null;
  const doc = {
    querySelector: (sel) => (sel === '.sj-home' && hasContainer ? container : null),
    createElement: () => mk(),
    readyState: 'complete',
  };
  const winListeners = {};
  const win = {
    addEventListener: (type, fn) => { (winListeners[type] = winListeners[type] || []).push(fn); },
    fire: (type) => (winListeners[type] || []).forEach((fn) => fn()),
    location: { pathname: path },
    matchMedia: () => ({ matches: reduceMotion }),
    requestAnimationFrame: (fn) => frames.push(fn),
  };
  win.self = win;
  win.top = framed ? {} : win;
  const runFrames = () => { while (frames.length) frames.shift()(); };
  return { doc, win, container, runFrames, LAYOUT };
}

test('isHomePath accepts the landing page paths only', () => {
  assert.equal(isHomePath('/'), true);
  assert.equal(isHomePath('/home'), true);
  assert.equal(isHomePath('/home/'), true);
  assert.equal(isHomePath('/index.html'), true); // the local preview
  assert.equal(isHomePath('/contact'), false);
  assert.equal(isHomePath('/let-us-help'), false);
});

test('opening the landing page adds the heart cover as the first thing in the container', () => {
  const s = setup();
  initHeartTransition(s.doc, s.win);
  const heart = s.container.children[0];
  assert.equal(heart.id, 'heart-transition');
  assert.equal(heart.attrs['aria-hidden'], 'true');
  assert.ok(heart.classes.has('visible') && heart.classes.has('cover'), 'starts fully covered');
  assert.equal(heart.style['--heart-duration'], '0ms', 'no animation while it sets up');
});

test('after two frames the cover shrinks away and the heart stays', () => {
  const s = setup();
  initHeartTransition(s.doc, s.win);
  s.runFrames();
  const heart = s.container.children[0];
  assert.ok(!heart.classes.has('cover'));
  assert.ok(heart.classes.has('persistent'));
  assert.equal(heart.style['--heart-duration'], '750ms');
});

test('reduced motion makes the transition 150ms', () => {
  const s = setup({ reduceMotion: true });
  initHeartTransition(s.doc, s.win);
  s.runFrames();
  assert.equal(s.container.children[0].style['--heart-duration'], '150ms');
});

test('running twice adds only one heart', () => {
  const s = setup();
  initHeartTransition(s.doc, s.win);
  initHeartTransition(s.doc, s.win);
  assert.equal(s.container.children.length, 1);
});

test('other pages, editor frames and pages without the container are left alone', () => {
  for (const opts of [{ path: '/contact' }, { framed: true }, { hasContainer: false }]) {
    const s = setup(opts);
    initHeartTransition(s.doc, s.win);
    assert.equal(s.container.children.length, 0, JSON.stringify(opts));
  }
});

// --- where the staying heart sits: centred on the headline, never reaching down into the photo ---
test('the heart is centred on the headline and sized to end where the photo begins', () => {
  const s = setup();
  initHeartTransition(s.doc, s.win);
  const heart = s.container.children[0];
  // headline block runs 56..220, so its middle is 138; the photo starts at 260, which leaves 122 below
  assert.equal(heart.style['--heart-y'], '138px');
  assert.equal(heart.style['--heart-size'], '244px');
});

test('a tall headline area is limited by the top of the section instead', () => {
  const s = setup({ layout: { container: rect(0, 900), h1: rect(20, 100), sub: rect(110, 140), card: rect(500, 900) } });
  initHeartTransition(s.doc, s.win);
  const heart = s.container.children[0];
  assert.equal(heart.style['--heart-y'], '80px');
  assert.equal(heart.style['--heart-size'], '160px'); // 2 * min(80 above, 420 below)
});

test('the heart is placed again when the window is resized or finishes loading', () => {
  const s = setup();
  initHeartTransition(s.doc, s.win);
  const heart = s.container.children[0];
  s.LAYOUT.h1 = rect(36, 110); s.LAYOUT.sub = rect(120, 160); s.LAYOUT.card = rect(200, 700);
  s.win.fire('resize');
  assert.equal(heart.style['--heart-y'], '98px');
  assert.equal(heart.style['--heart-size'], '196px');
  s.LAYOUT.card = rect(170, 700);
  s.win.fire('load');
  assert.equal(heart.style['--heart-size'], '144px'); // 2 * min(98 above, 72 below)
});

test('without a headline the heart keeps the stylesheet defaults', () => {
  const s = setup({ layout: null });
  s.container.querySelector = (sel) => (sel === '#heart-transition' ? s.container.children[0] || null : null);
  initHeartTransition(s.doc, s.win);
  const heart = s.container.children[0];
  assert.equal(heart.style['--heart-y'], undefined);
  assert.equal(heart.style['--heart-size'], undefined);
});
