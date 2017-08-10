#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Responsible module to create base handlers.
"""


from tornado.web import RequestHandler, HTTPError
from json import dumps, loads

# Let importing ALL
from models import *


class BaseHandler(RequestHandler):
    """
        Responsible class to be a base handler for the others classes.
        It extends of the RequestHandler class.
    """

    # Static list to be added the all valid urls to one handler
    urls = []

    # PGSQLConn = PGSQLConnection()
    PGSQLConn = PGSQLConnection.get_instance()

    def get_the_json_validated(self):
        """
            Responsible method to validate the JSON received in the POST method.

            Args:
                Nothing until the moment.

            Returns:
                The JSON validated.

            Raises:
                - HTTPError (400 - Bad request): if don't receive a JSON.
                - HTTPError (400 - Bad request): if the JSON received is empty or is None.
        """

        # Verify if the type of the content is JSON
        if self.request.headers["Content-Type"].startswith("application/json"):
            # Convert string to unicode in Python 2 or convert bytes to string in Python 3
            # How string in Python 3 is unicode, so independent of version, both are converted in unicode
            foo = self.request.body.decode("utf-8")

            # Transform the string/unicode received to JSON (dictionary in Python)
            search = loads(foo)
        else:
            raise HTTPError(400, "It is not a JSON...")  # 400 - Bad request

        if search == {} or search is None:
            raise HTTPError(400, "The search given is empty...")  # 400 - Bad request

        return search

    def set_and_send_status(self, status, reason=""):
        self.set_status(status, reason=reason)
        self.write(dumps({"status": status, "statusText": reason}))

    # def insert(self, insert_query_text):
    #
    #     status = self.__PGSQL_CURSOR__.execute(insert_query_text)
    #
    #     return status
