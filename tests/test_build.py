import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSS = (ROOT / "assets" / "styles.css").read_text()
CSS_NO_COMMENTS = re.sub(r"/\*.*?\*/", "", CSS, flags=re.S)


def rule(selector):
    """Return the body of the first CSS rule whose selector list contains `selector`."""
    for m in re.finditer(r"([^{}]+)\{([^{}]*)\}", CSS_NO_COMMENTS):
        selectors = [s.strip() for s in m.group(1).split(",")]
        if selector in selectors:
            return m.group(2)
    return None


class ThemeTests(unittest.TestCase):
    def test_brand_tokens(self):
        self.assertIn("--yellow: #fdcd17;", CSS)
        self.assertIn("--ink: #231f20;", CSS)
        self.assertIn("--bg: #ffffff;", CSS)

    def test_body_is_white(self):
        self.assertIn("background: var(--bg)", rule("body"))

    def test_header_is_sticky(self):
        self.assertIn("position: sticky", rule(".site-header"))

    def test_shared_classes_exist(self):
        for sel in [".wave", ".wave.flip", ".pill", ".pill.outline"]:
            self.assertIsNotNone(rule(sel), f"missing CSS rule for {sel}")

    def test_reduced_motion_block_turns_animation_off(self):
        m = re.search(r"@media \(prefers-reduced-motion: reduce\)\s*\{(.*?)\n\}", CSS, re.S)
        self.assertIsNotNone(m, "no prefers-reduced-motion block")
        self.assertIn("animation: none", m.group(1))


def build_index():
    subprocess.run([sys.executable, str(ROOT / "build.py")], check=True, capture_output=True)
    return (ROOT / "index.html").read_text()


def text_of(fragment):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", fragment)).strip()


HOME_CSS = (ROOT / "assets" / "home.css").read_text() if (ROOT / "assets" / "home.css").exists() else ""
HOME_CSS_NO_COMMENTS = re.sub(r"/\*.*?\*/", "", HOME_CSS, flags=re.S)


def home_rule(selector):
    for m in re.finditer(r"([^{}]+)\{([^{}]*)\}", HOME_CSS_NO_COMMENTS):
        if selector in [x.strip() for x in m.group(1).split(",")]:
            return m.group(2)
    return None


class GivebutterLinkTests(unittest.TestCase):
    # Every Givebutter address on the site must be a confirmed campaign (a typo'd or unowned slug would send gifts elsewhere).
    VERIFIED = {"SpreadJoyCollective", "socks-that-spread-joy"}
    SCANNED = {".html", ".js", ".md", ".json"}

    @classmethod
    def setUpClass(cls):
        build_index()  # scan fresh output, not stale files

    def test_givebutter_links_use_only_verified_campaign_slugs(self):
        from urllib.parse import urlsplit
        files = [p for p in ROOT.rglob("*") if p.is_file() and p.suffix in self.SCANNED
                 and not {".git", "node_modules", "docs"} & set(p.parts)]
        found = set()
        for f in files:
            text = f.read_text(errors="ignore")
            # any URL token that mentions givebutter, whatever the spelling around it
            for tok in re.findall(r"[A-Za-z][A-Za-z0-9+.-]*://[^\s\"'<>)`,]*givebutter[^\s\"'<>)`,]*", text, re.I):
                parts = urlsplit(tok.rstrip("."))
                host = (parts.hostname or "").lower()
                if host == "widgets.givebutter.com":
                    continue  # the goal-bar library, not a donation page
                self.assertEqual(parts.scheme, "https", f"{f}: {tok}")
                self.assertEqual(host, "givebutter.com", f"{f}: {tok}")
                slug = parts.path.strip("/")
                self.assertIn(slug, self.VERIFIED, f"{f}: {tok}")
                self.assertEqual(parts.path.rstrip("/"), "/" + slug, f"{f}: {tok}")
                self.assertFalse(parts.query or parts.fragment, f"{f}: {tok}")
                found.add(slug)
        self.assertEqual(found, self.VERIFIED)

    def test_every_givebutter_link_opens_in_a_new_tab(self):
        files = [p for p in ROOT.rglob("*") if p.is_file() and p.suffix in {".html", ".js"}
                 and not {".git", "node_modules", "docs"} & set(p.parts)]
        seen = 0
        for f in files:
            for tag in re.findall(r"<a\b[^>]*givebutter\.com/[^>]*>", f.read_text(errors="ignore")):
                seen += 1
                self.assertIn('target="_blank"', tag, f"{f}: {tag}")
                self.assertIn("noopener", tag, f"{f}: {tag}")
        self.assertGreater(seen, 0)


