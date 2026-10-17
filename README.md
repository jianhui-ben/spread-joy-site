# Spread Joy Collective: HTML mock

> Site-wide rules for every page: [SPEC.md](SPEC.md). Repo context for Claude sessions and known gaps against the spec: [CLAUDE.md](CLAUDE.md).

A static mock of the Squarespace site, used to settle layout, copy and links before rebuilding it in the Squarespace editor.

## Run

```bash
python3 build.py                    # regenerates the six .html pages and the Squarespace snippets
python3 -m http.server 8011         # then open http://localhost:8011/index.html
```

Edit page content in `build.py` and styles in `assets/styles.css`. The `.html` files and `squarespace/` snippets are generated, so change `build.py` or the assets rather than the output.

## Tests

```bash
node --test tests/                          # counter and idea logic, ripple behavior
python3 -m unittest discover -s tests       # theme, home page markup, snippets
```

## Pages

Home, Our Mission, Our Story, Events, How Can We Help, Contact (same as the live site's menu).

The home page is an Apple-style scrolling story: a giant headline and a photo that grows as you scroll, a pinned stage where photos and three short lines change with scroll, then a yellow "Your turn" band with swipeable photo cards (the last one is "Surprise me"). Tap the heart on the hero photo to send a ripple (the counter number is a placeholder, `PLACEHOLDER_START_COUNT` in `assets/joy.js`). The paste-ready Squarespace version of this page, with a step-by-step guide, is in `home-page/` (start with `home-page/README.md`). Styles are in `assets/home.css`, scroll logic in `assets/scroll-story.js`. With JavaScript off, the static photos, heart and counter show and "Surprise me" is hidden.

## Squarespace

`squarespace/` is the library of ready-to-paste, commented snippets (`heart-block.html`, `surprise-block.html`, `footer-injection.html`). Start at `squarespace/README.md`: it indexes every snippet, says where each goes, and explains how to add new ones. Follow `docs/squarespace-setup.md` to recreate the page in Squarespace 7.1. Design and plan: `docs/superpowers/specs/` and `docs/superpowers/plans/`.

## Placeholders to fill in

Every `href="#"` is a link still to be supplied:

| Where | Needed |
|---|---|
| Header, "I want to give" on Home, CTA band, Help page | Donation page URL |
| Footer, Help, Contact | Instagram, Facebook, YouTube URLs |
| Footer | Newsletter signup service |
| Footer, Contact | Real email address and phone number (currently `hello@example.com`) |
| Footer | Privacy policy page |
| Events | Registration link and calendar link per event, gallery link |
| Help | Volunteer sign-up form URL |
| Contact | Google Maps link |
| Mission | Press or partner link |

Brand: yellow `#FDCD17`, dark `#231f20`, League Spartan (supporting font) and Oooh Baby (accent) from Google Fonts. The brand's logo font, Brandon Grotesque, is an Adobe font, so the wordmark beside the heart is League Spartan with wide tracking until it is licensed. Web-sized photos and logos live in `assets/img/`; full-size originals and brand files stay in `assets/`. The header is sticky.
