"""Token contrast regression (spec 004).

The design tokens carry hard contrast requirements: text pairs need at least
4.5:1 and UI/focus pairs at least 3:1, in light AND dark mode. This test parses
``static/styles/design/tokens.css`` and asserts each declared pair directly, so
a palette edit that breaks a pair fails the suite instead of shipping.
"""

import re
from pathlib import Path

from django.test import SimpleTestCase

TOKENS_CSS = Path(__file__).resolve().parent.parent / 'static/styles/design/tokens.css'

LIGHT_SELECTOR = ':root'
DARK_SELECTOR = ':root[data-theme="dark"]'

TEXT_PAIRS = [
    ('--ink', '--canvas'),
    ('--head-ink', '--canvas'),
    ('--ink', '--rail-bg'),
    ('--active-ink', '--active-bg'),
    ('--tip-ink', '--tip-bg'),
    ('--danger', '--canvas'),
]
UI_PAIRS = [
    ('--icon', '--rail-bg'),
    ('--focus', '--canvas'),
]

TEXT_MIN = 4.5
UI_MIN = 3.0


def _block(css, selector):
    """Return {token: '#rrggbb'} for one selector block."""
    match = re.search(re.escape(selector) + r'\s*\{([^}]*)\}', css, re.S)
    if not match:
        raise AssertionError(f'selector {selector!r} not found in tokens.css')
    values = {}
    for name, value in re.findall(r'(--[\w-]+)\s*:\s*([^;]+);', match.group(1)):
        value = value.strip()
        if re.fullmatch(r'#[0-9A-Fa-f]{6}', value):
            values[name] = value
    return values


def _luminance(hex_color):
    channels = [int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    linear = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast(fg_hex, bg_hex):
    fg, bg = _luminance(fg_hex), _luminance(bg_hex)
    hi, lo = max(fg, bg), min(fg, bg)
    return (hi + 0.05) / (lo + 0.05)


class TokenContrastTests(SimpleTestCase):
    def setUp(self):
        self.css = TOKENS_CSS.read_text(encoding='utf-8')

    def _assert_pairs(self, selector, pairs, minimum):
        block = _block(self.css, selector)
        for fg, bg in pairs:
            with self.subTest(selector=selector, pair=f'{fg} on {bg}'):
                self.assertIn(fg, block, f'{fg} missing from {selector}')
                self.assertIn(bg, block, f'{bg} missing from {selector}')
                ratio = contrast(block[fg], block[bg])
                self.assertGreaterEqual(
                    ratio, minimum,
                    f'{fg} on {bg} in {selector}: {ratio:.2f} < {minimum}')

    def test_light_text_pairs_meet_aa(self):
        self._assert_pairs(LIGHT_SELECTOR, TEXT_PAIRS, TEXT_MIN)

    def test_light_ui_pairs_meet_aa(self):
        self._assert_pairs(LIGHT_SELECTOR, UI_PAIRS, UI_MIN)

    def test_dark_text_pairs_meet_aa(self):
        self._assert_pairs(DARK_SELECTOR, TEXT_PAIRS, TEXT_MIN)

    def test_dark_ui_pairs_meet_aa(self):
        self._assert_pairs(DARK_SELECTOR, UI_PAIRS, UI_MIN)
