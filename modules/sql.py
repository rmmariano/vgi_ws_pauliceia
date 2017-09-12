#!/usr/bin/env python
# -*- coding: utf-8 -*-


class SQLHelper:

    def __init__(self, pgsql_cursor):
        self.__PGSQL_CURSOR__ = pgsql_cursor

    def get_columns_name_and_data_types_of_table_name(self, table_name):

        query = """
                    SELECT a.attname as column_name, format_type(a.atttypid, a.atttypmod) as data_type
                    FROM pg_attribute a JOIN pg_class b ON (a.attrelid = b.relfilenode)
                    WHERE b.relname = '{0}' and a.attstattarget = -1;
                 """.format(table_name)

        self.__PGSQL_CURSOR__.execute(query)
        list_of_columns_name_and_data_types = self.__PGSQL_CURSOR__.fetchall()

        return list_of_columns_name_and_data_types

    def get_constraints_of_table_name(self, table_name):

        query = """
                    SELECT
                        tc.constraint_name, tc.table_name, kcu.column_name, 
                        ccu.table_name AS foreign_table_name,
                        ccu.column_name AS foreign_column_name 
                    FROM 
                        information_schema.table_constraints AS tc 
                        JOIN information_schema.key_column_usage AS kcu
                          ON tc.constraint_name = kcu.constraint_name
                        JOIN information_schema.constraint_column_usage AS ccu
                          ON ccu.constraint_name = tc.constraint_name
                    WHERE constraint_type = 'FOREIGN KEY' AND tc.table_name='{0}';        
                """.format(table_name)

        self.__PGSQL_CURSOR__.execute(query)
        list_of_constraints = self.__PGSQL_CURSOR__.fetchall()

        return list_of_constraints


