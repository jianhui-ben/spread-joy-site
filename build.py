"""Builds the static HTML mock pages. Run: python3 build.py

Edit page content below, rebuild, and open index.html in a browser.
Links marked href="#" are placeholders: see README.md for the list to fill in.
"""
import base64
import json
import re
from pathlib import Path

OUT = Path(__file__).parent


def start_count():
    """The made-up starting number lives only in assets/ripples.js; format it for the static markup."""
    joy = (OUT / "assets" / "ripples.js").read_text()
    return f"{int(re.search(r'PLACEHOLDER_START_COUNT\s*=\s*(\d+)', joy).group(1)):,}"


START_COUNT = start_count()

# Live Squarespace slugs, checked in the editor on 2026-10-17.
# Our Mission and Our Story are not pages yet: the nav items jump to /home#ourmission and /home#ourstory.
# There is no Get Involved page (dropped by the owner 2026-10-17), though SPEC.md still lists it in the nav.
GIVE_URL = "https://givebutter.com/SpreadJoyCollective"
SOCKS_URL = "https://givebutter.com/socks-that-spread-joy"

# Givebutter ids from the owner's dashboard (Settings > account id; campaign code beside the campaign title).
# Left empty until supplied: nothing is shown or invented without them.
_gb = json.loads((Path(__file__).parent / "home-page" / "image-urls.json").read_text()) if (Path(__file__).parent / "home-page" / "image-urls.json").exists() else {}
GB_ACCOUNT = _gb.get("GB_ACCOUNT", "")
GB_CAMPAIGN = _gb.get("GB_CAMPAIGN", "")
GB_LIBRARY = ('<script async src="https://widgets.givebutter.com/latest.umd.cjs?acct=%s"></script>' % GB_ACCOUNT) if GB_ACCOUNT else ""
GB_GOAL = ('<givebutter-goal-bar campaign="%s"></givebutter-goal-bar>' % GB_CAMPAIGN) if (GB_ACCOUNT and GB_CAMPAIGN) \
    else "<!-- Live total: add GB_ACCOUNT and GB_CAMPAIGN to home-page/image-urls.json and rebuild -->"
KOMO_URL = (
    "https://komonews.com/amazing-america/amazing-washington-kirkland-social-media-down-syndrome-"
    "weekly-tradition-blessed-chaos-happy-hour-marisa-mancke-david-jones-10-year-old-son-xavier"
)
PREVIEW_NOTE = (
    "This is a preview. On Squarespace this form is saved for the team to review. "
    "Nothing you type here is sent or stored."
)

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
  <link rel="stylesheet" href="assets/give-pill.css">
{head_extra}
</head>
<body>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="index.html"><img src="assets/img/heart.png" alt="">Spread Joy Collective</a>
    <nav aria-label="Main">
{nav}
    </nav>
    <a class="btn btn-dark" href="{give}" target="_blank" rel="noopener">Give &#9829;</a>
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
        <h4>Give</h4>
        <ul>
          <li><a href="{give}" target="_blank" rel="noopener">Give</a></li>
        </ul>
        <h4>Follow</h4>
        <ul>
          <li><span class="tbd">[TBD: Instagram]</span></li>
          <li><span class="tbd">[TBD: Facebook]</span></li>
          <li><span class="tbd">[TBD: X]</span></li>
        </ul>
      </div>
      <div>
        <h4>Stay in the loop</h4>
        <form class="signup" data-preview-form>
          <input type="email" placeholder="Your email" aria-label="Email address" required>
          <button class="btn btn-yellow" type="submit">Join</button>
          <p class="form-note" hidden data-preview-note="{preview_note}"></p>
        </form>
      </div>
    </div>
    <p class="legal">&copy; Spread Joy Collective &middot; <span class="tbd">[TBD: contact email]</span></p>
  </div>
</footer>
{scripts}
<script src="assets/give-pill.js" defer></script>
<script src="assets/site.js" defer></script>
</body>
</html>
"""

CTA = f"""
<section class="block alt">
  <div class="wrap">
    <h2>Ready to spread some joy?</h2>
    <p class="section-lead">Every gift, hour and share helps.</p>
    <div class="cta-row">
      <a class="btn btn-yellow" href="{GIVE_URL}" target="_blank" rel="noopener">Give</a>
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
    <img src="assets/img/socks-circle-hero.jpg" alt="A circle of volunteers holding up socks they collected">
    <div id="sj-fx" class="fx" aria-hidden="true"></div>
    <div class="tap">
      <div class="tap-stage-mini">
        <div id="sj-rings" class="rings" aria-hidden="true"></div>
        <button id="sj-heart" type="button" aria-label="Tap to send a ripple of joy"><img src="assets/img/heart.png" alt=""></button>
      </div>
      <p aria-live="polite"><b id="sj-count">{START_COUNT}</b> ripples of joy</p>
    </div>
  </div>
