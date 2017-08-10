#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Responsible module to create base handlers.
"""


from tornado.web import RequestHandler, HTTPError

# from psycopg2.extras import RealDictCursor
# from datetime import date, datetime
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

    # cursor_factory=RealDictCursor means that the "row" of the table will be
    # represented by a dictionary in python
    # __PGSQL_CURSOR__ = PGSQL_CONNECTION.cursor(cursor_factory=RealDictCursor)

    PGSQLConn = PGSQLConnection()

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

    # def get_columns_name_and_data_types_from_table(self, table_name):
    #     query_text = "SELECT a.attname as column_name, format_type(a.atttypid, a.atttypmod) as data_type " \
    #                  "FROM pg_attribute a JOIN pg_class b ON (a.attrelid = b.relfilenode) " \
    #                  "WHERE b.relname = '" + str(table_name) + "' and a.attstattarget = -1;"
    #
    #     self.__PGSQL_CURSOR__.execute(query_text)
    #     list_of_columns_name_and_data_types = self.__PGSQL_CURSOR__.fetchall()
    #
    #     # if there is a geometry field, so show it in WKT format
    #     for a_field in list_of_columns_name_and_data_types:
    #         # column_name = a_field["column_name"]
    #         data_type = a_field["data_type"]
    #
    #         if "geometry" in data_type:
    #             a_field["column_name"] = "ST_AsText("+a_field["column_name"]+") as " + a_field["column_name"]
    #                                     # something like: ST_AsText(geom) as geom
    #
    #     # for result in list_of_columns_name_and_data_types:
    #     #     print(result)
    #
    #     return list_of_columns_name_and_data_types

    # def get_list_of_columns_name_in_str(self, list_of_columns_name_and_data_types):
    #
    #     columns_name = ""
    #     last_index = len(list_of_columns_name_and_data_types) - 1
    #
    #     for i in range(0, len(list_of_columns_name_and_data_types)):
    #         result = list_of_columns_name_and_data_types[i]
    #
    #         columns_name += result["column_name"]
    #
    #         # put a comma in the end of string while is not the last column
    #         if i != last_index:
    #             columns_name += ", "
    #
    #     return columns_name

    # def search_in_database_by_query(self, query_text):
    #     # do the search in database
    #     self.__PGSQL_CURSOR__.execute(query_text)
    #     results_list = self.__PGSQL_CURSOR__.fetchall()
    #
    #     for dict_result in results_list:
    #         # dict_result is one of the results
    #         for key, value in dict_result.items():
    #
    #             # if the value is a datetime or date, so convert it in
    #             # a human readable string
    #             if isinstance(value, (datetime, date)):
    #                 dict_result[key] = value.isoformat()
    #
    #     return results_list

    # def insert(self, insert_query_text):
    #
    #     status = self.__PGSQL_CURSOR__.execute(insert_query_text)
    #
    #     return status
