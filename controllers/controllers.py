#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Responsible module to create handlers.
"""


from .base_controller import *
from json import dumps


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

    # urls = [r"/get/point/"]
    # urls = [r"/get/point/([^/]+)"]

    # urls = [r"/get/point/(?P<id>[^\/]+)/", r"/get/point/(?P<id>[^\/]+)"]
    urls = [r"/get/point/(?P<table_name>[^\/]+)/(?P<id_value>[^\/]+)/",
            r"/get/point/(?P<table_name>[^\/]+)/(?P<id_value>[^\/]+)"]

    def get(self, table_name, id_value):

        query_text = "SELECT id, number, original_number FROM " + table_name

        if id_value.isdigit():
            # if id_value is a number, so search by it
            query_text += " WHERE id=" + id_value
        elif id_value.lower() == "all":
            # the query get all values by default
            pass
        else:
            # if id_value is not a digit and is not "all", so raise error
            status = 400
            reason = "Invalid argument: " + id_value

            self.set_status(status, reason=reason)
            self.write(dumps({"status": status, "statusText": reason}))
            return

        # run the query
        result = self.search_in_database_by_query(query_text)

        # if result is empty
        if not result:
            # Not found values
            status = 404
            reason = "Not found anything with id: " + id_value

            self.set_status(status, reason=reason)
            self.write(dumps({"status": status, "statusText": reason}))
            return

        # if is all ok, return the result as JSON
        self.write(dumps(result))


class AddPoint(BaseHandler):

    urls = [r"/add/point/"]

    def get(self):
        print("/add/point/")