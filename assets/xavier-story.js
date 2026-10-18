// Xavier's animated story: the landing scene above the home page. One tall track, one pinned stage;
// scrolling steps through six scenes (the CSS in xavier-story.css reacts to data-scene and data-act).
(function (root) {
  var SCENES = [
      {
          "title": "",
          "lines": [
              "He’s where our story begins."
          ],
          "scene": 0,
          "act": "intro",
          "subtitle": "Meet our son, Xavier."
      },
      {
          "title": "His own pace.",
          "lines": [
              "Xavier was born with Down syndrome.",
              "He speaks a little slower, walks a little differently, and takes a little more time to learn some things."
          ],
          "scene": 1,
          "act": "different",
          "subtitle": "In his own way."
      },
      {
          "title": "So much we share.",
          "lines": [
              "He loves his family, and he loves to dance.",
              "And just like your kids, he brings so much joy to our lives."
          ],
          "scene": 1,
          "act": "familiar",
          "subtitle": "A lot like you and me."
      },
      {
          "title": "Sharing the joy.",
          "lines": [
              "So we started small—collecting socks to donate. Friends and families joined in."
          ],
          "scene": 3,
          "act": "socks",
          "subtitle": "He inspired us to share that joy."
      },
      {
          "title": "Growing together.",
          "lines": [
              "Those little acts of kindness became the glue that brought our community together.",
              "As Xavier grew, so did our vision."
          ],
          "scene": 2,
          "act": "community",
          "subtitle": "Little acts. A closer community."
      },
      {
          "title": "It starts with understanding.",
          "lines": [
              "When we take the time to understand one another, kindness grows—and so does our community."
          ],
          "scene": 5,
          "act": "vision",
          "subtitle": "And grows into kindness."
      }
  ];

  function sceneIndex(progress, count) {
    var p = Math.max(0, Math.min(1, progress));
    return Math.min(count - 1, Math.floor(p * count));
  }

  // Where the drawing and the text go so the whole picture fits between the title and the text.
  // titleBottom is measured from the top of the stage. Returns the text's top, the drawing's top and its scale.
  function fitScene(m) {
    var phone = m.stageW <= 650;
    var copyTop = Math.max(0, Math.min(m.stageH * (phone ? 0.65 : 0.70), m.stageH - 86 - m.copyHeight));
    var gap = phone ? 26 : 38;
    var start = m.titleBottom + gap, end = copyTop - gap;
    var scale = Math.max(0.15, Math.min(phone ? 0.9 : 1, (m.stageW - 36) / (phone ? 680 : 940), (end - start) / 430));
    return { copyTop: copyTop, theatreTop: start + Math.max(0, (end - start - 430 * scale) / 2), scale: scale };
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
      var bar = doc.querySelector('.xs .reading-progress');
      if (bar) bar.style.height = (Math.max(0, Math.min(1, progress)) * 100) + '%';
      if (index === current && stage.dataset.act) { fit(stage); return; }
      current = index;
      var scene = SCENES[index];
      stage.dataset.scene = scene.scene;
      stage.dataset.act = scene.act;
      var title = doc.querySelector('.xs .chapter-title');
      if (title) title.textContent = scene.title;
      var copy = doc.querySelector('.xs .copy');
      if (copy) {
        var sub = doc.createElement('h2'); sub.className = 'second-title'; sub.textContent = scene.subtitle;
        copy.replaceChildren.apply(copy, [sub].concat(scene.lines.map(function (text) {
          var p = doc.createElement('p'); p.textContent = text; return p;
        })));
      }
      var hint = doc.querySelector('.xs .scroll-hint');
      if (hint) hint.tabIndex = index === SCENES.length - 1 ? -1 : 0;
      fit(stage);
    }
    // measure the title and text, then place the drawing between them
    function fit(stage) {
      var theatre = doc.querySelector('.xs .theatre'), copy = doc.querySelector('.xs .copy');
      var title = doc.querySelector(stage.dataset.act === 'intro' ? '.xs .headline' : '.xs .chapter-title');
      if (!theatre || !copy || !title || !stage.getBoundingClientRect || !title.getBoundingClientRect) return;
      var f = fitScene({
        stageH: stage.clientHeight, stageW: stage.clientWidth,
        titleBottom: title.getBoundingClientRect().bottom - stage.getBoundingClientRect().top,
        copyHeight: copy.getBoundingClientRect().height
      });
      stage.style.setProperty('--copy-top', f.copyTop + 'px');
      theatre.style.top = f.theatreTop + 'px';
      theatre.style.transform = 'translateX(-50%) scale(' + f.scale + ')';
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
      win.scrollTo({ top: top + (track.offsetHeight - win.innerHeight) * Math.min(1, (current + 1.1) / SCENES.length), behavior: reduce ? 'auto' : 'smooth' });
    });
    render();
    if (doc.fonts && doc.fonts.ready) doc.fonts.ready.then(function () { render(); });
  }

  var api = { SCENES: SCENES, sceneIndex: sceneIndex, fitScene: fitScene, initXavierStory: initXavierStory };
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
