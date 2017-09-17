#!/usr/bin/env python
# -*- coding: utf-8 -*-


from ast import literal_eval


def convert_str_to_dict(string):
    return literal_eval(string)


def get_subclasses_from_class(vars_class):
    """
        Use: get_subclasses_from_class(vars()['NAME_CLASS'])
        :param vars_class: vars()['NAME_CLASS']
        :return: list with subclasses in a dict form: {"class_name": "class_name", "class_instance": instance}
    """

    return [{"class_name": cls.__name__, "class_instance": cls} for cls in vars_class.__subclasses__()]
