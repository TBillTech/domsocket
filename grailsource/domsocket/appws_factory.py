"""Copyright (c) 2015 TBillTech.  All rights reserved."""

import logging
from app_websocket import AppWebSocket


class AppWSFactory(object):

    """ AppWSFactory creates an app_websocket application to handle websocket requests
    """

    def __init__(self, appid, appname):
        self.appid = appid
        self.appname = appname

    def __call__(self, *args, **kw):
        return AppWebSocket(self.appid, self.appname, *args, **kw)
