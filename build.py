"""Builds the static HTML mock pages. Run: python3 build.py

Edit page content below, rebuild, and open index.html in a browser.
Links marked href="#" are placeholders: see README.md for the list to fill in.
"""
import json
import re
from pathlib import Path

OUT = Path(__file__).parent


def start_count():
    """The made-up starting number lives only in assets/joy.js; format it for the static markup."""
    joy = (OUT / "assets" / "joy.js").read_text()
    return f"{int(re.search(r'PLACEHOLDER_START_COUNT\s*=\s*(\d+)', joy).group(1)):,}"


START_COUNT = start_count()

NAV = [
    ("index.html", "Home"),
    ("mission.html", "Our Mission"),
    ("story.html", "Our Story"),
    ("events.html", "Events"),
    ("help.html", "How Can We Help"),
    ("contact.html", "Contact"),
]

SHELL = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} | Spread Joy Collective</title>
  <meta name="description" content="{description}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=League+Spartan:wght@400;500;600&family=Oooh+Baby&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="assets/styles.css">
{head_extra}
</head>
<body>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="index.html"><img src="assets/img/heart.png" alt="">Spread Joy Collective</a>
    <nav aria-label="Main">
{nav}
    </nav>
    <a class="btn btn-dark" href="#">Donate</a>
  </div>
</header>
<main>
{body}
</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="cols">
      <div>
        <a class="brand" href="index.html"><img src="assets/img/heart.png" alt="">Spread Joy Collective</a>
        <p class="accent">Small acts. Big impact. Spread joy.</p>
      </div>
      <div>
        <h4>Explore</h4>
        <ul>
{footer_links}
        </ul>
      </div>
      <div>
        <h4>Follow</h4>
        <ul>
          <li><a href="#">Instagram</a></li>
          <li><a href="#">Facebook</a></li>
          <li><a href="#">YouTube</a></li>
        </ul>
      </div>
      <div>
        <h4>Stay in the loop</h4>
        <form class="signup" action="#" onsubmit="return false">
          <input type="email" placeholder="Your email" aria-label="Email address">
          <button class="btn btn-yellow" type="submit">Join</button>
        </form>
      </div>
    </div>
    <p class="legal">&copy; Spread Joy Collective &middot; <a href="#">Privacy Policy</a> &middot; <a href="mailto:hello@example.com">hello@example.com</a></p>
  </div>
</footer>
{scripts}
</body>
</html>
"""

CTA = """
<section class="block alt">
  <div class="wrap">
    <h2>Ready to spread some joy?</h2>
    <p class="section-lead">Every gift, hour and share helps.</p>
    <div class="cta-row">
      <a class="btn btn-yellow" href="#">Donate</a>
      <a class="btn btn-outline" href="help.html">Get involved</a>
    </div>
  </div>
</section>
"""

PAGES = {}

WAVE = '<svg class="wave{flip}" viewBox="0 0 1200 44" preserveAspectRatio="none" aria-hidden="true"><path d="M0,20 C200,48 400,0 600,22 C800,44 1000,4 1200,24 L1200,44 L0,44 Z"/></svg>'
WAVE_DOWN = WAVE.format(flip="")
WAVE_UP = WAVE.format(flip=" flip")

HOME_HERO = f"""<section class="hero">
  <h1 class="reveal">Small acts. <br>Big impact.</h1>
  <p class="sub reveal d1">Spread joy.</p>
  <div class="hero-card" id="heroCard">
    <img src="assets/img/socks-circle.jpg" alt="A circle of volunteers holding up socks they collected">
    <div class="tap">
      <div class="tap-stage-mini">
        <div id="sj-rings" class="rings" aria-hidden="true"></div>
        <button id="sj-heart" type="button" aria-label="Tap to send a ripple of joy"><img src="assets/img/heart.png" alt=""></button>
      </div>
      <p aria-live="polite"><b id="sj-count">{START_COUNT}</b> ripples of joy so far</p>
    </div>
  </div>
</section>
"""

HOME_STORY = """<section class="story" id="story">
  <div class="stage-pin">
    <div class="frames">
      <div class="frame"><img src="assets/img/xavier-portrait.jpg" alt="Xavier, the kid whose story started it all"></div>
      <div class="frame"><img src="assets/img/socks-circle.jpg" alt="A circle of people holding socks together"></div>
      <div class="frame"><img src="assets/img/sock-pile.jpg" alt="A big pile of donated socks"></div>
      <div class="shade"></div>
      <div class="dots" aria-hidden="true"><i></i><i></i><i></i></div>
    </div>
    <div class="lines">
      <h2 class="line">It started with <span class="y">one kid.</span></h2>
      <h2 class="line">Then a whole <span class="y">circle</span> showed up.</h2>
      <h2 class="line"><span class="y">578 socks.</span> One kindness at a time.</h2>
    </div>
  </div>
