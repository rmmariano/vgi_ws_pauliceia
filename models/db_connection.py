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
from psycopg2 import connect, DatabaseError

from settings.db_settings import __PGSQL_CONNECTION_SETTINGS__


PGSQL_CONNECTION = ""

print("\nConnecting in PostgreSQL with:"
      "\n- hostname: ", __PGSQL_CONNECTION_SETTINGS__["HOSTNAME"],
      "\n- port: ", __PGSQL_CONNECTION_SETTINGS__["PORT"],
      "\n- database: ", __PGSQL_CONNECTION_SETTINGS__["DATABASE"], "\n")

try:
    PGSQL_CONNECTION = connect(host=__PGSQL_CONNECTION_SETTINGS__["HOSTNAME"],
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

