# Spread Joy Collective: HTML mock

A static mock of the Squarespace site, used to settle layout, copy and links before rebuilding it in the Squarespace editor.

## Run

```bash
python3 build.py          # regenerates the six .html pages
open index.html           # or: python3 -m http.server 8011
```

Edit page content in `build.py` and styles in `assets/styles.css`. The `.html` files are generated, so change `build.py` rather than the HTML.

## Pages

Home, Our Mission, Our Story, Events, How Can We Help, Contact (same as the live site's menu).

## Design fixes built in (from reviewing the live home page)

- Nav text is dark on the yellow header (white on yellow was hard to read).
- Hero has a headline and two buttons (Donate, Get involved) above the fold.
- No black-on-black logo text: the brand name sits in the header in dark-on-yellow.

## Placeholders to fill in

Every `href="#"` is a link still to be supplied:

| Where | Needed |
|---|---|
| Header, hero, CTA band, Help page | Donation page URL |
| Footer, Help, Contact | Instagram, Facebook, YouTube URLs |
| Footer | Newsletter signup service |
| Footer, Contact | Real email address and phone number (currently `hello@example.com`) |
| Footer | Privacy policy page |
| Events | Registration link and calendar link per event, gallery link |
| Help | Volunteer sign-up form URL |
| Contact | Google Maps link |
| Mission | Press or partner link |

Brand: yellow `#FDCD17`, dark `#231f20`, League Spartan (supporting font) and Oooh Baby (accent) from Google Fonts. The brand's logo font, Brandon Grotesque, is an Adobe font, so the wordmark beside the heart is League Spartan with wide tracking until it is licensed. Web-sized photos and logos live in `assets/img/`; full-size originals and brand files stay in `assets/`. The header is sticky.
