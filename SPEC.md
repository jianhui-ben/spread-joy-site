# Spread Joy Collective: Site-Wide Spec

Rules for **every page** of the Squarespace 7.1 site. Each page owner decides that page's layout, copy and ideas **inside** these rules; page-specific detail goes in that page's own doc. If a task conflicts with this file, say so and ask. **MUST** and **MUST NOT** are hard rules. Everything else is guidance.

## 1. Project

- **Who:** Spread Joy Collective, a nonprofit supporting individuals with disabilities and their families through community, opportunity and practical help. Tagline: *Together, we create the magic.*
- **North star:** a visitor leaves thinking *"I could be part of this. Something I do could start the next ripple."*
- **Platform:** Squarespace 7.1, **Givebutter** for all donations. Output is design, copy and **Custom Code Blocks** (HTML/CSS/vanilla JS). No server code.
- **Audience:** donors, volunteers, local families, partners. Many are on phones.
- **Feel:** warm, joyful, effortless. One idea per section; a first-time visitor finds the next step in five seconds. Joy leads, need is context.

## 2. Styling: Squarespace is the source of truth

Site Styles define color, fonts, buttons, spacing, header, footer and section themes. Code **inherits** them; it does not redefine them.

- **MUST** use Squarespace palette variables for color, written `hsla(var(--accent-hsl), 1)` (the variables hold HSL without the wrapper). **MUST** use `font-family: inherit`.
- **MUST NOT** hard-code hex colors or font names, or load extra fonts, scripts, trackers or libraries.
- **MUST NOT** restyle or rebuild the header, nav, footer, Give button or forms from a Code Block. Configure them in Site Styles or native blocks. Small site-wide additions go in the global **Custom CSS** panel, never inside individual blocks.
- **Brand character** (set in Squarespace, not code): warm brand yellow, dark text on yellow, white or yellow text on black, the hand-drawn **yellow heart** as the signature motif (inline SVG using the accent variable, or the uploaded heart image), real photos of real moments.

Variables read from the trial site on 2026-10-17 (live site and dark section themes not checked):

