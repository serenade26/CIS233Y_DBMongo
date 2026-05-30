"""
File: main.py
Author: Alexander Leykand
Date: 05/30/2026
Assignment: Module 8

Application entry point.

Initializes the WebUI and starts the Flask web server.
"""
from ui.WebUI import WebUI

if __name__ == '__main__':
    # This block executes when the module is run directly.
    # Initialize application data and start the Flask server.
    WebUI.init()
    WebUI.run()