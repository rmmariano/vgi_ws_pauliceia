#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Responsible module to create handlers.
"""


from .base_controller import BaseHandler


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


# # Simple routine to run a query on a database and print the results:
# def doQuery( conn ) :
#     cur = conn.cursor()
#
#     cur.execute( "SELECT fname, lname FROM employee" )
#
#     for firstname, lastname in cur.fetchall() :
#         print(firstname, lastname)


class GetPoint(BaseHandler):

    urls = [r"/get/point/"]

    def get(self):
        print("/get/point/")


class AddPoint(BaseHandler):

    urls = [r"/add/point/"]

    def get(self):
        print("/add/point/")