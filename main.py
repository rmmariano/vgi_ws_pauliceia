#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Responsible file to start the application.
"""


from os.path import join, dirname

from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.web import Application, StaticFileHandler
from tornado.options import define, options, parse_command_line

from settings import *
from controllers import *

from tornado.escape import xhtml_escape


# Define which IP will be used
define("address", default=IP_APP, help="run on the IP given", type=str)
# Define which port will be used
define("port", default=PORT_APP, help="run on the port given", type=int)
# Debug mode will detail the information on console
define("debug", default=DEBUG_MODE, help="run in debug mode", type=bool)


class HttpServerApplication(Application):
    """
        Responsible class to set the handlers and settings of the application.
    """

    def __init__(self):
        """
            Responsible method to be the constructor of the class.

            Args:
                Nothing until the moment.

            Returns:
                Nothing until the moment.

            Raises:
                Nothing until the moment.
        """

        # All the classes added in the under list have to extend of the BaseHandler class
        # because it that have the static variable called urls
        handler_classes = [
            IndexHandler, SimplePageHandler, GetPoint, AddPoint
        ]

        # Create a new handler ( (url, class) ) using the URL of the list of urls with its class correspondent
        __handlers__ = []
        for __class__ in handler_classes:
            for url in __class__.urls:
                __handlers__.append( (url, __class__) )

        # Add the path "static" as static file
        static_path = join(dirname(__file__), "static")
        __handlers__.append( ( r"/static/(.*)", StaticFileHandler, { "path": static_path } ) )

        # Put here the settings of the application, that can be accessed in the template
        __setting__s = dict(
            blog_title=TITLE_APP,
            template_path=join(dirname(__file__), "templates"),
            # static_path=join(dirname(__file__), "static"),
            xsrf_cookies=False,
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            # login_url="/auth/login",
            debug=options.debug,
            current_year=CURRENT_YEAR,
            author=AUTHOR,
            # Passed functions to be used in the template
            # process_text=process_text,
        )

        # Pass the handlers and the settings created to the constructor of the super class (father class)
        Application.__init__(self, __handlers__, **__setting__s)


def start_application():
    parse_command_line()
    http_server = HTTPServer(HttpServerApplication())
    http_server.listen(options.port, address=options.address)
    print("\nRunning Tornado on " + URL_APP + "\n")

    IOLoop.current().start()


def stop_application():
    print("Stopping PostgreSQL")
    PGSQL_CONNECTION.close()

    print("Closing the web service!")
    IOLoop.instance().stop()


def main():
    """
        Responsible function to execute routines to start the application.

        Args:
            Nothing until the moment.

        Returns:
            Nothing until the moment.

        Raises:
            Nothing until the moment.
    """

    try:
        start_application()

    # CTRL+C on linux / CTRL+BREAK on windows
    except KeyboardInterrupt:
        stop_application()


# If this file is the main application, so will execute the main function
if __name__ == "__main__":
    main()
