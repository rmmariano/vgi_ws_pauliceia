#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Responsible module to create handlers.
"""


from tornado.web import HTTPError, MissingArgumentError

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


# Login
# http://www.tornadoweb.org/en/stable/guide/security.html
# http://guillaumevincent.com/2013/02/12/Basic-authentication-on-Tornado-with-a-decorator.html


class GetGeometry(BaseHandler):

    urls = [r"/get/geometry/(?P<table_name>[^\/]+)/?(?P<params>[A-Za-z0-9-]+)?"]

    def get(self, table_name, params):
        # parameters = self.request.arguments

        ####################################################################################
        # getting the parameters

        try:
            query = self.get_argument("q")
        except MissingArgumentError:
            self.set_and_send_status(status=400,
                                     reason="It's necessary at least the query parameter (q)",
                                     raise_error=False)
            return

        # try:
        #     geom_format = self.get_argument("geom_format")
        # except MissingArgumentError:
        #     # if geom_format is undefined, return "wkt" by default
        #     geom_format = "wkt"

        geom_format = self.get_param_geometry_format()

        ####################################################################################

        # get the query from URL in form of dictionary
        QUERY_PARAM = self.get_dict_from_query_str(query)
        # remove the query, because I have already got it
        # del parameters["q"]

        ####################################################################################

        try:
            list_of_columns_name_and_data_types = self.PGSQLConn.get_columns_name_and_data_types_from_table(table_name=table_name,
                                                                                                            transform_geom_bin_in_wkt=True,
                                                                                                            geom_format=geom_format)
        except GeomFormatException as e:
            self.set_and_send_status(status=400, reason=e.value,
                                     raise_error=False)
                                     # raise_error=True)
            return

        ####################################################################################

        # verify if the params are valid
        result = self.exist_paramns_in_table_columns(list_of_columns_name_and_data_types, QUERY_PARAM)

        if not result["exist_paramns_in_table_columns"]:
            self.set_and_send_status(status=400,
                                     reason="Invalid arguments: " + str(result["invalid_columns"]),
                                     raise_error=False)
                                    # raise_error=True)
            return

        ####################################################################################

        # get the columns in string to put in query
        str_columns_names = self.PGSQLConn.get_list_of_columns_name_in_str(list_of_columns_name_and_data_types,
                                                                           get_srid=True,
                                                                           table_name=table_name,
                                                                           schema="public")

        # something like: 'SELECT id, id_street, ST_AsText(geom) as geom FROM tb_places'
        query_text = "SELECT " + str_columns_names + " FROM " + table_name

        ####################################################################################

        # add the where clause in the end of query
        query_text += self.build_where_clause_with_params(QUERY_PARAM)

        ####################################################################################

        # run the query
        results_list = self.PGSQLConn.search_in_database_by_query(query_text, geom_format=geom_format)
        # 'SELECT id, id_street, ST_AsText(geom) as geom, ... date
        # FROM tb_places WHERE id=45 AND lower(name) LIKE lower(\\'%Pref%\\')'

        # if result is empty
        if not results_list:
            # Not found values
            self.set_and_send_status(status=404,
                                     reason="Not found anything with the arguments",
                                     raise_error=False)
                                    # raise_error=True)
            return

        ####################################################################################

        # if is all ok, return the result as JSON (convert dict to JSON)
        self.write(dumps(results_list, default=json_util.default))


class AddPoint(BaseHandler):

    urls = [
            # r"/add/point/(?P<table_name>[^\/]+)",
            # r"/add/point/(?P<table_name>[^\/]+)/",
            r"/add/point/(?P<table_name>[^\/]+)/?(?P<params>[A-Za-z0-9-]+)?"
            ]

    def post(self, table_name, params):
        # TODO: get id user from logged user ("id_user": 6)

        ####################################################################################
        # getting the parameters

        geom_format = self.get_param_geometry_format()

        ####################################################################################

        geometries_to_add = self.get_the_json_validated()

        list_of_columns_name_and_data_types = self.PGSQLConn.get_columns_name_and_data_types_from_table(table_name=table_name,
                                                                                                        transform_geom_bin_in_wkt=False)

        columns = []
        values = []
        # masks = []
        tags = []

        for geometry in geometries_to_add:
            for key_field in geometry:

                column_name = key_field
                value = geometry[key_field]

                # to insert is necessary the column name exist in point dict
                if self.key_exist_in_list_of_columns_name_and_data_types(key_field,
                                                                         list_of_columns_name_and_data_types):

                    # the column name shouldn't be "id", because is a PK autoincrement
                    # if there is a None value, so doesn't add it
                    if column_name != "id" and value is not None:

                        # get the data type of the column
                        data_type = self.get_data_type_of_column_in_list_of_columns_name_and_data_types(column_name,
                                                                                                        list_of_columns_name_and_data_types)

                        # if the value is a geometry, so we get the SRID and use the function
                        # and use a specific function to add (WKT or geojson)
                        if 'geometry' in data_type:
                            # findall(r'\d+', data_type) will return a list of numbers in string: ['4326']
                            # findall(r'\d+', data_type)[0] will get the only element: '4326'
                            SRID = findall(r'\d+', data_type)[0]

                            if geom_format == "wkt":
                                # we can use ST_GeomFromText() function, to add WKT in DB
                                value = "ST_GeomFromText('" + value + "', " + SRID + ")"
                            elif geom_format == "geojson":
                                # we can use ST_GeomFromText() function, to add WKT in DB
                                geojson = str(value)

                                geojson = geojson.replace("'", '"')

                                value = "ST_SetSRID(ST_GeomFromGeoJSON('" + geojson + "'), " + SRID + ")"

                                print(value)



                                #
                                '''

                                insert into testbert1(id, location)
                                values(1, ST_SetSRID(
                                ST_GeomFromGeoJSON(
                                                    '{"type":"Polygon",
                                                    "coordinates":[[[-114.017347,51.048005],
                                                    [-114.014433,51.047927],[-114.005899,51.045381],
                                                    [-114.017347,51.048005]]]}'
                                                    ),
                                                     4326))
                                                     
                                                     
                                ST_SetSRID(ST_GeomFromGeoJSON(''),4326))


                                '''
                                #


                            else:
                                self.set_and_send_status(status=400,
                                                         reason="Invalid geom_format: " + geom_format,
                                                         raise_error=False)
                                return

                        # if value is text, so add two quotes, e.g.: 'TEST_'
                        elif isinstance(value, str):
                            value = "'" + value + "'"

                        columns.append(column_name)
                        values.append(value)
                else:
                    # if the column doens't exist in list of columns, so it is a tag
                    tags.append({column_name: value})


        # for point in geometries_to_add:
        #
        #     for field_of_table in list_of_columns_name_and_data_types:
        #
        #         column_name = field_of_table["column_name"]
        #         data_type = field_of_table["data_type"]
        #
        #         # if column_name in point:
        #         value = point[column_name]
        #
        #         # to insert is necessary the column name exist in point dict
        #         # the column name shouldn't be "id", because is a PK autoincrement
        #         # if there is a None value, so doesn't add it
        #         if column_name in point and column_name != "id" and value is not None:
        #             columns.append(column_name)
        #             # masks.append("%s")
        #
        #             # if the value is a geometry (in WKT), so we get the SRID and use the function
        #             # ST_GeomFromText() to add the geometry
        #             if 'geometry' in data_type:
        #                 # findall(r'\d+', data_type) will return a list of numbers in string: ['4326']
        #                 # findall(r'\d+', data_type)[0] will get the only element: '4326'
        #                 SRID = findall(r'\d+', data_type)[0]
        #
        #                 # the value is a geometry in WKT, so to add it in DB
        #                 # we can use ST_GeomFromText() function
        #                 value = "ST_GeomFromText('" + value + "', " + SRID + ")"
        #
        #             # if value is text, so add two quotes, e.g.: 'TEST_'
        #             elif isinstance(value, str):
        #                 value = "'" + value + "'"
        #
        #             values.append(value)
        #
        #         else:
        #             # print("\nColumn ", field_of_table["column_name"], " of the table ", table_name,
        #             #       " was not declared in point dict or column name is 'id' or the value is None. ",
        #             #       "\ncolumn_name: ", column_name,
        #             #       "\nvalue: ", value,
        #             #       "\npoint: ", point)
        #             pass


        ####################################################################################
        # inserting geometry in DB

        columns = ", ".join(columns)
        # masks = ", ".join(masks)

        values = [str(value) for value in values]
        values = ", ".join(values)

        # something like this:
        # INSERT INTO tb_places (id_street, geom, number, name)
        # VALUES (22, ST_GeomFromText('POINT(-518.644 -269.159)', 4326), 34, 'TEST_1')
        insert_query_text = "INSERT INTO " + table_name + " (" + columns + ") VALUES (" + values + ")"

        # self.PGSQLConn.__PGSQL_CURSOR__.execute(insert_query_text)
        self.PGSQLConn.execute(insert_query_text)


        ####################################################################################
        # inserting tags in DB

        # TODO: add tags in DB
        # for tag in tags:
        #     print(tag)



        # insert_query_text = "INSERT INTO " + table_name + " (" + columns + ") VALUES (" + masks + ")"
        # cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)", (100, "abc'def"))
        # self.PGSQLConn.__PGSQL_CURSOR__.execute(insert_query_text, values)


        ####################################################################################
        # saving modifications and sending the successful message

        # save modifications in DB
        self.PGSQLConn.commit()

        self.set_and_send_status(status=201, reason="Added the points")

