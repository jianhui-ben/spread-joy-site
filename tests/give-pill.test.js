const test = require('node:test');
const assert = require('node:assert/strict');
const { givePillVisible, initGive, GIVE_URL } = require('../assets/give-pill.js');

test('the Give pill is visible when there is no Give band on the page', () => {
  assert.equal(givePillVisible(null, 800), true);
});

test('the Give pill steps aside while the Give band is on screen', () => {
  assert.equal(givePillVisible({ top: 300, bottom: 900 }, 800), false);
  assert.equal(givePillVisible({ top: 1200, bottom: 1800 }, 800), true);
  assert.equal(givePillVisible({ top: -900, bottom: -100 }, 800), true);
});

test('the Give pill points at Givebutter and is created once, even if the page is re-drawn', () => {
  const made = [];
  const body = { appendChild(el) { made.push(el); body.last = el; } };
  let band = null;
  const byId = {};
  const doc = {
    body,
    getElementById(id) { return id === 'sj-give' ? band : (made.find((m) => m.id === id) || null); },
    createElement() {
      const classes = new Set();
      return { id: '', className: '', attrs: {}, setAttribute(k, v) { this.attrs[k] = v; },
        classList: { toggle: (c, on) => (on ? classes.add(c) : classes.delete(c)), contains: (c) => classes.has(c) } };
    },
  };
  let scroll;
  const win = { innerHeight: 800, addEventListener(t, f) { if (t === 'scroll') scroll = f; } };
  initGive(doc, win);
  scroll(); scroll();
  assert.equal(made.length, 1);
  assert.equal(made[0].attrs.href, GIVE_URL);
  assert.match(GIVE_URL, /^https:\/\/givebutter\.com\//);
  assert.ok(made[0].classList.contains('on'));
  band = { getBoundingClientRect: () => ({ top: 100, bottom: 700 }) };
  scroll();
  assert.ok(!made[0].classList.contains('on'));
});
