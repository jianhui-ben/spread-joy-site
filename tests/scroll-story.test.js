const test = require('node:test');
const assert = require('node:assert/strict');
const { storyState } = require('../assets/scroll-story.js');

test('at the top the first photo is shown and the others are not', () => {
  const s = storyState(0, 3, false);
  assert.equal(s.index, 0);
  assert.deepEqual(s.frames.map((f) => f.opacity), [1, 0, 0]);
});

test('by the end every photo has faded in and the last one is current', () => {
  const s = storyState(1, 3, false);
  assert.equal(s.index, 2);
  assert.deepEqual(s.frames.map((f) => f.opacity), [1, 1, 1]);
});

test('the next photo only starts fading in near the end of the current one', () => {
  const early = storyState(0.1, 3, false); // a third of the first segment
  assert.equal(early.frames[1].opacity, 0);
  const late = storyState(0.3, 3, false);  // 90% through the first segment
  assert.ok(late.frames[1].opacity > 0 && late.frames[1].opacity < 1);
});

test('exactly one line is the brightest at the middle of each segment', () => {
  for (let i = 0; i < 3; i++) {
    const p = (i + 0.42) / 3;
    const s = storyState(p, 3, false);
    const max = Math.max(...s.lines.map((l) => l.opacity));
    assert.equal(s.lines.filter((l) => l.opacity === max).length, 1);
    assert.equal(s.lines.findIndex((l) => l.opacity === max), i);
    assert.ok(max > 0.95);
  }
});

test('photos settle from zoomed in to normal size as you scroll', () => {
  const start = storyState(0, 3, false).frames[0].scale;
  const later = storyState(0.2, 3, false).frames[0].scale;
  assert.ok(start > later);
  assert.ok(start <= 1.12 && later >= 1);
});

test('progress outside 0..1 is clamped instead of breaking', () => {
  assert.deepEqual(storyState(-5, 3, false), storyState(0, 3, false));
  assert.deepEqual(storyState(9, 3, false), storyState(1, 3, false));
});

test('reduced motion shows one line at a time with no zoom or slide', () => {
  const s = storyState(0.5, 3, true);
  s.frames.forEach((f) => assert.equal(f.scale, 1));
  s.lines.forEach((l, i) => {
    assert.equal(l.shift, 0);
    assert.equal(l.opacity, i === s.index ? 1 : 0);
  });
});

test('headerHidden: hides when scrolling down past the top, shows when scrolling up', () => {
  const { headerHidden } = require('../assets/scroll-story.js');
  assert.equal(headerHidden(0, 40, false), false, 'near the top stays visible');
  assert.equal(headerHidden(100, 300, false), true, 'scrolling down hides');
  assert.equal(headerHidden(300, 296, true), true, 'tiny upward jitter keeps it hidden');
  assert.equal(headerHidden(300, 270, true), false, 'scrolling up shows');
  assert.equal(headerHidden(300, 20, true), false, 'back at the top shows');
});

// --- Squarespace re-draws Code Block HTML after the script has started; the story must follow the new elements ---
function fakePage() {
  const listeners = {};
  const mk = (cls) => ({ cls, style: {}, classList: { toggle() {}, add(c) { this.added = c; } }, getBoundingClientRect: () => ({ top: -500, height: 100, bottom: -400 }) });
  const page = {
    frames: [mk('frame'), mk('frame'), mk('frame')],
    lines: [mk('line'), mk('line'), mk('line')],
  };
  const story = () => ({
    offsetHeight: 4000,
    getBoundingClientRect: () => ({ top: -1500 }),
    querySelectorAll: (sel) => (sel === '.frame' ? page.frames : sel === '.line' ? page.lines : []),
  });
  const doc = {
    getElementById: (id) => (id === 'story' ? story() : null),
    querySelectorAll: () => [],
    querySelector: () => null,
    addEventListener() {},
  };
  const win = {
    scrollY: 1500, innerHeight: 1000,
    matchMedia: () => ({ matches: false }),
    requestAnimationFrame: (fn) => fn(),
    addEventListener: (t, fn) => { (listeners[t] = listeners[t] || []).push(fn); },
    fire: (t) => (listeners[t] || []).forEach((fn) => fn()),
  };
  return { doc, win, page, mk };
}

test('initStory keeps updating after the photos and lines are replaced by new elements', () => {
  const { initStory } = require('../assets/scroll-story.js');
  const { doc, win, page, mk } = fakePage();
  initStory(doc, win);
  // Squarespace swaps in fresh copies of the block HTML
  page.frames = [mk('frame'), mk('frame'), mk('frame')];
  page.lines = [mk('line'), mk('line'), mk('line')];
  win.scrollY = 1500;
  win.fire('scroll');
  assert.ok(page.frames[0].style.opacity !== undefined, 'new photos were updated');
  assert.ok(page.lines[1].style.opacity !== undefined, 'new lines were updated');
});