</section>
"""

# The heart and counter script travels inside the hero block, so nothing site-wide is needed for it.
RIPPLES_SCRIPT = "\n<script>\n" + (OUT / "assets" / "ripples.js").read_text().strip() + "\n</script>\n"

HOME_STORY = """<section class="story" id="story">
  <div class="stage-pin">
    <div class="frames">
      <div class="frame"><img src="assets/img/xavier-portrait.jpg" alt="Xavier, the kid whose story started it all"></div>
      <div class="frame"><img src="assets/img/story-circle.jpg" alt="A boy in a blue shirt smiling in the middle of a circle of children in colorful socks"></div>
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

# "I have something to share" overlay (the hope jar), supplied by a teammate and kept as supplied in
# assets/hope-jar.html. Its own launch button is hidden: the card below opens it via #share-a-hope.
HOPE_JAR = (Path(__file__).parent / "assets" / "hope-jar.html").read_text().replace(
    '<div class="sjc-launch">', '<div class="sjc-launch" hidden>', 1).strip()

HOME_TURN = f"""<section class="turn">
  <h2 class="reveal">Your turn.</h2>
  <div class="cards" id="cards">
    <a class="card" href="events.html"><img src="assets/img/family.jpg" alt="A family in Peace, Love and Inclusion shirts"><span class="go" aria-hidden="true">&rarr;</span><h3>I have time</h3></a>
    <a class="card" href="{SOCKS_URL}" target="_blank" rel="noopener"><img src="assets/img/card-socks.jpg" alt="A circle of children's feet in colorful, mismatched socks"><span class="go" aria-hidden="true">&rarr;</span><h3>Socks That Spread Joy</h3></a>
    <a class="card" href="#share-a-hope"><img src="assets/img/card-share.jpg" alt="Xavier smiling beside a teammate in green aprons"><span class="go" aria-hidden="true">&rarr;</span><h3>I have something to share</h3></a>
    <a class="card" href="help.html"><img src="assets/img/card-support.jpg" alt="Two smiling kids on a sports field, one in a cap and a bright vest, one in a red shirt, both holding up peace signs"><span class="go" aria-hidden="true">&rarr;</span><h3>I need support</h3></a>
    <div class="card surprise">
      <img class="beat" src="assets/img/heart.png" alt="">
      <p id="sj-idea" class="idea sj-needs-js" aria-live="polite"></p>
      <div class="joy-actions">
        <button id="sj-surprise" class="pill sj-needs-js" type="button">Surprise me &#9829;</button>
        <button id="sj-did-it" class="pill outline sj-needs-js" type="button">I did it!</button>
      </div>
      <p id="sj-done" class="done" hidden></p>
    </div>
  </div>
{HOPE_JAR}
</section>
<section class="give" id="sj-give">
  <h2 class="reveal">Help us keep it going.</h2>
  <div class="goal">{GB_GOAL}</div>
  <a id="sj-give-btn" class="pill" href="{GIVE_URL}" target="_blank" rel="noopener">Give &#9829;</a>
</section>
"""

PAGES["index.html"] = dict(
    title="Home",
    description="Spread Joy Collective supports families of individuals with disabilities. Small acts. Big impact. Spread joy.",
    head_extra='<link rel="stylesheet" href="assets/home.css">',
    scripts="""<script src="assets/ripples.js" defer></script>
<script src="assets/joy.js" defer></script>
<script src="assets/home.js" defer></script>
<script src="assets/scroll-story.js" defer></script>""" + GB_LIBRARY,
    body=HOME_HERO + "\n" + HOME_STORY + "\n" + WAVE_UP + "\n" + HOME_TURN,
)

PAGES["mission.html"] = dict(
    title="Our Mission",
    description="Spread Joy Collective supports individuals with disabilities and their families.",
    body="""
<div class="wrap page-title" id="ourmission"><h1>Our Mission</h1></div>
<section class="block">
  <div class="wrap prose">
    <p>Spread Joy Collective supports individuals with disabilities and their families by building community, creating opportunities, and providing meaningful assistance. Rooted in support, connection, and joy, we believe everyone deserves to feel seen, valued, included, and supported.</p>
    <p><a href="story.html">Read our story &rarr;</a></p>
  </div>
</section>
""" + CTA,
)

