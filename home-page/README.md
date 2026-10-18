# Home page on Squarespace

Everything needed to rebuild the localhost home page (`index.html`) on Squarespace 7.1. The six numbered files are generated from the local page, so what you see on localhost is what you paste. Open a file, copy everything, paste it where the table says.

| # | File | Paste into | Notes |
|---|------|------------|-------|
| 1 | `1-header-injection.html` | Pages > Custom Code > Code Injection > **Header** | All the styles. Once for the whole site. |
| 2 | `2-footer-injection.html` | Pages > Custom Code > Code Injection > **Footer** | The charcoal footer (same as localhost) and all the scripts. Replace the whole Footer field. This also hides Squarespace's own footer, so the white logo row does not sit on top. |
| 3 | `3-hero-block.html` | Code Block 1 | Headline, growing photo, tap-the-heart, page-open heart effect |
| 4 | `4-story-block.html` | Code Block 2 | Pinned photo story |
| 5 | `5-your-turn-block.html` | Code Block 3 | Yellow wave, "Your turn" cards, "Surprise me" |
| 6 | `6-footer-block.html` | Do not paste | Same footer markup, kept for reference. Paste 2 already puts it on every page. Pasting this block as well shows two footers. |

Needs a Core, Plus or Advanced plan (your trial allowed Code Injection). Do not hand-edit the numbered files: change `build.py` or `assets/*` and run `python3 build.py`, then paste again.

## Step 0: photos (already done for the trial site)

Code Blocks cannot read files from this repo, so the photos live on Squarespace. The six photos were uploaded to the trial site and their web addresses are saved in `image-urls.json`. `python3 build.py` puts those addresses into blocks 3-5, so the blocks are paste-ready as they are. The two page links (`LINK_HELP`, `LINK_CONTACT`) are in the same file; change them to your real page URLs if they differ.

To use another Squarespace site or new photos: upload each photo (for example in an Image block on a spare page, which uses the file picker), open the page, right-click the image, **Copy Image Address**, drop the `?format=...` ending, put the address into `image-urls.json` and rebuild. Any key missing from that file stays as a `{{PLACEHOLDER}}` in the block for you to replace by hand.

## Step 1 and 2: install the styles and the script

1. Pages > Custom Code > Code Injection. Paste file 1 into **Header**, file 2 into **Footer**. Click Save.
2. File 2 replaces the whole Footer field, including any older footer. Do not leave the old footer above it, and do not paste file 6 onto the page. Two copies of the script would both count taps, and two footers would stack.

## Step 3: the page

1. Create (or use) the page. Give it **one** section. Section background white.
2. In that section add **three Code Blocks**, one under the other, in this order: 3, 4, 5. The footer comes from file 2, not from a block.
3. For each block: open it, set the mode to **HTML**, make sure **Display Source Code** is off, paste the file (with the placeholders replaced), close the editor.
4. Header look: in Site Styles set the header background to white (or translucent white) and keep it fixed to the top if your template offers that. The script adds a class to `#header` so it slides away when you scroll down and comes back when you scroll up. The yellow line under the header is optional.
5. **Save, then test in Preview** (the play icon), not in the editing view. In the editor a click selects the block, and the script can hold stale references to blocks the editor re-drew.

## What the extra CSS in file 1 is for

Squarespace wraps every block in a padded grid that clips overflow, which would break a full-width pinned story. File 1 has a section marked "Squarespace" that, only for a section containing `.sj-home`, removes the padding, stacks the blocks, and lets the story stick. It also forces the brand font onto headings, paragraphs and buttons, which Squarespace styles itself. Everything we add sits inside `<div class="sj-home">`, so the rest of the site is untouched.

## Check list after pasting

- Headline fades up, photo grows as you scroll.
- Tapping the heart adds 1 to the number and sends a ring out.
- The story stays pinned while three photos and lines change.
- The yellow band and wave appear full width; cards drag sideways with a mouse and swipe on a phone.
- "Surprise me" shows a different kindness idea each tap. "I did it!" shows "You just put more joy into the world." The next idea clears that line. Nothing is saved.
- "I have time" goes to `/events`. "Socks That Spread Joy" opens its Givebutter page. "I have something to share" opens the hope jar. "I need support" goes to `/let-us-help`.
- The header slides away when scrolling down and returns when scrolling up.
- Check a phone width and the private window (Safe Mode turns custom code off).

## What I verified, and what I did not

Tested on your trial site (`Home (new)`), three Code Blocks in one section, real photos from Squarespace's image storage: white page even when the browser forces dark mode, full-width layout, block order, the pinned story with its photo and line changes, heart counter, "Surprise me", fade-ins, scrollable cards, header slide, and the story still updating after Squarespace re-draws the blocks. Not tested: a mouse drag on the cards, a fixed header set through Site Styles (on the trial the header is not fixed, so it scrolls away by itself and the slide never shows), a phone, other templates and other browsers.

Two things Squarespace did that the localhost page does not: the header is laid over the top of the page, so the hero has 170px extra space on top (set in file 1); and the browser's forced dark mode turned the page black until file 1 declared the page light-only.

## Changing things later

- Words, photos, links: edit the Code Block HTML directly in Squarespace, or change `build.py` (the `HOME_*` sections) and regenerate.
- Colours, sizes, motion: `assets/home.css`.
- The made-up counter number: `assets/ripples.js` (`PLACEHOLDER_START_COUNT`, `EPOCH_MS`, `TICK_MS`, `WRAP_AT`). It is worked out from the clock, with no server: it starts at 1,284 on 17 October 2026, goes up by one every 10 seconds for every visitor, and goes back to 0 at 10,000,000. A visitor's own taps are added on top and remembered in that browser only. It is not a real count. The heart and counter script travels inside the hero block (paste 3), not in the Footer injection. The kindness ideas: `assets/joy.js`.
