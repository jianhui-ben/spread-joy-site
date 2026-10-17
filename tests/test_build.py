import re
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


if __name__ == "__main__":
    unittest.main()