PAGES["story.html"] = dict(
    title="Our Story",
    description="How Spread Joy Collective began with Xavier and the community around him.",
    body=f"""
<div class="wrap page-title" id="ourstory"><h1>Our Story</h1></div>
<section class="block">
  <div class="wrap prose">
    <p>Spread Joy Collective began with our son, Xavier.</p>
    <p>When Xavier was born with Down syndrome, we knew we wanted him to grow up surrounded by people who would see him, celebrate him, include him, and believe in all that he could do. So we started building that community around him.</p>
    <p>Over the years, that community grew into something pretty incredible — a whole lot of kind, accepting, inclusive humans who showed up for Xavier, for our family, and for one another. Through Team Xavier, we spent more than a decade bringing people together, giving back, spreading kindness, and creating opportunities for connection and inclusion.</p>
    <p>As Xavier grew, so did our vision.</p>
    <p>We know firsthand the difference it makes to have people in your corner — people who show up, create opportunities, offer support, and make sure you know you belong. Spread Joy Collective was created to help bring more of that to individuals with disabilities and their families right here in our local community.</p>
    <p>Whether it’s providing meaningful assistance, creating opportunities, building connections, or simply finding ways to make life a little brighter, our goal is simple: to make a positive difference, one person, one family, and one act of joy at a time.</p>
    <p>What started with one little boy has grown into something much bigger.</p>
    <p>And we’re just getting started.</p>
    <p>Before Spread Joy Collective officially began, KOMO News shared a glimpse into our family, our community, and something that has always been at the heart of who we are — spreading joy.</p>
    <p><a href="{KOMO_URL}" target="_blank" rel="noopener">Watch our KOMO Amazing Washington story</a></p>
  </div>
  <div class="wrap gallery" style="margin-top:32px">
    <img src="assets/img/family.jpg" alt="Xavier with family in Peace, Love and Inclusion shirts">
    <img src="assets/img/xavier-portrait.jpg" alt="Xavier smiling with arms wide">
    <img src="assets/img/sock-pile.jpg" alt="A pile of donated colorful socks">
  </div>
</section>
""" + CTA,
)

PAGES["events.html"] = dict(
    title="Events",
    description="Pints for a Purpose and other ways Spread Joy Collective brings people together.",
    body=f"""
<div class="wrap page-title"><h1>Events</h1></div>
<section class="block" id="pints">
  <div class="wrap" style="display:grid;gap:32px;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));align-items:center">
    <img src="assets/img/socks-circle-hero.jpg" alt="A circle of people holding up socks they collected" style="width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:10px">
    <div class="prose">
      <h2>Pints for a Purpose</h2>
      <p>What happens when you fill a brewery with generous hearts, good humans, and incredible raffle prizes? A whole lot of joy — and a community showing up for local families.</p>
      <p>Pints for a Purpose is our annual fundraiser and one of our favorite ways to bring people together. Good, kind, accepting people coming together to make a difference is contagious. So is joy, and we love seeing it ripple beyond the event.</p>
      <p>At the heart of it is raising funds to support local families of individuals with disabilities. Every gift earns raffle tickets, and you choose which prizes you want to try to win. Every person matters. Every gift matters.</p>
      <p class="note"><span class="tbd">[TBD: event date, place, and how to join]</span></p>
      <p><a class="btn btn-yellow" href="{GIVE_URL}" target="_blank" rel="noopener">Give</a></p>
    </div>
  </div>
</section>
<section class="block alt" id="socks">
  <div class="wrap prose">
    <h2>Socks</h2>
    <p>Sock drives are one of the ways this community shows up. The story on the home page started with one of those piles.</p>
    <p class="note"><span class="tbd">[TBD: next sock drive date, place, and what to bring]</span></p>
  </div>
</section>
""" + CTA,
)

PAGES["help.html"] = dict(
    title="How Can We Help",
    description="A place for local families of individuals with disabilities to tell us what support would mean.",
    body=f"""
<div class="wrap page-title"><h1>How can we help?</h1></div>
<section class="block">
  <div class="wrap" style="display:grid;gap:40px;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));align-items:start">
    <div class="prose">
      <p><strong>Every family deserves support, connection, and joy.</strong></p>
      <p>If your family includes someone with a disability, we’d love to learn more about you. Whether you’re seeking help accessing a program, participating in an activity, or meeting another need, tell us how we might support your family.</p>
      <p>We’re a small nonprofit with a big heart. While support depends on available funding, every request will be considered with care.</p>
      <p>Tell us how we can help using this form — we’re glad you’re here.</p>
    </div>
    <form class="stack" data-preview-form>
      <div><label for="first">First name</label><input id="first" name="first" type="text" required autocomplete="given-name"></div>
      <div><label for="last">Last name</label><input id="last" name="last" type="text" required autocomplete="family-name"></div>
      <div><label for="email">Email</label><input id="email" name="email" type="email" required autocomplete="email"></div>
      <div><label for="seeking">What support are you seeking?</label><input id="seeking" name="seeking" type="text" required></div>
      <div><label for="more">Tell us more about your family and how we might help</label><textarea id="more" name="more" rows="5" required></textarea></div>
      <button class="btn btn-yellow" type="submit">Submit</button>
      <p class="form-note" hidden data-preview-note="{PREVIEW_NOTE}"></p>
    </form>
  </div>
</section>
""",
)

