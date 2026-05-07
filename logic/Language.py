"""Language class module.

File: Language.py
Author: Alexander Leykand
Date: 05/07/2026
Assignment: Module 5

This module defines the Language class, which represents a programming
language and its core characteristics, such as application domain,
programming paradigm, execution method, and typing discipline.

Each Language instance is automatically registered in a class-level
dictionary for lookup and management. The module also provides access
to all Language objects via a connection to the application database.
"""


class Language:
    """Represents a programming language and its core characteristics.

    Each Language object stores descriptive attributes such as application
    domain, programming paradigm, execution method, and typing discipline.
    Instances are automatically registered in a class-level dictionary
    for retrieval by key.
    """
    __name = ""
    __application_domain = ""
    __programming_paradigm = ""
    __execution_method = ""
    __typing = ""
    __map = {}

    def __init__(self, name, application_domain, programming_paradigm, execution_method, typing):
        """Initialize a Language object.

        Args:
            name (str): The name of the programming language.
            application_domain (str): The primary domain in which the language is used.
            programming_paradigm (str): The programming paradigm supported by the language.
            execution_method (str): How the language is executed (e.g., compiled or interpreted).
            typing (str): The typing discipline of the language (e.g., static or dynamic).
        """
        self.__name = name
        self.__application_domain = application_domain
        self.__programming_paradigm = programming_paradigm
        self.__execution_method = execution_method
        self.__typing = typing
        self.__class__.__map[self.get_key()] = self

    def to_dict(self):
        """Return a dictionary representation of the Language object."""
        return {
            "_id": self.get_key(),
            "type": "Language",
            "name": self.__name,
            "application_domain": self.__application_domain,
            "programming_paradigm": self.__programming_paradigm,
            "execution_method": self.__execution_method,
            "typing": self.__typing
        }

    def get_key(self):
        """Return a normalized key used to identify this language.

        Returns:
            str: The lowercase name of the language.
        """
        return f"{self.__name}".lower()

    def get_name(self):
        """Return the name of the programming language.

        Returns:
            str: The language name.
        """
        return self.__name

    def update_application_domain(self, application_domain):
        """Update the application domain of the language.

           Args:
               application_domain (str): The new application domain.
           """
        self.__application_domain = application_domain

    @classmethod
    def lookup(cls, key):
        """Retrieve a Language object by its key.

        Args:
            key (str): The lookup key (language name in lowercase).

        Returns:
            Language or None: The matching Language object, or None if not found.
        """
        if key in cls.__map:
            return cls.__map[key]
        else:
            return None

    def delete(self):
        """Remove this Language instance from the class-level registry."""
        del self.__class__.__map[self.get_key()]

    def __str__(self):
        """Return a human-readable string representation of the language.

        Returns:
            str: A descriptive summary of the language.
        """
        return (f"<{self.__name} used in {self.__application_domain} environment as"
                f" {self.__programming_paradigm} "
                f" language, executed as {self.__execution_method} with {self.__typing} typing >")

    @staticmethod
    def get_languages():
        """Retrieve all Language objects from the database.

        Returns:
            list: A list of Language instances.
        """
        from data.Database import Database
        return Database.get_data()
