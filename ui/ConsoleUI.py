"""ConsoleUI module.

File: ConsoleUI.py
Author: Alexander Leykand
Date: 05/14/2026
Assignment: Module 6

This module defines the ConsoleUI class, which provides a simple
command-line interface for interacting with Language, LanguageList,
and LanguageExposure data. It supports menu-driven user interaction
for creating, updating, displaying, and managing programming language
information and language lists.
"""

from logic.LanguageList import LanguageList
from logic.Language import Language
from logic.LanguageExposure import LanguageExposure
from ui.input_validation import select_item, input_string, y_or_n, input_int, input_float


class ConsoleUI:
    """Console-based user interface for managing language data.

    This class provides a menu-driven interface for interacting with
    Language, LanguageList, and LanguageExposure objects. It handles
    user input, validation, and coordination between the UI and data layer.
    """
    __all_languages = None
    __all_languagelists = []
    CHOICES = ['x', 'a', 'l', 'c', 'd', 's', 'i', 'k', 'r', 'u', 'j', 'z']

    @classmethod
    def init(cls):
        """Load language and languagelist data into the UI layer.

        Retrieves persisted Language and LanguageList objects
        from the configured data source and stores them for
        interactive use within the console application.
        """

        cls.__all_languages, cls.__all_languagelists = LanguageList.read_data()

    @classmethod
    def select_language(cls, prompt, languagelist=None):
        """Prompt the user to select a Language.

        Args:
            prompt (str): The input prompt to display.
            languagelist (iterable, optional): Collection of languages to choose from.
                Defaults to all available languages.

        Returns:
            Language or None: The selected Language object, or None if cancelled.
        """
        if languagelist is None:
            languagelist = cls.__all_languages
        keys = []
        for language in languagelist:
            keys.append(language.get_key())
        keys.append("None")
        key = select_item(prompt=prompt, choices=keys, error="Invalid Language entered")
        if key == "None":
            return None
        language = Language.lookup(key.lower())
        return language

    @classmethod
    def select_languagelist(cls, prompt, include_all_languagelists=False):
        """Prompt the user to select a LanguageList.

        Args:
            prompt (str): Input prompt to display.
            include_all_languagelists (bool): Whether to include the full list group.

        Returns:
            LanguageList or None: Selected LanguageList, or None if cancelled.
        """
        names = []
        map = {}
        pos = 1
        for languagelist in cls.__all_languagelists:
            if include_all_languagelists or languagelist.get_name() != LanguageList.ALL_LANGUAGES:
                names.append(languagelist.get_name())
                map[str(pos)] = languagelist.get_key()
                pos += 1
        names.append("None")
        map[str(pos)] = "None"
        print("Available Language Lists:")
        pos = 1
        for name in names:
            print(f"{pos}: {name}")
            pos += 1

        name = select_item(prompt=prompt, choices=names, error="Invalid Language List entered", mappings=map)
        if name == "None":
            return None
        languagelist = LanguageList.lookup(name.lower())
        return languagelist

    @classmethod
    def list_languages(cls):
        """Display all available languages.

        This method iterates through the stored Language objects
        and prints each language's key and descriptive string
        representation to the console.
        """
        for language in cls.__all_languages:
            print(language.get_key(), ": ", language, sep="")

    @classmethod
    def list_languagelists(cls):
        """Display all available language lists.

        This method iterates through the stored Language List
        objects and prints each language's key and descriptive
        string representation to the console.
        """
        for languagelist in cls.__all_languagelists:
            print(languagelist.get_name(), ": ", languagelist.get_description(), sep="")

    @classmethod
    def create_languagelist(cls):
        """Create and register a new LanguageList.

        Prompts the user for a list name and description,
        validates that the name is unique, creates the
        LanguageList object, and stores it in the active
        collection.
        """
        name = input_string(prompt="Enter a language list name or 'None' to exit: (string)", error="Cannot be empty")
        if name.lower() != "none":
            languagelist = LanguageList.lookup(name.lower())
            if languagelist is not None:
                print("Error: Language list already exists!")
                return
            description = input_string(prompt="Enter a language list description: (optional string)", valid=lambda x: True)  # allow empty
            languagelist = LanguageList(name, [], description, save=True)
            cls.__all_languagelists.append(languagelist)
            print(f"Language List {languagelist.get_name()} created")

    @classmethod
    def delete_languagelist(cls):
        """Delete an existing LanguageList.

        Prompts the user to select a language list,
        removes it from the active collection, and
        unregisters it from the lookup registry.
        """
        languagelist = cls.select_languagelist("Select Language List to delete or 'None' to exit: ")
        if languagelist is None:
            return
        deleted = languagelist.get_name()
        cls.__all_languagelists.remove(languagelist)
        languagelist.delete()

        print(f"Language List {deleted} deleted")

    @classmethod
    def show_languagelist(cls):
        """Display a selected LanguageList and its contents."""
        languagelist = cls.select_languagelist("Select Language List to display or 'None' to exit",
                                               True)
        if languagelist is None:
            return
        print(f"Language List: {languagelist.get_name()}")
        print(f"Description: {languagelist.get_description()}")
        print("Languages in the list: ")
        for language in languagelist:
            print(f"{language}")

    @classmethod
    def create_language(cls):
        """Create a new Language or LanguageExposure object.

        Prompts the user for language attributes and
        optionally collects exposure-related information
        when creating a LanguageExposure instance. The new
        object is registered and added to the active
        language collection.
        """
        language_exposure = y_or_n(prompt="Did you have any experience with this the language (y/n): ")

        name = input_string(prompt="Enter a language name: (string)")
        if Language.lookup(name) is not None:
            print("Error: Language already exists!")
            return
        application_domain = input_string(prompt="Enter its application domain: (string)")
        programming_paradigm = input_string(prompt="Enter its programming paradigm: (string)")
        execution_method = input_string(prompt="Enter its execution method: (string)")
        typing = input_string(prompt="Enter its typing: (string)")
        if language_exposure:
            year_last_used = input_int(prompt="Enter year last used: (integer)", ge=1940, lt=2100)
            years_of_exposure = input_float(prompt="How many years used: (decimal)", gt=0, lt=100)
            version_last_used = input_string("Last version used: (string)", valid=lambda x: True)  # allow empty
            language = LanguageExposure(name, application_domain, programming_paradigm, execution_method,
                                        typing, year_last_used, years_of_exposure, version_last_used, save=True)
        else:
            language = Language(name, application_domain, programming_paradigm, execution_method, typing, save=True)
        cls.__all_languages.append(language)
        print(f"Language {language.get_name()} created")

    @classmethod
    def delete_language(cls):
        """Delete a Language from the application.

        Removes the selected Language from all LanguageList
        objects that contain it, unregisters the Language
        from the lookup registry, and deletes its persisted
        data.
        """
        language = cls.select_language("Select Language to Delete: ")
        if language is not None:
            for languagelist in cls.__all_languagelists:
                if language in languagelist:
                    languagelist.remove(language)
            delete = language.get_name()
            language.delete()
            print(f"Language {delete} deleted")

    @classmethod
    def add_language(cls):
        """Add a Language to a selected LanguageList.

        Prompts the user to select both a LanguageList and
        a Language. Prevents duplicate membership within
        the target list.
        """
        languagelist = cls.select_languagelist("Select Language List to add Language to or 'None' to exit")
        if languagelist is not None:
            language = cls.select_language("Select the Language to add: ")
            if language is not None:
                if language not in languagelist:
                    languagelist.append(language)
                    print(f"Language {language.get_name()} added to {languagelist.get_name()} list")
                else:
                    print("Error: Language already exists in Language List!")

    @classmethod
    def remove_language(cls):
        """Remove a Language from a selected LanguageList.

        Prompts the user to select a LanguageList and one
        of its associated languages, then removes the
        selected Language from the list.
        """
        languagelist = cls.select_languagelist("Select a Language List to remove a Language from or 'None' to exit")
        if languagelist is not None:
            language = cls.select_language("Select the Language to remove: ", languagelist=languagelist)
            if language is not None:
                if language not in languagelist:
                    print("Error: That Language is NOT in the Language List!")
                else:
                    languagelist.remove(language)
                    print(f"Language {language.get_name()} removed from {languagelist.get_name()} list")

    @classmethod
    def update_language(cls):
        """Update the application domain of an existing Language.

        Prompts the user to select a Language object and
        enter a new application domain value.
        """
        language = cls.select_language("Select the Language to update or 'None' to exit")
        if language is not None:
            application_domain = input_string(prompt="Enter its application domain: (string)")
            language.update_application_domain(application_domain)
            print("Language updated!")

    @classmethod
    def join_languagelists(cls):
        """Merge two LanguageLists into a new combined list.

        Creates a new LanguageList containing the unique
        Language objects from both selected lists and adds
        the merged list to the active collection.
        """
        languagelist1 = cls.select_languagelist("Select the first Language List to join or 'None' to exit",
                                                include_all_languagelists=True)
        if languagelist1 is not None:
            languagelist2 = cls.select_languagelist("Select the second Language List to join or 'None' to exit",
                                                    include_all_languagelists=True)
            if languagelist2 is not None:
                new_languagelist = languagelist1 + languagelist2
                cls.__all_languagelists.append(new_languagelist)
                print(f"Language list {languagelist1.get_name()} added to {languagelist2.get_name()} list")

    @staticmethod
    def print_menu():
        """Display the main menu options.

        This method prints the list of available user actions
        to the console.
        """
        print("Select an option:")
        print("*   a: List Computer Languages")
        print("*   l: List Computer Language Lists")
        print("*   c: Create Computer Language List")
        print("*   j: Join Computer Language Lists")
        print("*   i: Create Computer Language")
        print("*   z: Delete Computer Language")
        print("*   k: Add Computer Language to the List")
        print("*   s: Show Computer Language List")
        print("*   d: Delete Computer Language List")
        print("*   r: Remove Computer Language from the List")
        print("*   u: Update Computer Language")
        print("*   x: Exit")

    @classmethod
    def run(cls):
        """Run the main application loop.

        This method repeatedly displays the menu, prompts the
        user for a selection, validates the input, and performs
        the requested action until the user chooses to exit.
        """
        while True:
            cls.print_menu()
            choice = select_item(prompt="Select from the menu",
                                 error="Item must be a choice in the menu",
                                 choices=ConsoleUI.CHOICES)
            print()
            if choice.lower() == 'x':
                break
            elif choice.lower() == 'l':
                cls.list_languagelists()
            elif choice.lower() == 'a':
                cls.list_languages()
            elif choice.lower() == 'c':
                cls.create_languagelist()
            elif choice.lower() == 's':
                cls.show_languagelist()
            elif choice.lower() == 'd':
                cls.delete_languagelist()
            elif choice.lower() == 'i':
                cls.create_language()
            elif choice.lower() == 'k':
                cls.add_language()
            elif choice.lower() == 'r':
                cls.remove_language()
            elif choice.lower() == 'u':
                cls.update_language()
            elif choice.lower() == 'j':
                cls.join_languagelists()
            elif choice.lower() == 'z':
                cls.delete_language()
            print()
        print("Bye now!")


if __name__ == "__main__":
    """Execute the ConsoleUI application.

    This block runs when the module is executed directly.
    It initializes the user interface and starts the main
    program loop.
    """
    ConsoleUI.init()
    ConsoleUI.run()