# Words and links for the contact page. The photo is assets/img/contact-socks.jpg.
CONTACT_EMAIL = "marisa@spreadjoycollective.org"
CONTACT_INSTAGRAM = "https://www.instagram.com/spreadjoycollective/"
CONTACT_FACEBOOK = "https://www.facebook.com/share/1FK6ceyMsn/?mibextid=wwXIfr"

CONTACT_SECTION = """<section id="sjc-contact" aria-label="Contact Spread Joy Collective">
  <section class="personal" aria-label="A note from Marisa">
    <div class="intro">
      <div class="tinyheart" aria-hidden="true">♥</div>
      <h1>Good things start <br>with a hello.</h1>
      <p>Have a question, an idea, or a little joy to share? I’d love to hear from you.</p>
      <p>Reach out by email, or find Spread Joy Collective on Instagram and Facebook.</p>
      <div class="signature">Marisa</div>
      <div class="role">Organizer, Spread Joy Collective</div>
    </div>
    <div class="photo-composition">
      <figure class="sock-photo">
        <img src="{img}" alt="A circle of people wearing colorful, mismatched socks">
        <figcaption>A little different. Better together.</figcaption>
      </figure>
      <div class="contact-note">
        <h2>Let’s connect.</h2>
        <div id="contact-list">
          <a class="channel" href="mailto:{email}">
            <span class="icon" aria-hidden="true"><svg viewBox="0 0 28 28"><rect x="3" y="5" width="22" height="17" rx="3"/><path d="m4 7 10 8 10-8"/></svg></span>
            <span><strong>Email us</strong><small>{email}</small></span>
            <span class="arrow" aria-hidden="true">↗</span>
          </a>
          <a class="channel" href="{instagram}" target="_blank" rel="noopener noreferrer">
            <span class="icon" aria-hidden="true"><svg viewBox="0 0 28 28"><rect x="4" y="4" width="20" height="20" rx="6"/><circle cx="14" cy="14" r="5"/><circle cx="20" cy="8" r="1"/></svg></span>
            <span><strong>Instagram</strong><small>@spreadjoycollective</small></span>
            <span class="arrow" aria-hidden="true">↗</span>
          </a>
          <a class="channel" href="{facebook}" target="_blank" rel="noopener noreferrer">
            <span class="icon" aria-hidden="true"><svg viewBox="0 0 28 28"><path d="M17 25V15h4l1-5h-5V8q0-3 4-3h1V1h-4q-6 0-6 7v2H8v5h4v10"/></svg></span>
            <span><strong>Facebook</strong><small>Spread Joy Collective</small></span>
            <span class="arrow" aria-hidden="true">↗</span>
          </a>
        </div>
      </div>
    </div>
  </section>
</section>
"""

