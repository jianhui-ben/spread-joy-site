# Joy Ripple Homepage Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the five-moment "Joy Ripple" home page as a clickable prototype in this repo, plus the Squarespace snippets and setup steps to recreate it.

**Architecture:** The static mock stays: `build.py` generates the HTML pages, `assets/styles.css` styles them. New interaction logic lives in two small scripts: `assets/joy.js` (pure, testable logic) and `assets/home.js` (DOM wiring). `build.py` also emits Squarespace-ready snippet files into `squarespace/` so the prototype and the live site share the same code.

**Tech Stack:** Plain HTML/CSS/vanilla JS, Python 3 (`build.py`, `unittest`), Node 20 (`node --test` for JS logic). No dependencies.

**Spec:** `docs/superpowers/specs/2026-10-16-joy-ripple-homepage-design.md`

## Global Constraints

- White page background, text `#231f20`, brand yellow `#FDCD17`; yellow bands alternate with white and join with a wave; hearts are white on yellow bands.
- Fonts: League Spartan (text), Oooh Baby (accent). Logo and photos unchanged; use the web copies in `assets/img/`.
- Header stays fixed while scrolling.
- Five moments in order: Tap the heart / "It started with one kid." / "Then a whole circle showed up." / "578 socks. One kindness at a time." / "Your turn."
- Counter is a made-up number: one named constant `PLACEHOLDER_START_COUNT = 1284`; +1 per tap for the current visit only; nothing stored.
- "Your turn" links: I have time and I have something to share go to `help.html`; I want to give goes to `#` (Donate placeholder, same as the header); My family could use support goes to `contact.html`.
- "Surprise me": 10 short kindness ideas, shuffled, never the same idea twice in a row.
- Works without JavaScript: static heart, counter line as plain text, "Surprise me" button hidden.
- Honor `prefers-reduced-motion`. Smooth on phones; no heavy full-screen canvas.
- Squarespace: native sections, wave dividers and scroll animations carry layout; custom code only for the heart ripple and "Surprise me". Code Blocks run JavaScript only in HTML mode inside script tags and need a Core, Plus or Advanced plan.
- Add `.superpowers/` to `.gitignore`.

## Review Focus

- Visitor taps the heart many times quickly: rings must not pile up without limit, and the counter must stay correct.
- Visitor uses the keyboard or a screen reader: the heart must be a real button, activate on Enter/Space, and the counter must announce politely.
- Page is opened with JavaScript off or the scripts missing: nothing looks broken, no empty gap where "Surprise me" would be.
- Reduced-motion setting is on: no drifting hearts or rings; counter and ideas still work.
- Phone width (375px): no horizontal scroll, text readable, heart tap target at least 44px.
- The snippet is pasted into a page missing one of the expected elements: script does nothing and throws no error.

---

### Task 1: Joy logic module

**Files:**
- Create: `assets/joy.js`
- Test: `tests/joy.test.js`

**Interfaces:**
- Produces (CommonJS `module.exports` and `window.Joy`):
  - `PLACEHOLDER_START_COUNT: number` (1284)
  - `IDEAS: string[]` (10 items; includes "Tell someone you're glad they're here.")
  - `formatCount(n: number): string` (thousands separators, e.g. `1284` → `"1,284"`)
  - `createCounter(start: number): { value(): number, tap(): number }` (`tap` increments and returns the new value)
  - `createShuffler(items: string[], rng?: () => number): { next(): string }` (visits every item before repeating; never returns the same item twice in a row when `items.length > 1`; with one item always returns it)

- [ ] **Step 1: Write failing tests** in `tests/joy.test.js` using `node:test`: `formatCount(1284) === "1,284"`, `formatCount(0) === "0"`, `formatCount(1234567) === "1,234,567"`; `createCounter(1284)` has `value() === 1284` and three `tap()` calls return 1285, 1286, 1287; `createShuffler(IDEAS)` called `IDEAS.length * 3` times never returns the same string twice consecutively and returns every idea within the first `IDEAS.length` calls; a one-item shuffler returns that item repeatedly; `IDEAS.length === 10`.
- [ ] **Step 2: Run** `node --test tests/` — expected: FAIL (module not found).
- [ ] **Step 3: Implement the interface above in `assets/joy.js`.** Shuffle with Fisher-Yates per cycle; when a new cycle starts, reshuffle until its first item differs from the last item of the previous cycle. Write the 10 ideas from the owner's list (compliment, "I'm so glad you're here", thinking-of-you message, notice someone's effort, ask how someone is doing and listen, celebrate an accomplishment, thank someone unnoticed, introduce yourself, check in on someone, offer a specific helping hand).
- [ ] **Step 4: Run** `node --test tests/` — expected: PASS.
- [ ] **Step 5: Commit** `git add assets/joy.js tests/joy.test.js && git commit -m "feat: joy counter and idea shuffler"`

