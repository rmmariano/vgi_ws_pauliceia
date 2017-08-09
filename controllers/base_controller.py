#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Responsible module to create base handlers.
"""


from tornado.web import RequestHandler
from psycopg2.extras import RealDictCursor

# Let importing ALL
from models import *


class BaseHandler(RequestHandler):
    """
        Responsible class to be a base handler for the others classes.
        It extends of the RequestHandler class.
    """

    # Static list to be added the all valid urls to one handler
    urls = []

    def search_in_database_by_query(self, query_text):
        # do the search in database
        cur = PGSQL_CONNECTION.cursor(cursor_factory=RealDictCursor)
        cur.execute(query_text)
        result = cur.fetchall()

        return result
