"""rebuild_database module.

File: rebuild_database.py
Author: Alexander Leykand
Date: 05/07/2026
Assignment: Module 5

 Rebuild language list seed data.

This module executes the LanguageList.rebuild_data() method when run
directly, allowing database or application seed data to be refreshed.
"""
from logic.LanguageList import LanguageList

if __name__ == "__main__":
    LanguageList.rebuild_data()
