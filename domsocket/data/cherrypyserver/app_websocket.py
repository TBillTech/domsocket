"""Copyright (c) 2015 TBillTech.  

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

import logging
import json
import zmq
from ws4py.websocket import WebSocket
import imp
import os
import time
from threading import Thread, Lock

ZMQDOMSOCKETSERVERPORT = 5555
IDLESLEEPTIME = 0.1

SHUTDOWN_SIGNAL = False

# TODO:  Make this more efficient, and do not fork a thread for EVERY websocket.
# I left this class here because I assume a further optimization will be to control the number of processes
# looking for messages comming from the zmq sockets.  NO doubt this class will be replaced by another 
# module that will handle the N <-> M mapping between send message listener threads and zmq sockets.
# Instead of forking a new process, AppWebSocket should use the send message listener module to be coded in the future.
# I expect that instead of sleeping, the send message listener threads will handle the zmq.Again exception 
# more in the aggregate for all the zmq sockets the listener thread is controlling.
# Instead of joining on shutdown, AppWebSocket should remove itself from the future send message listener module.
# And etc...
def from_app_to_websocket(app_websocket):
    while not app_websocket.closed and not SHUTDOWN_SIGNAL:
        try:
            app_websocket.send_message()
        except zmq.Again:
            time.sleep(IDLESLEEPTIME)

class AppWebSocket(WebSocket):

    """ appws is both the websocket handler class created for each new web socket connection, and the conduit
    back to the zmq domsocket app.
    """

    def __init__(self, app_name, server_ip, *args, **kw):
        self.app_name = app_name
        self.logger = logging.getLogger(self.app_name)
        self.logger.info(
            'Creating %s with args=%s and keywords=%s.' % (self.app_name, args, kw))
        WebSocket.__init__(self, *args, **kw)
        self.logger.setLevel(logging.DEBUG)
        context = zmq.Context()
        self.socket = context.socket(zmq.DEALER)
        self.socket.bind('tcp://%s:%s' % (server_ip, ZMQDOMSOCKETSERVERPORT))
        self.closed = False
        self.lock = Lock()
        self.message_sender = Thread(target=from_app_to_websocket, args=(self,))
        self.message_sender.start()

    def received_message(self, message):
        # flush is just a corny workaround for wss.  flush means do nothing.
        if message.data == 'flush':
            return
        print('Received message "%s"' % (message.data,))
        with self.lock:
            self.socket.send_multipart(['ws_recv', message.data])

    def send_message(self):
        with self.lock:
            (command, message) = self.socket.recv_multipart(zmq.NOBLOCK)
        print('About to send messge "%s"' % (message,))
        self.send(message, False)

    def closed(self, code, reason="no reason given"):
        self.logger.info('Application has shut down: %s:%s.' % (code, reason))
        json_msg = dict()
        json_msg['code'] = code
        json_msg['reason'] = reason
        with self.lock:
            self.socket.send_multipart(['ws_close',json.dumps(json_msg)])
        self.shutdown()

    def shutdown(self):
        self.closed = True
        self.message_sender.join()
        del self.socket
