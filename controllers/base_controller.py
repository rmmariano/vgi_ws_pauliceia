#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Responsible module to create base handlers.
"""


from tornado.escape import json_encode, json_decode
from tornado.web import RequestHandler, HTTPError, MissingArgumentError
from json import dumps, loads

# Let importing ALL
from models import *
from modules.user import get_new_user_struct_cookie



class BaseHandler(RequestHandler):
    """
        Responsible class to be a base handler for the others classes.
        It extends of the RequestHandler class.
    """

    # Static list to be added the all valid urls to one handler
    urls = []

    # DB connection
    PGSQLConn = PGSQLConnection.get_instance()

    # LOGIN  // external login (EL)
    __AFTER_LOGGED_REDIRECT_TO__ = "/auth/login/success/"
    __AFTER_LOGGED_OUT_REDIRECT_TO__ = "/auth/logout/success/"

    ################################################################################
    # control requests

    def set_default_headers(self):
        # list specific domains that are allow to use this webserver
        self.set_header("Access-Control-Allow-Origin", "http://localhost:8889")
        self.set_header("Access-Control-Allow-Headers", "Content-Type, x-requested-with")
        self.set_header('Access-Control-Allow-Methods', ' GET, POST, OPTIONS')

    def options(self):
        # https://stackoverflow.com/questions/35254742/tornado-server-enable-cors-requests
        # no body
        self.set_status(204)
        self.finish()

    ################################################################################

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

    def set_and_send_status(self, status=404, reason="", extra={}, raise_error=False):

        response_json = {"status": status, "statusText": reason}

        if extra != {}:
            response_json["extra"] = extra

        self.set_status(status, reason=reason)
        self.write(dumps(response_json))

        if raise_error:
            raise HTTPError(status, reason)

    def get_param_geometry_format(self):
        try:
            geom_format = self.get_argument("geom_format")
        except MissingArgumentError:
            # if geom_format is undefined, return "wkt" by default
            geom_format = "wkt"

        return geom_format

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

    def key_exist_in_list_of_columns_name_and_data_types(self, key, list_of_columns_name_and_data_types):

        for column_and_type in list_of_columns_name_and_data_types:
            if column_and_type["column_name"] == key:
                return True

        return False

    def get_data_type_of_column_in_list_of_columns_name_and_data_types(self, column_name, list_of_columns_name_and_data_types):

        for column_and_type in list_of_columns_name_and_data_types:
            if column_and_type["column_name"] == column_name:
                return column_and_type["data_type"]

        return None

    def exist_paramns_in_table_columns(self, list_of_columns_name_and_data_types, QUERY_PARAM):

        invalid_columns = []

        if QUERY_PARAM != "all":
            # add in invalid_columns the columns that doesn't exits in the table
            for param in QUERY_PARAM:
                if not self.key_exist_in_list_of_columns_name_and_data_types(param, list_of_columns_name_and_data_types):
                    invalid_columns.append(param)
        # if QUERY_PARAM == "all", do nothing, it is default

        # not invalid_columns (if invalid_columns is empty, return True else return False)
        result = {"exist_params_in_table_columns": not invalid_columns,
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


    # extra methods

    def create_extra_message_to_invalid_columns(self, invalid_columns):
        extra = {}

        # if is not empty
        if invalid_columns:
            invalid_columns = ", ".join(invalid_columns)
            extra["message"] = "There is(are) invalid column(s). Please check if is(are) correct(s)"
            extra["invalid_columns"] = invalid_columns

        return extra


    # login

    def do_login(self, email, password):
        query_text = """ SELECT id, name, email, institution, level, datestart, status FROM tb_users 
                            WHERE email = '{0}' AND password = '{1}';
                    """.format(email, password)

        result = self.PGSQLConn.search_in_database_by_query(query_text)

        return result


    # cookie

    def set_current_user(self, email="", type_login="", new_user=True):
        if new_user:
            user_cookie = get_new_user_struct_cookie()
        else:
            user_cookie = json_decode(self.get_secure_cookie("user"))

        user_cookie["login"]["email"] = email
        user_cookie["login"]["type_login"] = type_login

        # set the cookie (it needs to be separated)
        encode = json_encode(user_cookie)
        self.set_secure_cookie("user", encode)

    def get_current_user(self):
        user_cookie = self.get_secure_cookie("user")

        if user_cookie:
            return json_decode(user_cookie)
        else:
            return None
