"""LanguageList module.

File: LanguageList.py
Author: Alexander Leykand
Date: 05/07/2026
Assignment: Module 5

This module defines the LanguageList class, which represents a
named collection of Language objects. It supports iteration,
membership testing, addition (merging of lists), and basic
CRUD-style operations. LanguageList instances are also registered
in a class-level dictionary for lookup.
"""
from logic.Language import Language


class LanguageList:
    """Represents a collection of Language objects.

    A LanguageList groups Language instances under a shared category
    name and description. It supports iteration, membership checks,
    modification, and merging with other LanguageList instances.
    """
    ALL_LANGUAGES = "All Languages"
    __name = ""
    __languages = []
    __description = ""
    __map = {}

    def __init__(self, name, languages, description):
        """Initialize a LanguageList object.

        Args:
            name (str): The name of the language list.
            languages (list): A list of Language objects.
            description (str): A description of the language list.
        """
        self.__name = name
        self.__languages = languages
        self.__description = description
        self.__class__.__map[self.get_key()] = self

    def to_dict(self):
        """Return a dictionary representation of the LanguageList object."""
        return {
            "_id": self.get_key(),
            "name": self.__name,
            "description": self.__description,
            "languages": [language.get_key() for language in self.__languages]
        }

    def get_key(self):
        """Return a normalized key used to identify this list.

        Returns:
            str: The lowercase name of the language list.
        """
        return self.__name.lower()

    def get_name(self):
        """Return the name of the language list.

          Returns:
              str: The list name.
          """
        return self.__name

    def get_description(self):
        """Return the description of the language list.

         Returns:
            str: The list description.
        """
        return self.__description

    @classmethod
    def lookup(cls, key):
        """Retrieve a LanguageList by its key.

        Args:
            key (str): The lookup key (list name in lowercase).

        Returns:
            LanguageList or None: The matching LanguageList, or None if not found.
        """
        if key in cls.__map:
            return cls.__map[key.lower()]
        else:
            return None

    def append(self, language):
        """Add a Language to the list.

         Args:
             language (Language): The language to add.
         """
        self.__languages.append(language)

    def remove(self, language):
        """Remove a Language from the list.

            Args:
                language (Language): The language to remove.
            """
        self.__languages.remove(language)

    def delete(self):
        """Remove this LanguageList from the class-level registry."""
        del self.__class__.__map[self.get_key()]

    def __iter__(self):
        """Return an iterator over the languages in the list.

        Returns:
            iterator: Iterator over Language objects.
        """
        # instruction video does it this way: return self.__languages.__iter__()
        return iter(self.__languages)

    def __contains__(self, language):   # for older Python, because the new one uses iteration to check "x in y"
        """Check whether a language is in the list.

        Args:
            language (Language): The language to check.

        Returns:
            bool: True if the language is in the list, False otherwise.
        """
        return language in self.__languages

    def __add__(self, other):
        """Merge two LanguageList objects into a new one.

        Args:
            other (LanguageList): Another language list.

        Returns:
            LanguageList: A new merged LanguageList containing unique languages.
        """
        name = f"{self.get_name()}/{other.get_name()}"
        description = f"{self.get_description()}/{other.get_description()}"
        new_languagelist = LanguageList(name, [], description)
        for language in self:
            if language not in new_languagelist:
                new_languagelist.append(language)
        for language in other:
            if language not in new_languagelist:
                new_languagelist.append(language)
        return new_languagelist

    @staticmethod
    def get_languagelists():
        """Retrieve all LanguageList objects from the database.

        Returns:
            list: A list of LanguageList instances.
        """
        from data.Database import Database
        return Database.get_data()

    @staticmethod
    def rebuild_data():
        from data.Database import Database

        return Database.rebuild_data()
