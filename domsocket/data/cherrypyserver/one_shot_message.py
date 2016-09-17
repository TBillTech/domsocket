"""Copyright (c) 2015 TBillTech.  

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""
import zmq
import json

class OneShotMessage(object):
    def __init__(self, multipart_message, server_ip, zmq_port):
        self.server_ip = server_ip
        self.server_port = zmq_port
        self.command = multipart_message[0]
        self.args = multipart_message[1:]

    def __enter__(self):
        context = zmq.Context()
        self.socket = context.socket(zmq.DEALER)
        self.socket.bind('tcp://%s:%s' % (self.server_ip, self.server_port))
        print('about to send message: [%s,%s]' % (self.command, json.dumps(self.args)))
        self.socket.send_multipart(["0", self.command, json.dumps(self.args)])
        self.json_message = self.socket.recv()
        self.message_obj = json.loads(self.json_message)
        if 'blob' in self.message_obj:
            self.message_obj[self.message_obj['blob']] = self.socket.recv()
        return self

    def __exit__(self, ex_type, ex_message, ex_trace):
        del self.socket
        if ex_trace:
            import pdb; pdb.set_trace()

    def __getattr__(self, attribute):
        if not attribute in self.json_message:
            raise AttributeError('Could not find attribute "%s" in message "%s"' % \
                                 (attribute, self.json_message))
        try:
            return getattr(self.message_obj, attribute)
        except AttributeError:
            return self.message_obj[attribute]
