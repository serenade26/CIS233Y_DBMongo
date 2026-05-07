"""LanguageExposure class module.

File: LanguageExposure.py
Author: Alexander Leykand
Date: 05/07/2026
Assignment: Module 5

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
                 execution_method, typing, year_last_used, years_of_exposure, version_last_used):
        """Initialize a LanguageExposure object.

        Parameters:
            name (str): The name of the programming language.
            application_domain (str): The primary domain in which the
                language is used.
            programming_paradigm (str): The programming paradigm supported
                by the language.
            execution_method (str): How the language is executed
                (e.g., compiled or interpreted).
            typing (str): The typing discipline of the language
                (e.g., static or dynamic).
            year_last_used (int): The most recent year the language
                was used.
            years_of_exposure (float): Total number of years of
                experience with the language.
            version_last_used (str): The specific version of the
                language last used.
        """
        self.__year_last_used = year_last_used
        self.__years_of_exposure = years_of_exposure
        self.__version_last_used = version_last_used
        super().__init__(name, application_domain, programming_paradigm,
                         execution_method, typing)

    def to_dict(self):
        """Return a dictionary representation of the LanguageExposure object."""
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