class HomeTests(unittest.TestCase):
    def test_local_preview_has_the_heart_page_transition(self):
        html = build_index()
        self.assertIn('href="assets/heart-transition.css"', html)
        self.assertIn('src="assets/heart-transition.js"', html)
        # the effect attaches to .sj-home, which on Squarespace is the Code Block wrapper
        self.assertRegex(html, r'<div class="sj-home">\s*<section class="hero">')
        css = (ROOT / "assets" / "heart-transition.css").read_text()
        self.assertIn("url(\"img/heart.png\")", css)
        self.assertTrue((ROOT / "assets" / "img" / "heart.png").exists())

    def test_give_band_links_to_givebutter_and_never_shows_a_made_up_total(self):
        html = build_index()
        band = html[html.index('id="sj-give"'):]
        self.assertIn('id="sj-give-btn"', band)
        self.assertIn("https://givebutter.com/SpreadJoyCollective", band)
        self.assertIn(">Give", band)
        # without Givebutter ids the band holds no goal-bar tag and no dollar figure
        if "<givebutter-goal-bar" not in band:
            self.assertNotRegex(band, r"\$\d")

    def test_give_pill_address_matches_the_site_give_link(self):
        js = (ROOT / "assets" / "give-pill.js").read_text()
        self.assertIn("var GIVE_URL = 'https://givebutter.com/SpreadJoyCollective';", js)
        self.assertIn("https://givebutter.com/SpreadJoyCollective", build_index())

    def test_give_pill_is_on_every_page_and_in_the_squarespace_paste(self):
        build_index()
        for name in ("index", "mission", "contact"):
            html = (ROOT / f"{name}.html").read_text()
            self.assertIn("assets/give-pill.js", html)
            self.assertIn("assets/give-pill.css", html)
        self.assertIn("sj-give-pill", (ROOT / "home-page" / "1-header-injection.html").read_text())
        self.assertIn("initGive", (ROOT / "home-page" / "2-footer-injection.html").read_text())

    def test_give_pill_style_is_hidden_until_scrolled(self):
        css = (ROOT / "assets" / "give-pill.css").read_text()
        self.assertRegex(css, r"\.sj-give-pill\s*\{[^}]*opacity:\s*0")

    @classmethod
    def setUpClass(cls):
        cls.html = build_index()

    def test_hero_headline_and_subline(self):
        h1 = re.search(r'<section class="hero">\s*<h1[^>]*>(.*?)</h1>', self.html, re.S).group(1)
        self.assertEqual(text_of(h1), "Small acts. Big impact.")
        self.assertIn("Spread joy.", text_of(re.search(r'<p class="sub[^"]*"[^>]*>(.*?)</p>', self.html, re.S).group(1)))

    def test_story_lines_in_order(self):
        lines = [text_of(t) for t in re.findall(r'<h2 class="line"[^>]*>(.*?)</h2>', self.html, re.S)]
        self.assertEqual(lines, [
            "It started with one kid.",
            "Then a whole circle showed up.",
            "578 socks. One kindness at a time.",
        ])

    def test_story_photos_exist_and_have_alt_text(self):
        frames = re.findall(r'<div class="frame">(.*?)</div>', self.html, re.S)
        self.assertEqual(len(frames), 3)
        for frame, name in zip(frames, ["xavier-portrait.jpg", "story-circle.jpg", "sock-pile.jpg"]):
            self.assertIn(f'src="assets/img/{name}"', frame)
            self.assertTrue((ROOT / "assets" / "img" / name).exists(), name)
            alt = re.search(r'alt="([^"]*)"', frame)
            self.assertTrue(alt and alt.group(1).strip(), f"{name} has no alt text")

    def test_your_turn_cards_link_to_the_right_places(self):
        self.assertEqual(text_of(re.search(r'<section class="turn".*?<h2[^>]*>(.*?)</h2>', self.html, re.S).group(1)), "Your turn.")
        cards = re.findall(r'<a class="card"[^>]*href="([^"]*)"[^>]*>(.*?)</a>', self.html, re.S)
        links = {text_of(re.search(r"<h3>(.*?)</h3>", body, re.S).group(1)): href for href, body in cards}
        self.assertEqual(links, {
            "I have time": "events.html",
            "Socks That Spread Joy": "https://givebutter.com/socks-that-spread-joy",
            "I have something to share": "#share-a-hope",
            "I need support": "help.html",
        })

    def test_share_card_opens_the_hope_jar_overlay_without_a_second_button(self):
        self.assertIn("data-sjc-hope-widget", self.html)
        self.assertIn('a[href="#share-a-hope"]', self.html)
        # the widget's own launch button is hidden; the card is the way in
        self.assertIn('<div class="sjc-launch" hidden>', self.html)
        # the teammate's code is used as supplied
        src = (ROOT / "assets" / "hope-jar.html").read_text()
        self.assertIn("dialog", src)
        # Squarespace stops link clicks before they bubble up to the page, so the opener must listen
        # in the capture phase (a bubbling listener never fired on the trial site)
        self.assertRegex(src, r"closest\('a\[href=\"#share-a-hope\"\]'\);[\s\S]*?openModal\(link\);\s*\}, true\);")
        self.assertNotIn("localStorage", self.html)
        self.assertNotIn("fetch(", src)

    def test_hope_jar_has_no_consent_checkbox_and_starters_are_not_labelled_sample(self):
        src = (ROOT / "assets" / "hope-jar.html").read_text()
        self.assertNotIn('id="consent"', src)
        self.assertNotIn("#consent", src)
        self.assertNotIn("Sample message", src)
        self.assertNotIn("Interactive preview", src)
        self.assertNotIn("Preview only", src)
        self.assertNotIn("A shared hope", src)
        self.assertNotIn("preview", src.lower().replace("preview-", ""))
        self.assertNotIn("Local preview only", src)
        self.assertNotIn("sample:", src)
        # starter hopes live in one editable list, each with a text and a name (name may stay empty)
        self.assertRegex(src, r"const messages=\[\{text:'[^']+',name:'[^']*'\}")

    def test_jar_copy_says_joy_not_hope(self):
        src = (ROOT / "assets" / "hope-jar.html").read_text()
        self.assertIn("Share your joyful moment!", src)
        # ids, selectors and comments may keep "hope"; nothing a visitor sees or hears may
        visible = re.sub(r"<script>|//[^\n]*|data-sjc-hope-widget|#share-a-hope|[#'\"]hope(-form)?['\"\]]|id=\"hope(-form)?\"|for=\"hope\"", "", src)
        self.assertNotRegex(visible, r"(?i)hope")

    def test_every_link_card_has_a_photo_so_none_is_a_blank_white_block(self):
        cards = re.findall(r'<a class="card"[^>]*>(.*?)</a>', self.html, re.S)
        self.assertEqual(len(cards), 4)
        for body in cards:
            m = re.search(r'<img[^>]*src="(assets/img/[^"]+)"', body)
            self.assertIsNotNone(m, "card without a photo")
            self.assertTrue((ROOT / m.group(1)).exists(), m.group(1))

    def test_cards_row_has_no_extra_arrow_buttons(self):
        self.assertNotIn('cardsPrev', self.html)
        self.assertNotIn('cardsNext', self.html)

    def test_interaction_ids_exist_exactly_once(self):
        for ident in ["sj-heart", "sj-rings", "sj-count", "sj-surprise", "sj-idea", "sj-did-it", "sj-done"]:
            self.assertEqual(len(re.findall(r'id="%s"' % ident, self.html)), 1, ident)

    def test_heart_is_a_button_and_the_ticking_counter_is_not_a_live_region(self):
        self.assertRegex(self.html, r'<button[^>]*id="sj-heart"')
        # the number rises on its own every few seconds, so it must not be a live region (a screen reader would read it out each time)
        counter_p = re.search(r"<p[^>]*>\s*<b id=\"sj-count\"", self.html).group(0)
        self.assertNotIn("aria-live", counter_p)
        self.assertIn("1,284", re.search(r'id="sj-count"[^>]*>([^<]*)<', self.html).group(1))

    def test_script_only_elements_are_hidden_without_javascript(self):
        self.assertRegex(self.html, r'<button[^>]*id="sj-surprise"[^>]*sj-needs-js')
        self.assertRegex(self.html, r'<p[^>]*id="sj-idea"[^>]*sj-needs-js')

    def test_home_loads_its_own_styles_and_scripts(self):
        for ref in ["assets/home.css", "assets/joy.js", "assets/home.js", "assets/scroll-story.js"]:
            self.assertIn(ref, self.html)
            self.assertTrue((ROOT / ref).exists(), ref)

    def test_text_over_photos_is_forced_white_so_squarespace_headings_cannot_turn_it_black(self):
        rule_text = re.search(r"\.lines \.line, \.card h3[^{]*\{([^}]*)\}", HOME_CSS)
        self.assertIsNotNone(rule_text, "no colour rule for story lines and card titles")
        self.assertRegex(rule_text.group(1), r"color:\s*#fff\s*!important")

    def test_heart_pill_sits_above_the_part_of_the_hero_the_story_covers(self):
        rule_text = home_rule(".tap")
        self.assertRegex(rule_text, r"bottom:\s*calc\(9vh")

    def test_home_css_has_the_story_and_card_rules_and_a_reduced_motion_block(self):
        for sel in [".hero-card", ".story", ".stage-pin", ".frame", ".line", ".cards", ".card", ".reveal", ".reveal.in"]:
            self.assertIsNotNone(home_rule(sel), f"home.css missing {sel}")
        self.assertIn("prefers-reduced-motion", HOME_CSS)


class SnippetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        build_index()
        d = ROOT / "squarespace"
        cls.heart = (d / "heart-block.html").read_text()
        cls.surprise = (d / "surprise-block.html").read_text()
        cls.footer = (d / "footer-injection.html").read_text()

    def test_footer_injection_is_one_small_script_with_the_logic(self):
        self.assertEqual(self.footer.count("<script"), 1)
        self.assertEqual(self.footer.count("</script>"), 1)
        self.assertIn("createCounter", self.footer)
        self.assertIn("initHome", self.footer)
        self.assertLess(len(self.footer.encode()), 20 * 1024)

    def test_heart_block_has_its_ids_style_and_image_placeholder_but_no_script(self):
        for ident in ["sj-heart", "sj-rings", "sj-count"]:
            self.assertIn(f'id="{ident}"', self.heart)
        self.assertIn("<style>", self.heart)
        self.assertNotIn("<script", self.heart)
        self.assertIn("{{HEART_IMAGE_URL}}", self.heart)
        self.assertNotIn('src="assets/', self.heart)  # header comments may mention repo paths, markup may not
        self.assertIn("@keyframes ring-out", self.heart)

    def test_surprise_block_has_its_ids_and_style_but_no_script(self):
        for ident in ["sj-surprise", "sj-idea"]:
            self.assertIn(f'id="{ident}"', self.surprise)
        self.assertIn("<style>", self.surprise)
        self.assertNotIn("<script", self.surprise)
        self.assertRegex(self.surprise, r'<button[^>]*id="sj-surprise"[^>]*sj-needs-js')

    def test_script_only_elements_are_hidden_until_the_page_is_marked_script_enabled(self):
        for css in (self.surprise, CSS_NO_COMMENTS):
            self.assertRegex(css, r"\.sj-needs-js\s*\{[^}]*display:\s*none")
            self.assertRegex(css, r"\.sj-js\s+\.sj-needs-js\s*\{[^}]*display:\s*(block|inline-block)")

    def test_idea_line_is_script_only(self):
        self.assertRegex(self.surprise, r'<p[^>]*id="sj-idea"[^>]*sj-needs-js')
        html = (ROOT / "index.html").read_text()
        self.assertRegex(html, r'<p[^>]*id="sj-idea"[^>]*sj-needs-js')

    def test_start_count_comes_from_the_single_constant(self):
        const = re.search(r"PLACEHOLDER_START_COUNT\s*=\s*(\d+)", (ROOT / "assets" / "ripples.js").read_text()).group(1)
        formatted = f"{int(const):,}"
        for text in (self.heart, (ROOT / "index.html").read_text()):
            self.assertIn(f'id="sj-count">{formatted}<', text)

    def test_snippet_css_declares_the_brand_variables_it_uses(self):
        for block in (self.heart, self.surprise):
            self.assertIn("--yellow: #fdcd17", block)
            self.assertIn("--ink: #231f20", block)


