"""Regression coverage for CI change-scope detection."""

import unittest

from scripts.ci_test_scope import changed_paths


class ChangedPathsTests(unittest.TestCase):
    def test_missing_before_revision_returns_unknown_scope(self):
        self.assertIsNone(changed_paths("missing-before-sha-for-ci-test", "HEAD"))
