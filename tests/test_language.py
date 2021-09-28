# Copyright (C) 2021 YoungTrep

# This file is part of pycord18n.

# pycord18n is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# pycord18n is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with pycord18n.  If not, see <http://www.gnu.org/licenses/>.
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