class SnippetLibraryTests(unittest.TestCase):
    """squarespace/ is a paste-ready library: every file is formatted, commented and indexed."""

    @classmethod
    def setUpClass(cls):
        build_index()
        cls.dir = ROOT / "squarespace"
        cls.files = sorted(cls.dir.glob("*.html"))

    def test_every_snippet_starts_with_a_documenting_header(self):
        self.assertGreaterEqual(len(self.files), 3)
        for f in self.files:
            text = f.read_text()
            self.assertTrue(text.startswith("<!--"), f"{f.name} has no header comment")
            header = text[: text.index("-->")]
            for key in ("SNIPPET:", "WHAT IT DOES:", "WHERE TO PASTE:", "NEEDS:"):
                self.assertIn(key, header, f"{f.name} header is missing {key}")

    def test_snippets_are_formatted_not_minified(self):
        for f in self.files:
            lines = f.read_text().split("\n")
            self.assertGreater(len(lines), 10, f"{f.name} is too short to be formatted")
            self.assertLess(max(len(l) for l in lines), 160, f"{f.name} has a very long line")

    def test_footer_script_is_commented_by_section(self):
        footer = (self.dir / "footer-injection.html").read_text()
        self.assertIn("PART 1", footer)
        self.assertIn("PART 2", footer)

    def test_css_inside_block_snippets_is_commented(self):
        for name in ("heart-block.html", "surprise-block.html"):
            style = re.search(r"<style>(.*?)</style>", (self.dir / name).read_text(), re.S).group(1)
            self.assertIn("/*", style, f"{name} CSS has no comments")

    def test_readme_index_lists_every_snippet_and_the_convention(self):
        readme = (self.dir / "README.md").read_text()
        for f in self.files:
            self.assertIn(f.name, readme)
        self.assertIn("Adding a new snippet", readme)


