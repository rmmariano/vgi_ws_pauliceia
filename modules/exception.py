#!/usr/bin/env python
# -*- coding: utf-8 -*-


class GeomFormatException(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class DoesntExistTableException(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)