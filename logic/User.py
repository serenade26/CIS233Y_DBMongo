"""User module.

File: User.py
Author: Alexander Leykand
Date: 06/03/2026
Assignment: Module 9

Defines the User class used for application authentication.

This module provides the User class, which represents an
application user account. User objects store usernames and
password hashes, support password verification using bcrypt,
and provide methods for persistence through the Database
layer.
"""
import bcrypt

from data import Database


class User:
    """Represent an application user account.

    A User object stores a username and a bcrypt password
    hash. It provides methods for password verification,
    serialization, and retrieval from persistent storage.
    """
    __username = ""
    __hash = ""

    def __init__(self, username, hash):
        """Initialize a User object.

        Args:
            username (str): Account username.
            hash (bytes): Bcrypt password hash.
        """
        self.__username = username
        self.__hash = hash

    def to_dict(self):
        """Convert the User object into a MongoDB document.

        Returns:
            dict: Dictionary representation of the user.
        """
        return {"_id":self.get_key(),
                "username":self.__username,
                "hash":self.__hash}

    @classmethod
    def build(cls, dict):
        """Create a User object from a dictionary.

        Args:
            user_dict (dict): Dictionary containing user data.

        Returns:
            User: Newly constructed User object.
        """
        return cls(dict["username"],dict["hash"])

    def get_key(self):
        """Return the database key for the user.

        Returns:
            str: Lowercase username used as the primary key.
        """
        return (self.__username.lower())

    def get_username(self):
        """Return the username.

        Returns:
            str: Username associated with the account.
        """
        return self.__username

    def get_hash(self):
        """Return the password hash.

        Returns:
            bytes: Stored bcrypt password hash.
        """
        return self.__hash

    @staticmethod
    def read_user(username):
        """Retrieve a user by username.

        Args:
            username (str): Username to search for.

        Returns:
            User | None: Matching User object if found;
            otherwise None.
        """
        from data.Database import Database
        return Database.read_user(username)

    def verify_password(self, password):
        """Verify a password against the stored hash.

        Args:
            password (str): Plain-text password to verify.

        Returns:
            bool: True if the password matches the stored
            hash; otherwise False.
        """
        return bcrypt.checkpw(password.encode(), self.__hash)