</section>
"""

HOME_TURN = f"""<section class="turn">
  <h2 class="reveal">Your turn.</h2>
  <div class="cards" id="cards">
    <a class="card" href="help.html"><img src="assets/img/family.jpg" alt=""><span class="go" aria-hidden="true">&rarr;</span><h3>I have time</h3></a>
    <a class="card" href="#"><img src="assets/img/sock-pile.jpg" alt=""><span class="go" aria-hidden="true">&rarr;</span><h3>I want to give</h3></a>
    <a class="card" href="help.html"><img src="assets/img/socks-circle-2.jpg" alt=""><span class="go" aria-hidden="true">&rarr;</span><h3>I have something to share</h3></a>
    <a class="card" href="contact.html"><img src="assets/img/xavier-portrait.jpg" alt=""><span class="go" aria-hidden="true">&rarr;</span><h3>My family could use support</h3></a>
    <div class="card surprise">
      <img class="beat" src="assets/img/heart.png" alt="">
      <p id="sj-idea" class="idea sj-needs-js" aria-live="polite"></p>
      <button id="sj-surprise" class="pill outline sj-needs-js" type="button">Surprise me &#9829;</button>
    </div>
  </div>
</section>
"""

PAGES["index.html"] = dict(
    title="Home",
    description="Spread Joy Collective supports families of individuals with disabilities. Small acts. Big impact. Spread joy.",
    head_extra='<link rel="stylesheet" href="assets/home.css">',
    scripts="""<script src="assets/joy.js" defer></script>
<script src="assets/home.js" defer></script>
<script src="assets/scroll-story.js" defer></script>""",
    body=HOME_HERO + "\n" + HOME_STORY + "\n" + WAVE_UP + "\n" + HOME_TURN,
)

PAGES["mission.html"] = dict(
    title="Our Mission",
    description="Why Spread Joy Collective exists and who we serve.",
    body="""
<div class="wrap page-title"><h1>Our Mission</h1></div>
<section class="block">
  <div class="wrap prose">
    <p>To strengthen and support families of individuals with disabilities by building community, creating opportunities, and providing meaningful assistance wherever it is needed most.</p>
    <p><strong>Small acts. Big impact. Spread joy.</strong></p>
    <p>Our pillars: <strong>Support</strong>, <strong>Connection</strong>, <strong>Joy</strong>.</p>
    <p>The imperfect heart is our logo: it stands for care, connection and showing up for others. Its simplicity speaks to our belief that small acts of kindness create ripples of joy that spread far and wide.</p>
    <p><a href="story.html">Read our story &rarr;</a> &nbsp; <a href="events.html">Meet us at an event &rarr;</a></p>
  </div>
</section>
""" + CTA,
)

PAGES["story.html"] = dict(
    title="Our Story",
    description="How Spread Joy Collective started and where it is going.",
    body="""
<div class="wrap page-title"><h1>Our Story</h1></div>
<section class="block">
  <div class="wrap prose">
    <p>Placeholder copy. Tell the origin story in three short paragraphs: how it began, what you learned, what is next.</p>
    <p>Add a pull quote, and a link to a video or press piece if you have one.</p>
  </div>
  <div class="wrap gallery" style="margin-top:32px">
    <img src="assets/img/family.jpg" alt="Xavier with family in Peace, Love &amp; Inclusion shirts">
    <img src="assets/img/xavier-portrait.jpg" alt="Xavier smiling with arms wide">
    <img src="assets/img/sock-pile.jpg" alt="A huge pile of donated colorful socks">
  </div>
</section>
""" + CTA,
)

PAGES["events.html"] = dict(
    title="Events",
    description="Upcoming Spread Joy Collective events and how to register.",
    body="""
