import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from pycord18n.language import Language

class LanguageTesting(unittest.TestCase):
    def setUp(self) -> None:
        self.language = Language("English", "en", {
            "you_lost": "You lost the {game}",
            "game": "game",
            "hello": "Hello, {place}!",
            "and_": "and"
        })
    
    def test_basic_get(self):
        self.assertEqual(self.language.get_text("hello", place="World"), "Hello, World!")
    
    def test_templated(self):
        self.assertEqual(self.language.get_text("you_lost"), "You lost the game")
    
    def test_templated_priority(self):
        self.assertEqual(self.language.get_text("you_lost", game="lottery"), "You lost the lottery")
    
    def test_formatted_list(self):
        self.assertEqual(self.language.get_text("hello", list_formatter=self.language.and_, place=["World", "Universe"]), "Hello, World and Universe!")



if __name__ == '__main__':
    unittest.main(verbosity=2)