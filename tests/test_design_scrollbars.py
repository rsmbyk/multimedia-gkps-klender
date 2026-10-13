"""The scrollbar's mechanism (spec 087).

In Blink and WebKit the custom ``::-webkit-scrollbar`` path is taken only while the
standard properties are absent. Set ``scrollbar-width``/``scrollbar-color`` as well
and the standard properties win: the platform's thin bar is painted -- stepper
buttons and all -- and every ``::-webkit-scrollbar`` rule, the button suppression
included, is ignored (measured on Chromium 145: a 10px bar with a stepper glyph,
against 5px and bare on the custom path).

These assertions parse the stylesheets, so a later edit cannot quietly put both
mechanisms back in play, and they keep the thumb inside the contrast band the
"softer, but still visible" change was chosen for.
"""

import re
from pathlib import Path

from django.test import SimpleTestCase

DESIGN = Path(__file__).resolve().parent.parent / 'static/styles/design'
COMPONENTS_CSS = DESIGN / 'components.css'
TOKENS_CSS = DESIGN / 'tokens.css'

GATE = r'@supports\s+not\s+selector\(::-webkit-scrollbar\)\s*\{'
LIGHT = ':root'
DARK = ':root[data-theme="dark"]'


def _block(css, selector):
    """Return {token: value} for one selector block."""
    match = re.search(re.escape(selector) + r'\s*\{([^}]*)\}', css, re.S)
    if not match:
        raise AssertionError(f'selector {selector!r} not found in tokens.css')
    return dict(re.findall(r'(--[\w-]+)\s*:\s*([^;]+);', match.group(1)))


def _luminance(hex_color):
    channels = [int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    linear = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def _contrast(fg, bg):
    light, dark = _luminance(fg), _luminance(bg)
    hi, lo = max(light, dark), min(light, dark)
    return (hi + 0.05) / (lo + 0.05)


class ScrollbarMechanismTests(SimpleTestCase):
    def setUp(self):
        self.css = COMPONENTS_CSS.read_text(encoding='utf-8')
        gate = re.search(GATE, self.css)
        if not gate:
            raise AssertionError('the @supports gate around the standard properties is gone')
        self.gate = self.css[gate.start():self._gate_end(gate.start())]

    def _gate_end(self, start):
        depth = 0
        for index in range(start, len(self.css)):
            if self.css[index] == '{':
                depth += 1
            elif self.css[index] == '}':
                depth -= 1
                if depth == 0:
                    return index + 1
        raise AssertionError('unbalanced braces in components.css')

    def test_the_standard_properties_live_only_inside_the_gate(self):
        self.assertIn('scrollbar-width: thin', self.gate)
        self.assertIn('scrollbar-color: var(--scroll-thumb) transparent', self.gate)

    def test_no_standard_width_survives_outside_the_gate(self):
        # a lone `scrollbar-width: thin` anywhere else puts Blink back on the native
        # bar for that scroller, stepper buttons included
        outside = self.css.replace(self.gate, '')
        self.assertNotIn('scrollbar-width: thin', outside)
        self.assertNotIn('scrollbar-width: auto', outside)

    def test_the_custom_bar_is_five_pixels_and_buttonless(self):
        self.assertRegex(self.css, r'::-webkit-scrollbar\s*\{\s*width: 5px;\s*height: 5px;')
        self.assertRegex(
            self.css,
            r'::-webkit-scrollbar-button[^{]*\{\s*display: none;\s*width: 0;\s*height: 0;')

    def test_the_track_and_corner_never_paint(self):
        self.assertRegex(
            self.css, r'::-webkit-scrollbar-track[^{]*::-webkit-scrollbar-corner[^{]*\{[^}]*'
                       r'background: transparent;')

    def test_the_deliberately_hidden_bars_stay_hidden(self):
        self.assertIn(
            '[data-nav="mini"] .panel__body::-webkit-scrollbar { display: none; }', self.css)
        self.assertIn('.ch__body::-webkit-scrollbar { display: none; }', self.css)


class ScrollbarThumbTests(SimpleTestCase):
    """Softer, but still visible: the resting thumb has to read against its surface,
    and the hover state has to be clearly stronger (spec 087)."""

    def setUp(self):
        self.css = TOKENS_CSS.read_text(encoding='utf-8')

    def _ratios(self, selector, canvas):
        block = _block(self.css, selector)
        return (
            _contrast(block['--scroll-thumb'], block[canvas]),
            _contrast(block['--scroll-thumb-hover'], block[canvas]),
        )

    def test_the_light_thumb_sits_in_the_intended_band(self):
        block = _block(self.css, LIGHT)
        self.assertEqual(block['--scroll-thumb'], '#B4B0A6')
        self.assertEqual(block['--scroll-thumb-hover'], '#948F85')
        resting, hover = self._ratios(LIGHT, '--canvas')
        self.assertAlmostEqual(resting, 1.99, places=2)
        self.assertAlmostEqual(hover, 2.95, places=2)
        self.assertGreater(hover, resting)

    def test_the_dark_thumb_sits_in_the_intended_band(self):
        block = _block(self.css, DARK)
        self.assertEqual(block['--scroll-thumb'], '#45413A')
        self.assertEqual(block['--scroll-thumb-hover'], '#65615A')
        resting, hover = self._ratios(DARK, '--canvas')
        self.assertAlmostEqual(resting, 1.83, places=2)
        self.assertAlmostEqual(hover, 3.02, places=2)
        self.assertGreater(hover, resting)