### Task 2: White theme, bands and waves

**Files:**
- Modify: `assets/styles.css`, `build.py` (SHELL header/footer markup only)
- Test: `tests/test_build.py`

**Interfaces:**
- Produces CSS classes used by Task 3: `.band` (white section), `.band.yellow`, `.wave` (SVG divider element, `.wave.flip` mirrored), `.moment` (section wrapper), `.hl` (yellow highlighter span), `.photo-card` (image with offset block shadow), `.pill` / `.pill.outline`, `.drift-heart` (floating decoration, hidden under reduced motion).

- [ ] **Step 1: Write failing tests** in `tests/test_build.py` (`unittest`, reads generated `index.html` and `assets/styles.css`): CSS defines `--yellow: #fdcd17`, `--ink: #231f20`, `body` background is white, and contains rules for each class listed above plus an `@media (prefers-reduced-motion: reduce)` block; the header has `position: sticky`.
- [ ] **Step 2: Run** `python3 -m unittest discover -s tests` — expected: FAIL.
- [ ] **Step 3: Convert the stylesheet from the dark theme to white** (header becomes white with a yellow underline and dark nav; footer stays dark or becomes yellow, builder's choice), and add the classes above. Existing pages (mission, story, events, help, contact) must still render legibly on white.
- [ ] **Step 4: Run** `python3 build.py && python3 -m unittest discover -s tests` — expected: PASS.
- [ ] **Step 5: Commit** `git add assets/styles.css build.py tests/test_build.py && git commit -m "feat: white theme with yellow band and wave classes"`

### Task 3: Five-moment home page markup

**Files:**
- Modify: `build.py` (`PAGES["index.html"]` body)
- Test: `tests/test_build.py`

**Interfaces:**
- Consumes: Task 2 classes; `PLACEHOLDER_START_COUNT` value 1284 for the static counter text.
- Produces element ids that Task 4 requires: `#sj-heart` (a `<button>` wrapping `assets/img/heart.png`), `#sj-rings` (empty container), `#sj-count` (text `1,284`, inside a paragraph with `aria-live="polite"`), `#sj-surprise` (button, has `hidden` attribute in markup), `#sj-idea` (empty `<p>`).

- [ ] **Step 1: Write failing tests:** `index.html` contains five `.moment` sections in the specified order with the exact headline copy from Global Constraints; photos `xavier-portrait.jpg`, `socks-circle.jpg`, `sock-pile.jpg` are referenced and exist on disk with non-empty `alt`; the four "Your turn" links point to the targets in Global Constraints; the ids above exist exactly once; `#sj-surprise` is `hidden` in the markup; yellow moments (2 and 4) use `.band.yellow` and white hearts (`heart-white.png`).
- [ ] **Step 2: Run** `python3 build.py && python3 -m unittest discover -s tests` — expected: FAIL.
- [ ] **Step 3: Replace the home body in `build.py`** with the five moments, `.wave` dividers between bands, `<script src="assets/joy.js" defer>` and `<script src="assets/home.js" defer>` before `</body>` (home page only).
- [ ] **Step 4: Run** the same command — expected: PASS.
- [ ] **Step 5: Commit** `git add build.py index.html tests/test_build.py && git commit -m "feat: five-moment home page markup"`

### Task 4: Ripple and Surprise-me behavior

**Files:**
- Create: `assets/home.js`
- Modify: `assets/styles.css` (ring animation keyframes, drift animation)
- Test: `tests/home.test.js` (uses a minimal fake DOM object, no browser)

**Interfaces:**
- Consumes: `window.Joy` / `require('../assets/joy.js')`: `createCounter`, `createShuffler`, `formatCount`, `IDEAS`, `PLACEHOLDER_START_COUNT`; ids from Task 3.
- Produces: `initHome(doc: Document, joy: typeof Joy): void` (also called automatically on `DOMContentLoaded` when `window` exists). It does nothing, and throws nothing, if `#sj-heart`/`#sj-count` or `#sj-surprise`/`#sj-idea` are missing.

- [ ] **Step 1: Write failing tests** with a fake `doc`: after `initHome`, a click on `#sj-heart` appends exactly one ring to `#sj-rings` and sets `#sj-count` to `"1,285"`; twenty rapid clicks leave at most 6 rings present; each ring is removed after its animation ends; `#sj-surprise` loses its `hidden` attribute when elements exist; clicking it sets `#sj-idea` text to a member of `IDEAS`, and 20 clicks never repeat consecutively; `initHome` with an empty fake doc does not throw.
- [ ] **Step 2: Run** `node --test tests/` — expected: FAIL.
- [ ] **Step 3: Implement `initHome`** in `assets/home.js`. Cap live rings at 6 (drop the oldest). When `matchMedia('(prefers-reduced-motion: reduce)')` matches, skip the ring and use a brief opacity pulse class instead. Rings are absolutely positioned CSS-animated elements (transform/opacity only).
- [ ] **Step 4: Run** `node --test tests/` — expected: PASS. Then run `python3 -m http.server 8011` and open `http://localhost:8011/index.html` at 375px and 1280px: tap the heart, tap "Surprise me", Tab to the heart and press Enter. Expected: rings, counter +1, ideas rotate, no horizontal scroll, no console errors.
- [ ] **Step 5: Commit** `git add assets/home.js assets/styles.css tests/home.test.js && git commit -m "feat: tap-to-ripple heart and surprise-me ideas"`

### Task 5: Squarespace snippets and setup guide

**Files:**
- Modify: `build.py` (emit snippet files)
- Create (generated): `squarespace/heart-block.html`, `squarespace/surprise-block.html`, `squarespace/footer-injection.html`
- Create: `docs/squarespace-setup.md`
- Test: `tests/test_build.py`

**Interfaces:**
- Consumes: `assets/joy.js`, `assets/home.js`, the Task 3 element ids, and the ring/drift CSS from Task 4.
- Produces: `heart-block.html` (markup for `#sj-heart`, `#sj-rings`, `#sj-count` plus a `<style>` block with only the CSS those need; paste into a Code Block in HTML mode), `surprise-block.html` (markup and `<style>` for `#sj-surprise`, `#sj-idea`), `footer-injection.html` (one `<script>` containing `joy.js` and `home.js` inlined; paste into Code Injection > Footer).

- [ ] **Step 1: Write failing tests:** the three snippet files exist after `python3 build.py`; `footer-injection.html` contains `createCounter` and `initHome`, is a single `<script>` element, and is under 20 KB; each markup snippet has exactly the ids it should and contains no `<script>`; snippets reference no local file paths except absolute Squarespace-uploaded image placeholders written as `{{HEART_IMAGE_URL}}`.
- [ ] **Step 2: Run** `python3 build.py && python3 -m unittest discover -s tests` — expected: FAIL.
- [ ] **Step 3: Extend `build.py`** to generate the snippet files from the source assets so they never drift from the prototype.
- [ ] **Step 4: Write `docs/squarespace-setup.md`:** numbered steps covering (a) upload fonts and set site fonts and colors, (b) create a Not Linked page named "Home (new)", (c) add the five sections with background colors, wave dividers, site-wide scroll animation, and upload the web-sized photos, (d) paste the two block snippets and replace `{{HEART_IMAGE_URL}}`, (e) paste the footer injection (Pages > Custom Code > Code Injection > Footer), (f) check the saved page in a private window, logged out (not Safe Mode, which turns custom code off), (g) swap in as Home and how to roll back, (h) plan requirement (Core or higher) and the trial note. Each step names the exact Squarespace menu path. Mark the counter constant as the place to wire real data later.
- [ ] **Step 5: Run** the test command — expected: PASS. Commit `git add build.py squarespace docs/squarespace-setup.md tests/test_build.py && git commit -m "feat: squarespace snippets and setup guide"`

### Task 6: Cleanup and final verification

**Files:**
- Modify: `README.md`, `.gitignore`
- Create: `.gitignore`

- [ ] **Step 1: Create `.gitignore`** containing `.superpowers/`.
- [ ] **Step 2: Update `README.md`:** new test commands (`node --test tests/`, `python3 -m unittest discover -s tests`), the new files, and the snippet workflow.
- [ ] **Step 3: Run both test suites and `python3 build.py`** — expected: all pass, six pages and three snippets written.
- [ ] **Step 4: Browser check** at 375px, 768px and 1280px on all six pages: expected no console errors, no horizontal scroll, header fixed, no-JS check by disabling scripts shows the static heart and counter with "Surprise me" absent.
- [ ] **Step 5: Commit** `git add README.md .gitignore && git commit -m "docs: readme and gitignore for joy ripple home"`
