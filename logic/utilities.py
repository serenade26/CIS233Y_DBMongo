"""Utilities module.

File: Database.py
Author: Alexander Leykand
Date: 06/03/2026
Assignment: Module 9

Utility functions for environment and configuration file handling.

This module provides helper functions for locating the user's home
directory and resolving application configuration file paths.

It is primarily used to locate the application's `.ini` configuration
file in a platform-independent manner (Windows, macOS, Linux).
"""
import os


def get_home_path():
    """Return the current user's home directory path.

    Determines the home directory based on environment variables
    in a cross-platform manner.

    Supports:
        - Windows (USERPROFILE)
        - Unix/Linux/macOS (HOME)

    Returns:
        str: Absolute path to the user's home directory.

    Raises:
        Exception: If neither USERPROFILE nor HOME environment
        variable is set.
    """
    if 'USERPROFILE' in os.environ:  # Win11
        return os.environ['USERPROFILE']
    elif 'HOME' in os.environ:  # Unix/Mac
        return os.environ['HOME']
    else:
        raise Exception('Please set USERPROFILE or HOME')


def get_ini_file(app_name: str) -> tuple[str, str]:
    """Locate the application directory and INI configuration file.

    Constructs the expected application folder inside the user's
    home directory and verifies that the configuration file exists.

    Args:
        app_name (str): Name of the application used as both the
        folder name and the INI filename prefix.

    Returns:
        tuple[str, str]: A tuple containing:
            - path (str): Directory containing the application files
            - file (str): Full path to the INI configuration file

    Raises:
        Exception: If the INI file does not exist at the expected location.
    """
    home_path = get_home_path()
    path = os.path.join(home_path, app_name)  # app directory loc'n
    file = os.path.join(path, f"{app_name}.ini")  # app .ini file loc'n in the directory
    if os.path.exists(file):
        return path, file
    else:
        raise Exception(f"File {app_name}.ini not found")