if __name__ == "__main__":
    unittest.main()


class HomePageFolderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        build_index()
        cls.dir = ROOT / "home-page"

    def read(self, name):
        return (self.dir / name).read_text()

    def test_folder_has_the_five_pastes_in_order(self):
        for n in ["1-header-injection.html", "2-footer-injection.html", "3-hero-block.html", "4-story-block.html", "5-your-turn-block.html", "6-footer-block.html"]:
            self.assertTrue((self.dir / n).exists(), n)
            self.assertIn("PASTE", self.read(n).split("-->")[0], n)

    def test_blocks_hold_html_only_with_image_placeholders_and_no_local_paths(self):
        for n in ["3-hero-block.html", "4-story-block.html", "5-your-turn-block.html", "6-footer-block.html"]:
            text = self.read(n)
            # the supplied hope-jar overlay carries its own isolated (shadow DOM) style and script
            text = re.sub(r"<div data-sjc-hope-widget></div>\s*<script>.*?</script>", "", text, flags=re.S)
            if n == "3-hero-block.html":
                # the hero block carries the ripples heart and counter script by itself
                text = re.sub(r"<script>\n\(function \(root\) \{\n  // The \"ripples of joy\".*?</script>", "", text, flags=re.S)
                # ...and the page-open heart effect: one style (every rule scoped to .sj-home) and one script
                text = re.sub(r"<style>\n/\* Landing-page open effect.*?</style>", "", text, flags=re.S)
                text = re.sub(r"<script>\n\(function \(root\) \{\n  // Page-open effect.*?</script>", "", text, flags=re.S)
            self.assertNotIn("<style", text, n)
            self.assertNotIn("<script", text, n)
            self.assertNotIn("assets/img", text, n)
            self.assertIn('<div class="sj-home">', text, n)
        urls = json.loads((self.dir / "image-urls.json").read_text())
        hero = self.read("3-hero-block.html")
        # a key in image-urls.json is filled in; a missing key stays a {{PLACEHOLDER}}
        self.assertTrue(urls["IMG_SOCKS_CIRCLE"] in hero or "{{IMG_SOCKS_CIRCLE}}" in hero)
        self.assertNotIn("{{IMG_SOCKS_CIRCLE}}" if urls.get("IMG_SOCKS_CIRCLE") else "@@", hero)
        self.assertNotIn("{{LINK_HELP}}" if urls.get("LINK_HELP") else "@@", self.read("5-your-turn-block.html"))

    def test_header_has_all_the_css_and_the_squarespace_fixes(self):
        css = self.read("1-header-injection.html")
        for needle in [".hero-card", ".stage-pin", ".card", ".page-section:has(.sj-home)", "#header.tucked", "font-family: inherit", "League+Spartan", "color-scheme: only light", ".hero { padding-top", "#header .header-title-logo a::after", "#header .header-actions .btn", "Give \\u2665"]:
            self.assertIn(needle, css)
        index = (ROOT / "index.html").read_text()
        self.assertRegex(index, r'class="btn btn-dark"[^>]*>Give &#9829;</a>')
        self.assertIn("#header .header-menu-cta a", css)

    def test_page_script_block_runs_the_site_script_from_a_code_block_once(self):
        text = self.read("7-page-script-block.html")
        self.assertIn("PASTE 7", text.split("-->")[0])
        self.assertEqual(text.count("<script>"), 1)
        # the Givebutter goal bar needs its library; here it travels with the script, from Givebutter's host only
        srcs = re.findall(r'<script\b[^>]*\bsrc="([^"]+)"', text)
        self.assertEqual(len(srcs), 1)
        self.assertTrue(srcs[0].startswith("https://widgets.givebutter.com/"), srcs[0])
        self.assertIn("window.__sjHome", text)  # guard against running twice if Squarespace re-draws the block
        for needle in ["PART 1", "PART 2", "PART 3", "PART 4", "initStory", "initGive", "createShuffler"]:
            self.assertIn(needle, text)

    def test_ripples_counter_lives_only_in_the_hero_block_not_in_the_site_script(self):
        hero = self.read("3-hero-block.html")
        self.assertEqual(hero.count("<script>"), 2)  # heart counter, then the page-open heart transition
        self.assertIn("initRipples", hero)
        self.assertIn("sj-ripples", hero)
        # the page gives the counter the real clock, so the number rises and wraps at ten million on its own
        self.assertIn("initRipples(document, browserStorage(), Date.now)", hero)
        self.assertIn("WRAP_AT = 10000000", hero)
        for n in ("2-footer-injection.html", "7-page-script-block.html"):
            self.assertNotIn("initRipples", self.read(n), n)
            self.assertNotIn("sj-ripples", self.read(n), n)

    def test_heart_page_transition_lives_only_in_the_hero_block(self):
        hero = self.read("3-hero-block.html")
        self.assertEqual(hero.count("<style>"), 1)
        self.assertEqual(hero.count("function initHeartTransition"), 1)
        style = re.search(r"<style>(.*?)</style>", hero, re.S).group(1)
        for selector in re.findall(r"^\s*([.#][^{}/]+?)\s*\{", re.sub(r"/\*.*?\*/|@media[^{]*\{", "", style, flags=re.S), re.M):
            self.assertTrue(selector.startswith(".sj-home"), "unscoped rule: " + selector)
        self.assertIn("#heart-transition", hero)
        self.assertNotIn("{{HEART_IMG}}", hero)
        self.assertNotIn("assets/img", hero)
        # the effect's own heart picture is the uploaded heart, not a repo path
        self.assertIn("images.squarespace-cdn.com", hero[hero.index("#heart-transition::after"):][:600])
        for n in ("2-footer-injection.html", "7-page-script-block.html", "1-header-injection.html"):
            self.assertNotIn("heart-transition", self.read(n), n)

    def test_help_links_go_to_the_live_let_us_help_page_not_the_missing_volunteer_page(self):
        for n in ("2-footer-injection.html", "5-your-turn-block.html", "6-footer-block.html"):
            text = self.read(n)
            self.assertNotIn("/volunteer", text, n)
            self.assertIn('href="/let-us-help"', text, n)

    def test_story_overlap_beats_squarespace_own_margin_rules(self):
        # On Squarespace something in its own CSS resets the story's negative top margin to 0 (a white gap and white
        # corners between the hero photo and the story sheet), so the overlap rule has to be !important.
        css = self.read("1-header-injection.html")
        rule = re.search(r"\.story \{[^}]*\}", css).group(0)
        self.assertRegex(rule, r"margin-top:\s*-9vh\s*!important")

    def test_footer_has_every_script_part(self):
        js = self.read("2-footer-injection.html")
        # one inline script, plus at most one external script and only from Givebutter's widget host
        srcs = re.findall(r'<script\b[^>]*\bsrc="([^"]+)"', js)
        self.assertEqual(js.count("<script"), 1 + len(srcs))
        self.assertEqual(js.count("<script>"), 1)
        self.assertLessEqual(len(srcs), 1)
        for src in srcs:
            self.assertTrue(src.startswith("https://widgets.givebutter.com/"), src)
        for needle in ["PART 1", "PART 2", "PART 3", "initStory", "initCards", "initHeader", "createShuffler"]:
            self.assertIn(needle, js)
        self.assertIn('class="sj-footer"', js)
        self.assertIn("#footer-sections, .sjc-footer { display: none", js)
        self.assertIn('href="/let-us-help"', js)
        self.assertIn("Stay in the loop", js)
        self.assertNotIn("hello@yourdomain.org", js)
        self.assertNotIn(">Donate<", js)

    def test_story_position_does_not_use_offsettop(self):
        self.assertNotRegex((ROOT / "assets" / "scroll-story.js").read_text(), r"\.offsetTop")


class ContactPageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        build_index()
        cls.html = (ROOT / "contact.html").read_text()

    def test_contact_page_is_the_hello_note_with_real_channels(self):
        self.assertEqual(len(re.findall(r"<h1[\s>]", self.html)), 1)
        h1 = text_of(re.sub(r"<br\s*/?>", " ", re.search(r"<h1[^>]*>(.*?)</h1>", self.html, re.S).group(1)))
        self.assertEqual(h1, "Good things start with a hello.")
        # three lines on every screen width ("start with" together on line two); each line cannot break itself
        self.assertIn('<span style="white-space:nowrap">Good things</span><br><span style="white-space:nowrap">start with</span><br><span style="white-space:nowrap">a hello.</span>', self.html)
        self.assertIn("I’d love to hear from you.", self.html)
        self.assertIn("marisa@spreadjoycollective.org", self.html)
        self.assertIn('href="mailto:marisa@spreadjoycollective.org"', self.html)
        self.assertIn('href="https://www.instagram.com/spreadjoycollective/"', self.html)
        self.assertIn("https://www.facebook.com/share/1FK6ceyMsn/", self.html)
        self.assertIn("A little different. Better together.", self.html)
        self.assertIn('alt="A circle of people wearing colorful, mismatched socks"', self.html)
        self.assertIn('src="assets/img/contact-socks.jpg"', self.html)
        self.assertTrue((ROOT / "assets" / "img" / "contact-socks.jpg").exists())
        self.assertIn("assets/contact.css", self.html)
        self.assertIn("#sjc-contact", (ROOT / "assets" / "contact.css").read_text())
        self.assertNotIn("The live Contact page on Squarespace is still empty", self.html)
        self.assertNotIn("[TBD: public contact email]", self.html)
        paste = (ROOT / "contact-page" / "1-contact-block.html").read_text()
        self.assertIn('<span style="white-space:nowrap">start with</span>', paste)
        self.assertIn("mailto:marisa@spreadjoycollective.org", paste)
        self.assertIn("<style>", paste)
        self.assertNotIn("assets/img", paste)
        self.assertTrue("data:image/jpeg;base64," in paste or "images.squarespace-cdn.com" in paste)


class SiteLinkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        build_index()
        cls.pages = {p.name: p.read_text() for p in ROOT.glob("*.html")}

    def test_every_internal_page_link_resolves_and_nothing_is_a_dead_hash(self):
        self.assertNotIn("get-involved.html", self.pages)
        for name, html in self.pages.items():
            self.assertNotIn('href="#"', html, name)
            self.assertNotIn("hello@example.com", html, name)
            self.assertNotRegex(html, r">\s*Donate\s*<", name)
            for href in re.findall(r'href="([^"]+)"', html):
                if href.startswith(("http://", "https://", "mailto:", "tel:")):
                    continue
                path = href.split("#", 1)[0]
                if path.endswith(".html"):
                    self.assertIn(path, self.pages, f"{name} links to missing {href}")

    def test_live_squarespace_copy_is_on_the_local_pages(self):
        self.assertIn("everyone deserves to feel seen, valued, included, and supported", self.pages["mission.html"])
        self.assertIn("Spread Joy Collective began with our son, Xavier.", self.pages["story.html"])
        self.assertIn("komonews.com", self.pages["story.html"])
        self.assertIn("Pints for a Purpose", self.pages["events.html"])
        self.assertNotIn("DEC", self.pages["events.html"])
        self.assertIn("Every family deserves support, connection, and joy.", self.pages["help.html"])
        self.assertIn("givebutter.com/SpreadJoyCollective", self.pages["index.html"])
        self.assertNotIn("Get Involved", self.pages["index.html"])


