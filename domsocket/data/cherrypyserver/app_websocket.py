"""Copyright (c) 2015 TBillTech.  

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

import cherrypy
import json
import zmq
from ws4py.websocket import WebSocket
import imp
import os
import time
from zmq_backend import get_backend

ZMQDOMSOCKETSERVERPORT = 5555
IDLESLEEPTIME = 0.1

class AppWebSocket(WebSocket):

    """ appws is both the websocket handler class created for each new web socket connection, and the conduit
    back to the zmq domsocket app.
    """

    def __init__(self, app_name, *args, **kw):
        self.app_name = app_name
        self.backend = get_backend()
        self.verbose = self.backend.verbose
        cherrypy.log.access_log.info(
            'Creating %s with args=%s and keywords=%s.' % (self.app_name, args, kw))
        WebSocket.__init__(self, *args, **kw)
        self.backend.register(self)

    def received_message(self, message):
        # flush is just a corny workaround for wss.  flush means do nothing.
        if message.data == 'flush':
            return
        if self.verbose: print('Received message "%s"' % (message.data,))
        self.backend.message_from_client(self, 'ws_recv', message.data)

    def send_message(self, command, message):
        if command == 'shutdown':
            cherrypy.log.error_log.error('close down websocket because zmq_runner reports "%s"' % (message,))
            self.close(1001, message)
        else:
            if self.verbose: print('About to send messge "%s"' % (message,))
            self.send(message, False)

    def closed(self, code, reason="no reason given"):
        cherrypy.log.access_log.info('Application has shut down: %s:%s.' % (code, reason))
        self.backend.deregister(self, code, reason)
