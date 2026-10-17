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

    def test_new_classes_exist(self):
        for sel in [".band", ".band.yellow", ".wave", ".wave.flip", ".moment",
                    ".hl", ".photo-card", ".pill", ".pill.outline", ".drift-heart"]:
            self.assertIsNotNone(rule(sel), f"missing CSS rule for {sel}")

    def test_reduced_motion_block_hides_drift_hearts(self):
        m = re.search(r"@media \(prefers-reduced-motion: reduce\)\s*\{(.*?)\n\}", CSS, re.S)
        self.assertIsNotNone(m, "no prefers-reduced-motion block")
        self.assertIn(".drift-heart", m.group(1))


def build_index():
    subprocess.run([sys.executable, str(ROOT / "build.py")], check=True, capture_output=True)
    return (ROOT / "index.html").read_text()


def text_of(fragment):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", fragment)).strip()


class HomeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = build_index()
        cls.moments = re.findall(
            r'<section class="([^"]*\bmoment\b[^"]*)"[^>]*>(.*?)</section>', cls.html, re.S)

    def test_five_moments_with_exact_headlines(self):
        self.assertEqual(len(self.moments), 5)
        headlines = [text_of(re.search(r"<h2[^>]*>(.*?)</h2>", body, re.S).group(1))
                     for _, body in self.moments]
        self.assertEqual(headlines, [
            "Tap the heart.",
            "It started with one kid.",
            "Then a whole circle showed up.",
            "578 socks. One kindness at a time.",
            "Your turn.",
        ])

    def test_photos_exist_and_have_alt_text(self):
        for name in ["xavier-portrait.jpg", "socks-circle.jpg", "sock-pile.jpg"]:
            self.assertTrue((ROOT / "assets" / "img" / name).exists(), name)
            m = re.search(r'<img[^>]*src="assets/img/%s"[^>]*>' % re.escape(name), self.html)
            self.assertIsNotNone(m, f"{name} not used on the home page")
            alt = re.search(r'alt="([^"]*)"', m.group(0))
            self.assertTrue(alt and alt.group(1).strip(), f"{name} has no alt text")

    def test_your_turn_links(self):
        body = self.moments[4][1]
        links = dict((text_of(t), h) for h, t in re.findall(r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>', body, re.S))
        self.assertEqual(links["I have time"], "help.html")
        self.assertEqual(links["I have something to share"], "help.html")
        self.assertEqual(links["I want to give"], "#")
        self.assertEqual(links["My family could use support"], "contact.html")

    def test_interaction_ids_exist_exactly_once(self):
        for ident in ["sj-heart", "sj-rings", "sj-count", "sj-surprise", "sj-idea"]:
            self.assertEqual(len(re.findall(r'id="%s"' % ident, self.html)), 1, ident)

    def test_heart_is_a_button_and_counter_announces_politely(self):
        self.assertRegex(self.html, r'<button[^>]*id="sj-heart"')
        self.assertRegex(self.html, r'<p[^>]*aria-live="polite"[^>]*>.*?id="sj-count".*?</p>|'
                                    r'<p[^>]*id="sj-count"[^>]*aria-live="polite"')
        self.assertIn("1,284", re.search(r'id="sj-count"[^>]*>([^<]*)<', self.html).group(1))

    def test_surprise_button_is_hidden_without_javascript(self):
        self.assertRegex(self.html, r'<button[^>]*id="sj-surprise"[^>]*\bhidden\b')

    def test_yellow_moments_use_white_hearts(self):
        for idx in (1, 3):
            classes, body = self.moments[idx]
            self.assertIn("band", classes)
            self.assertIn("yellow", classes)
            self.assertIn("heart-white.png", body)
        for idx in (0, 2, 4):
            self.assertNotIn("yellow", self.moments[idx][0].split())


if __name__ == "__main__":
    unittest.main()