<div class="wrap page-title"><h1>Events</h1></div>
<section class="block">
  <div class="wrap">
    <div class="event"><div class="date">DEC<br>14</div><div class="info"><strong>Event one</strong><span>Location &middot; Time</span></div><a class="btn btn-outline" href="#">Register</a><a href="#">Add to calendar</a></div>
    <div class="event"><div class="date">JAN<br>18</div><div class="info"><strong>Event two</strong><span>Location &middot; Time</span></div><a class="btn btn-outline" href="#">Register</a><a href="#">Add to calendar</a></div>
    <div class="event"><div class="date">FEB<br>08</div><div class="info"><strong>Event three</strong><span>Location &middot; Time</span></div><a class="btn btn-outline" href="#">Register</a><a href="#">Add to calendar</a></div>
    <p class="section-lead" style="margin-top:24px">Past events and photos: <a href="#">see the gallery</a>.</p>
  </div>
</section>
""" + CTA,
)

PAGES["help.html"] = dict(
    title="How Can We Help",
    description="Volunteer, partner, or donate to Spread Joy Collective.",
    body="""
<div class="wrap page-title"><h1>How Can We Help</h1></div>
<section class="block">
  <div class="wrap">
    <div class="cards">
      <div class="card"><h3>Volunteer</h3><p>Give a few hours at an event.</p><a class="btn btn-yellow" href="#">Sign up</a></div>
      <div class="card"><h3>Partner or sponsor</h3><p>Businesses and schools welcome.</p><a class="btn btn-outline" href="contact.html">Start a conversation</a></div>
      <div class="card"><h3>Donate</h3><p>Every gift funds more joy.</p><a class="btn btn-yellow" href="#">Give now</a></div>
      <div class="card"><h3>Spread the word</h3><p>Follow and share our posts.</p><a href="#">Instagram</a> &middot; <a href="#">Facebook</a></div>
    </div>
  </div>
</section>
""",
)

PAGES["contact.html"] = dict(
    title="Contact",
    description="Get in touch with Spread Joy Collective.",
    body="""
<div class="wrap page-title"><h1>Contact</h1></div>
<section class="block">
  <div class="wrap" style="display:grid;gap:40px;grid-template-columns:repeat(auto-fit,minmax(260px,1fr))">
    <form class="stack" action="#" onsubmit="return false">
      <div><label for="n">Name</label><input id="n" type="text"></div>
      <div><label for="e">Email</label><input id="e" type="email"></div>
      <div><label for="m">Message</label><textarea id="m" rows="5"></textarea></div>
      <button class="btn btn-yellow" type="submit">Send message</button>
    </form>
    <div class="prose">
      <p><strong>Email</strong><br><a href="mailto:hello@example.com">hello@example.com</a></p>
      <p><strong>Phone</strong><br><a href="tel:+10000000000">(000) 000-0000</a></p>
      <p><strong>Find us</strong><br><a href="#">Open in Google Maps</a></p>
      <p><strong>Follow</strong><br><a href="#">Instagram</a> &middot; <a href="#">Facebook</a></p>
    </div>
  </div>
</section>
""",
)


def snippet_css(name):
    """Collect the CSS between /* snippet:NAME:start */ and /* snippet:NAME:end */ markers."""
    css = (OUT / "assets" / "styles.css").read_text()
    parts = re.findall(r"/\* snippet:%s:start \*/(.*?)/\* snippet:%s:end \*/" % (name, name), css, re.S)
    return "".join(parts).strip()


SNIPPET_VARS = ":root { --yellow: #fdcd17; --ink: #231f20; --bg: #ffffff; --muted: #6b6560; }"

GENERATED_NOTE = (
    "GENERATED:      by build.py (CSS from assets/styles.css, logic from assets/joy.js and assets/home.js).\n"
    "                  Change the sources and run `python3 build.py`; edits made here are overwritten."
)

HEART_BLOCK = """<!--
  SNIPPET:        Tap-the-heart (heart button, rings, counter)
  WHAT IT DOES:   Shows a yellow heart. Each tap sends a ring across the screen and adds 1 to
                  the "ripples of joy so far" number. The number is made up (see footer-injection.html).
  WHERE TO PASTE: A Code Block in the section where the heart should appear. Set the block's mode to HTML.
  NEEDS:          footer-injection.html installed once (Pages > Custom Code > Code Injection > Footer).
                  Without it the heart still shows but does nothing.
  PLACEHOLDERS:   {{HEART_IMAGE_URL}}  replace with the URL of the uploaded assets/img/heart.png.
  __GENERATED__
-->
<style>
/* Brand colours used below */
__VARS__

__CSS__
</style>

