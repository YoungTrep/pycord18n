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

from discord.ext import commands

from pycord18n.extension import I18nExtension, _
from pycord18n.language import Language


class I18nExtensionTesting(unittest.TestCase):    
    def test_basic_get_contextual(self):
        self.i18n = I18nExtension([
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

        self.i18n.set_current_locale("en")
        self.assertEqual(_("hello"), "Hello")
        self.i18n.set_current_locale("fr")
        self.assertEqual(_("hello"), "Bonjour")
    
    def test_no_i18n_set(self):
        # Manually get rid of it
        I18nExtension.default_i18n_instance = None
        with self.assertRaises(NameError):
            _("hello")
    
    def test_bot(self):
        async def get_locale(_):
            return "en"

        self.i18n = I18nExtension([
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
        ], bot=commands.Bot("!"), get_locale_func=get_locale, fallback="en")

        self.assertEqual(self.i18n.contextual_get_text("hello"), "Hello")
    

if __name__ == '__main__':
    unittest.main(verbosity=2)
