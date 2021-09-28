<!--
 Copyright (C) 2021 YoungTrep
 
 This file is part of pycord18n.
 
 pycord18n is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.
 
 pycord18n is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.
 
 You should have received a copy of the GNU General Public License
 along with pycord18n.  If not, see <http://www.gnu.org/licenses/>.
-->

# Pycord18n

### Ported by [YoungTrep](https://github.com/YoungTrep) for the new [Discord.py](https://github.com/Rapptz/discord.py) fork - [Pycord](https://pypi.org/project/py-cord/)

This is a open sourced version of the internal internationalization engine used for [Kolumbao](https://kolumbao.com/).

[![](https://img.shields.io/pypi/v/pycord18n.svg)](https://pypi.org/project/Pycord18n/)
[![](https://img.shields.io/pypi/implementation/pycord18n.svg)](https://pypi.org/project/Pycord18n/)


## Installation
To install the Pycord18n, you can just run the following command:

```bash
# Windows
py -m pip install pycord18n

# Linux/MacOS
python3 -m pip install pycord18n
```

You can now use the library!

## Usage

### Setting up languages
A language can be initialized like this:
```python
french = Language("French", "fr", {
    "hello": "Bonjour",
    "goodbye": "Au revoir",
    "francais": "Français"
})
```

But you may want to store languages seperately and create them as follows:
```python
import json
french = Language("French", "fr", json.load(open("fr.json")))
```

### Base I18n class
When setting up the i18n class, we need to setup our languages and declare a fallback language:
```python
i18n = I18n([
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
```

`i18n` will now fallback to english if it can't find a translation for other languages.
```python
>>> i18n.get_text("hello", "en")
'Hello'
>>> i18n.get_text("hello", "fr")
'Bonjour'
>>> # "english" is not a listed translation in the French locale, so we revert to english
>>> i18n.get_text("english", "fr")
'English'
>>> # However we can make it not fallback, but this will throw an error if the translation isn't found
>>> i18n.get_text("english", "fr", should_fallback=False) 
Traceback (most recent call last):
  ...      
py18n.i18n.InvalidTranslationKeyError: 'Translation foo not found for en!'
```

### Discord
For Pycord, we can use the extension `py18n.extension.I18nExtension`. Setup your bot as you would usually, and then run `i18n.init_bot` as follows.

```python
from discord.ext import commands
from py18n.extension import I18nExtension

# Make our bot
bot = commands.Bot("prefix")

# Setup similarly to the usual class
i18n = I18nExtension([
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

# Setup the bot by giving it a function to get the user's locale.
# This could potentially refer to a database or other file.
# Anything you want!
# Otherwise, it will always be the fallback locale.
def get_locale(ctx: commands.Context):
    preferences = {
       301736945610915852: "en"
    }
    return preferences[ctx.author.id]

# Set it up!
i18n.init_bot(bot, get_locale)

@bot.command(pass_context=True)
async def hello(ctx):
    await ctx.send(i18n.contextual_get_text("hello"))
```

This is all good, but because of our line `i18n.init_bot(bot, get_locale)`, we can shorten things.

This function adds a pre-invoke hook that sets the language based on the result of `get_locale`. The `contextually_get_text` function is also exposed as `py18n.extension._`, and it is a `classmethod`.

We can change it by adding the following import and change our function:
```python
from py18n.extension import I18nExtension, _

# ...

@bot.command(pass_context=True)
async def hello(ctx):
    await ctx.send(_("hello"))
```

There, much tidier!
- The `_` function considers the current context and uses the correct locale by default.
- When initializing any `I18nExtension`, as we did earlier, it becomes the default i18n instance. The default instance is used by `_` and `contextually_get_text`.

## Issues
If you encounter any problems, check out [current issues](https://github.com/YoungTrep/pycord18n/issues) or [make a new issue](https://github.com/YoungTrep/pycord18n/issues/new).

## Notes
- Feel free to contribute! This is released under the GLP-3 license. (If you suggest another license, make an issue suggesting).
