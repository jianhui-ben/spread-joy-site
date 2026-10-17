# Home page on Squarespace

Everything needed to rebuild the localhost home page (`index.html`) on Squarespace 7.1. The five numbered files are generated from the local page, so what you see on localhost is what you paste. Open a file, copy everything, paste it where the table says.

| # | File | Paste into | Notes |
|---|------|------------|-------|
| 1 | `1-header-injection.html` | Pages > Custom Code > Code Injection > **Header** | All the styles. Once for the whole site. |
| 2 | `2-footer-injection.html` | Pages > Custom Code > Code Injection > **Footer** | All the scripts. Once for the whole site. Replaces any older footer script from the heart/surprise snippets. |
| 3 | `3-hero-block.html` | Code Block 1 | Headline, growing photo, tap-the-heart |
| 4 | `4-story-block.html` | Code Block 2 | Pinned photo story |
| 5 | `5-your-turn-block.html` | Code Block 3 | Yellow wave, "Your turn" cards, "Surprise me" |

Needs a Core, Plus or Advanced plan (your trial allowed Code Injection). Do not hand-edit the numbered files: change `build.py` or `assets/*` and run `python3 build.py`, then paste again.

## Step 0: upload the photos and get their web addresses

Code Blocks cannot read files from this repo, so the photos must live on Squarespace. Blocks 3-5 contain placeholders in double curly braces that you replace with those addresses.

| Placeholder | Local file |
|---|---|
| `{{IMG_SOCKS_CIRCLE}}` | `assets/img/socks-circle.jpg` |
| `{{IMG_XAVIER}}` | `assets/img/xavier-portrait.jpg` |
| `{{IMG_SOCK_PILE}}` | `assets/img/sock-pile.jpg` |
| `{{IMG_FAMILY}}` | `assets/img/family.jpg` |
| `{{IMG_SOCKS_CIRCLE_2}}` | `assets/img/socks-circle-2.jpg` |
| `{{IMG_HEART}}` | `assets/img/heart.png` |
| `{{LINK_HELP}}`, `{{LINK_CONTACT}}` | the URLs of your How Can We Help and Contact pages, for example `/how-can-we-help` |

Suggested way (not tested by me): make a spare "Not Linked" page, add an Image block per photo and upload it, open the page, right-click each image, **Copy Image Address**, and keep the list in a note. In each block use find-and-replace in your editor of choice before pasting, or edit the address inside the Code Block afterwards.

## Step 1 and 2: install the styles and the script

1. Pages > Custom Code > Code Injection. Paste file 1 into **Header**, file 2 into **Footer**. Click Save.
2. If the footer already has an older script from `squarespace/footer-injection.html`, replace it. Two copies would both count taps.

## Step 3: the page

1. Create (or use) the page. Give it **one** section. Section background white.
2. In that section add **three Code Blocks**, one under the other, in this order: 3, 4, 5.
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
- "Surprise me" shows a different line each tap.
- The header slides away when scrolling down and returns when scrolling up.
- Check a phone width and the private window (Safe Mode turns custom code off).

## What I verified, and what I did not

Tested on your trial site (`Home (new)`) with the three blocks in one section and coloured stand-ins for the photos: full-width layout, block order, the pinned story and its photo/line changes, heart counter, "Surprise me", fade-ins, scrollable cards, header slide. Not tested: the real photos (they cannot load from localhost inside Squarespace), the photo upload steps above, a fixed/white header set through Site Styles, a dragged mouse on the cards, other templates and other browsers. If something looks off, it is most likely one of those.

## Changing things later

- Words, photos, links: edit the Code Block HTML directly in Squarespace, or change `build.py` (the `HOME_*` sections) and regenerate.
- Colours, sizes, motion: `assets/home.css`.
- The made-up counter number and the kindness ideas: `assets/joy.js`.
