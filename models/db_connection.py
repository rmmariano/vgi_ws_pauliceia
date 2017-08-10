#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Create a file named:
    vgi_ws_pauliceia/settings/db_settings.py

    With the follow content:
    __PGSQL_CONNECTION_SETTINGS__ = {
        "HOSTNAME": "HOSTNAME",
        "USERNAME": "USERNAME",
        "PASSWORD": "PASSWORD",
        "DATABASE": "DATABASE",
        "PORT": 5432
    }

    This __PGSQL_CONNECTION_SETTINGS__ dictionary is the connection with PostgreSQL
"""


from sys import exit
from datetime import date, datetime
from psycopg2 import connect, DatabaseError
from psycopg2.extras import RealDictCursor

from settings.db_settings import __PGSQL_CONNECTION_SETTINGS__


# PGSQL_CONNECTION = ""
#
# print("\nConnecting in PostgreSQL with:"
#       "\n- hostname: ", __PGSQL_CONNECTION_SETTINGS__["HOSTNAME"],
#       "\n- port: ", __PGSQL_CONNECTION_SETTINGS__["PORT"],
#       "\n- database: ", __PGSQL_CONNECTION_SETTINGS__["DATABASE"], "\n")
#
# try:
#     PGSQL_CONNECTION = connect(host=__PGSQL_CONNECTION_SETTINGS__["HOSTNAME"],
#                                port=__PGSQL_CONNECTION_SETTINGS__["PORT"],
#                                user=__PGSQL_CONNECTION_SETTINGS__["USERNAME"],
#                                password=__PGSQL_CONNECTION_SETTINGS__["PASSWORD"],
#                                dbname=__PGSQL_CONNECTION_SETTINGS__["DATABASE"])
#
#     print("PostgreSQL's connection was: successful!")
# except (DatabaseError, Exception) as error:
#     print("PostgreSQL's connection was: failed! \n")
#     print("Error: ", error)
#     print("Closing web service!")
#     exit(1)


class PGSQLConnection():

    def __init__(self):
        self.PGSQL_CONNECTION = ""

        print("\nConnecting in PostgreSQL with:"
              "\n- hostname: ", __PGSQL_CONNECTION_SETTINGS__["HOSTNAME"],
              "\n- port: ", __PGSQL_CONNECTION_SETTINGS__["PORT"],
              "\n- database: ", __PGSQL_CONNECTION_SETTINGS__["DATABASE"], "\n")

        try:
            self.PGSQL_CONNECTION = connect(host=__PGSQL_CONNECTION_SETTINGS__["HOSTNAME"],
                                            port=__PGSQL_CONNECTION_SETTINGS__["PORT"],
                                            user=__PGSQL_CONNECTION_SETTINGS__["USERNAME"],
                                            password=__PGSQL_CONNECTION_SETTINGS__["PASSWORD"],
                                            dbname=__PGSQL_CONNECTION_SETTINGS__["DATABASE"])

            print("PostgreSQL's connection was: successful!")
        except (DatabaseError, Exception) as error:
            print("PostgreSQL's connection was: failed! \n")
            print("Error: ", error)
            print("Closing web service!")
            exit(1)

        self.__PGSQL_CURSOR__ = self.PGSQL_CONNECTION.cursor(cursor_factory=RealDictCursor)

    def get_columns_name_and_data_types_from_table(self, table_name):
        query_text = "SELECT a.attname as column_name, format_type(a.atttypid, a.atttypmod) as data_type " \
                     "FROM pg_attribute a JOIN pg_class b ON (a.attrelid = b.relfilenode) " \
                     "WHERE b.relname = '" + str(table_name) + "' and a.attstattarget = -1;"

        self.__PGSQL_CURSOR__.execute(query_text)
        list_of_columns_name_and_data_types = self.__PGSQL_CURSOR__.fetchall()

        # if there is a geometry field, so show it in WKT format
        for a_field in list_of_columns_name_and_data_types:
            # column_name = a_field["column_name"]
            data_type = a_field["data_type"]

            if "geometry" in data_type:
                a_field["column_name"] = "ST_AsText("+a_field["column_name"]+") as " + a_field["column_name"]
                                        # something like: ST_AsText(geom) as geom

        # for result in list_of_columns_name_and_data_types:
        #     print(result)

        return list_of_columns_name_and_data_types

    def get_list_of_columns_name_in_str(self, list_of_columns_name_and_data_types):

        columns_name = ""
        last_index = len(list_of_columns_name_and_data_types) - 1

        for i in range(0, len(list_of_columns_name_and_data_types)):
            result = list_of_columns_name_and_data_types[i]

            columns_name += result["column_name"]

            # put a comma in the end of string while is not the last column
            if i != last_index:
                columns_name += ", "

        return columns_name

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
