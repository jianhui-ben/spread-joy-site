# Contact

Local preview: `contact.html`. Live Squarespace page: **`/contact`**.

## What the page is

A note from Marisa, the sock photo, and three links: email (`marisa@spreadjoycollective.org`), Instagram (`@spreadjoycollective`), and Facebook. There is no form. The words live in `build.py`. The layout lives in `assets/contact.css`. The photo is `assets/img/contact-socks.jpg`.

`python3 build.py` writes `contact-page/1-contact-block.html`, a self-contained Code Block with the photo inlined.

## How to put it on Squarespace

1. Open the existing Contact page (`/contact`).
2. Add one Code Block, set its mode to HTML, and paste `1-contact-block.html`.
3. Save. The block carries its own photo, so nothing else needs uploading.

X is still `[TBD]` in the footer.
