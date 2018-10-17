"""Copyright (c) 2015 TBillTech.  

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

from threading import Thread
from binascii import hexlify
import zmq
import time
import json

IDLESLEEPTIME = 0.1

def client_id(client):
    return str(hash(client))

class ZmqBackend(Thread):

    singleton = None
    
    def __init__(self, parsed_args):
        self.parsed_args = parsed_args
        self.zmq_bind_ip = parsed_args.zmq_bind_ip
        self.server_port = parsed_args.zmq_port
        self.app_websockets = dict()
        self.shutdown = False
        self.verbose = self.parsed_args.verbose
        self.clients = dict()
        super(ZmqBackend, self).__init__()

        context = zmq.Context()
        self.socket = context.socket(zmq.DEALER)
        self.socket.bind('tcp://%s:%s' % (self.get_zmq_bind_ip(), self.server_port))
        
    def get_zmq_bind_ip(self):
        if self.zmq_bind_ip != '*' and self.zmq_bind_ip != '"*"':
            return socket.gethostbyname(self.zmq_bind_ip)
        return '*'
        
    def register(self, client):
        self.clients[client_id(client)] = client
        
    def deregister(self, client, code, reason):
        if client_id(client) in self.clients:
            json_msg = dict()
            json_msg['code'] = code
            json_msg['reason'] = reason
            self.socket.send_multipart([client_id(client), 'ws_close', json.dumps(json_msg)])
            del self.clients[client_id(client)]
        
    def run(self):
        while not self.shutdown:
            try:
                self.message_to_client()
            except zmq.Again:
                time.sleep(IDLESLEEPTIME)

    def stop(self):
        self.shutdown = True
        self.join()

    def message_to_client(self):
        (client_hash, command, message) = self.recv_from_backend()
        if client_hash in self.clients:
            client = self.clients[client_hash]
            client.send_message(command, message)

    def recv_from_backend(self):
        return self.socket.recv_multipart(zmq.NOBLOCK)

    def message_from_client(self, client, command, message_data):
        self.socket.send_multipart([client_id(client), command, message_data])

def init_backend(parsed_args):
    ZmqBackend.singleton = ZmqBackend(parsed_args)
    return get_backend()

def get_backend():
    return ZmqBackend.singleton