<!-- The heart, and the container the rings are added to -->
<div class="tap-stage">
  <div id="sj-rings" class="rings" aria-hidden="true"></div>
  <button id="sj-heart" class="heart-btn" type="button" aria-label="Tap to send a ripple of joy">
    <img src="{{HEART_IMAGE_URL}}" alt="">
  </button>
</div>

<!-- The counter line. aria-live lets screen readers announce the new number -->
<p class="counter" aria-live="polite" style="text-align:center">
  <span id="sj-count">__COUNT__</span> ripples of joy so far
</p>
"""

SURPRISE_BLOCK = """<!--
  SNIPPET:        "Surprise me" button and idea line
  WHAT IT DOES:   A button that shows a random kindness idea each time it is tapped. It never shows
                  the same idea twice in a row. The ideas live in footer-injection.html (the IDEAS list).
  WHERE TO PASTE: A Code Block in the "Your turn" section. Set the block's mode to HTML.
  NEEDS:          footer-injection.html installed once (Pages > Custom Code > Code Injection > Footer).
                  Without it the button and the idea line stay hidden, so nothing looks broken.
  PLACEHOLDERS:   none
  __GENERATED__
-->
<style>
/* Brand colours used below */
__VARS__

__CSS__
</style>

<!-- Both elements are hidden (class sj-needs-js) until the footer script has run -->
<div style="text-align:center">
  <button id="sj-surprise" class="pill outline sj-needs-js" type="button">Surprise me &#9829;</button>
  <p id="sj-idea" class="idea sj-needs-js" aria-live="polite"></p>
</div>
"""

FOOTER_HEADER = """<!--
  SNIPPET:        Site script (counter, ideas, click handling)
  WHAT IT DOES:   Makes the heart and "Surprise me" blocks work. Part 1 holds the logic (counter,
                  idea list, shuffler). Part 2 listens for taps on the whole page, so it keeps working
                  even when Squarespace's editor re-draws a Code Block.
  WHERE TO PASTE: Pages > Custom Code > Code Injection > FOOTER, then Save. Paste it once for the whole
                  site. It does nothing on pages that have no heart or "Surprise me" block.
  NEEDS:          A Core, Plus or Advanced plan (JavaScript is not allowed on Basic).
  PLACEHOLDERS:   none. To change the made-up starting number, edit PLACEHOLDER_START_COUNT in Part 1.
                  To change the kindness ideas, edit the IDEAS list in Part 1.
  __GENERATED__
-->
"""


def build_snippets():
    out = OUT / "squarespace"
    out.mkdir(exist_ok=True)
    for filename, template, name in [("heart-block.html", HEART_BLOCK, "heart"),
                                     ("surprise-block.html", SURPRISE_BLOCK, "surprise")]:
        text = template.replace("__GENERATED__", GENERATED_NOTE.replace("\n                  ", "\n                  ")).replace("__COUNT__", START_COUNT).replace("__VARS__", SNIPPET_VARS).replace("__CSS__", snippet_css(name))
        (out / filename).write_text(text)
        print("wrote squarespace/" + filename)
    joy = (OUT / "assets" / "joy.js").read_text()
    home = (OUT / "assets" / "home.js").read_text()
    script = (FOOTER_HEADER.replace("__GENERATED__", GENERATED_NOTE)
              + "<script>\n"
              + "/* ===== PART 1: logic (assets/joy.js) ===== */\n" + joy + "\n"
              + "/* ===== PART 2: click handling (assets/home.js) ===== */\n" + home
              + "</script>\n")
    (out / "footer-injection.html").write_text(script)
    print("wrote squarespace/footer-injection.html")


HOME_DIR = OUT / "home-page"

# Images used on the home page: placeholder name -> local file (uploaded to Squarespace by hand)
HOME_IMAGES = {
    "SOCKS_CIRCLE": "socks-circle.jpg",
    "XAVIER": "xavier-portrait.jpg",
    "SOCK_PILE": "sock-pile.jpg",
    "FAMILY": "family.jpg",
    "SOCKS_CIRCLE_2": "socks-circle-2.jpg",
    "HEART": "heart.png",
}

HOME_HEADER = """<!--
  PASTE 1 OF 5:   Home page styles
  WHAT IT DOES:   All the look of the home page: fonts, colours, the big headline, the growing photo,
                  the pinned photo story, the yellow "Your turn" band and cards, and the header that
                  tucks away when you scroll down.
  WHERE TO PASTE: Pages > Custom Code > Code Injection > HEADER, then Save. Once for the whole site.
  NEEDS:          A Core, Plus or Advanced plan for Code Injection.
  PLACEHOLDERS:   none
  GENERATED:      by build.py from assets/home.css, assets/styles.css and build.py.
                  Change the sources and run `python3 build.py`; edits made here are overwritten.
