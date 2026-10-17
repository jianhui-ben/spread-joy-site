# Recreating the Joy Ripple home page in Squarespace 7.1

The prototype (`index.html`) is the visual reference. In Squarespace, layout, colors, waves and scroll animations are built with the editor. Only two things use custom code: the tap-to-ripple heart and "Surprise me". Menu names below match your site as of 2026-10-16 (checked: Pages panel > Custom Code > Code Injection exists). Squarespace renames things now and then, so if a label differs, use the search icon in the editor.

## Before you start

- **Plan.** JavaScript in Code Blocks and Code Injection needs the Core, Plus or Advanced plan ([Squarespace help](https://support.squarespace.com/hc/en-us/articles/206543167-Code-blocks)). On the free trial, Code Injection showed an "Upgrade" padlock but still saved and ran a test script (verified 2026-10-16). Subscribe before launch, since trial behavior can change.
- **Support.** Squarespace does not troubleshoot custom code. Keep the snippets as they are.
- **Files you need** (all in this repo):
  - `squarespace/heart-block.html`, `squarespace/surprise-block.html`, `squarespace/footer-injection.html`
  - Photos in `assets/img/`: `xavier-portrait.jpg`, `socks-circle.jpg`, `sock-pile.jpg`, and `heart.png`, `heart-white.png`
  - Re-generate the snippets any time with `python3 build.py`.

## 1. Fonts and colors

1. Download League Spartan and Oooh Baby from Google Fonts (free). Convert or download as WOFF2/TTF.
2. Pages panel > Custom Code > Custom CSS > Manage Custom Files, and upload them. Add an `@font-face` rule for each in Custom CSS, then choose them in the site styles (paintbrush icon > Fonts).
3. In the site styles, set the colors: yellow `#FDCD17`, dark text `#231F20`, white background `#FFFFFF`.

## 2. Build the page as a Not Linked page

1. Pages panel > Not Linked > **+** > add a blank page, named "Home (new)". Leave the old Home alone so it can be rolled back.
2. Add five sections, alternating background white / yellow / white / yellow / white (Edit Section > Design > Background).
3. Between sections, turn on the divider (Edit Section > Design > Divider) and pick the wave shape. If your plan's divider shapes do not include a wave, copy the wave from the live site's home page.
4. Turn on site-wide scroll animations (paintbrush icon > Animations, Fade or Clip, Medium speed).

## 3. Fill in the five moments

| # | Section | What goes in it |
|---|---|---|
| 1 | White | A Text block "Tap the heart." (highlight the word "heart."), the **Code Block** from step 4, and an accent line "Small acts. Big impact. Spread joy." in Oooh Baby |
| 2 | Yellow | Image block with `xavier-portrait.jpg` and the text "It started with one kid." |
| 3 | White | Text "Then a whole circle showed up." and image `socks-circle.jpg` |
| 4 | Yellow | Image `sock-pile.jpg` and the text "578 socks. One kindness at a time." |
| 5 | White | Text "Your turn.", four Button blocks (I have time and I have something to share link to How Can We Help; I want to give links to the Donate page; My family could use support links to Contact), then the **Code Block** from step 5 |

Use the image block's built-in effect to add the offset shadow, or leave it flat. Add the small drifting hearts only if you like them: they are optional decoration and not part of the snippets.

## 4. Heart block (moment 1)

1. Upload `heart.png` to the site (Media Manager is fine). Copy its URL.
2. Open `squarespace/heart-block.html`, replace `{{HEART_IMAGE_URL}}` with that URL.
3. In section 1, Add Block > Code, set the mode to **HTML**, and paste the whole file.

## 5. Surprise-me block (moment 5)

1. Add Block > Code, mode **HTML**, paste `squarespace/surprise-block.html`.
2. The button stays hidden until the footer script runs, so the page still looks right if the script is missing.

## 6. Footer script

Pages panel > Custom Code > Code Injection > **Footer**, paste the whole of `squarespace/footer-injection.html`, and Save.

The made-up counter number lives in `PLACEHOLDER_START_COUNT` near the top of that script. Change it there to adjust the starting number. To make the counter real later, replace the code that reads this constant with a call to a data source. Visitors cannot write to Squarespace itself, so this needs an outside service.

## 7. Check before swapping it in

- Preview the page (Edit > Preview). Code may not show while you are logged in, so use Preview in Safe Mode if the heart does nothing.
- Code Blocks may not render on index pages or with Ajax loading on. If the page shows plain text, turn Ajax loading off (search the site styles for "Ajax loading"; I did not confirm where it sits in your menu).
- Tap the heart: rings appear, the number goes up by one. Tap "Surprise me": a new idea appears and never repeats twice in a row.
- Check on a phone, and with the device's "reduce motion" setting on: rings are replaced by a quick pulse.

## 8. Go live and roll back

1. Pages panel: drag "Home (new)" into Main Navigation and set it as the Home page (page settings > Set as homepage).
2. To roll back, set the old Home page as the homepage again. Nothing was deleted.
