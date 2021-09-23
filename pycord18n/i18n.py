# Copyright (C) 2021 Avery
#
# This file is part of py18n.
#
# py18n is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# py18n is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with py18n.  If not, see <http://www.gnu.org/licenses/>.

from typing import List, Union

from .language import Language


class Py18nError(KeyError):
    pass


class InvalidLocaleError(Py18nError):
    def __init__(self, *args, locale: str) -> None:
        super().__init__(*args)
        self.locale = locale


class InvalidTranslationKeyError(Py18nError):
    def __init__(self, *args, key: str) -> None:
        super().__init__(*args)
        self.key = key


class I18n:
    def __init__(self, languages: List[Language], fallback: Union[str, int]) -> None:
        self._languages = {
            language.code: language
            for language in languages
        }

        self._fallback = None
        if isinstance(fallback, str):
            self._fallback = fallback

            if self._fallback not in self._languages:
                raise KeyError(
                    f"No language found with code {fallback} as fallback")
        elif isinstance(fallback, int):
            self._fallback = self._languages[languages[fallback].code]

        if self._fallback is None:
            raise KeyError(
                f"No fallback language set. Check documentation for correct usage")

    def get_text(
        self,
        key: str,
        locale: str,
        list_formatter: bool = None,
        use_translations: bool = True,
        should_fallback: bool = True,
        **kwargs
    ) -> str:
        """
        Wraps :func:`Language.get_text` to get translation based on the given locale

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
        InvalidLocaleError
            If the locale does not exist on this instance
        InvalidTranslationKeyError
            If the key could not be found in the locale, nor in the fallback
            if `should_fallback` is `True`
        """
        # Get locale
        if locale not in self._languages:
            raise InvalidLocaleError(
                f"Given locale `{locale}` does not exist!", locale=locale)

        language = self._languages[locale]

        try:
            result = language.get_text(
                key, list_formatter=list_formatter, use_translations=use_translations, **kwargs)
        except KeyError as exc:
            # If we shouldn't fallback or this is the fallback
            if not should_fallback or locale == self._fallback:
                raise InvalidTranslationKeyError(
                    f"Translation {key} not found for {locale}!", key=key) from exc
        else:
            return result

        # We only get here if fallback is enabled and the text wasn't found in
        # the initial language
        try:
            result = self._languages[self._fallback].get_text(
                key, list_formatter=list_formatter, use_translations=use_translations, **kwargs)
        except KeyError as exc:
            raise InvalidTranslationKeyError(
                f"Translation {key} not found for {locale} nor fallback {self._fallback}", key=key) from exc
        else:
            return result