-->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=League+Spartan:wght@400;500;600;700&family=Oooh+Baby&display=swap" rel="stylesheet">
<style>
/* Brand colours */
:root { --yellow: #fdcd17; --ink: #231f20; --bg: #ffffff; --muted: #6b6560; }

/* Everything we add lives inside .sj-home so it does not disturb the rest of the site */
.sj-home { font-family: "League Spartan", system-ui, -apple-system, "Segoe UI", sans-serif; color: var(--ink); line-height: 1.2; }
.sj-home, .sj-home * { box-sizing: border-box; }
.sj-home img { display: block; max-width: 100%; }
.sj-home a { color: inherit; }

/* --- Squarespace: let our sections run edge to edge, with no padding or gaps around them --- */
__SQS__

/* --- Header that tucks away on scroll down (Squarespace header is #header) --- */
#header { transition: transform 0.4s cubic-bezier(0.2, 0.7, 0.2, 1); }
#header.tucked { transform: translateY(-100%); }

/* --- Button + script-only rules (used by the "Surprise me" card) --- */
__SURPRISE__

/* --- Wave between the photo story and the yellow band --- */
__WAVE__

/* --- Home page layout (assets/home.css) --- */
__HOMECSS__
</style>
"""

SQS_OVERRIDES = """.page-section:has(.sj-home) { padding: 0 !important; min-height: 0 !important; }
.page-section:has(.sj-home) .content-wrapper,
.page-section:has(.sj-home) .content { padding: 0 !important; max-width: none !important; width: 100% !important; }
.page-section:has(.sj-home) .fluid-engine { display: block !important; }
.page-section:has(.sj-home) .fe-block { grid-area: auto !important; }
.page-section:has(.sj-home) .sqs-block-code,
.page-section:has(.sj-home) .sqs-block-content { padding: 0 !important; margin: 0 !important; overflow: visible !important; }
/* Squarespace gives headings, paragraphs and buttons their own font; make ours use the brand font */
.page-section:has(.sj-home) .hero { padding-top: 170px; }
:root { color-scheme: only light; }
.sj-home h1, .sj-home h2, .sj-home h3, .sj-home p, .sj-home b, .sj-home button, .sj-home a { font-family: inherit; text-transform: none; font-style: normal; }"""

HOME_FOOTER = """<!--
  PASTE 2 OF 5:   Home page script
  WHAT IT DOES:   Makes the home page move. Part 1: heart counter, kindness ideas. Part 2: taps on the
                  heart and "Surprise me" (listens on the whole page, so it survives Squarespace
                  re-drawing a block). Part 3: the growing hero photo, the pinned photo story, fade-ins,
                  dragging the cards, and the header tucking away.
  WHERE TO PASTE: Pages > Custom Code > Code Injection > FOOTER, then Save. Once for the whole site.
                  It does nothing on pages that have none of our blocks.
  NEEDS:          A Core, Plus or Advanced plan.
  PLACEHOLDERS:   none. Starting number: PLACEHOLDER_START_COUNT in Part 1. Kindness ideas: IDEAS in Part 1.
  GENERATED:      by build.py from assets/joy.js, assets/home.js and assets/scroll-story.js.
                  Change the sources and run `python3 build.py`; edits made here are overwritten.
-->
"""

HOME_BLOCK = """<!--
  PASTE __N__ OF 5:   __TITLE__
  WHAT IT IS:     __WHAT__
  WHERE TO PASTE: __WHERE__
  NEEDS:          Pastes 1 and 2 installed once (Code Injection Header and Footer).
  PLACEHOLDERS:   __PLACEHOLDERS__
  GENERATED:      by build.py. Change build.py (HOME_* sections) and run `python3 build.py`.
-->
<div class="sj-home">
__HTML__
</div>
"""


def to_placeholders(html):
    for key, name in HOME_IMAGES.items():
        html = html.replace("assets/img/" + name, "{{IMG_%s}}" % key)
    html = html.replace('href="help.html"', 'href="{{LINK_HELP}}"').replace('href="contact.html"', 'href="{{LINK_CONTACT}}"')
    # home-page/image-urls.json holds the real Squarespace addresses; any key it lacks stays a placeholder
    urls_file = HOME_DIR / "image-urls.json"
    if urls_file.exists():
        for key, url in json.loads(urls_file.read_text()).items():
            html = html.replace("{{%s}}" % key, url)
    return html


def build_home_page():
    HOME_DIR.mkdir(exist_ok=True)
    header = (HOME_HEADER.replace("__SQS__", SQS_OVERRIDES)
              .replace("__SURPRISE__", snippet_css("surprise"))
              .replace("__WAVE__", ".sj-home .wave { display: block; width: 100%; height: 44px; margin: -1px 0; color: var(--yellow); fill: currentColor; }\n.sj-home .wave.flip { transform: scaleY(-1); }")
              .replace("__HOMECSS__", (OUT / "assets" / "home.css").read_text().strip()))
    (HOME_DIR / "1-header-injection.html").write_text(header)

    parts = [(OUT / "assets" / n).read_text() for n in ("joy.js", "home.js", "scroll-story.js")]
    footer = (HOME_FOOTER + "<script>\n"
              + "/* ===== PART 1: logic (assets/joy.js) ===== */\n" + parts[0] + "\n"
              + "/* ===== PART 2: taps on heart and Surprise me (assets/home.js) ===== */\n" + parts[1] + "\n"
              + "/* ===== PART 3: scroll story, cards, header (assets/scroll-story.js) ===== */\n" + parts[2]
              + "</script>\n")
    (HOME_DIR / "2-footer-injection.html").write_text(footer)

    blocks = [
        (3, "3-hero-block.html", "Hero: headline and growing photo with the heart",
         "Giant headline, the photo that grows as you scroll, and the tap-the-heart pill on top of it.",
         "A Code Block (mode HTML) in the FIRST section of the Home page.",
         "{{IMG_SOCKS_CIRCLE}}, {{IMG_HEART}}", HOME_HERO),
        (4, "4-story-block.html", "Pinned photo story",
         "Three photos and three short lines that change as you scroll while the stage stays pinned.",
         "A Code Block (mode HTML) in the SECOND section.",
         "{{IMG_XAVIER}}, {{IMG_SOCKS_CIRCLE}}, {{IMG_SOCK_PILE}}", HOME_STORY),
        (5, "5-your-turn-block.html", "Yellow wave and the Your turn cards",
         "The wave, the yellow band, the Your turn headline and the swipeable photo cards, ending with Surprise me.",
         "A Code Block (mode HTML) in the THIRD (last) section.",
         "{{IMG_FAMILY}}, {{IMG_SOCK_PILE}}, {{IMG_SOCKS_CIRCLE_2}}, {{IMG_XAVIER}}, {{IMG_HEART}}, {{LINK_HELP}}, {{LINK_CONTACT}}",
         WAVE_UP + "\n" + HOME_TURN),
    ]
    urls_file = HOME_DIR / "image-urls.json"
    known = json.loads(urls_file.read_text()) if urls_file.exists() else {}
    for n, fname, title, what, where, ph, html in blocks:
        ph = ", ".join(p for p in ph.split(", ") if p.strip("{}") not in known) or "none (addresses come from home-page/image-urls.json)"
        text = (HOME_BLOCK.replace("__N__", str(n)).replace("__TITLE__", title).replace("__WHAT__", what)
                .replace("__WHERE__", where).replace("__PLACEHOLDERS__", ph)
                .replace("__HTML__", to_placeholders(html.strip("\n"))))
        (HOME_DIR / fname).write_text(text)
    print("wrote home-page/ (5 files)")


def nav_html(current):
    lines = []
    for href, label in NAV:
        aria = ' aria-current="page"' if href == current else ""
        lines.append(f'      <a href="{href}"{aria}>{label}</a>')
    return "\n".join(lines)


def footer_links():
    return "\n".join(f'          <li><a href="{h}">{l}</a></li>' for h, l in NAV)


for filename, page in PAGES.items():
    html = SHELL.format(
        title=page["title"],
        description=page["description"],
        nav=nav_html(filename),
        body=page["body"].strip("\n"),
        head_extra=page.get("head_extra", ""),
        scripts=page.get("scripts", ""),
        footer_links=footer_links(),
    )
    (OUT / filename).write_text(html)
    print("wrote", filename)

build_snippets()
build_home_page()
