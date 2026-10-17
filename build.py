"""Builds the static HTML mock pages. Run: python3 build.py

Edit page content below, rebuild, and open index.html in a browser.
Links marked href="#" are placeholders: see README.md for the list to fill in.
"""
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

PAGES["index.html"] = dict(
    title="Home",
    description="Spread Joy Collective supports families of individuals with disabilities. Small acts. Big impact. Spread joy.",
    scripts="""<script src="assets/joy.js" defer></script>
<script src="assets/home.js" defer></script>""",
    body=f"""
<section class="moment band center" id="tap">
  <div class="wrap">
    <div class="tap-stage">
      <div id="sj-rings" class="rings" aria-hidden="true"></div>
      <button id="sj-heart" class="heart-btn" type="button" aria-label="Tap to send a ripple of joy"><img src="assets/img/heart.png" alt=""></button>
    </div>
    <h2>Tap the <span class="hl">heart.</span></h2>
    <p class="counter" aria-live="polite"><span id="sj-count">{START_COUNT}</span> ripples of joy so far</p>
    <p class="accent">Small acts. Big impact. Spread joy.</p>
  </div>
</section>
{WAVE_DOWN}

<section class="moment band yellow">
  <img class="drift-heart" src="assets/img/heart-white.png" alt="" style="left:5%;top:36px">
  <div class="wrap">
    <div class="photo-card"><img src="assets/img/xavier-portrait.jpg" alt="Xavier smiling with his arms wide open"></div>
    <h2>It started with <span class="hl">one kid.</span></h2>
  </div>
</section>
{WAVE_UP}

<section class="moment band">
  <img class="drift-heart" src="assets/img/heart.png" alt="" style="right:5%;top:36px;animation-delay:1s">
  <div class="wrap">
    <h2>Then a whole <span class="hl">circle</span> showed up.</h2>
    <div class="photo-card"><img src="assets/img/socks-circle.jpg" alt="Xavier smiling in a circle of friends in colorful socks"></div>
  </div>
</section>
{WAVE_DOWN}

<section class="moment band yellow">
  <img class="drift-heart" src="assets/img/heart-white.png" alt="" style="left:5%;top:36px;animation-delay:2s">
  <div class="wrap">
    <div class="photo-card"><img src="assets/img/sock-pile.jpg" alt="A huge pile of donated colorful socks"></div>
    <h2><span class="hl">578</span> socks. One kindness at a time.</h2>
  </div>
</section>
{WAVE_UP}

<section class="moment band center" id="your-turn">
  <div class="wrap">
    <img class="small-heart" src="assets/img/heart.png" alt="">
    <h2>Your <span class="hl">turn.</span></h2>
    <div class="choices">
      <a class="pill" href="help.html">I have time</a>
      <a class="pill" href="#">I want to give</a>
      <a class="pill" href="help.html">I have something to share</a>
      <a class="pill" href="contact.html">My family could use support</a>
    </div>
    <button id="sj-surprise" class="pill outline" type="button" hidden>Surprise me &#9829;</button>
    <p id="sj-idea" class="idea" aria-live="polite" hidden></p>
  </div>
</section>
""",
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

HEART_BLOCK = """<!-- Spread Joy: tap-the-heart. Paste into a Code Block (HTML mode). Replace {{HEART_IMAGE_URL}} with the uploaded heart.png URL. -->
<style>
__VARS__
__CSS__
</style>
<div class="tap-stage">
  <div id="sj-rings" class="rings" aria-hidden="true"></div>
  <button id="sj-heart" class="heart-btn" type="button" aria-label="Tap to send a ripple of joy"><img src="{{HEART_IMAGE_URL}}" alt=""></button>
</div>
<p class="counter" aria-live="polite" style="text-align:center"><span id="sj-count">__COUNT__</span> ripples of joy so far</p>
"""

SURPRISE_BLOCK = """<!-- Spread Joy: Surprise me. Paste into a Code Block (HTML mode). The button stays hidden until the footer script runs. -->
<style>
__VARS__
__CSS__
</style>
<div style="text-align:center">
  <button id="sj-surprise" class="pill outline" type="button" hidden>Surprise me &#9829;</button>
  <p id="sj-idea" class="idea" aria-live="polite" hidden></p>
</div>
"""


def build_snippets():
    out = OUT / "squarespace"
    out.mkdir(exist_ok=True)
    for filename, template, name in [("heart-block.html", HEART_BLOCK, "heart"),
                                     ("surprise-block.html", SURPRISE_BLOCK, "surprise")]:
        text = template.replace("__COUNT__", START_COUNT).replace("__VARS__", SNIPPET_VARS).replace("__CSS__", snippet_css(name))
        (out / filename).write_text(text)
        print("wrote squarespace/" + filename)
    joy = (OUT / "assets" / "joy.js").read_text()
    home = (OUT / "assets" / "home.js").read_text()
    script = ("<!-- Spread Joy: paste into Pages > Custom Code > Code Injection > Footer -->\n"
              "<script>\n" + joy + "\n" + home + "</script>\n")
    (out / "footer-injection.html").write_text(script)
    print("wrote squarespace/footer-injection.html")


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
        scripts=page.get("scripts", ""),
        footer_links=footer_links(),
    )
    (OUT / filename).write_text(html)
    print("wrote", filename)

build_snippets()
