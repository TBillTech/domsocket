"""Copyright (c) 2015 TBillTech.  All rights reserved."""

import logging
import json
from ws4py.websocket import WebSocket
import imp
import os


class AppWebSocket(WebSocket):

    """ appws is both the websocket handler class created for each new web socket connection, and the context and
    container for the Gui application object.  This class connects the websocket with a specific App class.
    Most importantly, it defines the:
    1) self.create_app function (which equals the App constructor)
    2) self.appid (which equals the top level div tag for the Gui application)
    """

    def __init__(self, appid, appname, *args, **kw):
        self.appid = appid
        self.appname = appname
        self.logger = logging.getLogger(self.appid)
        self.logger.info(
            'Creating %s with args=%s and keywords=%s.' % (self.appid, args, kw))
        WebSocket.__init__(self, *args, **kw)

        self.logger.setLevel(logging.DEBUG)
        (filename, pathname, description) = imp.find_module(
            self.appname, [os.path.abspath('apps')])
        app_module = imp.load_module(
            self.appname, filename, pathname, description)
        self.create_app = app_module.create_app

    def received_message(self, message):
        # flush is just a corny workaround for wss.  flush means do nothing.
        if message.data == 'flush':
            return
        self.logger.info('Received message = %s' % message.data)
        json_msg = json.loads(message.data)
        try:
            self.app.process_client_msg(self, json_msg)
        except AttributeError:
            if json_msg['eventName'] == 'init' and json_msg['nodeid'] == self.appid:
                self.app = self.create_app(self.appid, None, self)
            else:
                raise  # pragma: no cover

    def closed(self, code, reason="no reason given"):
        self.logger.info('Application has shut down: %s:%s.' % (code, reason))
        self.app.client_has_closed_ws(code, reason)
