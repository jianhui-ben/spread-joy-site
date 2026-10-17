"""Builds the static HTML mock pages. Run: python3 build.py

Edit page content below, rebuild, and open index.html in a browser.
Links marked href="#" are placeholders: see README.md for the list to fill in.
"""
from pathlib import Path

OUT = Path(__file__).parent

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

PAGES["index.html"] = dict(
    title="Home",
    description="Spread Joy Collective: replace with a one-sentence description for search results.",
    body="""
<section class="hero">
  <div class="wrap">
    <div>
      <div class="eyebrow">Spread Joy Collective</div>
      <h1>Small acts.<br>Big impact.<br>Spread joy.</h1>
      <p class="lead">We strengthen and support families of individuals with disabilities by building community, creating opportunities, and providing meaningful assistance wherever it is needed most.</p>
      <div class="cta-row">
        <a class="btn btn-yellow" href="#">Donate</a>
        <a class="btn btn-outline" href="help.html">Get involved</a>
      </div>
    </div>
    <div class="photo-frame">
      <img src="assets/img/socks-circle.jpg" alt="Xavier smiling in a circle of friends in colorful socks">
    </div>
  </div>
</section>

<section class="block alt">
  <div class="wrap">
    <h2>Ways to join in</h2>
    <p class="section-lead">Three quick paths for new visitors.</p>
    <div class="cards">
      <div class="card"><h3>Our Mission</h3><p>What we believe and who we serve.</p><a href="mission.html">Read our mission &rarr;</a></div>
      <div class="card"><h3>Upcoming Events</h3><p>Come celebrate with us.</p><a href="events.html">See events &rarr;</a></div>
      <div class="card"><h3>How Can We Help</h3><p>Volunteer, partner, or give.</p><a href="help.html">Find your way in &rarr;</a></div>
    </div>
  </div>
</section>

<section class="block">
  <div class="wrap">
    <h2>Next event</h2>
    <div class="event">
      <div class="date">DEC<br>14</div>
      <div class="info"><strong>Event name placeholder</strong><span>Location &middot; Time</span></div>
      <a class="btn btn-outline" href="#">Register</a>
    </div>
  </div>
</section>
""" + CTA,
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
        footer_links=footer_links(),
    )
    (OUT / filename).write_text(html)
    print("wrote", filename)
