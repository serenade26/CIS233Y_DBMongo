from ui.WebUI import WebUI

if __name__ == '__main__':
    """Run the WebUI application.

    This block executes when the module is run directly.
    It initializes application data and starts the Flask server.
    """
    WebUI().init()
    WebUI().run()