"""WebUI class module.

File: Language.py
Author: Alexander Leykand
Date: 05/21/2026
Assignment: Module 7

This module defines the WebUI class, which manages browser-based
interaction with Language and LanguageList objects using the
Flask web framework. It supports rendering HTML templates,
displaying language data, and handling user requests through
URL routes.

The module serves as the main entry point for the web version
of the application and initializes application data from the
database before starting the Flask development server.
"""
from flask import Flask, render_template, request
from logic.LanguageList import LanguageList


class WebUI:
    """Provide a Flask-based web interface for the Language Catalog application.

    This class manages:
        - Initialization of language and language list data
        - Flask route registration
        - Rendering of HTML templates
        - User interaction through browser-based pages

    The application supports viewing and managing programming
    languages and categorized language lists.
    """
    __all_languages = None
    __all_languagelists = None
    __app = Flask(__name__)
    MENU = {
        "Print": {"print_languagelist?languagelist=All%20Languages": "Print a list of all languages.",
                  "print_languagelists": "Print a list of all Language Lists"},
        "Create": {"create_language": "Create a new language.",
                   "create_languagelist": "Create a new Language List",
                   "join_languagelists": "Join two Language Lists together."},
        "Update": {"update_language": "Update computer language.",
                   "add_language_to_languagelist": "Add Computer Language to the List",
                   "remove_language_from_languagelist": "Remove Computer Language from the List"},
        "Delete": {"delete_language": "Delete language.",
                   "delete_languagelist": "Delete a Language List"}
    }

    @classmethod
    def init(cls):
        """Initialize application data from the database.

        Retrieves all available Language and LanguageList objects
        and stores them for use by the web interface.
        """
        cls.__all_languages, cls.__all_languagelists = LanguageList.read_data()

    @__app.route('/')
    @__app.route('/index')
    @__app.route('/index.html')
    @__app.route('/index.php')
    @staticmethod
    def homepage():
        """Render the application homepage.

        Returns:
            str: Rendered homepage template containing the
            application menu options.
        """
        return render_template('homepage.html', options=WebUI.MENU)

    @__app.route('/print_languagelists')
    @staticmethod
    def print_languagelists():
        """Display all available language lists.

        Returns:
            str: Rendered template showing all LanguageList objects.
        """
        return render_template('print/print_languagelists.html', languagelists=WebUI.__all_languagelists)

    @__app.route('/print_languagelist')
    @staticmethod
    def print_languagelist():
        """Display a single LanguageList and its contents.

        The target LanguageList is specified through the
        'languagelist' URL query parameter.

        Returns:
           str: Rendered LanguageList template if found,
           otherwise an error page.
        """
        if "languagelist" not in request.args:
            return render_template("error.html", message_header="Unspecified Language List",
                                   message_body="No Language List specified. Check the URL and try again.")
        key = request.args["languagelist"]
        languagelist = LanguageList.lookup(key)
        if languagelist is None:
            return render_template("error.html", message_header="Language List not found",
                                   message_body=f"Language List {key} not found. Check the URL and try again.")
        return render_template("print/print_languagelist.html", languagelist=languagelist)

    @classmethod
    def run(cls):
        """Start the Flask web application server.

        Launches the application on port 8000.
        """
        cls.__app.run(port=8000)


if __name__ == '__main__':
    """Run the WebUI application.

    This block executes when the module is run directly.
    It initializes application data and starts the Flask server.
    """
    WebUI().init()
    WebUI().run()
