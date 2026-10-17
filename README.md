# Spread Joy Collective: site workspace

Local mock and paste-ready code for the Squarespace 7.1 site. Site-wide rules for every page: [SPEC.md](SPEC.md). Repo context and known gaps against the spec: [CLAUDE.md](CLAUDE.md).

## Run

```bash
python3 build.py                    # regenerates the pages, squarespace/ and home-page/
python3 -m http.server 8011         # then open http://localhost:8011/index.html
node --test tests/                  # logic tests
python3 -m unittest discover -s tests   # markup, CSS and snippet tests
```

Edit content in `build.py` and styles in `assets/`; the `.html` pages, `squarespace/` and `home-page/1-6*` are generated.

## Pages

Home, Our Mission, Our Story, Events, How Can We Help, Contact. The home page is an Apple-style scroll story; its paste-ready Squarespace version and rebuild guide are in `home-page/` (start with `home-page/README.md`). `squarespace/` holds older standalone snippets (legacy).

## Placeholders still to fill

Every `href="#"` in the mock is a link still to be supplied: the Givebutter campaign URL (header, CTAs), social URLs, newsletter service, real contact email and phone (currently `hello@example.com`), privacy page, event registration links, volunteer form, map link.

Brand: yellow `#FDCD17`, dark `#231F20`, League Spartan and Oooh Baby. Photos and logos for the mock are in `assets/img/`.
