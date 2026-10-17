# Spread Joy Collective: "Joy Ripple" homepage

Date: 2026-10-16. Status: draft for approval.

## Intent and why

Spread Joy Collective is a nonprofit that supports families of individuals with disabilities ("Small acts. Big impact. Spread joy."). The live Squarespace home page is warm and clear but flat: a visitor reads it and nothing moves or responds. The owner wants a homepage that feels modern (Apple-like), warm and connected, with fewer words and more interaction. The vibe matters most. A visitor should leave thinking "I could be part of this. Something I do could start the next ripple."

The emotional core is the yellow heart and the idea of a ripple of joy that spreads. The page makes the visitor start a ripple first, then walks them through the story, then offers ways to join.

## Deliverables

1. A working prototype in this repo (plain HTML/CSS/JS, extending the existing static mock built by `build.py`) that can be clicked through in a browser.
2. The exact Squarespace code snippets (Code Block and Code Injection) and step-by-step setup instructions to recreate the page in the live Squarespace 7.1 site.

The prototype is the design reference. Squarespace is where it ships. Nothing is deployed from this repo.

## Goals

- A one-scroll homepage with five moments (below), alternating white and yellow bands joined by a wave.
- A tappable heart that sends a ripple across the screen, with a "ripples of joy so far" counter.
- Photos fill the width, one short line each, content fades in on scroll.
- A "Your turn" ending that routes visitors to ways to take part.
- Everything buildable on Squarespace 7.1 with native features plus small custom code.

## Non-goals (for this version)

- A real counter. The number is made up for now and sits in one clearly labeled place so it can be wired to real data later.
- Visitors submitting their own hearts or stories, a Wall of Joy, testimonials, a video welcome, or a "Big Dreams" page. These come from the owner's brainstorm doc and are later work.
- Rebuilding the other pages (Mission, Story, Events, Help, Contact). Only the home page is designed here.
- New logo, fonts or photos. The brand assets stay as they are.

## Anti-goals (a failure even if it technically works)

- Reads as a playful game or toy instead of a heartfelt cause. Motion should feel gentle, not arcade.
- Slow, janky or broken on phones. Most visitors from Instagram and events arrive on a phone.
- Heavy text. Each screen carries about one short line.
- Motion with no way out: respect reduced-motion settings.
- Custom code that breaks the Squarespace page or the editor.

## Design (decisions made with the owner)

**Look.** White page background, dark text (#231f20), brand yellow #FDCD17 as the highlight and in full-width bands. Bands alternate white and yellow with a soft wave divider (the live site already uses a yellow wave). On yellow bands the hearts are white, as on the live site. Photos use the live site's offset-block treatment. Fonts: League Spartan for text, Oooh Baby for the accent tagline. Logo and photos unchanged. The header stays fixed at the top while scrolling (a stated owner preference).

**Five moments, in order.**

1. Tap the heart. One large yellow heart on white. Tapping sends rings across the screen. A line reads "N ripples of joy so far".
2. "It started with one kid." Full-width Xavier photo (`xavier-portrait.jpg`).
3. "Then a whole circle showed up." Sock-circle photo (`socks-circle.jpg`).
4. "578 socks. One kindness at a time." Sock-pile photo (`sock-pile.jpg`).
5. "Your turn." Four choices: I have time, I want to give, I have something to share, My family could use support, plus a "Surprise me" heart that reveals one small kindness idea (from the owner's list, e.g. "Tell someone you're glad they're here").

Small hearts drift between sections so the ripple feels like one thread through the page. Mockups for these are in `.superpowers/brainstorm/*/content/yellow-bands.html`.

## Constraints

- Platform: Squarespace 7.1 (Fluid Engine). The live site must be on a Core, Plus or Advanced plan for JavaScript in Code Blocks and Code Injection. The current account is a free trial with 14 days left; verified on 2026-10-16 that JavaScript injected on the trial runs on site pages despite the "Upgrade" lock on the Code Injection panel. The live site still needs a paid plan after the trial.
- Native first: use Squarespace section backgrounds, section dividers, site-wide scroll animations and Fluid Engine layout wherever they can do the job. Use custom code only for the tap-to-ripple heart and "Surprise me".
- Code Blocks cap at 400 KB, only run JavaScript in HTML mode inside script tags, and may not render on index pages or with Ajax loading on. Squarespace support will not troubleshoot custom code.
- No visitor-writable database exists in Squarespace, which is why the counter is fake for now.
- Squarespace help says Custom CSS is meant for fonts, colors and backgrounds. Animation CSS works but is unsupported.
- Brand: logo font is Brandon Grotesque (Adobe, not licensed here). Wordmark text uses League Spartan with wide tracking until it is licensed.
- Uploaded photos are web-sized copies in `assets/img/`. Originals stay in `assets/`.

## Left to the builder

- Exact wave shape, animation timing and easing, ripple look, drift pattern of the small hearts.
- Whether the wave dividers are Squarespace's native dividers or a custom shape.
- Breakpoints and the mobile layout of each moment.
- Final short copy for the "Surprise me" kindness ideas, drawing from the owner's brainstorm list.
- Where each snippet is injected (Code Block vs Header/Footer injection), as long as it degrades gracefully if the code does not run.
- Whether the "Your turn" choices link to existing pages (Help, Contact, Donate) or open small panels.

## Calls made by the designer (not yet confirmed by the owner)

- **Phones first.** Tap-to-ripple must work smoothly on a mid-range phone. Build it with lightweight CSS/JS animation (no heavy full-screen canvas), test at phone width first, and reduce effects (fewer drifting hearts) on small screens. Honor `prefers-reduced-motion` by replacing motion with a simple fade.
- **Counter behavior.** The page loads with one fixed made-up number. Each tap adds 1 for the current visit only. Nothing is stored, and a reload resets it. The starting number lives in one named constant with a comment saying it is a placeholder, so it can be swapped for real data later.
- **"Your turn" destinations.** Link, don't build panels: I have time and I have something to share go to How Can We Help, I want to give goes to the Donate page, My family could use support goes to Contact. Panels are later work.
- **Staging.** Build the new home as a Not Linked page on the live Squarespace site, review it there, then swap it in as the Home page. The old home stays so it can be rolled back. A paid plan must be active before launch, since trial code can stop running when the trial ends.
- **Without JavaScript.** The page must stand on its own: static heart, the counter line shown as plain text, and the "Surprise me" button hidden. Nothing should look broken.
- **"Surprise me" content.** About ten short kindness ideas taken from the owner's brainstorm list, shuffled so the same one never shows twice in a row. The list lives in one place so the owner can edit it.

## Open items for the owner (not blocking the prototype)

- Donate button placement beyond the header.
- Real links for Donate, social accounts, newsletter and contact details (listed in `README.md`).
- Paid Squarespace plan choice before launch.
