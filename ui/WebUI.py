"""WebUI class module.

File: WebUI.py
Author: Alexander Leykand
Date: 06/03/2026
Assignment: Module 9

Flask-based web interface for the Language Catalog application.

This module defines the WebUI class, which manages browser-based
interaction with Language, LanguageList, LanguageExposure, and User
objects using the Flask web framework.

It supports:
    - Rendering HTML templates
    - Displaying and managing language data
    - User authentication (login/logout/session handling)
    - Handling user requests through URL routes

The module serves as the main entry point for the web version
of the application, initializing application data from the
database and launching the Flask development server over HTTPS.
"""
from flask import Flask, render_template, request, session, redirect, url_for
from pymongo import ssl_context
from data.Database import Database
from logic.LanguageList import LanguageList
from logic.Language import Language
from logic.LanguageExposure import LanguageExposure
from logic.User import User
from logic.utilities import get_ini_file
from flask_session import Session
import bcrypt


class WebUI:
    """Provide a Flask-based web interface for the Language Catalog application.

    This class manages:
        - Initialization of application data (languages, language lists, users)
        - Flask route registration and request handling
        - User authentication and session management
        - Rendering of HTML templates for browser interaction
        - CRUD operations for languages and language lists

    The application supports viewing, creating, updating, and deleting
    programming languages and language lists, as well as user login and
    session-based access control.
    """
    __all_languages = None
    __all_languagelists = None
    __app = Flask(__name__)
    ALLOWED_PATHS = ["/login", "/do_login", "/static/language_catalog.css"]
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
        """Validate a submitted form field.

        Checks whether the specified field exists in the
        submitted form data and contains a non-blank value.

        Args:
            field_name (str): Name of the form field.

        Returns:
            tuple: A pair containing the validated field value
            and None if validation succeeds, or None and a
            rendered error page if validation fails.
        """
        if field_name not in request.form:
            return None, render_template("error.html", message_header=f"Unspecified {field_name}",
                                         message_body=f"No {field_name} specified. Check the form and try again.")
        field_value = request.form[field_name].strip()
        if field_value == "":
            return None, render_template("error.html", message_header=f"Unspecified {field_name}",
                                         message_body=f"No {field_name} specified. Check the form and try again.")
        return field_value, None

    @staticmethod
    @__app.before_request
    def before_request():
        """Enforce authentication before processing requests.

        Checks whether a user is currently authenticated and
        stored in the session. If no authenticated user exists
        and the requested path is not publicly accessible,
        redirects the client to the login page.

        Returns:
            Response | None: A redirect response to the login
            page when authentication is required; otherwise
            None to allow normal request processing.
        """
        if "user" not in session:
            if request.path not in WebUI.ALLOWED_PATHS:
                return redirect(url_for("login"))

    @staticmethod
    @__app.route('/index')
    @__app.route('/index.html')
    @__app.route('/index.php')
    @__app.route('/')
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
        """Display a selected LanguageList and its contents.

        The target LanguageList is specified through the
        'languagelist' URL query parameter. If the parameter
        is missing or the LanguageList does not exist, an
        error page is displayed instead.

        Returns:
            str: Rendered LanguageList template or an error page.
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
        """Display a form for selecting a LanguageList.

        Returns:
            str: Rendered template containing a list of
            available LanguageLists for user selection.
        """
        return render_template('print/show_languagelist_contents.html',
                               languagelists=WebUI.__all_languagelists)

    @staticmethod
    @__app.route('/create_languagelist')
    def create_languagelist():
        """Display the LanguageList creation form.

        Returns:
            str: Rendered template for entering a new
            LanguageList name and description.
        """
        return render_template('create/create_languagelist.html')

    @staticmethod
    @__app.route('/do_create_languagelist', methods=['GET', 'POST'])
    def do_create_languagelist():
        """Create a new LanguageList.

        Validates submitted form data, verifies that the
        LanguageList does not already exist, creates it,
        and displays a confirmation page.

        Returns:
            str: Confirmation page or an error page.
        """
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
        """Display the Language creation form.

        Returns:
            str: Rendered template for entering a new
            Language.
        """
        return render_template('create/create_language.html')

    @staticmethod
    @__app.route('/do_create_language', methods=['GET', 'POST'])
    def do_create_language():
        """Create a new Language.

        Validates submitted form data, verifies that the
        Language does not already exist, creates it,
        and displays a confirmation page.

        Returns:
            str: Confirmation page or an error page.
        """
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
        """Display the LanguageExposure creation form.

        Returns:
            str: Rendered template for entering a new
            LanguageExposure object.
        """
        return render_template('create/create_languageexposure.html')

    @staticmethod
    @__app.route('/do_create_languageexposure', methods=['GET', 'POST'])
    def do_create_languageexposure():
        """Create a new LanguageExposure.

        Validates submitted form data, verifies that the
        Language does not already exist, creates the
        LanguageExposure object, and displays a
        confirmation page.

        Returns:
            str: Confirmation page or an error page.
        """
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
        """Display the LanguageList join form.

        Returns:
            str: Rendered template for selecting two
            LanguageLists to combine.
        """
        return render_template('create/join_languagelists.html', languagelists=WebUI.__all_languagelists)

    @staticmethod
    @__app.route('/do_join_languagelist', methods=['GET', 'POST'])
    def do_join_languagelist():
        """Join two LanguageLists.

        Validates submitted LanguageLists, verifies that
        the resulting combined list does not already
        exist, creates the new LanguageList, and displays
        a confirmation page.

        Returns:
            str: Confirmation page or an error page.
        """
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
        """Display the Language update form.

        Returns:
            str: Rendered template for selecting a
            Language to update.
        """
        return render_template('update/update_language.html', languages=WebUI.__all_languages)

    @staticmethod
    @__app.route('/do_update_language', methods=['GET', 'POST'])
    def do_update_language():
        """Update an existing Language.

        Updates the application domain of the selected
        Language and displays a confirmation page.

        Returns:
            str: Confirmation page or an error page.
        """
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

    @staticmethod
    @__app.route('/add_language_to_languagelist')
    def add_language_to_languagelist():
        """Display the add-to-LanguageList form.

        Returns:
            str: Rendered template for selecting a
            Language and LanguageList.
        """
        return render_template('update/add_language_to_languagelist.html',
                               languages=WebUI.__all_languages,
                               languagelists=WebUI.__all_languagelists)

    @staticmethod
    @__app.route('/do_add_language_to_languagelist', methods=['GET', 'POST'])
    def do_add_language_to_languagelist():
        """Add a Language to a LanguageList.

        Validates submitted selections, verifies that the
        Language is not already present, adds it to the
        LanguageList, and displays a confirmation page.

        Returns:
            str: Confirmation page or an error page.
        """
        language_key, error = WebUI.validate_input("language")
        if language_key is None:
            return error
        language = Language.lookup(language_key)
        if language is None:
            return render_template("error.html", message_header="Language does not exist",
                                   message_body=f"Language {language_key} does not exist. Choose another language.")

        languagelist_key, error = WebUI.validate_input("languagelist")
        if languagelist_key is None:
            return error
        languagelist = LanguageList.lookup(languagelist_key.lower())
        if languagelist is None:
            return render_template("error.html", message_header=f"Language List {languagelist_key} does not exist",
                                   message_body=f"Language List {languagelist_key} was not found. Choose another one.")
        if language in languagelist:
            return render_template("error.html", message_header=f"Language {language.get_name()} already in Language "
                                                                f"List",
                                   message_body=f"Language {language.get_name()} already exists in Language "
                                                f"List {languagelist.get_name()}.")
        languagelist.append(language)
        return render_template("update/confirm_language_added_to_languagelist.html",
                               language=language, languagelist=languagelist)

    @staticmethod
    @__app.route('/remove_language_from_languagelist')
    def remove_language_from_languagelist():
        """Display the remove-from-LanguageList form.

        Returns:
            str: Rendered template for selecting a
            Language and LanguageList.
        """
        return render_template('update/remove_language_from_languagelist.html',
                               languages=WebUI.__all_languages,
                               languagelists=WebUI.__all_languagelists)

    @staticmethod
    @__app.route('/do_remove_language_from_languagelist', methods=['GET', 'POST'])
    def do_remove_language_from_languagelist():
        """Remove a Language from a LanguageList.

        Validates submitted selections, verifies that the
        Language exists in the specified LanguageList,
        removes it, and displays a confirmation page.

        Returns:
            str: Confirmation page or an error page.
        """
        language_key, error = WebUI.validate_input("language")
        if language_key is None:
            return error
        language = Language.lookup(language_key)
        if language is None:
            return render_template("error.html", message_header="Language does not exist",
                                   message_body=f"Language {language_key} does not exist. Choose another language.")
        languagelist_key, error = WebUI.validate_input("languagelist")
        if languagelist_key is None:
            return error
        languagelist = LanguageList.lookup(languagelist_key.lower())
        if languagelist is None:
            return render_template("error.html", message_header=f"Language List {languagelist_key} does not exist",
                                   message_body=f"Language List {languagelist_key} was not found. Choose another one.")
        if languagelist.get_name() == LanguageList.ALL_LANGUAGES:
            return render_template("error.html", message_header="Cannot remove the Language",
                                   message_body=f"Language is not allowed to be removed "
                                                f"from {LanguageList.ALL_LANGUAGES} Language List.")
        if language not in languagelist:
            return render_template("error.html",
                                   message_header=f"Language {language.get_name()} is not in Language List",
                                   message_body=f"Language {language.get_name()} does not exist in Language "
                                                f"List {languagelist.get_name()}.")
        languagelist.remove(language)
        return render_template("update/confirm_language_removed_from_languagelist.html",
                               language=language, languagelist=languagelist)

    @staticmethod
    @__app.route('/delete_languagelist')
    def delete_languagelist():
        """Display the LanguageList deletion form.

        Returns:
            str: Rendered template for selecting a
            LanguageList to delete.
        """
        return render_template('delete/delete_languagelist.html',
                               languagelists=WebUI.__all_languagelists)

    @staticmethod
    @__app.route('/do_delete_languagelist', methods=['GET', 'POST'])
    def do_delete_languagelist():
        """Delete a LanguageList.

        Validates the selected LanguageList, prevents
        deletion of the All Languages list, removes the
        LanguageList, and displays a confirmation page.

        Returns:
            str: Confirmation page or an error page.
        """
        languagelist_key, error = WebUI.validate_input("languagelist")
        if languagelist_key is None:
            return error
        languagelist = LanguageList.lookup(languagelist_key.lower())
        if languagelist is None:
            return render_template("error.html", message_header=f"Language List {languagelist_key} does not exist",
                                   message_body=f"Language List {languagelist_key} was not found. Choose another one.")
        if languagelist.get_name() == LanguageList.ALL_LANGUAGES:
            return render_template("error.html", message_header="Cannot delete the Language List",
                                   message_body=f"Language List {LanguageList.ALL_LANGUAGES} cannot be removed.")
        WebUI.__all_languagelists.remove(languagelist)
        languagelist.delete()
        return render_template("delete/confirm_languagelist_deleted.html", languagelist=languagelist)

    @staticmethod
    @__app.route('/delete_language')
    def delete_language():
        """Display the Language deletion form.

        Returns:
            str: Rendered template for selecting a
            Language to delete.
        """
        return render_template('delete/delete_language.html',
                               languages=WebUI.__all_languages)

    @staticmethod
    @__app.route('/do_delete_language', methods=['GET', 'POST'])
    def do_delete_language():
        """Delete a Language.

        Removes the selected Language from all LanguageLists,
        deletes it from storage, and displays a confirmation
        page.

        Returns:
            str: Confirmation page or an error page.
        """
        language_key, error = WebUI.validate_input("language")
        if language_key is None:
            return error
        language = Language.lookup(language_key)
        if language is None:
            return render_template("error.html", message_header="Language does not exist",
                                   message_body=f"Language {language_key} does not exist. Choose another language.")
        for languagelist in WebUI.__all_languagelists:
            if language in languagelist:
                languagelist.remove(language)
        language.delete()
        return render_template("delete/confirm_language_deleted.html", language=language)

    @staticmethod
    @__app.route('/get_user')
    def get_user():
        """ This is a test method to retrieve the session user. """
        if "username" in session:
            return session["username"]
        else:
            return "No user is set"

    @staticmethod
    @__app.route('/set_user')
    def set_user():
        """ This is a test method to establish the session user. """
        if "username" in request.args:
            session["username"] = request.args["username"]
            return "User set"
        if "username" in session:
            del session["username"]
        return "User cleared"

    @staticmethod
    @__app.route('/login')
    def login():
        """Render the login page.

        Displays the HTML form for user authentication.

        Returns:
            str: Rendered login page template.
        """
        return render_template("user/login.html")

    @staticmethod
    @__app.route('/do_login', methods=['GET', 'POST'])
    def do_login():
        """Authenticate a user and establish a session.

        Validates submitted username and password, verifies the
        user against stored credentials, and logs the user into
        the session if authentication succeeds. If authentication
        fails, an error page is returned.

        Returns:
            Response: Redirect to homepage on success, or rendered
            error page on failure.
        """
        username, error = WebUI.validate_input("username")
        if error is not None:
            return error
        password, error = WebUI.validate_input("password")
        if error is not None:
            return error
        user = User.read_user(username)
        if user is None:
            return render_template("error.html",
                                   message_header="Login failed",
                                   message_body="Invalid account credentials. Please try again.")
        logged_in = user.verify_password(password)
        if not logged_in:
            return render_template("error.html",
                                   message_header="Login failed",
                                   message_body="Invalid account credentials. Please try again.")
        session["user"] = user
        return redirect(url_for("homepage"))


    @staticmethod
    @__app.route('/logout')
    def logout():
        """Log out the current user.

        Removes the user from the session if present and redirects
        to the login page.

        Returns:
            Response: Redirect to the login page.
        """
        if "user" in session:
            del session["user"]
        return redirect(url_for("login"))

    @classmethod
    def run(cls):
        """Start the Flask web application server.

        Configures session handling and launches the Flask
        development server over HTTPS using a self-signed
        certificate.

        The server listens on all network interfaces on port 8443.

        Returns:
            None
        """
        cls.__app.secret_key = bcrypt.gensalt()
        cls.__app.config["SESSION_TYPE"] = "filesystem"
        Session(cls.__app)
        path, file = get_ini_file(Database.APP_NAME)
        cls.__app.run(host="0.0.0.0", port=8443, ssl_context=(path + "/cert.pem", path + "/key.pem"))


if __name__ == '__main__':
    # This block executes when the module is run directly.
    # Initialize application data and start the Flask server.
    WebUI().init()
    WebUI().run()
