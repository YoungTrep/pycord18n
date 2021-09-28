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


import contextvars
from typing import Any, Callable, List, Optional, Union, Coroutine

from discord.ext import commands

from .i18n import I18n
from .language import Language


class I18nExtension(I18n):
    default_i18n_instance = None

    def __init__(
        self,
        languages: List[Language],
        fallback: Union[str, int],
        bot: Optional[commands.Bot] = None,
        get_locale_func: Callable[..., Coroutine[Any, Any, Any]] = None,
        default: bool = True
    ) -> None:
        """
        Initialize the extension class.

        .. warning::

            The bot will only be attached to if both `bot` and `get_locale_func`
            are provided to this function. Otherwise it will not attach
            automatically.

        Parameters
        ----------
        languages : List[Language]
            List of lanugages to use
        fallback : Union[str, int]
            String ID or list index of the fallback locale
        bot : commands.Bot, optional
            The bot to attach to, by default None
        get_locale_func : Callable, optional
            If provided, init_bot will be run for you
        default : bool, optional
            Whether to make this i18n instance the default, by default True

            If there is no default i18n instance, this parameter is ignored and
            it is always set.

            The default is used by :func:`I18nExtension.contextual_get_text`.
        """
        super().__init__(languages, fallback)
        self._current_locale = contextvars.ContextVar("_current_locale")
        self._bot = None

        if default or I18nExtension.default_i18n_instance is None:
            I18nExtension.default_i18n_instance = self
        
        if self._bot and get_locale_func:
            self.init_bot(self._bot, get_locale_func)

    def init_bot(self, bot: commands.Bot, get_locale_func: Callable[..., Coroutine[Any, Any, Any]] = None):
        """
        Initialize the given bot with the pre-invoke hooks to set the current
        context. 

        .. note ::

            Due to how discord.py works, this will override any previously
            set global pre-invoke hook.

            I recommend creating an override to have multiple pre- and post-
            invoke hooks if required, or setting the current locale yourself
            with :func:`set_current_locale`.

        Parameters
        ----------
        bot : commands.Bot
            The bot to attach to
        get_locale_func : Callable, coroutine, optional
            The function that provides the locale code for the context, by default None

            It should take one argument, of type :cls:`discord.ext.commands.Context`
        """
        self._bot = bot
        if get_locale_func is None:
            # Just use the fallback
            get_locale_func = lambda *_: self._fallback

        async def pre(ctx):
            self.set_current_locale(get_locale_func(ctx))

        self._bot.before_invoke(pre)

    def set_current_locale(self, locale: str) -> str:
        """
        Set the current locale (for this context)

        Parameters
        ----------
        locale : str
            The locale
        """
        self._current_locale.set(locale)

    def get_current_locale(self) -> str:
        """
        Get the locale for this context, or the fallback locale if none is set

        Returns
        -------
        str
            The locale
        """
        return self._current_locale.get(self._fallback)

    @classmethod
    def contextual_get_text(
        cls,
        key: str,
        list_formatter: bool = None,
        use_translations: bool = True,
        should_fallback: bool = True,
        **kwargs
    ) -> str:
        """
        Wraps :func:`get_text` to use the current context's locale

        .. seealso: documentation for :func:`Language.get_text`

        Parameters
        ----------
        key : str
            The key to search for
        list_formatter : bool, optional
            Function to format lists, by default None
        use_translations : bool, optional
            Whether to use translations in formatting, by default True
        should_fallback : bool, optional
            Should fallback to default locale, by default True

        Returns
        -------
        str
            Translated and formatted string

        Raises
        ------
        NameError
            If there is no current i18n instance set
        """
        i18n = cls.default_i18n_instance
        if i18n is None:
            raise NameError("No default i18n instance has been initialized!")

        return i18n.get_text(
            key, i18n.get_current_locale(), list_formatter=list_formatter,
            use_translations=use_translations, should_fallback=should_fallback,
            **kwargs)


_ = I18nExtension.contextual_get_text