class XavierStoryTests(unittest.TestCase):
    """The animated story is its own landing page (no header, no footer); it leads to the home page."""

    def setUp(self):
        subprocess.run([sys.executable, str(ROOT / "build.py")], check=True, capture_output=True)
        self.home = (ROOT / "index.html").read_text()
        self.landing = (ROOT / "landing.html").read_text()
        self.block = (ROOT / "landing-page" / "1-landing-block.html").read_text()

    def test_landing_is_its_own_page_without_header_footer_or_give_pill(self):
        self.assertIn('id="xs-story"', self.landing)
        for bad in ("<header", "<footer", "site-header", "give-pill", 'class="hero"'):
            self.assertNotIn(bad, self.landing, bad)

    def test_home_page_is_back_to_just_the_home_page(self):
        self.assertNotIn("xs-story", self.home)
        self.assertNotIn("xavier-story", self.home)
        self.assertIn('class="hero"', self.home)

    def test_landing_leads_to_home(self):
        self.assertIn('data-home="index.html"', self.landing)
        self.assertIn('href="index.html"', self.landing)  # the visible button at the end

    def test_paste_block_leads_to_the_master_home(self):
        self.assertIn('data-home="/home"', self.block)
        self.assertNotIn("index.html", self.block)

    def test_paste_block_hides_the_site_header_and_footer(self):
        self.assertIn("body:has(.xs)", self.block)
        self.assertIn("#header", self.block)

    def test_the_sprite_is_a_file_not_inlined(self):
        self.assertTrue((ROOT / "assets" / "img" / "xavier-sprite.png").exists())
        self.assertNotIn("base64", self.landing)
        self.assertLess(len(self.block), 60000)

    def test_paste_block_carries_style_markup_and_script_and_an_image_placeholder(self):
        self.assertEqual(self.block.count("<style>"), 1)
        self.assertIn('class="xs"', self.block)
        self.assertIn("initXavierStory", self.block)
        self.assertNotIn("assets/img/xavier-sprite.png", self.block)

    def test_story_css_is_scoped_to_xs(self):
        css = (ROOT / "assets" / "xavier-story.css").read_text()
        for m in re.finditer(r"(?:^|\})\s*([^{}@]+)\{", css, flags=re.M):
            for sel in m.group(1).split(","):
                self.assertTrue(sel.strip().startswith(".xs"), sel.strip())
