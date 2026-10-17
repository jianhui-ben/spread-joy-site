const test = require('node:test');
const assert = require('node:assert/strict');
const Joy = require('../assets/joy.js');

test('the brainstorm list is intact, including the glad-you-are-here idea', () => {
  assert.equal(Joy.IDEAS.length, 16);
  assert.ok(Joy.IDEAS.includes('Tell someone, "I\'m so glad you\'re here."'));
});

test('shuffler never repeats an idea back to back', () => {
  const s = Joy.createShuffler(Joy.IDEAS);
  let prev = null;
  for (let i = 0; i < Joy.IDEAS.length * 3; i++) {
    const next = s.next();
    assert.notEqual(next, prev);
    prev = next;
  }
});

test('shuffler visits every idea before any repeats', () => {
  const s = Joy.createShuffler(Joy.IDEAS);
  const seen = new Set();
  for (let i = 0; i < Joy.IDEAS.length; i++) seen.add(s.next());
  assert.equal(seen.size, Joy.IDEAS.length);
});

test('a one-item shuffler keeps returning that item', () => {
  const s = Joy.createShuffler(['only']);
  assert.equal(s.next(), 'only');
  assert.equal(s.next(), 'only');
});