PAGES["contact.html"] = dict(
    title="Contact",
    description="Reach Spread Joy Collective. A note from Marisa, with email, Instagram, and Facebook.",
    head_extra='<link rel="stylesheet" href="assets/contact.css">',
    body=CONTACT_SECTION.format(
        img="assets/img/contact-socks.jpg",
        email=CONTACT_EMAIL,
        instagram=CONTACT_INSTAGRAM,
        facebook=CONTACT_FACEBOOK,
    ),
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
                  the "ripples of joy" number. The number is made up (see footer-injection.html).
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
  <span id="sj-count">__COUNT__</span> ripples of joy
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
    ripples = (OUT / "assets" / "ripples.js").read_text()
    script = (FOOTER_HEADER.replace("__GENERATED__", GENERATED_NOTE)
              + "<script>\n"
              + "/* ===== PART 1: logic (assets/joy.js) ===== */\n" + joy + "\n"
              + "/* ===== PART 2: click handling (assets/home.js) ===== */\n" + home + "\n"
              + "/* ===== PART 3: heart and counter (assets/ripples.js) ===== */\n" + ripples
              + "</script>\n")
    (out / "footer-injection.html").write_text(script)
    print("wrote squarespace/footer-injection.html")


HOME_DIR = OUT / "home-page"

# Images used on the home page: placeholder name -> local file (uploaded to Squarespace by hand)
HOME_IMAGES = {
    "SOCKS_CIRCLE": "socks-circle-hero.jpg",
    "STORY_CIRCLE": "story-circle.jpg",
    "XAVIER": "xavier-portrait.jpg",
    "SOCK_PILE": "sock-pile.jpg",
    "FAMILY": "family.jpg",
    "CARD_SOCKS": "card-socks.jpg",
    "CARD_SHARE": "card-share.jpg",
    "CARD_SUPPORT": "card-support.jpg",
    "HEART": "heart.png",
}


HOME_FOOTER_HTML = """<footer class="sj-footer">
  <div class="sj-footer-wrap">
    <div class="sj-footer-cols">
      <div>
        <a class="sj-brand" href="/"><img src="{{IMG_HEART}}" alt="">Spread Joy Collective</a>
        <p class="sj-accent">Small acts. Big impact. Spread joy.</p>
      </div>
      <div>
        <h4>Explore</h4>
        <ul>
          <li><a href="/">Home</a></li>
          <li><a href="mission.html">Our Mission</a></li>
          <li><a href="story.html">Our Story</a></li>
          <li><a href="events.html">Events</a></li>
          <li><a href="help.html">How Can We Help</a></li>
          <li><a href="contact.html">Contact</a></li>
        </ul>
      </div>
      <div>
        <h4>Give</h4>
        <ul>
          <li><a href="https://givebutter.com/SpreadJoyCollective">Give</a></li>
        </ul>
        <h4>Follow</h4>
        <ul>
          <li><span class="sj-tbd">[TBD: Instagram]</span></li>
          <li><span class="sj-tbd">[TBD: Facebook]</span></li>
          <li><span class="sj-tbd">[TBD: X]</span></li>
        </ul>
      </div>
      <div>
        <h4>Stay in the loop</h4>
        <form class="sj-signup" onsubmit="event.preventDefault();var n=this.querySelector('.sj-form-note');if(n)n.hidden=false;return false;">
          <input type="email" placeholder="Your email" aria-label="Email address" required>
          <button type="submit">Join</button>
          <p class="sj-form-note" hidden>Nothing you type here is sent or stored.</p>
        </form>
      </div>
    </div>
    <p class="sj-legal">&copy; Spread Joy Collective &middot; <span class="sj-tbd">[TBD: contact email]</span></p>
  </div>
</footer>
"""

HOME_FOOTER_CSS = """.sj-footer { background: var(--ink); color: #fff; padding: 56px 0 32px; font-family: "League Spartan", system-ui, sans-serif; line-height: 1.6; }
.sj-footer-wrap { width: min(1180px, 92vw); margin: 0 auto; }
.sj-footer-cols { display: grid; gap: 36px; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); }
.sj-footer h4 { margin: 0 0 12px; color: var(--yellow) !important; font-family: inherit !important; font-weight: 600; font-size: 0.85rem; letter-spacing: 0.15em; text-transform: uppercase !important; }
.sj-footer ul { list-style: none; margin: 0; padding: 0; }
.sj-footer li { margin: 8px 0; }
.sj-footer a { color: #fff !important; text-decoration: none; }
.sj-footer a:hover { color: var(--yellow) !important; }
.sj-footer .sj-brand { display: inline-flex; align-items: center; gap: 10px; text-transform: uppercase; letter-spacing: 0.22em; font-weight: 500; font-size: 0.95rem; color: #fff !important; }
.sj-footer .sj-brand img { height: 40px; width: auto; }
.sj-footer .sj-accent { margin: 14px 0 0; color: var(--yellow) !important; font-family: "Oooh Baby", cursive; font-size: 1.5rem; line-height: 1.2; }
.sj-footer .sj-legal { margin: 36px 0 0; color: #b8b2ad !important; font-size: 0.8rem; }
.sj-footer .sj-tbd { background: var(--yellow); color: var(--ink) !important; padding: 0 0.25em; }
.sj-signup { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }
.sj-signup input { flex: 1; min-width: 140px; width: auto !important; padding: 12px 16px; border: 0; border-radius: 12px; font: inherit; color: var(--ink); background: #fff; }
.sj-signup button { padding: 12px 24px; min-height: 44px; border: 0; border-radius: 999px; background: var(--yellow); color: var(--ink); font: inherit; font-weight: 600; cursor: pointer; }
.sj-form-note { flex-basis: 100%; margin: 4px 0 0; color: #fff !important; font-weight: 500; }
#footer-sections, .sjc-footer { display: none !important; }"""

# Squarespace header restyled to match the localhost header. Applies to EVERY page (one header for the site).
SITE_HEADER_CSS = """#header .header-background { background: rgba(255, 255, 255, 0.86) !important; -webkit-backdrop-filter: saturate(180%) blur(14px); backdrop-filter: saturate(180%) blur(14px); }
#header, #header .header-inner { background: transparent !important; }
#header .header-border { background: #fdcd17 !important; height: 2px !important; opacity: 1 !important; }
#header .header-dropshadow { display: none !important; }
#header .header-nav-item a { font-family: "League Spartan", system-ui, sans-serif !important; text-transform: uppercase !important; letter-spacing: 0.14em !important; font-weight: 500 !important; font-size: 0.9rem !important; color: #231f20 !important; }
#header .header-nav-item--active a { border-bottom: 3px solid #fdcd17; }
#header .header-actions .btn { background: #fdcd17 !important; color: #231f20 !important; border: 0 !important; border-radius: 999px !important; font-family: "League Spartan", system-ui, sans-serif !important; font-weight: 600 !important; text-transform: none !important; letter-spacing: 0 !important; }
/* logo: yellow heart picture + the name as text, like the localhost header */
#header .header-title-logo img { display: none !important; }
#header .header-title-logo a { display: inline-flex !important; align-items: center; gap: 10px; text-decoration: none; }
#header .header-title-logo a::before { content: ""; width: 34px; height: 34px; background: url({{IMG_HEART}}) center / contain no-repeat; }
#header .header-title-logo a::after { content: "Spread Joy Collective"; font-family: "League Spartan", system-ui, sans-serif; text-transform: uppercase; letter-spacing: 0.22em; font-weight: 500; font-size: 0.95rem; color: #231f20; white-space: nowrap; }"""

HOME_HEADER = """<!--
  PASTE 1 OF 6:   Home page styles
  WHAT IT DOES:   The site header look (white, yellow line, uppercase menu, yellow Give heart pill; this changes the
                  header on every page) and all the look of the home page: fonts, colours, the big headline, the growing photo,
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

/* --- Site header: white, yellow line, uppercase menu, Give heart pill (all pages) --- */
__HEADERCSS__

/* --- Header that tucks away on scroll down (home page only) --- */
body:has(.sj-home) #header { transition: transform 0.4s cubic-bezier(0.2, 0.7, 0.2, 1); }
body:has(.sj-home) #header.tucked { transform: translateY(-100%); }

/* --- Button + script-only rules (used by the "Surprise me" card) --- */
__SURPRISE__

/* --- Footer block (paste 6) --- */
__FOOTERCSS__

/* --- Wave between the photo story and the yellow band --- */
__WAVE__

/* --- Home page layout (assets/home.css) --- */
__HOMECSS__

__GIVEPILLCSS__
</style>
<script>
/* The header button is Squarespace's own. Relabel Donate or a plain Give so it matches the local header. */
(function () {
  var LABEL = 'Give \\u2665';
  function labelHeader() {
    var nodes = document.querySelectorAll('#header .header-actions a, #header .header-menu-cta a');
    for (var i = 0; i < nodes.length; i++) {
      var text = (nodes[i].textContent || '').replace(/\\s+/g, ' ').trim();
      if (text === 'Donate' || text === 'Give') nodes[i].textContent = LABEL;
    }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', labelHeader);
  labelHeader();
  [300, 1200].forEach(function (ms) { setTimeout(labelHeader, ms); });
})();
</script>
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
  PASTE 2 OF 6:   Footer and home page script
  WHAT IT DOES:   Replaces the site footer with the same charcoal footer as the local preview (logo,
                  Explore, Give, Follow, Stay in the loop), and hides Squarespace's own footer so the
                  white logo row does not sit above it. Then the home page script. Part 1: kindness ideas.
                  Part 2: "Surprise me" and "I did it". (The heart counter is NOT here: it lives in the hero
                  block, paste 3.) Part 3: the growing hero
                  photo, the pinned photo story, fade-ins, dragging the cards, and the header tucking away.
  WHERE TO PASTE: Pages > Custom Code > Code Injection > FOOTER, then Save. Replace the whole field.
                  Once for the whole site. Do not leave an older footer above this paste.
  NEEDS:          A Core, Plus or Advanced plan. Paste 1 (header) for the brand colours and fonts.
  PLACEHOLDERS:   Follow links and the contact email are [TBD]. Starting number: PLACEHOLDER_START_COUNT in Part 1.
  GENERATED:      by build.py from assets/joy.js, assets/home.js, assets/scroll-story.js and assets/give-pill.js.
                  Change the sources and run `python3 build.py`; edits made here are overwritten.
-->
<style>
:root { --yellow: #fdcd17; --ink: #231f20; }
__FOOTERCSS__
</style>
<div class="sj-home">
__FOOTERHTML__
</div>
"""

HOME_BLOCK = """<!--
  PASTE __N__ OF 6:   __TITLE__
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


LINK_TOKENS = [
    ("help.html", "{{LINK_HELP}}"),
    ("contact.html", "{{LINK_CONTACT}}"),
    ("mission.html", "{{LINK_MISSION}}"),
    ("story.html", "{{LINK_STORY}}"),
    ("events.html", "{{LINK_EVENTS}}"),
]


def to_placeholders(html):
    for key, name in HOME_IMAGES.items():
        html = html.replace("assets/img/" + name, "{{IMG_%s}}" % key)
    for href, token in LINK_TOKENS:
        html = html.replace('href="' + href + '"', 'href="' + token + '"')
    # home-page/image-urls.json holds the real Squarespace addresses; any key it lacks stays a placeholder
    urls_file = HOME_DIR / "image-urls.json"
    if urls_file.exists():
        for key, url in json.loads(urls_file.read_text()).items():
            html = html.replace("{{%s}}" % key, url)
    return html


def fill_urls(text):
    urls_file = HOME_DIR / "image-urls.json"
    if urls_file.exists():
        for key, url in json.loads(urls_file.read_text()).items():
            text = text.replace("{{%s}}" % key, url)
    return text


def build_home_page():
    HOME_DIR.mkdir(exist_ok=True)
    header = (HOME_HEADER.replace("__SQS__", SQS_OVERRIDES)
              .replace("__HEADERCSS__", fill_urls(SITE_HEADER_CSS))
              .replace("__SURPRISE__", snippet_css("surprise"))
              .replace("__FOOTERCSS__", HOME_FOOTER_CSS)
              .replace("__WAVE__", ".sj-home .wave { display: block; width: 100%; height: 44px; margin: -1px 0; color: var(--yellow); fill: currentColor; }\n.sj-home .wave.flip { transform: scaleY(-1); }")
              .replace("__HOMECSS__", (OUT / "assets" / "home.css").read_text().strip())
              .replace("__GIVEPILLCSS__", (OUT / "assets" / "give-pill.css").read_text().strip()))
    (HOME_DIR / "1-header-injection.html").write_text(header)

    parts = [(OUT / "assets" / n).read_text() for n in ("joy.js", "home.js", "scroll-story.js", "give-pill.js")]
    footer_html = to_placeholders(HOME_FOOTER_HTML.strip("\n"))
    footer = (HOME_FOOTER.replace("__FOOTERCSS__", HOME_FOOTER_CSS).replace("__FOOTERHTML__", footer_html)
              + (GB_LIBRARY + "\n" if GB_LIBRARY else "") + "<script>\n"
              + "/* ===== PART 1: logic (assets/joy.js) ===== */\n" + parts[0] + "\n"
              + "/* ===== PART 2: Surprise me and I did it (assets/home.js) ===== */\n" + parts[1] + "\n"
              + "/* ===== PART 3: scroll story, cards, header (assets/scroll-story.js) ===== */\n" + parts[2] + "\n"
              + "/* ===== PART 4: floating Give pill on every page (assets/give-pill.js) ===== */\n" + parts[3]
              + "</script>\n")
    (HOME_DIR / "2-footer-injection.html").write_text(footer)

    # Same script as paste 2, for a Code Block on the home page. Use it when the site's Footer injection
    # belongs to someone else. The guard stops it from running twice if Squarespace re-draws the block.
    page_script = ("<!--\n"
                   "  PASTE 7:        Page script (alternative to paste 2)\n"
                   "  WHAT IT IS:     The same script as paste 2 (counter, ideas, I did it, scroll story, cards, floating Give pill).\n"
                   "  WHERE TO PASTE: A Code Block (mode HTML) in the last section of the Home page, under block 5.\n"
                   "                  Use this INSTEAD of paste 2 when the Footer injection is not yours to edit.\n"
                   "  GENERATED:      by build.py from assets/*.js. Do not hand-edit.\n"
                   "-->\n" + (GB_LIBRARY + "\n" if GB_LIBRARY else "") + "<script>\nif (!window.__sjHome) { window.__sjHome = true;\n"
                   + "/* ===== PART 1: logic (assets/joy.js) ===== */\n" + parts[0] + "\n"
                   + "/* ===== PART 2: Surprise me and I did it (assets/home.js) ===== */\n" + parts[1] + "\n"
                   + "/* ===== PART 3: scroll story, cards, header (assets/scroll-story.js) ===== */\n" + parts[2] + "\n"
                   + "/* ===== PART 4: floating Give pill (assets/give-pill.js) ===== */\n" + parts[3]
                   + "\n}\n</script>\n")
    (HOME_DIR / "7-page-script-block.html").write_text(page_script)

    blocks = [
        (3, "3-hero-block.html", "Hero: headline and growing photo with the heart",
         "Giant headline, the photo that grows as you scroll, and the tap-the-heart pill on top of it.",
         "A Code Block (mode HTML) in the FIRST section of the Home page. It carries its own heart and counter script, so nothing in the Footer injection is needed for the counter.",
         "{{IMG_SOCKS_CIRCLE}}, {{IMG_HEART}}", HOME_HERO + RIPPLES_SCRIPT),
        (4, "4-story-block.html", "Pinned photo story",
         "Three photos and three short lines that change as you scroll while the stage stays pinned.",
         "A Code Block (mode HTML) in the SECOND section.",
         "{{IMG_XAVIER}}, {{IMG_STORY_CIRCLE}}, {{IMG_SOCK_PILE}}", HOME_STORY),
        (5, "5-your-turn-block.html", "Yellow wave and the Your turn cards",
         "The wave, the yellow band, the Your turn headline and the swipeable photo cards, ending with Surprise me.",
         "A Code Block (mode HTML) in the THIRD (last) section.",
         "{{IMG_FAMILY}}, {{IMG_CARD_SOCKS}}, {{IMG_CARD_SHARE}}, {{IMG_CARD_SUPPORT}}, {{IMG_HEART}}, {{LINK_EVENTS}}, {{LINK_HELP}}",
         WAVE_UP + "\n" + HOME_TURN),
        (6, "6-footer-block.html", "Dark footer with links and sign-up",
         "The charcoal footer: logo, tagline, links, follow and the email sign-up box.",
         "Do not paste this block. Paste 2 already includes this footer on every page. Pasting it here as well shows two.",
         "{{IMG_HEART}}, {{LINK_MISSION}}, {{LINK_STORY}}, {{LINK_EVENTS}}, {{LINK_HELP}}, {{LINK_CONTACT}}", HOME_FOOTER_HTML),
    ]
    urls_file = HOME_DIR / "image-urls.json"
    known = json.loads(urls_file.read_text()) if urls_file.exists() else {}
    for n, fname, title, what, where, ph, html in blocks:
        ph = ", ".join(p for p in ph.split(", ") if p.strip("{}") not in known) or "none (addresses come from home-page/image-urls.json)"
        text = (HOME_BLOCK.replace("__N__", str(n)).replace("__TITLE__", title).replace("__WHAT__", what)
                .replace("__WHERE__", where).replace("__PLACEHOLDERS__", ph)
                .replace("__HTML__", to_placeholders(html.strip("\n"))))
        (HOME_DIR / fname).write_text(text)
    print("wrote home-page/ (6 files)")


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
        give=GIVE_URL,
        preview_note=PREVIEW_NOTE,
    )
    (OUT / filename).write_text(html)
    print("wrote", filename)

def build_contact_block():
    """Paste-ready Code Block. The photo is inlined so the block does not depend on a repo path."""
    photo = base64.b64encode((OUT / "assets" / "img" / "contact-socks.jpg").read_bytes()).decode()
    css = (OUT / "assets" / "contact.css").read_text().strip()
    html = CONTACT_SECTION.format(
        img="data:image/jpeg;base64," + photo,
        email=CONTACT_EMAIL,
        instagram=CONTACT_INSTAGRAM,
        facebook=CONTACT_FACEBOOK,
    ).strip()
    block = f"""<!--
  PASTE 1 of 1:  Contact page
  WHAT IT DOES:  A note from Marisa, the sock photo, and links for email, Instagram, and Facebook.
  WHERE TO PASTE: The only Code Block (mode HTML) on the Contact page (/contact).
  EDIT:          The words and links live in build.py (CONTACT_EMAIL and the section). Rebuild, then paste this file again.
-->
<style>
{css}
</style>
{html}
"""
    folder = OUT / "contact-page"
    folder.mkdir(exist_ok=True)
    (folder / "1-contact-block.html").write_text(block)
    print("wrote contact-page/1-contact-block.html")


build_snippets()
build_home_page()
build_contact_block()
