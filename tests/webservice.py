#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from urllib.request import urlopen

# https://www.google.com.br/search?client=ubuntu&hs=nkZ&channel=fs&dcr=0&q=python+unit+test+web+service+method&oq=python+unit+test+web+service+method&gs_l=psy-ab.3..0i71k1l4.3548.3659.0.3755.2.2.0.0.0.0.0.0..0.0.foo%2Ccfro%3D1%2Cnso-ehuqi%3D1%2Cnso-ehuui%3D1%2Cewh%3D0%2Cnso-mplt%3D2%2Cnso-enksa%3D0%2Cnso-enfk%3D1%2Cnso-usnt%3D1%2Cnso-qnt-npqp%3D0-1701%2Cnso-qnt-npdq%3D0-54%2Cnso-qnt-npt%3D0-1%2Cnso-qnt-ndc%3D300%2Ccspa-dspm-nm-mnp%3D0-05%2Ccspa-dspm-nm-mxp%3D0-125%2Cnso-unt-npqp%3D0-17%2Cnso-unt-npdq%3D0-54%2Cnso-unt-npt%3D0-0602%2Cnso-unt-ndc%3D300%2Ccspa-uipm-nm-mnp%3D0-007525%2Ccspa-uipm-nm-mxp%3D0-052675...0...1.1.64.psy-ab..2.0.0._11Xc6SCPtA
# http://seminar.io/2013/09/27/testing-your-rest-client-in-python/
class ClientAPI:

    def request(self, user):
        url = "https://api.github.com/users/%s" % user
        response = urlopen(url)
        raw_data = response.read().decode('utf-8')

        return json.loads(raw_data)