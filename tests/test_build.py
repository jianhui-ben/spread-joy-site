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


class HomeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = build_index()

    def test_hero_headline_and_subline(self):
        h1 = re.search(r"<h1[^>]*>(.*?)</h1>", self.html, re.S).group(1)
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
        for frame, name in zip(frames, ["xavier-portrait.jpg", "socks-circle.jpg", "sock-pile.jpg"]):
            self.assertIn(f'src="assets/img/{name}"', frame)
            self.assertTrue((ROOT / "assets" / "img" / name).exists(), name)
            alt = re.search(r'alt="([^"]*)"', frame)
            self.assertTrue(alt and alt.group(1).strip(), f"{name} has no alt text")

    def test_your_turn_cards_link_to_the_right_places(self):
        self.assertEqual(text_of(re.search(r'<section class="turn".*?<h2[^>]*>(.*?)</h2>', self.html, re.S).group(1)), "Your turn.")
        cards = re.findall(r'<a class="card"[^>]*href="([^"]*)"[^>]*>(.*?)</a>', self.html, re.S)
        links = {text_of(re.search(r"<h3>(.*?)</h3>", body, re.S).group(1)): href for href, body in cards}
        self.assertEqual(links, {
            "I have time": "help.html",
            "I want to give": "#",
            "I have something to share": "help.html",
            "My family could use support": "contact.html",
        })

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
        for ident in ["sj-heart", "sj-rings", "sj-count", "sj-surprise", "sj-idea"]:
            self.assertEqual(len(re.findall(r'id="%s"' % ident, self.html)), 1, ident)

    def test_heart_is_a_button_and_counter_announces_politely(self):
        self.assertRegex(self.html, r'<button[^>]*id="sj-heart"')
        self.assertRegex(self.html, r'<p[^>]*aria-live="polite"[^>]*>[^<]*(?:<[^>]*>[^<]*)*id="sj-count"|id="sj-count"[^>]*>[^<]*</[^>]+>[^<]*</p>')
        self.assertIn("1,284", re.search(r'id="sj-count"[^>]*>([^<]*)<', self.html).group(1))

    def test_script_only_elements_are_hidden_without_javascript(self):
        self.assertRegex(self.html, r'<button[^>]*id="sj-surprise"[^>]*sj-needs-js')
        self.assertRegex(self.html, r'<p[^>]*id="sj-idea"[^>]*sj-needs-js')

    def test_home_loads_its_own_styles_and_scripts(self):
        for ref in ["assets/home.css", "assets/joy.js", "assets/home.js", "assets/scroll-story.js"]:
            self.assertIn(ref, self.html)
            self.assertTrue((ROOT / ref).exists(), ref)

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
        const = re.search(r"PLACEHOLDER_START_COUNT\s*=\s*(\d+)", (ROOT / "assets" / "joy.js").read_text()).group(1)
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
        for n in ["1-header-injection.html", "2-footer-injection.html", "3-hero-block.html", "4-story-block.html", "5-your-turn-block.html"]:
            self.assertTrue((self.dir / n).exists(), n)
            self.assertIn("PASTE", self.read(n).split("-->")[0], n)

    def test_blocks_hold_html_only_with_image_placeholders_and_no_local_paths(self):
        for n in ["3-hero-block.html", "4-story-block.html", "5-your-turn-block.html"]:
            text = self.read(n)
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
        for needle in [".hero-card", ".stage-pin", ".card", ".page-section:has(.sj-home)", "#header.tucked", "font-family: inherit", "League+Spartan", "color-scheme: only light", ".hero { padding-top"]:
            self.assertIn(needle, css)

    def test_footer_has_every_script_part(self):
        js = self.read("2-footer-injection.html")
        self.assertEqual(js.count("<script"), 1)
        for needle in ["PART 1", "PART 2", "PART 3", "initStory", "initCards", "initHeader", "createShuffler"]:
            self.assertIn(needle, js)

    def test_story_position_does_not_use_offsettop(self):
        self.assertNotRegex((ROOT / "assets" / "scroll-story.js").read_text(), r"\.offsetTop")
