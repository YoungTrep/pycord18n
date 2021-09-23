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

from typing import Dict


class SafeDict(dict):
    def __missing__(self, key):
        return "{" + key + "}"


class Language:
    def __init__(self, name: str, code: str, translations: Dict[str, str]) -> None:
        self.name = name
        self.code = code
        self._translations = translations

    def _get_translation_from_key(self, key: str, raise_on_empty: bool = True) -> str:
        """
        Get the translation string from a given key. The default behaviour 
        supports simple key-translation access and dotted nesting.

        Parameters
        ----------
        key : str
            The key to parse
        raise_on_empty : bool, optional
            Whether to raise a KeyError when the returned value is an empty string, by default True

        Returns
        -------
        str
            The translation listed under the given key

        Raises
        ------
        KeyError
            The function attempted to access a key when using dotted nesting,
            but the value did not have this key
        KeyError
            If ``raise_on_empty`` is True, the value found is an empty string
        """
        if "." in key:
            parts = key.split(".")
            current = self._translations[parts[0]]
            for part in parts[1:]:
                if part in current:
                    current = current[part]
                else:
                    raise KeyError(f"{part} was not found under {current}")
        else:
            current = self._translations[key]

        if raise_on_empty and current == "":
            raise KeyError("Resultant string was empty")

        return current

    def join_list(self, value: list, connector: str) -> str:
        """
        Sensibly join list elements together

        Parameters
        ----------
        value : list
            The list of values to combine. Automatically converted to strings
        connector : str
            The text that goes either between two items when the list is 2
            items long, or between all but the last item of the list
            and the last item of the list when the list has more than 2
            items

        Returns
        -------
        str
            The list as a "sensible" string
        """
        # Stringify everything first
        value = [str(v) for v in value]
        if len(value) == 1:
            return value[0]
        elif len(value) == 2:
            # Just two items
            return connector.join(value)
        else:
            # All but last connected by ",", and last connected by connector
            return connector.join([','.join(value[:-1]), value[-1]])

    def and_(self, value: list, *args, **kwargs) -> str:
        """
        Wraps :func:`join_list` but uses the translation key ``and_``

        Parameters
        ----------
        value : list
            The list of values to combine. Automatically converted to strings

        Returns
        -------
        str
            The list as a "sensible" string
        """
        return self.join_list(value, " " + self._get_translation_from_key("and_",  *args, **kwargs) + " ")

    def or_(self, value: list, *args, **kwargs) -> str:
        """
        Wraps :func:`join_list` but uses the translation key ``or_``

        Parameters
        ----------
        value : list
            The list of values to combine. Automatically converted to strings

        Returns
        -------
        str
            The list as a "sensible" string
        """
        return self.join_list(value, " " + self._get_translation_from_key("or_",  *args, **kwargs) + " ")

    def get_text(
        self,
        key: str,
        list_formatter: bool = None,
        use_translations: bool = True,
        safedict=SafeDict,
        **kwargs
    ) -> str:
        """
        Get the formatted translation string

        Parameters
        ----------
        key : str
            The key to search for
        list_formatter : bool, optional
            Function to format lists, by default None

            .. seealso :: functions :func:`and_`, :func:`or_`, :func:`join_list`
        use_translations : bool, optional
            Whether to use translations in formatting, by default True

            For example, any missing parameters for the string (wrapped
            in curly braces) can be replaced by translations in the current
            language. This could be used to mix translation entries.

                >>> language = Language("English", "en", {
                    "you_lost": "You lost the {game}",
                    "game": "game",
                })

                >>> language.get_text("you_lost")
                "You lost the game"
        safedict : Any, optional
            Class to use as a "Safe dict", by default :cls:`SafeDict`
        **kwargs : dict, optional
            Parameters to pass to translation

        Returns
        -------
        str
            The translated string

        Raises
        ------
        KeyError
            The translation was not found (raised through `_get_translation_from_key`)
        """
        base_string = self._get_translation_from_key(key)

        # Sanitize passed arguments
        params = kwargs.copy()
        for key, value in params.items():
            if list_formatter and isinstance(value, list):
                params[key] = list_formatter(value)

        # Create the dict using given kwargs
        mapping = params
        if use_translations:
            # Put `**kwargs` after to prioritize given translations
            mapping = {
                **self._translations,
                **mapping
            }

        return base_string.format_map(safedict(**mapping))
