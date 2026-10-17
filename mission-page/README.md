# Our Mission

Local preview: `mission.html`. Copy is the mission paragraph from the live **Home (old)** page (`/home`), checked in the Squarespace editor on 2026-10-17.

## What Squarespace has now

Our Mission is not its own page. In Main Navigation it is a **link** to `/home#ourmission` on Home (old). There is no `/our-mission` page (that address is a 404).

## How to make the page

1. Add a blank page. Navigation title **Our Mission**. Suggested URL slug `our-mission`.
2. One text section. Paste the copy below. One heading: Our Mission.
3. Add a button labeled **Give** linking to `https://givebutter.com/SpreadJoyCollective`.
4. Add a text link to Our Story.
5. Replace the Main Navigation link item with this page.
6. In `home-page/image-urls.json`, `LINK_MISSION` is already `/our-mission`. Rebuild with `python3 build.py` and re-paste home block 6 if the footer should point here.

## Copy

Spread Joy Collective supports individuals with disabilities and their families by building community, creating opportunities, and providing meaningful assistance. Rooted in support, connection, and joy, we believe everyone deserves to feel seen, valued, included, and supported.

## Not on this page

No extra pillars, logo explanation, or photos were on the live mission section, so none were added.
