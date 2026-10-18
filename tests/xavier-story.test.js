const test = require('node:test');
const assert = require('node:assert/strict');
const { SCENES, sceneIndex, fitScene, headerOffset, initXavierStory } = require('../assets/xavier-story.js');

test('there are six scenes, the first with no chapter title', () => {
  assert.equal(SCENES.length, 6);
  assert.equal(SCENES[0].title, '');
  assert.ok(SCENES.every((s) => s.lines.length >= 1 && typeof s.act === 'string' && s.subtitle));
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
  const progress = mk(), track = mk(), stage = mk(), title = mk(), copy = mk(), hint = mk();
  track.offsetHeight = 700; track.getBoundingClientRect = () => ({ top: -scrollY, height: 700 });
  const els = { '.xs-track': track, '.xs .stage': stage, '.xs .chapter-title': title, '.xs .copy': copy, '.xs .scroll-hint': hint, '.xs .reading-progress': progress };
  const doc = {
    querySelector: (s) => els[s] || null,
    createElement: () => ({ textContent: '', className: '' }),
  };
  const win = { innerHeight: 100, matchMedia: () => ({ matches: false }), addEventListener() {}, scrollTo() {} };
  return { doc, win, stage, title, copy, hint, progress };
}

test('at the top it shows the opening scene and the scroll hint', () => {
  const s = setup(0);
  initXavierStory(s.doc, s.win);
  assert.equal(s.stage.dataset.act, 'intro');
  assert.equal(s.copy.children.length, SCENES[0].lines.length + 1, 'a subtitle then the lines');
  assert.equal(s.copy.children[0].className, 'second-title');
  assert.equal(s.copy.children[0].textContent, SCENES[0].subtitle);
  assert.equal(s.hint.tabIndex, 0);
});

test('scrolled to the end it shows the last scene and keeps the arrow, which now leads on to the yellow ending', () => {
  const s = setup(600); // track 700 - viewport 100
  initXavierStory(s.doc, s.win);
  assert.equal(s.stage.dataset.act, 'vision');
  assert.equal(s.title.textContent, SCENES[5].title);
  assert.equal(s.hint.tabIndex, 0);
});

test('the last subtitle says joy', () => {
  assert.equal(SCENES[5].subtitle, 'And grows into joy.');
});

test('a page without the story is left alone', () => {
  initXavierStory({ querySelector: () => null }, { innerHeight: 100, addEventListener() {} });
});

test('the story never navigates away by itself', () => {
  const s = setup(600);
  const calls = [];
  s.win.location = { assign: (u) => calls.push(u) };
  const scrollFns = [];
  s.win.addEventListener = (type, fn) => { if (type === 'scroll') scrollFns.push(fn); };
  s.win.requestAnimationFrame = (f) => f();
  s.doc.querySelector = ((orig) => (sel) => (sel === '.xs' ? { dataset: { home: 'index.html' } } : orig(sel)))(s.doc.querySelector);
  initXavierStory(s.doc, s.win);
  scrollFns.forEach((f) => f());
  assert.deepEqual(calls, []);
});

test('the arrow on the last scene scrolls on past the story to the ending', () => {
  const s = setup(600);
  let click; s.hint.addEventListener = (type, fn) => { if (type === 'click') click = fn; };
  const jumps = []; s.win.scrollTo = (o) => jumps.push(o.top);
  initXavierStory(s.doc, s.win);
  click({ preventDefault() {} });
  assert.equal(jumps[0], -600 + 700, 'the very bottom of the track, where the ending begins');
});

test('the story button stays put until it has a real address', () => {
  const s = setup(0);
  const link = { getAttribute: () => '#', addEventListener(type, fn) { this.fn = fn; } };
  s.doc.querySelector = ((orig) => (sel) => (sel === '.xs .story-link' ? link : orig(sel)))(s.doc.querySelector);
  initXavierStory(s.doc, s.win);
  let prevented = false; link.fn({ preventDefault() { prevented = true; } });
  assert.ok(prevented);
});

test('the reading bar grows with scroll progress', () => {
  const s = setup(300); // halfway through 600
  initXavierStory(s.doc, s.win);
  assert.equal(s.progress.style.height, '50%');
});

test('the drawing is fitted between the title and the text, and never above the title', () => {
  const f = fitScene({ stageH: 900, stageW: 1280, titleBottom: 150, copyHeight: 120 });
  assert.equal(f.copyTop, 630);                       // 70% of the stage
  assert.ok(f.theatreTop >= 150 + 38);                // below the title with its gap
  assert.ok(f.scale <= 1 && f.scale >= 0.15);
});

test('a short screen pulls the text up and shrinks the drawing', () => {
  const tall = fitScene({ stageH: 900, stageW: 1280, titleBottom: 150, copyHeight: 120 });
  const short = fitScene({ stageH: 600, stageW: 1280, titleBottom: 130, copyHeight: 160 });
  assert.equal(short.copyTop, 600 - 86 - 160);
  assert.ok(short.scale < tall.scale);
});

test('on a phone the drawing is capped to fit the width', () => {
  const f = fitScene({ stageH: 800, stageW: 360, titleBottom: 140, copyHeight: 150 });
  assert.ok(f.scale <= (360 - 36) / 680 + 1e-9);
});

test('the reading bar fades out once the visitor is past the story', () => {
  const s = setup(0);
  const track = { style: {} }; s.doc.querySelector = ((orig) => (sel) => (sel === '.xs .reading-track' ? track : orig(sel)))(s.doc.querySelector);
  initXavierStory(s.doc, s.win);
  assert.equal(track.style.opacity, '1');
  const s2 = setup(800); // 200 past the end of a 600 range, more than 30% of the 100 viewport
  const track2 = { style: {} }; s2.doc.querySelector = ((orig) => (sel) => (sel === '.xs .reading-track' ? track2 : orig(sel)))(s2.doc.querySelector);
  initXavierStory(s2.doc, s2.win);
  assert.equal(track2.style.opacity, '0');
});

test('a header that stays on screen pushes the story stage down by its height', () => {
  assert.equal(headerOffset({ bottom: 140 }, 'sticky'), 140);
  assert.equal(headerOffset({ bottom: 96 }, 'fixed'), 96);
});

test('a header that scrolls away, is missing or has slid off the top adds nothing', () => {
  assert.equal(headerOffset({ bottom: 140 }, 'static'), 0);
  assert.equal(headerOffset(null, 'fixed'), 0);
  assert.equal(headerOffset({ bottom: -40 }, 'sticky'), 0);
});

test('the stage is told how far down to sit', () => {
  const s = setup(0);
  const root = { style: { setProperty(k, v) { this[k] = v; } } };
  const header = { getBoundingClientRect: () => ({ bottom: 120 }) };
  s.doc.querySelector = ((orig) => (sel) => (sel === '.xs' ? root : sel === '.site-header, #header' ? header : orig(sel)))(s.doc.querySelector);
  s.win.getComputedStyle = () => ({ position: 'sticky' });
  initXavierStory(s.doc, s.win);
  assert.equal(root.style['--xs-top'], '120px');
});
