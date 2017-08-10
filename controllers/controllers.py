#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Responsible module to create handlers.
"""


from .base_controller import *
from bson import json_util



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

        list_of_columns_name_and_data_types = self.get_columns_name_and_data_types_from_table(table_name=table_name)
        columns_name = self.get_list_of_columns_name_in_str(list_of_columns_name_and_data_types)

        # print("columns_name: ", columns_name)

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
        results_list = self.search_in_database_by_query(query_text)

        # if result is empty
        if not results_list:
            # Not found values
            self.set_and_send_status(status=404,
                                     reason="Not found anything with id: " + id_value)
            return

        # if is all ok, return the result as JSON (convert dict to JSON)
        self.write(dumps(results_list, default=json_util.default))


class AddPoint(BaseHandler):

    # urls = [r"/add/point/"]
    urls = [r"/add/point/(?P<table_name>[^\/]+)",
            r"/add/point/(?P<table_name>[^\/]+)/"]

    def post(self, table_name):

        points_to_add = self.get_the_json_validated()

        print("\npoints_to_add: ", points_to_add)



        columns = "id_street, name, geom, number, id_user"
        values = "22, 'TEST', ST_GeomFromText('POINT(-46.98 -19.57)', 4326), 34, 6"

        insert_query_text = "INSERT INTO " + table_name + " (" + columns + ") VALUES (" + values + ")"

        print("\ninsert_query_text: ", insert_query_text)

        # cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)", (100, "abc'def"))

        status = self.__PGSQL_CURSOR__.execute(insert_query_text)

        PGSQL_CONNECTION.commit()




        print("\nstatus: ", status)









        self.set_and_send_status(status=201, reason="Added the points")


