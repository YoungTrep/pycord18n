import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest

from pycord18n.i18n import I18n, InvalidLocaleError, InvalidTranslationKeyError
from pycord18n.language import Language

class I18nTesting(unittest.TestCase):
    def setUp(self) -> None:
        self.i18n = I18n([
            Language("English", "en", {
                "hello": "Hello",
                "goodbye": "Goodbye",
                "english": "English"
            }),
            Language("French", "fr", {
                "hello": "Bonjour",
                "goodbye": "Au revoir",
                "francais": "Français"
            }),
        ], fallback="en")
    
    def test_basic_get(self):
        self.assertEqual(self.i18n.get_text("hello", "en"), "Hello")
        self.assertEqual(self.i18n.get_text("hello", "fr"), "Bonjour")
        self.assertEqual(self.i18n.get_text("francais", "fr"), "Français")
    
    def test_fallback(self):
        self.assertEqual(self.i18n.get_text("english", "fr"), "English")
        with self.assertRaises(InvalidTranslationKeyError):
            self.i18n.get_text("english", "fr", should_fallback=False)
    
    def test_locale_error(self):
        with self.assertRaises(InvalidLocaleError):
            self.i18n.get_text("foo", "bar", should_fallback=False)

if __name__ == '__main__':
    unittest.main(verbosity=2)
