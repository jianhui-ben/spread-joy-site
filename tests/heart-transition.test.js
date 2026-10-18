const test = require('node:test');
const assert = require('node:assert/strict');
const { initHeartTransition, isHomePath } = require('../assets/heart-transition.js');

// A tiny fake page: one .sj-home container, a window with a path, frames and queued animation frames.
function setup({ path = '/', framed = false, reduceMotion = false, hasContainer = true } = {}) {
  const frames = [];
  const makeEl = () => ({
    id: '',
    attrs: {},
    style: { setProperty(k, v) { this[k] = v; } },
    classes: new Set(),
    classList: null,
    children: [],
    setAttribute(k, v) { this.attrs[k] = v; },
    querySelector(sel) { return sel === '#heart-transition' ? this.children.find((c) => c.id === 'heart-transition') || null : null; },
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
  const win = {
    location: { pathname: path },
    matchMedia: () => ({ matches: reduceMotion }),
    requestAnimationFrame: (fn) => frames.push(fn),
  };
  win.self = win;
  win.top = framed ? {} : win;
  const runFrames = () => { while (frames.length) frames.shift()(); };
  return { doc, win, container, runFrames };
}

test('isHomePath accepts the landing page paths only', () => {
  assert.equal(isHomePath('/'), true);
  assert.equal(isHomePath('/home'), true);
  assert.equal(isHomePath('/home/'), true);
  assert.equal(isHomePath('/index.html'), true); // the local preview
  assert.equal(isHomePath('/contact'), false);
  assert.equal(isHomePath('/volunteer'), false);
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
