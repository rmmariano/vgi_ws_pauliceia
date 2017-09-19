#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Responsible module to create handlers.
"""

from tornado.web import authenticated
from tornado.escape import xhtml_escape
from tornado.auth import GoogleOAuth2Mixin, FacebookGraphMixin
from tornado.gen import coroutine

from .base_controller import *
from bson import json_util
from re import findall

from settings.accounts import __FACEBOOK_SETTINGS__, __GOOGLE_SETTINGS__
from modules.util import get_subclasses_from_class


# pages

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


# pages of CRUD

class PageExampleCRUDGet(BaseHandler):

    # A list of URLs that can be use for the HTTP methods
    urls = [r"/example/crud/get", r"/example/crud/get/"]

    def get(self):

        # Some fictional context
        context = {"text": "Example of getting service"}

        # The ** before the context do that dictionary is "break" in the positions of the render method
        # The under line is like this: self.render("index.html", text = "Welcome")
        self.render("example/crud/get.html", **context)


class PageExampleCRUDAdd(BaseHandler):

    # A list of URLs that can be use for the HTTP methods
    urls = [r"/example/crud/add", r"/example/crud/add/"]

    def get(self):

        # Some fictional context
        context = {"text": "Example of addition service"}

        # The ** before the context do that dictionary is "break" in the positions of the render method
        # The under line is like this: self.render("index.html", text = "Welcome")
        self.render("example/crud/add.html", **context)


class PageExampleCRUDRemove(BaseHandler):
    # A list of URLs that can be use for the HTTP methods
    urls = [r"/example/crud/remove", r"/example/crud/remove/"]

    def get(self):
        # Some fictional context
        context = {"text": "Example of removing service"}

        # The ** before the context do that dictionary is "break" in the positions of the render method
        # The under line is like this: self.render("index.html", text = "Welcome")
        self.render("example/crud/remove.html", **context)



# authentication

class AuthLogoutHandler(BaseHandler):

    urls = [r"/auth/logout/", r"/auth/logout"]

    def get(self):
        self.clear_cookie("user")
        self.redirect(self.__AFTER_LOGGED_OUT_REDIRECT_TO__)


class AuthLoginHandler(BaseHandler):
    # Login
    # http://www.tornadoweb.org/en/stable/guide/security.html
    # http://guillaumevincent.com/2013/02/12/Basic-authentication-on-Tornado-with-a-decorator.html
    # https://github.com/tornadoweb/tornado/tree/stable/demos/blog

    urls = [r"/auth/login/", r"/auth/login"]

    def get(self):
        errormessage = self.get_argument("error", "")

        self.render("example/auth/login.html", errormessage=errormessage)

    def post(self):
        email = self.get_argument("email", "")
        password = self.get_argument("password", "")

        result = self.do_login(email, password)

        if result:
            self.set_current_user(email=email, type_login="normal", new_user=True)
            # user_cookie = self.get_current_user()

            self.set_and_send_status(status=200, reason="Logged in system")
            return
            # super(BaseHandler, self).redirect(self.__AFTER_LOGGED_REDIRECT_TO__)
        else:
            self.set_and_send_status(status=404, reason="Login is invalid. Correct them and try again.")
            return


class GoogleLoginHandler(BaseHandler, GoogleOAuth2Mixin):
    """
        Tornado Auth:
        http://www.tornadoweb.org/en/stable/auth.html


    """

    urls = [r"/auth/google/", r"/auth/google"]

    redirect_uri = "http://localhost:8888/auth/google/"

    @coroutine
    def get(self):

        self.application.settings['google_oauth'] = __GOOGLE_SETTINGS__['google_oauth']

        if self.get_argument('code', False):
            access = yield self.get_authenticated_user(
                            redirect_uri=self.redirect_uri,
                            code=self.get_argument('code'))
            user = yield self.oauth2_request(
                            "https://www.googleapis.com/oauth2/v1/userinfo",
                            access_token=access["access_token"])

            # for key in user:
            #     print(key, ": ", user[key])
            # print(user)

            self.set_current_user(email=user["email"], type_login="google", new_user=True)
            # user_cookie = self.get_current_user()
            #
            # self.set_and_send_status(status=200, reason="Logged in system")
            super(BaseHandler, self).redirect(self.__AFTER_LOGGED_REDIRECT_TO__)
        else:
            yield self.authorize_redirect(
                redirect_uri=self.redirect_uri,
                client_id=self.settings['google_oauth']['key'],
                scope=['profile', 'email'],
                response_type='code',
                extra_params={'approval_prompt': 'auto'}
            )


class FacebookLoginHandler(BaseHandler, FacebookGraphMixin):
    """
        Tornado Auth:
        http://www.tornadoweb.org/en/stable/auth.html

        How to create a new Facebook App:
        https://developers.facebook.com/docs/apps/register
        https://developers.facebook.com/docs/apps/register#developer-account

        In the Facebook App page in App Domains, add the domain of the server,
        in this case "localhost" and in the web site "http://localhost:8888/".
        https://developers.facebook.com/apps/461266394258303/settings/

        Permissions:
        https://developers.facebook.com/docs/facebook-login/permission
    """

    urls = [r"/auth/facebook/", r"/auth/facebook"]

    redirect_uri = "http://localhost:8888/auth/facebook/"

    @coroutine
    def get(self):

        self.application.settings['facebook_api_key'] = __FACEBOOK_SETTINGS__['facebook_api_key']
        self.application.settings['facebook_secret'] = __FACEBOOK_SETTINGS__['facebook_secret']

        if self.get_argument("code", False):
            user = yield self.get_authenticated_user(
                    redirect_uri=self.redirect_uri,
                    client_id=self.settings["facebook_api_key"],
                    client_secret=self.settings["facebook_secret"],
                    code=self.get_argument("code"),
                    extra_fields=['email']
            )

            # for key in user:
            #     print(key, ": ", user[key])
            # print(user)

            self.set_current_user(email=user["email"], type_login="facebook", new_user=True)
            # user_cookie = self.get_current_user()
            #
            # self.set_and_send_status(status=200, reason="Logged in system")
            super(BaseHandler, self).redirect(self.__AFTER_LOGGED_REDIRECT_TO__)
        else:
            yield self.authorize_redirect(
                    redirect_uri=self.redirect_uri,
                    client_id=self.settings["facebook_api_key"],
                    extra_params={"scope": "user_posts,email"}
            )


# login and logout with success

class AuthLoginSuccessHandler(BaseHandler):

    # nl = need login
    urls = [r"/auth/login/success/", r"/auth/login/success"]

    def get(self):
        self.render("example/auth/login_success.html")


class AuthLogoutSuccessHandler(BaseHandler):

    # nl = need login
    urls = [r"/auth/logout/success/", r"/auth/logout/success"]

    def get(self):
        self.render("example/auth/logout.html")


# other handlers

class MainHandlerNeedLogin(BaseHandler):

    # nl = need login
    urls = [r"/main/nl/", r"/main/nl"]

    @authenticated
    def get(self):
        username = xhtml_escape(self.current_user)
        self.render("example/main/mainneedlogin.html", username=username)


class MainHandlerDontNeedLogin(BaseHandler):

    # dnl = don't need login
    urls = [r"/main/dnl/", r"/main/dnl"]

    def get(self):
        username = xhtml_escape(self.current_user)
        self.render("example/main/maindontneedlogin.html", username=username)


# geometry

# TODO: GET WITH TAGS (?)
class GetGeometry(BaseHandler):

    urls = [r"/get/geometry/(?P<table_name>[^\/]+)/?(?P<params>[A-Za-z0-9-]+)?"]

    def get(self, table_name, params):

        ####################################################################################
        # getting the parameters
        try:
            query = self.get_argument("q")
        except MissingArgumentError:
            self.set_and_send_status(status=400,
                                     reason="It's necessary at least the query parameter (q)",
                                     raise_error=False)
            return

        geom_format = self.get_param_geometry_format()

        ####################################################################################
        # get the query from URL in form of dictionary
        QUERY_PARAM = self.get_dict_from_query_str(query)

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

        if not result["exist_params_in_table_columns"]:
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

        ####################################################################################
        # create the WHERE clause
        where = self.build_where_clause_with_params(QUERY_PARAM)

        ####################################################################################
        # something like: 'SELECT id, id_street, ST_AsText(geom) as geom FROM tb_places'
        # query_text = "SELECT " + str_columns_names + " FROM " + table_name
        query_text = "SELECT {0} FROM {1} {2};".format(str_columns_names, table_name, where)

        ####################################################################################
        # run the query
        # something like: 'SELECT id, id_street, ST_AsText(geom) as geom, ... date
        # FROM tb_places WHERE id=45 AND lower(name) LIKE lower(\\'%Pref%\\')'
        results_list = self.PGSQLConn.search_in_database_by_query(query_text, geom_format=geom_format)

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


class AddGeometry(BaseHandler):
    # TODO: create a ADD OR UPDATE HERE

    urls = [r"/add/geometry/(?P<table_name>[^\/]+)/?(?P<params>[A-Za-z0-9-]+)?"]

    def options(self, table_name, params):
        super(BaseHandler, self).options()

    @authenticated
    def post(self, table_name, params):
        # TODO: get id user from logged user ("id_user": 6)

        ####################################################################################
        # getting the parameters

        geom_format = self.get_param_geometry_format()

        ####################################################################################

        geometries_to_add = self.get_the_json_validated()

        list_of_columns_name_and_data_types = self.PGSQLConn.get_columns_name_and_data_types_from_table(table_name=table_name,
                                                                                                        transform_geom_bin_in_wkt=False)

        ####################################################################################

        invalid_columns = []  # columns that is in JSON, but doesn't exist in DB

        for geometry in geometries_to_add:

            columns = []
            values = []
            # masks = []

            for key_field in geometry:

                column_name = key_field
                value = geometry[key_field]

                # to insert is necessary the column name exist in point dict
                if self.key_exist_in_list_of_columns_name_and_data_types(column_name,
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
                                geojson = str(value).replace("'", '"')
                                value = "ST_SetSRID(ST_GeomFromGeoJSON('" + geojson + "'), " + SRID + ")"
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
                    # columns that is in JSON, but doesn't exist in DB
                    # how tags is a key word, so it is a exception
                    if column_name != "tags":
                        invalid_columns.append({column_name: value})


            ####################################################################################
            # building the values

            str_columns = ", ".join(columns)
            # masks = ", ".join(masks)

            str_values = [str(value) for value in values]
            str_values = ", ".join(str_values)

            ####################################################################################
            # inserting geometry in DB

            # something like this:
            # INSERT INTO tb_places (id_street, geom, number, name)
            # VALUES (22, ST_GeomFromText('POINT(-518.644 -269.159)', 4326), 34, 'TEST_1')
            insert_query_text = "INSERT INTO " + table_name + " (" + str_columns + ") VALUES (" + str_values + ");"

            id_generated_geom = self.PGSQLConn.insert_in_database_by_query(insert_query_text)

            ####################################################################################
            # inserting tags in DB

            if "tags" in geometry:

                try:
                    table_of_tags = self.PGSQLConn.get_table_of_tags_from_table_name(table_name)
                except DoesntExistTableException as e:
                    self.set_and_send_status(status=404,
                                             reason=e.value,
                                             raise_error=False)
                    return

                # if exist a table of tags for the table name passed
                if table_of_tags is not None:

                    list_tags = geometry["tags"]

                    list_columns_types_tags = self.PGSQLConn.get_columns_name_and_data_types_from_table(table_name=table_of_tags,
                                                                                                        transform_geom_bin_in_wkt=False)

                    for tag in list_tags:

                        columns = []
                        values = []

                        for key_field in tag:
                            column_name = key_field
                            value = tag[key_field]

                            # to insert is necessary the column name exist in point dict
                            if self.key_exist_in_list_of_columns_name_and_data_types(column_name,
                                                                                     list_columns_types_tags):

                                # the column name shouldn't be "id", because is a PK autoincrement
                                # if there is a None value, so doesn't add it
                                if column_name != "id" and value is not None:
                                    value = "'" + value + "'"

                                    columns.append(column_name)
                                    values.append(value)
                            else:
                                # columns that is in JSON, but doesn't exist in DB
                                invalid_columns.append({column_name: value})

                        ####################################################################################
                        # building the values

                        # getting the foreign key
                        constraint = self.PGSQLConn.get_constraint_about_table_of_tags_from_table_name(table_of_tags, table_name)
                        fk_column_name = constraint["column_name"]

                        # adding the foreign key column
                        columns.append(fk_column_name)
                        values.append(id_generated_geom)

                        # concatenate the lists
                        str_columns = ", ".join(columns)

                        str_values = [str(value) for value in values]
                        str_values = ", ".join(str_values)

                        ####################################################################################
                        # inserting geometry in DB

                        # something like this:
                        # INSERT INTO node_tags (k, v, fk_id_node) VALUES ('tipo1', 'tipo111', 75);
                        insert_query_text = "INSERT INTO node_tags ({0}) VALUES ({1})".format(str_columns, str_values)

                        self.PGSQLConn.insert_in_database_by_query(insert_query_text)


        ####################################################################################
        # if there are invalid columns, create a extra message to it

        extra = self.create_extra_message_to_invalid_columns(invalid_columns)

        ####################################################################################
        # sending the successful message

        self.set_and_send_status(status=201, reason="Added the points", extra=extra)


class RemoveGeometry(BaseHandler):

    urls = [r"/remove/geometry/(?P<table_name>[^\/]+)/?(?P<params>[A-Za-z0-9-]+)?"]

    @authenticated
    def get(self, table_name, params):

        ####################################################################################
        # getting the parameters
        try:
            query = self.get_argument("q")
        except MissingArgumentError:
            self.set_and_send_status(status=400,
                                     reason="It's necessary at least the query parameter (q)",
                                     raise_error=False)
            return

        ####################################################################################
        # get the query from URL in form of dictionary
        QUERY_PARAM = self.get_dict_from_query_str(query)

        # if the param is "all", raise exception, because the client CAN'T remove ALL records in DB by service
        if QUERY_PARAM == "all":
            self.set_and_send_status(status=400, reason="It is not possible use the 'all' parameter in removing service",
                                     raise_error=False)
            return

        ####################################################################################

        try:
            list_of_columns_name_and_data_types = self.PGSQLConn.get_columns_name_and_data_types_from_table(
                                                                                        table_name=table_name,
                                                                                        transform_geom_bin_in_wkt=True)
        except GeomFormatException as e:
            self.set_and_send_status(status=400, reason=e.value,
                                     raise_error=False)
            return

        ####################################################################################
        # verify if the params are valid
        result = self.exist_paramns_in_table_columns(list_of_columns_name_and_data_types, QUERY_PARAM)

        if not result["exist_params_in_table_columns"]:
            self.set_and_send_status(status=400,
                                     reason="Invalid arguments: " + str(result["invalid_columns"]),
                                     raise_error=False)
            return

        ####################################################################################
        # create the WHERE clause
        where = self.build_where_clause_with_params(QUERY_PARAM)

        ####################################################################################
        # something like: 'SELECT id, id_street, ST_AsText(geom) as geom FROM tb_places'
        # query_text = "SELECT " + str_columns_names + " FROM " + table_name
        query_text = "DELETE FROM {0} {1};".format(table_name, where)

        ####################################################################################
        # run the query
        # something like: DELETE FROM tb_places WHERE name like 'TEST%';
        number_removed = self.PGSQLConn.delete_in_database_by_query(query_text)

        ####################################################################################

        if number_removed > 0:
            extra = {"message": "Number of rows removed", "number": number_removed}
            self.set_and_send_status(status=200, reason="Removed the point(s)", extra=extra)
        else:
            self.set_and_send_status(status=400, reason="No point was removed")



# tag

class GetTag(BaseHandler):

    urls = [r"/get/tag/(?P<table_name>[^\/]+)/?(?P<params>[A-Za-z0-9-]+)?"]

    def get(self, table_name, params):

        ####################################################################################
        # getting the parameters
        try:
            query = self.get_argument("q")
        except MissingArgumentError:
            self.set_and_send_status(status=400,
                                     reason="It's necessary at least the query parameter (q)",
                                     raise_error=False)
            return

        geom_format = self.get_param_geometry_format()

        ####################################################################################
        # get the query from URL in form of dictionary
        QUERY_PARAM = self.get_dict_from_query_str(query)

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

        if not result["exist_params_in_table_columns"]:
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

        ####################################################################################
        # create the WHERE clause
        where = self.build_where_clause_with_params(QUERY_PARAM)

        ####################################################################################
        # something like: 'SELECT id, id_street, ST_AsText(geom) as geom FROM tb_places'
        # query_text = "SELECT " + str_columns_names + " FROM " + table_name
        query_text = "SELECT {0} FROM {1} {2};".format(str_columns_names, table_name, where)

        ####################################################################################
        # run the query
        # something like: 'SELECT id, id_street, ST_AsText(geom) as geom, ... date
        # FROM tb_places WHERE id=45 AND lower(name) LIKE lower(\\'%Pref%\\')'
        results_list = self.PGSQLConn.search_in_database_by_query(query_text, geom_format=geom_format)

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


class AddTag(BaseHandler):
    # TODO: create a ADD OR UPDATE HERE

    urls = [r"/add/tag/(?P<table_name>[^\/]+)/?(?P<params>[A-Za-z0-9-]+)?"]

    def post(self, table_name, params):
        # TODO: get id user from logged user ("id_user": 6)

        ####################################################################################
        # getting the parameters

        geom_format = self.get_param_geometry_format()

        ####################################################################################

        geometries_to_add = self.get_the_json_validated()

        list_of_columns_name_and_data_types = self.PGSQLConn.get_columns_name_and_data_types_from_table(table_name=table_name,
                                                                                                        transform_geom_bin_in_wkt=False)

        ####################################################################################

        invalid_columns = []  # columns that is in JSON, but doesn't exist in DB

        for geometry in geometries_to_add:

            columns = []
            values = []
            # masks = []

            for key_field in geometry:

                column_name = key_field
                value = geometry[key_field]

                # to insert is necessary the column name exist in point dict
                if self.key_exist_in_list_of_columns_name_and_data_types(column_name,
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
                                geojson = str(value).replace("'", '"')
                                value = "ST_SetSRID(ST_GeomFromGeoJSON('" + geojson + "'), " + SRID + ")"
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
                    # columns that is in JSON, but doesn't exist in DB
                    # how tags is a key word, so it is a exception
                    if column_name != "tags":
                        invalid_columns.append({column_name: value})


            ####################################################################################
            # building the values

            str_columns = ", ".join(columns)
            # masks = ", ".join(masks)

            str_values = [str(value) for value in values]
            str_values = ", ".join(str_values)

            ####################################################################################
            # inserting geometry in DB

            # something like this:
            # INSERT INTO tb_places (id_street, geom, number, name)
            # VALUES (22, ST_GeomFromText('POINT(-518.644 -269.159)', 4326), 34, 'TEST_1')
            insert_query_text = "INSERT INTO " + table_name + " (" + str_columns + ") VALUES (" + str_values + ");"

            id_generated_geom = self.PGSQLConn.insert_in_database_by_query(insert_query_text)

            ####################################################################################
            # inserting tags in DB

            if "tags" in geometry:

                try:
                    table_of_tags = self.PGSQLConn.get_table_of_tags_from_table_name(table_name)
                except DoesntExistTableException as e:
                    self.set_and_send_status(status=404,
                                             reason=e.value,
                                             raise_error=False)
                    return

                # if exist a table of tags for the table name passed
                if table_of_tags is not None:

                    list_tags = geometry["tags"]

                    list_columns_types_tags = self.PGSQLConn.get_columns_name_and_data_types_from_table(table_name=table_of_tags,
                                                                                                        transform_geom_bin_in_wkt=False)

                    for tag in list_tags:

                        columns = []
                        values = []

                        for key_field in tag:
                            column_name = key_field
                            value = tag[key_field]

                            # to insert is necessary the column name exist in point dict
                            if self.key_exist_in_list_of_columns_name_and_data_types(column_name,
                                                                                     list_columns_types_tags):

                                # the column name shouldn't be "id", because is a PK autoincrement
                                # if there is a None value, so doesn't add it
                                if column_name != "id" and value is not None:
                                    value = "'" + value + "'"

                                    columns.append(column_name)
                                    values.append(value)
                            else:
                                # columns that is in JSON, but doesn't exist in DB
                                invalid_columns.append({column_name: value})

                        ####################################################################################
                        # building the values

                        # getting the foreign key
                        constraint = self.PGSQLConn.get_constraint_about_table_of_tags_from_table_name(table_of_tags, table_name)
                        fk_column_name = constraint["column_name"]

                        # adding the foreign key column
                        columns.append(fk_column_name)
                        values.append(id_generated_geom)

                        # concatenate the lists
                        str_columns = ", ".join(columns)

                        str_values = [str(value) for value in values]
                        str_values = ", ".join(str_values)

                        ####################################################################################
                        # inserting geometry in DB

                        # something like this:
                        # INSERT INTO node_tags (k, v, fk_id_node) VALUES ('tipo1', 'tipo111', 75);
                        insert_query_text = "INSERT INTO node_tags ({0}) VALUES ({1})".format(str_columns, str_values)

                        self.PGSQLConn.insert_in_database_by_query(insert_query_text)


        ####################################################################################
        # if there are invalid columns, create a extra message to it

        extra = self.create_extra_message_to_invalid_columns(invalid_columns)

        ####################################################################################
        # sending the successful message

        self.set_and_send_status(status=201, reason="Added the points", extra=extra)


class RemoveTag(BaseHandler):

    urls = [r"/remove/tag/(?P<table_name>[^\/]+)/?(?P<params>[A-Za-z0-9-]+)?"]

    def get(self, table_name, params):

        ####################################################################################
        # getting the parameters
        try:
            query = self.get_argument("q")
        except MissingArgumentError:
            self.set_and_send_status(status=400,
                                     reason="It's necessary at least the query parameter (q)",
                                     raise_error=False)
            return

        ####################################################################################
        # get the query from URL in form of dictionary
        QUERY_PARAM = self.get_dict_from_query_str(query)

        # if the param is "all", raise exception, because the client CAN'T remove ALL records in DB by service
        if QUERY_PARAM == "all":
            self.set_and_send_status(status=400, reason="It is not possible use the 'all' parameter in removing service",
                                     raise_error=False)
            return

        ####################################################################################

        try:
            list_of_columns_name_and_data_types = self.PGSQLConn.get_columns_name_and_data_types_from_table(
                                                                                        table_name=table_name,
                                                                                        transform_geom_bin_in_wkt=True)
        except GeomFormatException as e:
            self.set_and_send_status(status=400, reason=e.value,
                                     raise_error=False)
            return

        ####################################################################################
        # verify if the params are valid
        result = self.exist_paramns_in_table_columns(list_of_columns_name_and_data_types, QUERY_PARAM)

        if not result["exist_params_in_table_columns"]:
            self.set_and_send_status(status=400,
                                     reason="Invalid arguments: " + str(result["invalid_columns"]),
                                     raise_error=False)
            return

        ####################################################################################
        # create the WHERE clause
        where = self.build_where_clause_with_params(QUERY_PARAM)

        ####################################################################################
        # something like: 'SELECT id, id_street, ST_AsText(geom) as geom FROM tb_places'
        # query_text = "SELECT " + str_columns_names + " FROM " + table_name
        query_text = "DELETE FROM {0} {1};".format(table_name, where)

        ####################################################################################
        # run the query
        # something like: DELETE FROM tb_places WHERE name like 'TEST%';
        number_removed = self.PGSQLConn.delete_in_database_by_query(query_text)

        ####################################################################################

        if number_removed > 0:
            extra = {"message": "Number of rows removed", "number": number_removed}
            self.set_and_send_status(status=200, reason="Removed the point(s)", extra=extra)
        else:
            self.set_and_send_status(status=400, reason="No point was removed")


# CONSTANTS

__LIST_BASEHANDLER_SUBCLASSES__ = get_subclasses_from_class(vars()['BaseHandler'])

# print("BaseHandler subclasses: ", __LIST_BASEHANDLER_SUBCLASSES__)