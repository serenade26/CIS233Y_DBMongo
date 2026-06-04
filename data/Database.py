"""Database module.

File: Database.py
Author: Alexander Leykand
Date: 06/03/2026
Assignment: Module 9

Provides MongoDB-backed storage and seed data for application objects.

This module defines the Database class, which manages MongoDB
connections and constructs collections of Language,
LanguageExposure, LanguageList, and User objects used within
the application. It can also be executed directly for testing
or database initialization purposes.
"""
from logic.Language import Language
from logic.LanguageExposure import LanguageExposure
from logic.LanguageList import LanguageList
from logic.User import User
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from configparser import ConfigParser
from logic.utilities import get_ini_file


class Database:
    """Manage MongoDB persistence for application data.

    This class provides centralized access to MongoDB
    connectivity, collection management, seed data creation,
    and CRUD-style persistence operations for Language,
    LanguageList, and User objects.
    """
    """ PASSWORD = 'CIS233Y'
    USER = 'alexanderleykand'
    CLUSTER = 'cluster0.oyqujth.mongodb.net' """
    __connection = None
    __database = None
    __languages_collection = None
    __languagelists_collection = None
    __users_collection = None
    APP_NAME = "language_catalog"

    @classmethod
    def connect(cls):
        """Establish a MongoDB connection if one does not already exist.

        Initializes:
            - MongoDB client connection
            - LanguageCatalog database reference
            - Languages collection
            - LanguageLists collection
            - Users collection

        Returns:
            None
        """
        if cls.__connection is None:
            path, file = get_ini_file(cls.APP_NAME)
            config_parser = ConfigParser()
            config_parser.read(file)
            username = config_parser["Database"]["USER"]
            password = config_parser["Database"]["PASSWORD"]
            cluster = config_parser["Database"]["CLUSTER"]
            uri = f"mongodb+srv://{username}:{password}@{cluster}/?appName=Cluster0"
            cls.__connection = MongoClient(uri, server_api=ServerApi('1'))
            cls.__database = cls.__connection.LanguageCatalog
            cls.__languages_collection = cls.__database.Languages
            cls.__languagelists_collection = cls.__database.LanguageLists
            cls.__users_collection = cls.__database.Users

        """ print("Connection: ", cls.__connection)
            print("Database: ", cls.__database)
            print("Languages collection: ", cls.__languages_collection)
            print("LanguageLists collection: ", cls.__languagelists_collection) """

    @classmethod
    def rebuild_data(cls):
        """Drop and rebuild all database collections with seed data.

        This method:
            1. Establishes a database connection
            2. Drops existing collections
            3. Recreates collection references
            4. Inserts predefined user accounts
            5. Inserts predefined language data
            6. Inserts predefined language list data

        Returns:
            None
        """

        cls.connect()
        cls.__languages_collection.drop()
        cls.__languagelists_collection.drop()
        cls.__users_collection.drop()
        cls.__languages_collection = cls.__database.Languages
        cls.__languagelists_collection = cls.__database.LanguageLists
        cls.__users_collection = cls.__database.Users
        user = User("Alex", b'$2b$13$PlMxb/WrvtKkWPaMYdtNUu0ox.lyTghllW45Pqrez.T0DF1iAAlgK')
        user_Marc = User("Marc", b'$2b$13$nJWdalQC4isVBwBpd/jtn.OQgBeof7T5GhhgPoGe6tjDseusGz8Ou')
        user2 = User("Admin", b'$2b$13$DfaEBYA3TrvjPgTxd8F4ze8aW/nrFJfQswCeIFDvYg.I6.uuyrnYa')
        user_dicts = [user.to_dict() for user in [user, user_Marc, user2]]
        cls.__users_collection.insert_many(user_dicts)
        #  cls.__users_collection.insert_one(user.to_dict())   when only 1 user
        all_languages, all_languagelists = cls.get_data()
        language_dict = [language.to_dict() for language in all_languages]
        cls.__languages_collection.insert_many(language_dict)
        languagelist_dict = [languagelist.to_dict() for languagelist in all_languagelists]
        cls.__languagelists_collection.insert_many(languagelist_dict)

    @classmethod
    def read_data(cls):
        """Retrieve persisted Language and LanguageList data.

        Loads Language and LanguageList documents from MongoDB,
        reconstructs their corresponding Python objects, and
        restores object relationships through lookup mappings.

        Returns:
            tuple:
                - LanguageList: The master "All Languages" list.
                - list[LanguageList]: All persisted LanguageList
                  objects.
        """
        cls.connect()
        language_dicts = list(cls.__languages_collection.find())  # make a list from iterable to iterate repeatedly
        languages = [Language.build(language_dict) for language_dict in language_dicts]

        languagelist_dicts = list(
            cls.__languagelists_collection.find())  # make a list from iterable to iterate repeatedly
        languagelists = [LanguageList.build(languagelist_dict) for languagelist_dict in languagelist_dicts]

        return LanguageList.lookup(LanguageList.ALL_LANGUAGES), languagelists

    @classmethod
    def get_data(cls):
        """Create and return predefined language collections.

        Returns:
            tuple:
                - LanguageList: A master list containing all languages.
                - list[LanguageList]: A list of categorized LanguageList
                  instances (including the master list).
        """
        c = LanguageExposure("C", "Systems Programming", "Procedural",
                             "Compiled", "Static", 1996,
                             0.5, "C90")
        ada = Language("Ada", "Systems Programming", "Object-Oriented",
                       "Compiled", "Static")
        cobol = LanguageExposure("COBOL", "Commercial", "Procedural",
                                 "Compiled", "Static", 2005,
                                 5, "ILE V5R6")
        swift = Language("Swift", "General Purpose", "Multi-Paradigm",
                         "Compiled", "Static")
        systems = LanguageList("Systems Programming", [c, ada],
                               "Languages that are used for system-level programming")
        general = LanguageList("General Purpose", [swift],
                               "Capable of variety of programming tasks")
        all = LanguageList(LanguageList.ALL_LANGUAGES, [c, ada, cobol, swift],
                           "All Languages")
        return all, [all, systems, general]

    @classmethod
    def read_user(cls, username):
        """Retrieve a User object by username.

        Searches the users collection for a user whose
        username matches the specified value (case-insensitive).
        If a matching record is found, a User object is
        constructed and returned. Otherwise, None is returned.

        Args:
            username (str): Username of the account to retrieve.

        Returns:
            User | None: The matching User object if found,
            otherwise None.
        """
        user_dict = cls.__users_collection.find_one({"_id": username.lower()})
        if user_dict is None:
            return None
        else:
            return User.build(user_dict)

    @classmethod
    def save_languagelist(cls, languagelist):
        """Insert or update a LanguageList document in MongoDB.

        Persists the provided LanguageList object using its
        lookup key as the MongoDB document identifier. Existing
        documents are updated and missing documents are created.

        Args:
            languagelist (LanguageList): The LanguageList object
                to persist.
        """
        cls.connect()
        cls.__languagelists_collection.update_one({"_id": languagelist.get_key()}, {"$set": languagelist.to_dict()},
                                                  upsert=True)

    @classmethod
    def save_language(cls, language):
        """Insert or update a Language document in MongoDB.

        Persists the provided Language object using its lookup
        key as the MongoDB document identifier. Existing
        documents are updated and missing documents are created.

        Args:
            language (Language): The Language object to persist.
        """
        cls.connect()
        cls.__languages_collection.update_one({"_id": language.get_key()}, {"$set": language.to_dict()}, upsert=True)

    @classmethod
    def delete_languagelist(cls, languagelist):
        """Delete a LanguageList document from MongoDB.

        Removes the document associated with the provided
        LanguageList object's lookup key.

        Args:
            languagelist (LanguageList): The LanguageList object
                to delete.
        """
        cls.connect()
        cls.__languagelists_collection.delete_one({"_id": languagelist.get_key()})

    @classmethod
    def delete_language(cls, language):
        """Delete a Language document from MongoDB.

        Removes the document associated with the provided
        Language object's lookup key.

        Args:
            language (Language): The Language object to delete.
        """
        cls.connect()
        cls.__languages_collection.delete_one({"_id": language.get_key()})


if __name__ == '__main__':
    # Establish a database connection when the module
    # is executed directly.
    Database.connect()
