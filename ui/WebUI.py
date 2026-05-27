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
from logic.Language import Language
from logic.LanguageExposure import LanguageExposure


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
                  "print_languagelists": "Print a list of all Language Lists.",
                  "show_languagelist_contents": "Select a Language List to show its contents."},
        "Create": {"create_language": "Create a new language.",
                   "create_languageexposure": "Create a new language that I have experience with.",
                   "create_languagelist": "Create a new Language List.",
                   "join_languagelists": "Join two Language Lists together."},
        "Update": {"update_language": "Update computer language.",
                   "add_language_to_languagelist": "Add Computer Language to the List.",
                   "remove_language_from_languagelist": "Remove Computer Language from the List."},
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

    @classmethod
    def validate_input(cls, field_name):
        if field_name not in request.form:
            return None, render_template("error.html", message_header=f"Unspecified {field_name}",
                                         message_body=f"No {field_name} specified. Check the form and try again.")
        field_value = request.form[field_name].strip()
        if field_value == "":
            return None, render_template("error.html", message_header=f"Unspecified {field_name}",
                                         message_body=f"No {field_name} specified. Check the form and try again.")
        return field_value, None

    @staticmethod
    @__app.route('/')
    @__app.route('/index')
    @__app.route('/index.html')
    @__app.route('/index.php')
    def homepage():
        """Render the application homepage.

        Returns:
            str: Rendered homepage template containing the
            application menu options.
        """
        return render_template('homepage.html', options=WebUI.MENU)

    @staticmethod
    @__app.route('/print_languagelists')
    def print_languagelists():
        """Display all available language lists.

        Returns:
            str: Rendered template showing all LanguageList objects.
        """
        return render_template('print/print_languagelists.html', languagelists=WebUI.__all_languagelists)

    @staticmethod
    @__app.route('/print_languagelist')
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

    @staticmethod
    @__app.route('/show_languagelist_contents')
    def show_languagelist_contents():

        return render_template('print/show_languagelist_contents.html',
                               languagelists=WebUI.__all_languagelists)

    @staticmethod
    @__app.route('/create_languagelist')
    def create_languagelist():

        return render_template('create/create_languagelist.html')

    @staticmethod
    @__app.route('/do_create_languagelist', methods=['GET', 'POST'])
    def do_create_languagelist():
        name, error = WebUI.validate_input("name")
        if name is None:
            return error
        key = name.lower()
        languagelist = LanguageList.lookup(key)
        if languagelist is not None:
            return render_template("error.html", message_header="Language List already exists",
                                   message_body=f"Language List {name} already exist. Choose another name.")
        if "description" in request.form:
            description = request.form["description"].strip()
        else:
            description = ""
        languagelist = LanguageList(name, [], description, save=True)
        WebUI.__all_languagelists.append(languagelist)
        return render_template("create/confirm_languagelist_created.html", languagelist=languagelist)

    @staticmethod
    @__app.route('/create_language')
    def create_language():

        return render_template('create/create_language.html')

    @staticmethod
    @__app.route('/do_create_language', methods=['GET', 'POST'])
    def do_create_language():
        name, error = WebUI.validate_input("name")
        if name is None:
            return error
        key = name.lower()
        language = Language.lookup(key)
        if language is not None:
            return render_template("error.html", message_header="Language already exists",
                                   message_body=f"Language {name} already exist. Choose another name.")
        application_domain, error = WebUI.validate_input("application_domain")
        if application_domain is None:
            return error
        programming_paradigm, error = WebUI.validate_input("programming_paradigm")
        if programming_paradigm is None:
            return error
        execution_method, error = WebUI.validate_input("execution_method")
        if execution_method is None:
            return error
        typing, error = WebUI.validate_input("typing")
        if typing is None:
            return error
        language = Language(name, application_domain, programming_paradigm, execution_method, typing, save=True)
        WebUI.__all_languages.append(language)
        return render_template("create/confirm_language_created.html", language=language)

    @staticmethod
    @__app.route('/create_languageexposure')
    def create_languageexposure():

        return render_template('create/create_languageexposure.html')

    @staticmethod
    @__app.route('/do_create_languageexposure', methods=['GET', 'POST'])
    def do_create_languageexposure():
        name, error = WebUI.validate_input("name")
        if name is None:
            return error
        key = name.lower()
        language = Language.lookup(key)
        if language is not None:
            return render_template("error.html", message_header="Language already exists",
                                   message_body=f"Language {name} already exist. Choose another name.")
        application_domain, error = WebUI.validate_input("application_domain")
        if application_domain is None:
            return error
        programming_paradigm, error = WebUI.validate_input("programming_paradigm")
        if programming_paradigm is None:
            return error
        execution_method, error = WebUI.validate_input("execution_method")
        if execution_method is None:
            return error
        typing, error = WebUI.validate_input("typing")
        if typing is None:
            return error
        year_last_used, error = WebUI.validate_input("year_last_used")
        if year_last_used is None:
            return error
        years_of_exposure, error = WebUI.validate_input("years_of_exposure")
        if years_of_exposure is None:
            return error
        if "version_last_used" in request.form:
            version_last_used = request.form["version_last_used"].strip()
        else:
            version_last_used = ""
        language = LanguageExposure(name, application_domain, programming_paradigm, execution_method,
                                    typing, year_last_used, years_of_exposure, version_last_used, save=True)
        WebUI.__all_languages.append(language)
        return render_template("create/confirm_languageexposure_created.html", language=language)

    @staticmethod
    @__app.route('/join_languagelists')
    def join_languagelists():
        return render_template('create/join_languagelists.html', languagelists=WebUI.__all_languagelists)

    @staticmethod
    @__app.route('/do_join_languagelist', methods=['GET', 'POST'])
    def do_join_languagelist():
        first_key, error = WebUI.validate_input("first_languagelist")
        if first_key is None:
            return error
        second_key, error = WebUI.validate_input("second_languagelist")
        if second_key is None:
            return error
        first_languagelist = LanguageList.lookup(first_key.lower())
        if first_languagelist is None:
            return render_template("error.html", message_header=f"Language List {first_key} does not exist",
                                   message_body=f"Language List {first_key} was not found. Choose another one.")
        second_languagelist = LanguageList.lookup(second_key.lower())
        if second_languagelist is None:
            return render_template("error.html", message_header=f"Language List {second_key} does not exist",
                                   message_body=f"Language List {second_key} was not found. Choose another one.")
        new_key = f"{first_languagelist.get_name()}/{second_languagelist.get_name()}"
        new_languagelist = LanguageList.lookup(new_key.lower())
        if new_languagelist is not None:
            return render_template("error.html", message_header=f"Language List {new_key} already exists",
                                   message_body=f"Language List {new_key} already exists. Choose another combimation.")
        new_languagelist = first_languagelist + second_languagelist
        WebUI.__all_languagelists.append(new_languagelist)
        return render_template("create/confirm_languagelists_joined.html",
                               first_languagelist=first_languagelist,
                               second_languagelist=second_languagelist,
                               new_languagelist=new_languagelist)

    @staticmethod
    @__app.route('/update_language')
    def update_language():
        return render_template('update/update_language.html', languages=WebUI.__all_languages)

    @staticmethod
    @__app.route('/do_update_language', methods=['GET', 'POST'])
    def do_update_language():
        key, error = WebUI.validate_input("language")
        if key is None:
            return error
        language = Language.lookup(key)
        if language is None:
            return render_template("error.html", message_header="Language does not exist",
                                   message_body=f"Language {key} does not exist. Choose another language.")
        if "application_domain" in request.form:
            application_domain = request.form["application_domain"].strip()
        else:
            application_domain = ""
        language.update_application_domain(application_domain)
        return render_template("update/confirm_language_updated.html", language=language)

    @classmethod
    def run(cls):
        """Start the Flask web application server.

        Launches the application on port 8000.
        """
        cls.__app.run(host="0.0.0.0", port=8000)


if __name__ == '__main__':
    """Run the WebUI application.

    This block executes when the module is run directly.
    It initializes application data and starts the Flask server.
    """
    WebUI().init()
    WebUI().run()
