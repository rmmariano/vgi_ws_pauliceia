#!/usr/bin/env python
# -*- coding: utf-8 -*-

from copy import deepcopy


__USER_STRUCT_COOKIE__ = {
    # information of the user
    "login": {
        "email": "",
        "type_login": ""
    },
    "information": {
        "id": "",
        "name": "",
    }
}

def get_new_user_struct_cookie():
    return deepcopy(__USER_STRUCT_COOKIE__)
