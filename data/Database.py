"""Database module.

File: Database.py
Author: Alexander Leykand
Date: 05/07/2026
Assignment: Module 5

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
    """Manage MongoDB connectivity and seed language catalog data.

    This class provides:
        - MongoDB connection management
        - Database/collection initialization
        - Rebuilding seed data
        - Factory methods for predefined language objects
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

            print("Connection: ", cls.__connection)
            print("Database: ", cls.__database)
            print("Languages collection: ", cls.__languages_collection)
            print("LanguageLists collection: ", cls.__languagelists_collection)

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


if __name__ == '__main__':
    Database.connect()
