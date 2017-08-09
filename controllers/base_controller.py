#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Responsible module to create base handlers.
"""


from tornado.web import RequestHandler
from psycopg2.extras import RealDictCursor
from datetime import date, datetime
from json import dumps

# Let importing ALL
from models import *


class BaseHandler(RequestHandler):
    """
        Responsible class to be a base handler for the others classes.
        It extends of the RequestHandler class.
    """

    # Static list to be added the all valid urls to one handler
    urls = []

    # cursor_factory=RealDictCursor means that the "row" of the table will be
    # represented by a dictionary in python
    __PGSQL_CURSOR__ = PGSQL_CONNECTION.cursor(cursor_factory=RealDictCursor)

    def set_and_send_status(self, status, reason=""):
        self.set_status(status, reason=reason)
        self.write(dumps({"status": status, "statusText": reason}))

    def search_in_database_by_query(self, query_text):
        # do the search in database
        self.__PGSQL_CURSOR__.execute(query_text)
        results_list = self.__PGSQL_CURSOR__.fetchall()

        for dict_result in results_list:
            # dict_result is one of the results
            for key, value in dict_result.items():

                # if the value is a datetime or date, so convert it in
                # a human readable string
                if isinstance(value, (datetime, date)):
                    dict_result[key] = value.isoformat()

        return results_list
