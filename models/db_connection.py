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

    __LIST_TABLES_INFORMATION__ = [
        {"table_name": "TABLE_NAME"},
        {"table_name": "TABLE_NAME"},
        ...
    ]

    This __PGSQL_CONNECTION_SETTINGS__ dictionary is the connection with PostgreSQL
    The __LIST_TABLES_INFORMATION__ is a list with all tables` name
"""


from sys import exit
from datetime import date, datetime
from psycopg2 import connect, DatabaseError
from psycopg2.extras import RealDictCursor

from copy import deepcopy

from modules.design_pattern import Singleton
from modules.exception import GeomFormatException, DoesntExistTableException
from modules.util import convert_str_to_dict
from modules.sql import SQLHelper
from settings.db_settings import __PGSQL_CONNECTION_SETTINGS__, __LIST_TABLES_INFORMATION__


@Singleton
class PGSQLConnection:

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

        # cursor_factory=RealDictCursor means that the "row" of the table will be
        # represented by a dictionary in python
        self.__PGSQL_CURSOR__ = self.PGSQL_CONNECTION.cursor(cursor_factory=RealDictCursor)

        # create the SQL Helper passing the cursor
        self.__SQL_HELPER__ = SQLHelper(self.__PGSQL_CURSOR__)

        self.__generate_a_set_with_tables_names__()
        self.__fill_list_tables_information__()

    def __generate_a_set_with_tables_names__(self):
        """
            Create a SET with the tables` names
        """

        self.__TABLES_NAMES__ = set()

        for ONE_TABLE_INF in __LIST_TABLES_INFORMATION__:
            self.__TABLES_NAMES__.add(ONE_TABLE_INF["table_name"])

    def __fill_list_tables_information__(self):
        """
            Given the __LIST_TABLES_INFORMATION__ list, do a SELECT in DB and fill the dictionaries with the
            information about the table columns
        """

        for ONE_TABLE_INF in __LIST_TABLES_INFORMATION__:
            table_name = ONE_TABLE_INF["table_name"]

            ONE_TABLE_INF["list_of_columns_name_and_data_types"] = self.__SQL_HELPER__.get_columns_name_and_data_types_of_table_name(table_name)
            ONE_TABLE_INF["list_of_constraints"] = self.__SQL_HELPER__.get_constraints_of_table_name(table_name)

        print("\nFilled the __LIST_TABLES_INFORMATION__")

    def commit(self):
        """
            Just do the COMMIT operator in DB
        """

        self.PGSQL_CONNECTION.commit()

    def execute(self, sql_command_text):
        """
            Just execute the SQL command text, like a INSERT
        """

        self.__PGSQL_CURSOR__.execute(sql_command_text)

    def get_columns_name_and_data_types_from_table(self, table_name, transform_geom_bin_in_wkt=False,
                                                   geom_format="wkt"):

        list_of_columns_name_and_data_types = []

        # Just search in list (O(n)), if the table_name was added in set (self.__TABLES_NAMES__)
        if table_name in self.__TABLES_NAMES__:

            for ONE_TABLE_INF in __LIST_TABLES_INFORMATION__:
                if ONE_TABLE_INF["table_name"] == table_name:

                    list_of_columns_name_and_data_types = deepcopy(ONE_TABLE_INF["list_of_columns_name_and_data_types"])

                    if transform_geom_bin_in_wkt:
                        # if there is a geometry field, so show it in WKT format
                        for a_field in list_of_columns_name_and_data_types:
                            # column_name = a_field["column_name"]
                            data_type = a_field["data_type"]

                            if "geometry" in data_type:

                                if geom_format == "wkt":
                                    a_field["column_name"] = "ST_AsText("+a_field["column_name"]+") as " + a_field["column_name"]
                                                            # something like: ST_AsText(geom) as geom

                                elif geom_format == "geojson":
                                    a_field["column_name"] = "ST_AsGeoJSON(" + a_field["column_name"] + ") as " + a_field["column_name"]
                                                            # something like: ST_AsGeoJSON(geom) as geom

                                else:
                                    raise GeomFormatException("Invalid geom format: " + geom_format)

                    break

        return list_of_columns_name_and_data_types

    def get_table_of_tags_from_table_name(self, table_name):

        # Just search in list (O(n)), if the table_name was added in set (self.__TABLES_NAMES__)
        if table_name in self.__TABLES_NAMES__:

            for ONE_TABLE_INF in __LIST_TABLES_INFORMATION__:
                if ONE_TABLE_INF["table_name"] == table_name:

                    if "table_of_tags" in ONE_TABLE_INF:
                        return ONE_TABLE_INF["table_of_tags"]
                    else:
                        raise DoesntExistTableException("Doesn't exist table of tags in table: " + table_name)

        return None

    def get_constraint_about_table_of_tags_from_table_name(self, table_of_tags_with_fk, original_table_name):
        """
        :param original_table_name: original table
        :param table_of_tags_with_fk: the table that contains the FK from original table
        :return: the constraint of the relation, or a error if doesn't the relation, or None if the
        """

        # Just search in list (O(n)), if the table_name was added in set (self.__TABLES_NAMES__)
        if table_of_tags_with_fk in self.__TABLES_NAMES__:

            for ONE_TABLE_INF in __LIST_TABLES_INFORMATION__:
                if ONE_TABLE_INF["table_name"] == table_of_tags_with_fk:

                    list_of_constraints = ONE_TABLE_INF["list_of_constraints"]

                    for constraint in list_of_constraints:
                        if constraint["foreign_table_name"] == original_table_name:
                            return constraint

                    raise DoesntExistTableException("Doesn't exist table of tags (with FK) '{0}' that indicates the table '{1}'".format(table_of_tags_with_fk, original_table_name))

        return None

    def get_list_of_columns_name_in_str(self, list_of_columns_name_and_data_types, get_srid=True,
                                                table_name="", schema="public"):

        columns_name = ""
        last_index = len(list_of_columns_name_and_data_types) - 1

        for i in range(0, len(list_of_columns_name_and_data_types)):
            result = list_of_columns_name_and_data_types[i]

            columns_name += result["column_name"]

            # if there is a geometry column, so get the SRID together
            if "geometry" in result["data_type"] and get_srid:
                columns_name += ", Find_SRID('" + schema + "', '" + table_name + "', 'geom') as srid "

            # put a comma in the end of string while is not the last column
            if i != last_index:
                columns_name += ", "

        return columns_name

    def search_in_database_by_query(self, query_text, geom_format="wkt"):
        """
            Execute the `query_text`, with the result list, if some value has a datetime/data type,
            so it`s necessary to convert in a human readable string
        """

        # do the search in database
        self.__PGSQL_CURSOR__.execute(query_text)
        results_list = self.__PGSQL_CURSOR__.fetchall()

        # on the result list, if some value has a datetime/data type
        # so it`s necessary to convert in a human readable string
        for dict_result in results_list:
            # dict_result is one of the results
            for key, value in dict_result.items():

                # if the value is a datetime or date, so convert it in
                # a human readable string
                if isinstance(value, (datetime, date)):
                    dict_result[key] = value.isoformat()

        if geom_format == "wkt":
            # is default
            pass

        elif geom_format == "geojson":
            # convert the geoms in dict, because by default the postgresql returns in string the geojson
            for result in results_list:
                result["geom"] = convert_str_to_dict(result["geom"])

        else:
            raise GeomFormatException("Invalid geom format: " + geom_format)

        return results_list


    def insert_in_database_by_query(self, insert_query_text):
        """
            Insert the insert_query_text in DB and returns the id generated from this row
        """

        # do a INSERT in DB
        self.__PGSQL_CURSOR__.execute(insert_query_text)
        self.commit()

        # select the last value (id) from last row inserted
        self.__PGSQL_CURSOR__.execute('SELECT LASTVAL()')
        last_row_id = self.__PGSQL_CURSOR__.fetchone()['lastval']

        return last_row_id
