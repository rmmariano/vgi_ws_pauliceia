#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Responsible module to create handlers.
"""


from .base_controller import *
from bson import json_util
from re import findall


class IndexHandler(BaseHandler):
    """
        Responsible class to render the Home Page (Index).
    """

    # A list of URLs that can be use for the HTTP methods
    urls = [r"/", r"/index", r"/index/"]

    def get(self):
        """
            Responsible method to be the GET method for the URLs listed in the attribute called urls.

            Args:
                Nothing until the moment.

            Returns:
                Just render the index page with some context given.

            Raises:
                Nothing until the moment.
        """

        # Some fictional context
        context = {"text": "Welcome"}

        # The ** before the context do that dictionary is "break" in the positions of the render method
        # The under line is like this: self.render("index.html", text = "Welcome")
        self.render("index.html", **context)


class SimplePageHandler(BaseHandler):
    """
        Responsible class to render the Home Page (Index).
    """

    # A list of URLs that can be use for the HTTP methods
    urls = [r"/", r"/simple_page", r"/simple_page/"]

    def get(self):

        # Some fictional context
        context = {"text": "Welcome"}

        # The ** before the context do that dictionary is "break" in the positions of the render method
        # The under line is like this: self.render("index.html", text = "Welcome")
        self.render("simple_page/simple_page.html", **context)


class GetPoint(BaseHandler):

    urls = [r"/get/point/(?P<table_name>[^\/]+)/(?P<id_value>[^\/]+)/",
            r"/get/point/(?P<table_name>[^\/]+)/(?P<id_value>[^\/]+)"]

    def get(self, table_name, id_value):

        list_of_columns_name_and_data_types = self.PGSQLConn.get_columns_name_and_data_types_from_table(table_name=table_name,
                                                                                                        transform_geom_bin_in_wkt=True)
        columns_name = self.PGSQLConn.get_list_of_columns_name_in_str(list_of_columns_name_and_data_types)

        # something like: 'SELECT id, id_street, ST_AsText(geom) as geom FROM tb_places'
        query_text = "SELECT " + columns_name + " FROM " + table_name

        if id_value.isdigit():
            # if id_value is a number, so search by it
            query_text += " WHERE id=" + id_value
        elif id_value.lower() == "all":
            # the query get all values by default
            pass
        else:
            # if id_value is not a digit and is not "all", so raise error
            self.set_and_send_status(status=400,
                                     reason="Invalid argument: " + id_value)
            return

        # run the query
        results_list = self.PGSQLConn.search_in_database_by_query(query_text)

        # if result is empty
        if not results_list:
            # Not found values
            self.set_and_send_status(status=404,
                                     reason="Not found anything with id: " + id_value)
            return

        # if is all ok, return the result as JSON (convert dict to JSON)
        self.write(dumps(results_list, default=json_util.default))


class AddPoint(BaseHandler):

    urls = [r"/add/point/(?P<table_name>[^\/]+)",
            r"/add/point/(?P<table_name>[^\/]+)/"]

    def post(self, table_name):

        points_to_add = self.get_the_json_validated()

        list_of_columns_name_and_data_types = self.PGSQLConn.get_columns_name_and_data_types_from_table(table_name=table_name,
                                                                                                        transform_geom_bin_in_wkt=False)
        # columns_name = self.PGSQLConn.get_list_of_columns_name_in_str(list_of_columns_name_and_data_types)

        columns = []
        values = []
        # masks = []

        for point in points_to_add:

            for field_of_table in list_of_columns_name_and_data_types:

                column_name = field_of_table["column_name"]
                data_type = field_of_table["data_type"]

                value = point[column_name]

                # to insert is necessary the column name exist in point dict
                # the column name shouldn't be "id", because is a PK autoincrement
                # if there is a None value, so doesn't add it
                if column_name in point and column_name != "id" and value is not None:
                    columns.append(column_name)
                    # masks.append("%s")

                    # if the value is a geometry in WKT, so we get the SRID and use the function
                    # ST_GeomFromText() to add the geometry
                    if 'geometry' in data_type:
                        # findall(r'\d+', data_type) will return a list of numbers in string: ['4326']
                        # findall(r'\d+', data_type)[0] will get the only element: '4326'
                        SRID = findall(r'\d+', data_type)[0]

                        # the value is a geometry in WKT, so to add it in DB
                        # we can use ST_GeomFromText() function
                        value = "ST_GeomFromText('" + value + "', " + SRID + ")"

                    # if value is text, so add two quotes, e.g.: 'TEST_'
                    elif isinstance(value, str):
                        value = "'" + value + "'"

                    values.append(value)

                    #

                    # value = str(value)
                    #
                    # # if the value is a geometry in WKT, so we get the SRID and use the function
                    # # ST_GeomFromText() to add the geometry
                    # if 'geometry' in data_type:
                    #     # findall(r'\d+', data_type) will return a list of numbers in string: ['4326']
                    #     # findall(r'\d+', data_type)[0] will get the only element: '4326'
                    #     SRID = findall(r'\d+', data_type)[0]
                    #
                    #     value = "ST_GeomFromText('" + value + "', " + SRID + ")"
                    #
                    # # if value is text, so add two quotes, e.g.: 'TEST_'
                    # elif not value.isdigit():
                    #     value = "'" + value + "'"
                    #
                    # values += value

                else:
                    # print("\nColumn ", field_of_table["column_name"], " of the table ", table_name,
                    #       " was not declared in point dict or column name is 'id' or the value is None. ",
                    #       "\ncolumn_name: ", column_name,
                    #       "\nvalue: ", value,
                    #       "\npoint: ", point)
                    pass

        columns = ", ".join(columns)
        # masks = ", ".join(masks)

        values = [str(value) for value in values]
        values = ", ".join(values)

        insert_query_text = "INSERT INTO " + table_name + " (" + columns + ") VALUES (" + values + ")"

        self.PGSQLConn.__PGSQL_CURSOR__.execute(insert_query_text)


        # insert_query_text = "INSERT INTO " + table_name + " (" + columns + ") VALUES (" + masks + ")"

        # cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)", (100, "abc'def"))
        # self.PGSQLConn.__PGSQL_CURSOR__.execute(insert_query_text, values)


        # save modifications in DB
        self.PGSQLConn.commit()

        self.set_and_send_status(status=201, reason="Added the points")

