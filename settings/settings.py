#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Responsible module to put the configurations of the system.
"""


import os
from datetime import datetime


# Put the reference of the function called "get" (os.environ.get) in os_environ_get
os_environ_get = os.environ.get


CURRENT_YEAR = str(datetime.now().year)
AUTHOR = "AUTHOR"


VERSION = "1.0.0"
TITLE_APP = "Test text"


IP_APP = "0.0.0.0"
PORT_APP = int(os_environ_get("PORT", 8888))


URL_APP = "https://" + IP_APP + ":" + str(PORT_APP)


DEBUG_MODE = True
