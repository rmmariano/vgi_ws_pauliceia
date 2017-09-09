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

    # DB connection
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

    def get_dict_from_query_str(self, str_query):

        str_query = str_query.strip()

        # exceptional case: when I want all values
        if str_query.lower() == "all":
            return "all"

        # normal case: I have a query
        prequery = str_query.replace(r"[", "").replace(r"]", "").split(",")

        # with each part of the string, create a dictionary
        query = {}
        for condiction in prequery:
            parts = condiction.split("=")
            query[parts[0]] = parts[1]

        return query

    def param_in_list_of_columns_name_and_data_types(self, param, list_of_columns_name_and_data_types):

        for column_and_type in list_of_columns_name_and_data_types:
            if column_and_type["column_name"] == param:
                return True

        return False

    def exist_paramns_in_table_columns(self, list_of_columns_name_and_data_types, QUERY_PARAM):

        invalid_columns = []

        if QUERY_PARAM != "all":
            # add in invalid_columns the columns that doesn't exits in the table
            for param in QUERY_PARAM:
                if not self.param_in_list_of_columns_name_and_data_types(param, list_of_columns_name_and_data_types):
                    invalid_columns.append(param)
        # if QUERY_PARAM == "all", do nothing, it is default

        # not invalid_columns (if invalid_columns is empty, return True else return False)
        result = {"exist_paramns_in_table_columns": not invalid_columns,
                  "invalid_columns": invalid_columns}

        return result

    def build_where_clause_with_params(self, QUERY_PARAM):

        str_where = ""

        if QUERY_PARAM != "all":

            list_where = []
            for condiction in QUERY_PARAM:

                if QUERY_PARAM[condiction].isdigit():
                    c = condiction + "=" + QUERY_PARAM[condiction]
                else:
                    # if text
                    c = "lower(" + condiction + ") LIKE lower('%" + QUERY_PARAM[condiction] + "%')"
                    # something line: lower(name) LIKE lower('%Prefeitura%')

                list_where.append(c)

            # join the condictions separating by AND
            str_where = " WHERE " + (" AND ".join(list_where))

        # if QUERY_PARAM == "all", do nothing, it is default

        return str_where
