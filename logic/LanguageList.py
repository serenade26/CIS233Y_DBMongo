"""LanguageList module.

File: LanguageList.py
Author: Alexander Leykand
Date: 05/14/2026
Assignment: Module 6

This module defines the LanguageList class, which represents a
named collection of Language objects. It supports iteration,
membership testing, addition (merging of lists), and basic
CRUD-style persistance operations. LanguageList instances are
also registeredin a class-level dictionary for lookup.
"""
from logic.Language import Language


class LanguageList:
    """Represent a named collection of Language objects.

    A LanguageList groups Language instances under a shared
    category name and description. It supports iteration,
    membership testing, modification, merging, and persistence
    through a backing database.
    """
    ALL_LANGUAGES = "All Languages"
    __name = ""
    __languages = []
    __description = ""
    __map = {}

    def __init__(self, name, languages, description, save=False):
        """Initialize a LanguageList object.

        Args:
            name (str): Name of the language list.
            languages (list): Initial list of Language objects.
            description (str): Description of the language group.
            save (bool): If True, persist the object to the database.
        """
        self.__name = name
        self.__languages = languages
        self.__description = description
        self.__class__.__map[self.get_key()] = self
        if save:
            self.save()

    @classmethod
    def build(cls, languagelist_dict):
        """Reconstruct a LanguageList object from a dictionary.

        Builds a LanguageList instance from persisted MongoDB
        data, resolving stored language keys into Language objects.

        Args:
            languagelist_dict (dict): Serialized LanguageList data.

        Returns:
            LanguageList: Reconstructed LanguageList instance.
        """
        from logic.Language import Language
        return LanguageList(languagelist_dict["name"],
                            [Language.lookup(key) for key in languagelist_dict["languages"]],
                            languagelist_dict["description"])

    def to_dict(self):
        """Convert the LanguageList object to a MongoDB-compatible dictionary.

        Returns:
            dict: Serialized representation of the LanguageList,
            including language keys and metadata.
        """
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

    def __str__(self):
        """Return a human-readable summary of the LanguageList.

        Returns:
            str: Name, description, and contained languages.
        """
        return (f"Language List: {self.__name}  Description: {self.__description} \n Languages:"
                f" {', '.join([language.get_name() for language in self.__languages])}")

    @classmethod
    def lookup(cls, key):
        """Retrieve a LanguageList from the class registry.

        Args:
            key (str): Lookup key (case-insensitive list name).

        Returns:
            LanguageList or None: Matching object or None.
        """
        if key.lower() in cls.__map:
            return cls.__map[key.lower()]
        else:
            return None

    def append(self, language, save=True):
        """Add a Language to this LanguageList.

        Args:
            language (Language): Language to add.
            save (bool): If True, persist updated list to database.
        """
        from data.Database import Database

        self.__languages.append(language)
        if save:
            Database.save_languagelist(self)

    def remove(self, language):
        """Remove a Language from this LanguageList.

        Also persists the updated list to the database.

        Args:
            language (Language): Language to remove.
        """
        from data.Database import Database

        self.__languages.remove(language)
        Database.save_languagelist(self)

    def delete(self):
        """Delete this LanguageList from memory and persistence.

        Removes the object from the class registry and deletes
        its corresponding database document.
        """
        from data.Database import Database

        del self.__class__.__map[self.get_key()]
        Database.delete_languagelist(self)

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
        """Merge two LanguageList objects into a new one and persist it.

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
                new_languagelist.append(language, save=False)
        for language in other:
            if language not in new_languagelist:
                new_languagelist.append(language, save=False)
        new_languagelist.save()
        return new_languagelist

    @staticmethod
    def get_languagelists():
        """Retrieve all LanguageList objects from the database.

        Returns:
            tuple: Seed data returned from the database layer.
        """
        from data.Database import Database
        return Database.get_data()

    @staticmethod
    def rebuild_data():
        """Rebuild all LanguageList data in the database.

        Deletes and recreates persisted collections using seed data.
        """
        from data.Database import Database

        return Database.rebuild_data()

    @staticmethod
    def read_data():
        """Load all LanguageList data from the database.

        Returns reconstructed LanguageList objects from persisted data.
        """
        from data.Database import Database

        return Database.read_data()

    def save(self):
        """Persist this LanguageList to the database.

        Inserts or updates the LanguageList document using its
        lookup key as the identifier.
        """
        from data.Database import Database

        Database.save_languagelist(self)
