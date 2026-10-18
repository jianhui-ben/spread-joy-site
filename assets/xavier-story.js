// Xavier's animated story: the landing scene above the home page. One tall track, one pinned stage;
// scrolling steps through six scenes (the CSS in xavier-story.css reacts to data-scene and data-act).
(function (root) {
  var SCENES = [
    { title: '', lines: ['Meet our son, Xavier.', 'He’s where our story begins.'], scene: 0, act: 'intro' },
    { title: 'His own pace.', lines: ['Xavier was born with Down syndrome.', 'He speaks a little slower, walks a little differently, and takes a little more time to learn some things.'], scene: 1, act: 'different' },
    { title: 'So much we share.', lines: ['But… he’s also a lot like you and me.', 'He loves his family, and he loves to dance.', 'And just like your kids, he brings so much joy to our lives.'], scene: 1, act: 'familiar' },
    { title: 'Sharing the joy.', lines: ['He inspired us to share that joy.', 'So we started small—collecting socks to donate. Friends and families joined in.'], scene: 3, act: 'socks' },
    { title: 'Growing together.', lines: ['Those little acts of kindness became the glue that brought our community together.', 'As Xavier grew, so did our vision.'], scene: 2, act: 'community' },
    { title: 'Understanding grows kindness.', lines: ['When we take the time to understand one another, kindness grows—and so does our community.'], scene: 5, act: 'vision' }
  ];

  function sceneIndex(progress, count) {
    var p = Math.max(0, Math.min(1, progress));
    return Math.min(count - 1, Math.floor(p * count));
  }

  // Elements are looked up on every update, never kept: Squarespace can re-draw a Code Block's HTML.
  function initXavierStory(doc, win) {
    var current = -1;
    var navigated = false;
    // go to the home page only when a scroll (not the page loading) reaches the very end of the story
    function maybeLeave(progress) {
      var root = doc.querySelector('.xs');
      var home = root && root.dataset && root.dataset.home;
      if (home && !navigated && progress >= 0.999) { navigated = true; win.location.assign(home); }
    }
    function render(fromScroll) {
      var track = doc.querySelector('.xs-track');
      var stage = doc.querySelector('.xs .stage');
      if (!track || !stage) return;
      var total = track.offsetHeight - win.innerHeight;
      var scrolled = -track.getBoundingClientRect().top;
      var progress = total > 0 ? scrolled / total : 0;
      if (fromScroll === true) maybeLeave(progress);
      var index = sceneIndex(progress, SCENES.length);
      if (index === current && stage.dataset.act) return;
      current = index;
      var scene = SCENES[index];
      stage.dataset.scene = scene.scene;
      stage.dataset.act = scene.act;
      var title = doc.querySelector('.xs .chapter-title');
      if (title) title.textContent = scene.title;
      var copy = doc.querySelector('.xs .copy');
      if (copy) copy.replaceChildren.apply(copy, scene.lines.map(function (text) {
        var p = doc.createElement('p'); p.textContent = text; return p;
      }));
      var hint = doc.querySelector('.xs .scroll-hint');
      if (hint) {
        hint.style.opacity = index === 0 ? '1' : '0';
        hint.style.pointerEvents = index === 0 ? 'auto' : 'none';
        hint.tabIndex = index === 0 ? 0 : -1;
      }
    }
    var queued = false;
    function later() {
      if (queued) return;
      queued = true;
      (win.requestAnimationFrame || function (f) { f(); })(function () { queued = false; render(true); });
    }
    win.addEventListener('scroll', later, { passive: true });
    win.addEventListener('resize', render);
    var hint = doc.querySelector('.xs .scroll-hint');
    if (hint) hint.addEventListener('click', function (e) {
      e.preventDefault();
      var track = doc.querySelector('.xs-track');
      var reduce = win.matchMedia && win.matchMedia('(prefers-reduced-motion: reduce)').matches;
      var top = track.getBoundingClientRect().top + (win.scrollY || 0);
      win.scrollTo({ top: top + (track.offsetHeight - win.innerHeight) * 1.1 / SCENES.length, behavior: reduce ? 'auto' : 'smooth' });
    });
    render();
  }

  var api = { SCENES: SCENES, sceneIndex: sceneIndex, initXavierStory: initXavierStory };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  if (typeof document !== 'undefined' && typeof window !== 'undefined') {
    if (!window.__sjXavierStory) {
      window.__sjXavierStory = true;
      if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function () { initXavierStory(document, window); }, { once: true });
      } else {
        initXavierStory(document, window);
      }
    }
  }
})(this);
