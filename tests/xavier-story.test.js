const test = require('node:test');
const assert = require('node:assert/strict');
const { SCENES, sceneIndex, initXavierStory } = require('../assets/xavier-story.js');

test('there are six scenes, the first with no chapter title', () => {
  assert.equal(SCENES.length, 6);
  assert.equal(SCENES[0].title, '');
  assert.ok(SCENES.every((s) => s.lines.length >= 1 && typeof s.act === 'string'));
});

test('scene index follows scroll progress and never leaves the range', () => {
  assert.equal(sceneIndex(0, 6), 0);
  assert.equal(sceneIndex(0.5, 6), 3);
  assert.equal(sceneIndex(1, 6), 5);
  assert.equal(sceneIndex(-3, 6), 0);
  assert.equal(sceneIndex(9, 6), 5);
});

// a tiny fake page: a track 7 screens tall, a stage, a title, a copy box, a scroll hint
function setup(scrollY) {
  const mk = () => ({ dataset: {}, style: {}, textContent: '', children: [], tabIndex: 0,
    replaceChildren(...c) { this.children = c; }, addEventListener() {}, });
  const track = mk(), stage = mk(), title = mk(), copy = mk(), hint = mk();
  track.offsetHeight = 700; track.getBoundingClientRect = () => ({ top: -scrollY, height: 700 });
  const els = { '.xs-track': track, '.xs .stage': stage, '.xs .chapter-title': title, '.xs .copy': copy, '.xs .scroll-hint': hint };
  const doc = {
    querySelector: (s) => els[s] || null,
    createElement: () => ({ textContent: '' }),
  };
  const win = { innerHeight: 100, matchMedia: () => ({ matches: false }), addEventListener() {}, scrollTo() {} };
  return { doc, win, stage, title, copy, hint };
}

test('at the top it shows the opening scene and the scroll hint', () => {
  const s = setup(0);
  initXavierStory(s.doc, s.win);
  assert.equal(s.stage.dataset.act, 'intro');
  assert.equal(s.copy.children.length, SCENES[0].lines.length);
  assert.equal(s.hint.style.opacity, '1');
});

test('scrolled to the end it shows the last scene and hides the hint', () => {
  const s = setup(600); // track 700 - viewport 100
  initXavierStory(s.doc, s.win);
  assert.equal(s.stage.dataset.act, 'vision');
  assert.equal(s.title.textContent, SCENES[5].title);
  assert.equal(s.hint.style.opacity, '0');
});

test('a page without the story is left alone', () => {
  initXavierStory({ querySelector: () => null }, { innerHeight: 100, addEventListener() {} });
});

test('scrolling into the end of the story goes to the home page once', () => {
  const s = setup(600);
  const calls = [];
  s.win.location = { assign: (u) => calls.push(u) };
  const scrollFns = [];
  s.win.addEventListener = (type, fn) => { if (type === 'scroll') scrollFns.push(fn); };
  s.win.requestAnimationFrame = (f) => f();
  s.doc.querySelector = ((orig) => (sel) => (sel === '.xs' ? { dataset: { home: 'index.html' } } : orig(sel)))(s.doc.querySelector);
  initXavierStory(s.doc, s.win);
  assert.deepEqual(calls, [], 'not on load');
  scrollFns.forEach((f) => f()); scrollFns.forEach((f) => f());
  assert.deepEqual(calls, ['index.html']);
});
