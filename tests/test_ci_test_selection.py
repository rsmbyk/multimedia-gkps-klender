"""Keep browser tests out of the fast lane by tagging every E2E test class."""

import importlib
import inspect
import pkgutil
import unittest

from django.test import SimpleTestCase

import tests.e2e


class E2ETaggingTests(SimpleTestCase):
    def test_every_e2e_test_class_has_the_e2e_tag(self):
        untagged = []
        for module_info in pkgutil.iter_modules(tests.e2e.__path__):
            if not module_info.name.startswith('test_'):
                continue
            module = importlib.import_module(f'tests.e2e.{module_info.name}')
            for _, test_class in inspect.getmembers(module, inspect.isclass):
                if (issubclass(test_class, unittest.TestCase)
                        and test_class.__module__ == module.__name__
                        and 'e2e' not in getattr(test_class, 'tags', set())):
                    untagged.append(f'{module.__name__}.{test_class.__name__}')

        self.assertEqual(untagged, [])
