"""read_database module.

File: read_database.py
Author: Alexander Leykand
Date: 05/14/2026
Assignment: Module 6
Console script for loading and displaying Language data from the database.

This module serves as a simple entry point for testing database retrieval.
It loads all Language and LanguageList objects via the LanguageList
data access layer and prints them to the console in a readable format.
"""
from logic.LanguageList import LanguageList

if __name__ == "__main__":
    all_languages, all_languagelists = LanguageList.read_data()
    print("Languages:")
    for language in all_languages:
        print(language)
    print()
    for languagelist in all_languagelists:
        print(languagelist)