# Spread Joy Collective: Site-Wide Spec

Shared style and guardrails for **every page** of this website. Read the whole file before designing or coding anything. **MUST** and **MUST NOT** are hard requirements. If a task conflicts with this file, say so and ask; do not quietly choose.

**Scope:** this file sets what is true on *all* pages. Each page owner decides that page's layout, content, and creative ideas, **inside** these rules. Page-specific detail belongs in that page's own doc, never here.

---

## 1. Project snapshot

- **Who:** Spread Joy Collective, a nonprofit supporting individuals with disabilities and their families by building community, creating opportunities, and providing meaningful assistance.
- **Tagline:** *Together, we create the magic.*
- **North star:** a visitor leaves thinking *"I could be part of this. Something I do could start the next ripple."*
- **Platform:** Squarespace (7.1) site, GoDaddy domain, **Givebutter** for all donations.
- **What gets produced:** design decisions, copy, and **Custom Code Blocks** (HTML / CSS / JavaScript) placed inside Squarespace pages. No server code.
- **Audience:** donors, volunteers, local families, community partners; many on phones.

## 2. Feel: *warm, joyful, effortless*

Every page passes three checks:

1. **Warm:** does it feel welcoming and uplifting?
2. **Simple:** is there one clear idea per section?
3. **Findable:** can a first-time visitor find their next step in five seconds?

Joy leads; need is context. Visitors should feel **connected** and able to **contribute** something, even something small.

## 3. Styling source of truth: Squarespace

**Squarespace already defines the site's look** (Site Styles: color palette, fonts, buttons, spacing, header, footer, section color themes). Custom code **inherits** it; it never redefines it.

- **Colors:** use Squarespace's palette variables on `:root`, which hold HSL values without the `hsl()` wrapper, so wrap them: `hsla(var(--accent-hsl), 1)`. Palette variables: `--white-hsl`, `--lightAccent-hsl`, `--accent-hsl`, `--darkAccent-hsl`, `--black-hsl`.
- **Section themes:** where a snippet sits inside a themed section, use the section's variables (for example `--headingLargeColor`) so it follows light or dark sections automatically.
- **Fonts:** `font-family: inherit` from the surrounding block. Sizes and weights follow the site's heading and paragraph styles.
- **Verify before use:** inspect the live site's `:root` and confirm each variable exists and holds the expected color. Add only the variables actually used to the list below.
- **Site-wide style changes** go in Squarespace **Site Styles** (or the global **Custom CSS** panel for small additions), never copied into individual code blocks.

**Brand character to preserve** (set in Squarespace, not in code): warm brand yellow, near-black dark sections, the hand-drawn **yellow heart** from the logo as the signature motif, wide-tracked wordmark, real photos of real moments. Dark text on yellow; white or yellow text on black.

**The heart motif in code:** inline SVG filled with the palette's accent variable (or the heart image uploaded to Squarespace). Reuse it as the visual thread across pages (accents, icons, interactions, dividers).

## 4. Shared structure (configured in Squarespace, not rebuilt in code)

- **Header:** fixed to the top while scrolling, on desktop and phone. Nav link text is dark on the yellow header.
- **Nav order:** Home · Our Mission · Our Story · Events · Get Involved · How Can We Help · Contact · **Give** (button). No more than 8 top-level items; new ideas live inside existing pages.
- **Give:** the label is **"Give"** everywhere and every Give button links to the Givebutter campaign. Give is in the header on every page, and each page offers a natural, unpushy place to Give.
- **Footer:** logo, Give link, Facebook, Instagram, X, contact email, newsletter signup, on every page.
- **Every page:** one H1, a clear purpose, one primary next step. Complete content before a page appears in the nav; unfinished pages stay hidden.

## 5. MUST HAVE (all pages)

Each item is checkable.

- [ ] Colors and fonts come from Squarespace variables and inheritance (§3).
- [ ] Header, nav, Give button, and footer follow §4 using native Squarespace blocks and settings.
- [ ] Text contrast meets WCAG AA (4.5:1 body, 3:1 large text and UI), in both light and dark sections.
- [ ] Works by keyboard and touch; tap targets ≥ 44×44px; visible focus states.
- [ ] Alt text on every image; captions or subtitles on every video.
- [ ] Animation respects `prefers-reduced-motion` and offers a calm fallback.
- [ ] Works at 360px wide with vertical scrolling only.
- [ ] Voice follows §7; language follows §7.
- [ ] Any interactive element has an obvious label, a clear result, and a way back.
- [ ] Content that changes over time (stories, events, numbers, prompts) lives in a simple list the NGO can edit without touching code.
- [ ] Visitor-submitted content waits for NGO review before it appears.
- [ ] Each Code Block is self-contained (HTML + CSS + vanilla JS), scoped under the `.sjc-` class prefix, and starts with a short comment saying what it does and how the NGO edits its content.
- [ ] Each Code Block works inside a Squarespace section on desktop and phone, in light and dark themes.

