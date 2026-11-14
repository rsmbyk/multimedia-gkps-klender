"""Guards for the font mapping the deck converter relies on (spec 182).

Two rules live in ``docker/slides-fonts.conf`` and cannot be checked by a Django test that draws a
slide: an alias must yield to a family the computer actually has, and the operator's own directory
must be searched before the computer's. Both are properties of the file, so they are asserted here —
the behaviour they produce is verified in the image (``fc-match``), as the slice's plan records.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path

from django.test import SimpleTestCase

REPO_ROOT = Path(__file__).resolve().parent.parent
FONTS_CONF = REPO_ROOT / "docker" / "slides-fonts.conf"

OPERATOR_DIR = "/usr/share/fonts/operator"
HOST_DIR = "/usr/share/fonts/host"


class SlidesFontsConfTests(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        if not FONTS_CONF.exists():
            raise AssertionError("docker/slides-fonts.conf is missing")
        cls.root = ET.parse(FONTS_CONF).getroot()

    def test_every_named_family_yields_to_an_installed_family(self):
        generics = {"sans-serif", "serif", "monospace"}
        named = [
            alias
            for alias in self.root.findall("alias")
            if alias.findtext("family") not in generics
        ]
        self.assertTrue(named, "the mapping is empty")
        for alias in named:
            family = alias.findtext("family")
            self.assertEqual(
                alias.get("binding"),
                "weak",
                f"{family} is bound with {alias.get('binding')!r}, which overrides a family "
                "the computer already has",
            )

    def test_the_generic_families_stay_bound_same(self):
        # A weak alias is ignored for a generic family, and this mapping exists so a generic request
        # is never answered with a monospaced face.
        by_family = {alias.findtext("family"): alias for alias in self.root.findall("alias")}
        for generic in ("sans-serif", "serif"):
            self.assertIn(generic, by_family, f"the {generic} mapping is missing")
            self.assertEqual(
                by_family[generic].get("binding"),
                "same",
                f"{generic} is bound weak, so fontconfig would ignore the mapping",
            )

    def test_the_operator_directory_precedes_the_host_directory(self):
        dirs = [node.text for node in self.root.findall("dir")]
        self.assertIn(OPERATOR_DIR, dirs, "the operator's directory is not named explicitly")
        self.assertIn(HOST_DIR, dirs, "the computer's font directory is not named explicitly")
        self.assertLess(
            dirs.index(OPERATOR_DIR),
            dirs.index(HOST_DIR),
            "the computer's fonts are searched before the operator's, so a file placed "
            "deliberately in the folder loses the clash",
        )