| Purpose | Variable | Value |
|---|---|---|
| Brand yellow | `--accent-hsl` | `47.48,98.29%,54.12%` (= `#FDCD17`) |
| Black | `--black-hsl` | `0,0%,0%` (pure black; the logo's charcoal `#231F20` is **not** in the palette) |
| White | `--white-hsl` | `0,0%,100%` |
| Light / mid grey | `--lightAccent-hsl` / `--darkAccent-hsl` | `270,8%,90.2%` / `0,0%,47.45%` |
| Section heading color | `--headingLargeColor` | `hsla(0,0%,0%,1)` in the light theme |

### Type, buttons and spacing (brand look, for every page)

Set these in Squarespace's Site Styles where possible. Code should match them, not replace them.

- **Body and headings:** League Spartan, weight 400 for body, 700 for big headlines, tight letter-spacing (-0.02 to -0.03em) on headlines. Set League Spartan in Site Styles (see §7 on the font decision).
- **Accent words:** Oooh Baby, script, about 1.4rem beside the body text. Use one accent per section at most.
- **Headlines:** one big line per section (roughly 3rem to 6rem on desktop), line-height about 1.05. Body text about 1.05rem to 1.15rem, line-height 1.5 to 1.6, max width about 40em.
- **Muted text:** `#6B6560` for secondary copy (the palette has no matching slot yet).
- **Buttons:** pill shape (fully rounded), at least 44px tall, 12px by 26px padding. Three styles only:
  - **Primary:** brand yellow background, charcoal text (for example "Give").
  - **Dark:** charcoal background, white text (on yellow sections).
  - **Outline:** white background, charcoal border (secondary actions).
- **Dividers:** the yellow wave (see the home page) is the only divider. Do not add other decorative lines.
- **Motif:** the yellow heart is the signature mark. Use the uploaded heart image, not new icons.
- **Spacing:** generous. Sections use at least 80px top and bottom padding on desktop and 56px on phone. Maximum one idea per section.
- **Photos:** full-bleed or rounded corners (about 24px to 32px). No frames, no drop shadows except a soft one on floating elements.

Reference build: `index.html` and `assets/styles.css` (local preview), and the home-page paste files. When in doubt, match the home page.

## 3. Shared structure (native Squarespace, not rebuilt in code)

- **Header:** fixed to the top on desktop and phone. **Nav order:** Home · Our Mission · Our Story · Events · How Can We Help · Contact · **Give** (button). At most 8 top-level items.
- **Give:** the one label for donating, everywhere, always linking to the Givebutter campaign. **MUST NOT** use "Donate", "Contribute" or "Support" for that action. Every page offers a natural, unpushy place to Give.
- **Footer:** logo, Give link, Facebook, Instagram, X, contact email, newsletter signup.
- **Every page:** one H1, one clear purpose, one primary next step. Unfinished pages stay hidden from the nav (no "coming soon" pages).

## 4. Code Block rules

Each Code Block **MUST**:

- be self-contained (HTML + CSS + vanilla JS), scoped under the `.sjc-` class prefix, and start with a short comment saying what it does and how to edit its content;
- work inside a Squarespace section on desktop and phone, in light and dark themes;
- keep content that changes over time (stories, events, numbers, prompts) in one simple list the NGO can edit without touching code;
- never target Squarespace's internal classes or IDs, never store visitor data in the page, URL or browser (use Squarespace forms or Givebutter), and never collect payments (link or embed Givebutter only);
- hold visitor-submitted content for NGO review before it appears.

**Squarespace gotchas** (learned building the home page):

- Squarespace **re-draws Code Block HTML after load**. Do not keep element references; look elements up when the event happens (listen on `document`).
- Test in Squarespace **Preview** or the saved page, not the editing view. Safe Mode turns custom code off, so use a private window to test.
- Use `getBoundingClientRect().top + scrollY`, not `offsetTop`.
- Squarespace sets its own heading/paragraph/button colour and font. Inside your container set the colour of text that must differ (for example white over a photo) with enough specificity.
- A forced-dark-mode browser can turn a white page black. Check in one.
- `position: sticky` breaks under any parent with `overflow: hidden` or `auto`; Squarespace's section grid clips overflow by default.
- Images must be uploaded to Squarespace; a Code Block cannot read repo files. JavaScript needs a Core, Plus or Advanced plan.
- If code is unavailable or unsafe, use native blocks and Givebutter's embeds with the same brand and tone.

## 5. Quality checks (all pages)

- Text contrast WCAG AA (4.5:1 body, 3:1 large text and UI), in light and dark sections.
- Works by keyboard and touch; tap targets at least 44×44px; visible focus states.
- Alt text on every image; captions on every video.
- Animation respects `prefers-reduced-motion` and has a calm fallback. No autoplay with sound, no auto-advancing carousels, no load-time popups.
- Works at 360px wide with vertical scrolling only; compressed images, lazy-loaded below the fold.
- Every interactive element has an obvious label, a clear result and a way back.

## 6. Content, voice and dignity

- **MUST NOT** invent facts: donation totals, impact numbers, testimonials, donor names, dates, venues, prices. Use a visible placeholder such as `[TBD: event date]` and list it for the founder.
- **MUST NOT** use identifiable photos of people, especially minors, without recorded consent. Use approved images only and flag any without consent. Keep the founder family's story, photos and video within what they approved; ask before any new use.
- **Voice:** warm, hopeful, specific; short sentences, plain words, grade 6 to 8, "you" and "we". Invite once, thank always. **MUST NOT** use guilt, countdown pressure or "only X left" urgency.
- **Disability language:** people with disabilities are neighbors, friends, teammates and contributors, never objects of pity. Use *individuals with disabilities*, *people with Down syndrome*, *families*; name people when they and their families choose. Frame outcomes as belonging, connection, inclusion and opportunity. Pair a person's image with their own words or a family-approved caption. Avoid *suffering from*, *confined to*, *brave* and *inspirational* for ordinary activities.
- Founder-written copy lives in `/content` or the work plan; code reads from it rather than retyping it.

## 7. Undecided: ask, don't assume

Use a visible placeholder and list each in your response.

- Live-site brand yellow: `--accent-hsl` on the trial site; owner to confirm on the live site.
- Dark color for footers and dark sections: pure black (`--black-hsl`), or add the logo's charcoal `#231F20` to the palette?
- Fonts: the live site's own font is Poppins; the brand guide and the local preview use League Spartan (text) and Oooh Baby (accent). Working default in §2 is League Spartan set in Site Styles. Owner to confirm.
- Whether stock photography is used, and where videos are hosted (Squarespace, YouTube or Vimeo).
- Final nav order if a page is added or merged.

## 8. Done means

Everything in §3 to §6 that applies is true. In your final message list what you verified and how, any §7 placeholders you used, and anything you could not verify. If something is unverified, say so instead of calling the work complete.
