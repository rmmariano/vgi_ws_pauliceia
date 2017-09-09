#!/usr/bin/env python
# -*- coding: utf-8 -*-


from ast import literal_eval


def convert_str_to_dict(string):
    return literal_eval(string)
