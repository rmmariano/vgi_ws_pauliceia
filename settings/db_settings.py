#!/usr/bin/env python
# -*- coding: utf-8 -*-


from sys import exit

from psycopg2 import connect, DatabaseError


__PGSQL_CONNECTION_SETTINGS__ = {
    "HOSTNAME": "HOSTNAME",
    "USERNAME": "USERNAME",
    "PASSWORD": "PASSWORD",
    "DATABASE": "DATABASE",
    "PORT": 5432
}


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