## 6. MUST NOT HAVE

Each rule is paired with what to do instead.

| MUST NOT | Do this instead |
|---|---|
| Hard-coded hex colors or font names in code | Squarespace palette variables and `font-family: inherit` |
| Restyling or rebuilding the header, nav, footer, Give button, or forms from a Code Block | Configure them in Site Styles / native blocks |
| Site-wide CSS pasted into individual code blocks | Site Styles or the global Custom CSS panel |
| CSS that targets Squarespace's internal classes or IDs | Your own `.sjc-` classes inside your own container |
| Black text on dark backgrounds, or white text on the yellow header | Dark on yellow; white or yellow on black |
| Empty or "coming soon" pages reachable from the nav | Hide the page until it has real content |
| Invented facts: donation totals, impact numbers, testimonials, donor names, dates, venues, prices | A visible placeholder like `[TBD: event date]`, listed for the founder |
| Identifiable photos of people, especially minors, without recorded consent | Approved images only; flag any without consent |
| Autoplay with sound, auto-advancing carousels, load-time popups | Let the visitor choose to play or advance |
| Guilt copy, countdown pressure, "only X left!" urgency | Gratitude and invitation (§7) |
| Third-party scripts, trackers, fonts, or libraries beyond what Squarespace loads | Vanilla JS and inherited fonts |
| Visitor personal data stored in the page, URL, or browser | Squarespace forms or Givebutter |
| Custom payment forms or card collection | Link or embed Givebutter only |
| Several labels for one action ("Donate", "Contribute", "Support") | One label: **Give** |

## 7. Voice, tone, and dignity

**Voice:** warm, hopeful, specific. Short sentences, plain words, grade 6–8 reading level, "you" and "we." Invite once, clearly; thank always. Celebrate; do not plead.

**Disability language (all copy, imagery, and design):** show people with disabilities as **neighbors, friends, teammates, and contributors**, never as objects of pity.

- Use *individuals with disabilities*, *people with Down syndrome*, *families*. Name people when they and their families choose to be named.
- Frame outcomes as **belonging, connection, inclusion, opportunity**.
- Pair a person's image with their own words or a family-approved caption.
- Avoid *suffering from*, *confined to*, *brave*, and *inspirational* as a label for ordinary activities.
- Keep the founder family's story, photos, and video **within what they approved**; ask before any new use.

## 8. Technical guardrails

- **Content source of truth:** founder-written copy lives in `/content` (or the work plan). Code reads from it; it does not retype it.
- **Performance:** compressed images, lazy-loaded below the fold, light enough for a phone connection.
- **SEO basics:** page title, description, one H1, descriptive link text.
- **Browsers:** current Safari, Chrome, Firefox, Edge; iOS Safari and Android Chrome.
- **Fallback when code is unavailable or unsafe:** use native Squarespace blocks (galleries, buttons, forms) and Givebutter's own embeds, keeping the same brand and tone.

## 9. Squarespace variables in use (fill in after inspecting the live site)

| Purpose | Variable | Verified |
|---|---|---|
| Brand yellow | `--accent-hsl` (confirm) | [ ] |
| Dark background | `--black-hsl` (confirm) | [ ] |
| Light text | `--white-hsl` (confirm) | [ ] |
| Heading color in a section | `--headingLargeColor` (confirm) | [ ] |

## 10. Undecided site-wide: ask, don't assume

Use a visible placeholder and list each in your response.

- Which Squarespace palette slot holds the brand yellow
- Whether stock photography is used
- Where videos are hosted (Squarespace, YouTube, or Vimeo)
- Final nav order if a page is added or merged

## 11. Definition of done

Work is done when **every** box in §5 that applies is checked and **no row** in §6 is violated. In your final message list: (1) which §5 items you verified and how, (2) any §10 placeholders you used, (3) anything you could not verify. If any item is unverified, say so plainly instead of calling the work complete.
