"""Database module.

File: Database.py
Author: Alexander Leykand
Date: 05/14/2026
Assignment: Module 6

Provides MongoDB-backed storage and seed data for language objects.

This module defines the Database class, which manages MongoDB
connections and constructs collections of Language,
LanguageExposure, and LanguageList objects used within the
application. It can also be executed directly for testing or
database initialization purposes.
"""
from logic.Language import Language
from logic.LanguageExposure import LanguageExposure
from logic.LanguageList import LanguageList
from pymongo import MongoClient
from pymongo.server_api import ServerApi


class Database:
    """Manage MongoDB persistence for language catalog data.

    This class provides centralized access to MongoDB
    connectivity, collection management, seed data creation,
    and CRUD-style persistence operations for Language and
    LanguageList objects.
    """
    PASSWORD = 'CIS233Y'
    USER = 'alexanderleykand'
    CLUSTER = 'cluster0.oyqujth.mongodb.net'
    __connection = None
    __database = None
    __languages_collection = None
    __languagelists_collection = None
    URI = f"mongodb+srv://{USER}:{PASSWORD}@{CLUSTER}/?appName=Cluster0"

    @classmethod
    def connect(cls):
        """Establish a MongoDB connection if one does not already exist.

          Initializes:
              - MongoDB client connection
              - LanguageCatalog database reference
              - Languages collection
              - LanguageLists collection

          Returns:
              None
          """
        if cls.__connection is None:
            cls.__connection = MongoClient(cls.URI, server_api=ServerApi('1'))
            cls.__database = cls.__connection.LanguageCatalog
            cls.__languages_collection = cls.__database.Languages
            cls.__languagelists_collection = cls.__database.LanguageLists

        """ print("Connection: ", cls.__connection)
            print("Database: ", cls.__database)
            print("Languages collection: ", cls.__languages_collection)
            print("LanguageLists collection: ", cls.__languagelists_collection) """

    @classmethod
    def rebuild_data(cls):
        """Drop and rebuild all database collections with seed data.

             This method:
                 1. Establishes a connection
                 2. Drops existing collections
                 3. Recreates collection references
                 4. Inserts predefined language data

        Returns:
                 None
        """

        cls.connect()
        cls.__languages_collection.drop()
        cls.__languagelists_collection.drop()
        cls.__languages_collection = cls.__database.Languages
        cls.__languagelists_collection = cls.__database.LanguageLists
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
        cls.__languagelists_collection.update_one({"_id": languagelist.get_key()}, {"$set": languagelist.to_dict()}, upsert=True)

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
