# Squarespace snippets

> **Legacy.** The home page now lives in `../home-page/` (start with its `README.md`). The files below are older standalone snippets (tap-the-heart and "Surprise me"), kept but not maintained.

Paste-ready code for the Spread Joy Collective Squarespace site. Open a file, copy everything, paste it where the table says. Each file starts with a comment that says what it does, where to paste it and what it needs. That comment is safe to paste along with the code.

## Index

| File | What it is | Where to paste | Needs |
|---|---|---|---|
| `footer-injection.html` | The site script: counter, kindness ideas, click handling | Pages > Custom Code > Code Injection > **Footer** (once for the whole site) | Core, Plus or Advanced plan |
| `heart-block.html` | Tap-the-heart: heart button, rings, "ripples of joy so far" counter | A **Code Block** (mode HTML) where the heart goes | `footer-injection.html`; replace `{{HEART_IMAGE_URL}}` |
| `surprise-block.html` | "Surprise me" button and idea line | A **Code Block** (mode HTML) in the "Your turn" section | `footer-injection.html` |

## Install order

1. Paste `footer-injection.html` into the site Footer and save (once).
2. Paste the block snippets into Code Blocks on the pages that should have them.
3. Check in the editor's **Preview** (play icon), not the editing view: while editing, a click selects the block instead of tapping it.

## Generated files

The three files above are **generated** by `python3 build.py` from `assets/styles.css`, `assets/joy.js` and `assets/home.js`, so the website prototype and the Squarespace code never drift apart. Do not edit them by hand: change the source and rebuild. The comment at the top of each says so.

## Adding a new snippet

For a block that is not tied to the prototype, write the file here by hand, formatted and commented, and add a row to the index above.

1. Create `squarespace/<short-name>.html` (use `-block` in the name for Code Blocks, `-injection` for Code Injection).
2. Start it with this header comment:

   ```html
   <!--
     SNIPPET:        Short name of what it is
     WHAT IT DOES:   One or two sentences a non-developer can follow.
     WHERE TO PASTE: Code Block (mode HTML), or Pages > Custom Code > Code Injection > Header/Footer.
     NEEDS:          Other snippets, a paid plan, or "nothing".
     PLACEHOLDERS:   {{NAME}} values to replace before pasting, or "none".
   -->
   ```

3. Format it properly: one rule or tag per line, indentation, and a short comment above each group of CSS or each part of a script. No minified lines.
4. Keep CSS in a `<style>` block and scripts in a `<script>` block inside the file. JavaScript only runs in a Code Block in **HTML** mode or in Code Injection, and needs a Core, Plus or Advanced plan.
5. Add a row to the index above. `python3 -m unittest discover -s tests` checks that every snippet has the header, is formatted, and appears in this index.
