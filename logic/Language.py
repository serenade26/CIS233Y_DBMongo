"""Language class module.

File: Language.py
Author: Alexander Leykand
Date: 05/21/2026
Assignment: Module 7

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

    def __init__(self, name, application_domain, programming_paradigm, execution_method, typing, save=False):
        """Initialize a Language object.

        Args:
            name (str): The name of the programming language.
            application_domain (str): The primary domain in
                which the language is commonly used.
            programming_paradigm (str): The programming
                paradigm supported by the language.
            execution_method (str): How the language is
                executed, such as compiled or interpreted.
            typing (str): The typing discipline of the
                language, such as static or dynamic.
            save (bool): Whether the object should be
                immediately persisted to the database.
        """
        self.__name = name
        self.__application_domain = application_domain
        self.__programming_paradigm = programming_paradigm
        self.__execution_method = execution_method
        self.__typing = typing
        self.__class__.__map[self.get_key()] = self
        if save:
            self.save()

    @classmethod
    def build(cls, language_dict):
        """Construct a Language or LanguageExposure object from a dictionary.

        Rebuilds persisted language data retrieved from MongoDB
        into the appropriate Python object type based on the
        stored document type field.

        Args:
            language_dict (dict): Dictionary representation
                of a persisted Language or LanguageExposure
                object.

        Returns:
            Language or LanguageExposure: The reconstructed
            language object.
        """

        from logic.LanguageExposure import LanguageExposure

        if language_dict["type"] == "Language":
            return Language(language_dict["name"],
                            language_dict["application_domain"],
                            language_dict["programming_paradigm"],
                            language_dict["execution_method"],
                            language_dict["typing"])
        elif language_dict["type"] == "LanguageExposure":
            return LanguageExposure(language_dict["name"],
                                    language_dict["application_domain"],
                                    language_dict["programming_paradigm"],
                                    language_dict["execution_method"],
                                    language_dict["typing"],
                                    language_dict["year_last_used"],
                                    language_dict["years_of_exposure"],
                                    language_dict["version_last_used"]
                                    )

    def to_dict(self):
        """Return a dictionary representation of the Language object.

        Converts the Language instance into a MongoDB-compatible
        dictionary structure suitable for persistence.

        Returns:
            dict: Serialized Language object data.
        """
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
        """Update the language application domain.

        Modifies the stored application domain value and
        persists the updated object to the database.

        Args:
            application_domain (str): The new application
                domain value.
        """
        self.__application_domain = application_domain
        self.save()

    @classmethod
    def lookup(cls, key):
        """Retrieve a Language object by its key.

        Args:
            key (str): The lookup key (language name in lowercase).

        Returns:
            Language or None: The matching Language object, or None if not found.
        """
        if key.lower() in cls.__map:
            return cls.__map[key]
        else:
            return None

    def delete(self):
        """Delete the Language object from the application.

        Removes the Language instance from the class-level
        lookup registry and deletes its persisted database
        document.
        """
        from data.Database import Database

        del self.__class__.__map[self.get_key()]
        Database.delete_language(self)

    def __str__(self):
        """Return a human-readable string representation of the language.

        Returns:
            str: A descriptive summary of the language.
        """
        return (f"<{self.__name} used in {self.__application_domain} environment as"
                f" {self.__programming_paradigm}"
                f" language, executed as {self.__execution_method} with {self.__typing} typing >")

    def to_html(self):
        """Return an HTML-formatted representation of the language.

        The generated HTML string is intended for rendering in
        Flask/Jinja templates and includes basic formatting tags
        describing the language and its characteristics.

        Returns:
            str: An HTML-formatted description of the language.
        """
        return (f"<strong>{self.__name}</strong> used in {self.__application_domain} environment as"
                f" {self.__programming_paradigm}"
                f" language, executed as {self.__execution_method} with {self.__typing} typing")

    @staticmethod
    def get_languages():
        """Retrieve all Language objects from the database.

        Returns:
            list: A list of Language instances.
        """
        from data.Database import Database
        return Database.get_data()

    def save(self):
        """Persist the Language object to the database.

        Inserts or updates the Language document in MongoDB
        using the object's lookup key as its identifier.
        """
        from data.Database import Database

        Database.save_language(self)
