"""LanguageExposure class module.

File: LanguageExposure.py
Author: Alexander Leykand
Date: 05/21/2026
Assignment: Module 7

This module defines the LanguageExposure class, which extends the
Language class by adding information about a user's experience with
a specific programming language, including usage history, duration
of exposure, and version information.
"""

from logic.Language import Language


class LanguageExposure(Language):
    """Represents a programming language with user exposure details.

    This subclass of Language adds attributes describing when the
    language was last used, how many years of experience the user
    has with it, and the specific version last used.
    """
    __year_last_used = 0
    __years_of_exposure = 0
    __version_last_used = ""

    def __init__(self, name, application_domain, programming_paradigm,
                 execution_method, typing, year_last_used, years_of_exposure, version_last_used, save=False):
        """Initialize a LanguageExposure object.

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
            year_last_used (int): The most recent year in
                which the language was used.
            years_of_exposure (float): Total years of
                experience with the language.
            version_last_used (str): The specific language
                version most recently used.
            save (bool): Whether the object should be
                immediately persisted to the database.
        """
        self.__year_last_used = year_last_used
        self.__years_of_exposure = years_of_exposure
        self.__version_last_used = version_last_used
        super().__init__(name, application_domain, programming_paradigm,
                         execution_method, typing, save=save)

    def to_dict(self):
        """Return a dictionary representation of the LanguageExposure object.

        Extends the base Language dictionary representation
        with exposure-specific attributes for MongoDB
        persistence.

        Returns:
            dict: Serialized LanguageExposure object data.
        """
        dict = super().to_dict()
        dict["year_last_used"] = self.__year_last_used
        dict["years_of_exposure"] = self.__years_of_exposure
        dict["version_last_used"] = self.__version_last_used
        dict["type"] = "LanguageExposure"
        return dict

    def __str__(self):
        """Return a human-readable string representation of the language.

        Returns:
            str: A descriptive summary of the language.
        """

        s = super().__str__()
        return (s + f"\nLast used in {self.__year_last_used} "
                f"for {self.__years_of_exposure} years {self.__version_last_used} version")

    def to_html(self):
        """Return an HTML-formatted representation of the language exposure.

        Extends the base Language HTML representation with additional
        formatting that displays user exposure details such as the
        last year used and the version last used.

        Returns:
            str: An HTML-formatted description of the language exposure.
        """
        html = super().to_html()
        return html + f"<br><i>I used it last in {self.__year_last_used} and the version was {self.__version_last_used}</i>"
