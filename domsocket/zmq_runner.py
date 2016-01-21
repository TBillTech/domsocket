"""Copyright (c) 2015 TBillTech.  

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

import zmq
import imp
from app_instance import AppInstance

class ZMQRunner(object):
    
    def __init__(self, app_cls):
        self.context = zmq.Context()
        self.socket = context.socket(zmq.REP)
        self.socket.bind("tcp://*:5555")
        self.app_cls = app_cls
        self.instances = dict()

    def run(self):
        while True:
            raw_message = socket.recv()
    
            json_msg = json.loads(raw_message)
            command = json_msg['command']
            ws_id = json_msg['ws_id']
            message = json_msg['message']

            on_command = getattr(self, command, self.command_error)
            on_command(ws_id, message)

    def command_error(self, ws_id, message):
        print('Could not find command "%s" (websocket id=%s)' \
              % (message, ws_id))

    def ws_recv(self, ws_id, message):
        # flush is just a corny workaround for wss.  flush means do nothing.
        if message == 'flush':
            return
        json_msg = json.loads(message)

        if not ws_id in self.instances:
            self.instances[ws_id] = AppInstance(ws_id, self)

        self.instances[ws_id].recv(json_msg)
            
    def ws_send(self, ws_id, message):
        msg_dict = dict()
        msg_dict['command'] = 'ws_send'
        msg_dict['ws_id'] = ws_id
        msg_dict['message'] = message
        
        raw_message = json.dumps(msg_dict)
        socket.send(raw_message)

    def ws_close(self, ws_id, message):
        json_msg = json.loads(message)
        code = json_msg['code']
        reason = json_reason['reason']
        self.instances[ws_id].closed(code, reason)
        del self.instances[ws_id]

