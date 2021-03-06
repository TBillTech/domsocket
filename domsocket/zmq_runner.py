"""Copyright (c) 2015 TBillTech.  

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

import argparse
import zmq
import imp
import os
import sys
import site
import json
import time
import socket
from os.path import join, abspath
from .app_instance import AppInstance
from binascii import hexlify
from threading import Lock

CLOSE_GOING_AWAY = 1001

def get_domsocket_js_path():
    for location in site.getsitepackages():
        if os.path.isdir(join(location, 'domsocket')):
            return join(location, 'domsocket', 'data', 'js')
    raise Error('Cannot find domsocket library in site packages: %s' % (site.getsitepackages(),)) # pragma: no cover

domsocket_js_path = get_domsocket_js_path()

class ZMQRunner(object):
    
    def __init__(self, app_cls, manifest, args=None):
        self.app_cls = app_cls
        self.instances = dict()
        if not args:
            parser = argparse.ArgumentParser(description='%s Web Application Runner' \
                                             % (self.app_name(),))
            parser.add_argument('--port', '-p', dest='port', default='5555',
                                help='The port number to listen for web app zmq messages.')
            parser.add_argument('--ip', '-i', dest='ip_addr', default='localhost',
                                help='The ip address to make the connection to the client.')
            parser.add_argument('--verbose', '-v', dest='verbose', action='store_true',
                                help='Print out verbose messaging (reduces apparent server responsiveness)')
            args = parser.parse_args()

        self.port = args.port
        self.ip_addr = args.ip_addr
        self.manifest = manifest
        self.verbose = args.verbose
        self.socket_lock = Lock()

    def app_name(self):
        return self.app_cls._html_source_app_name

    def __enter__(self):
        return self

    def gethostbyname(self):
        for i in range(10):
            try:
                return socket.gethostbyname(self.ip_addr)
            except socket.gaierror:
                time.sleep(1.0)

    def run(self):
        print('Running %s service to location %s:%s' % (self.app_name(), self.ip_addr, self.port))

        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.ROUTER)
        self.socket.connect("tcp://%s:%s" % (self.gethostbyname(), self.port))
        print("Socket connected to tcp://%s:%s" % (self.gethostbyname(), self.port))
        self.running = True

        while self.running:
            (front, client, command, message) = self.locked_recv_multipart()
            if sys.version_info >= (3,0,0): 
                command = command.decode('utf-8')
                message = message.decode('utf-8')
    
            on_command = getattr(self, command, self.command_error)
            on_command((front, client), message)

    def heartbeat(self, client, message):
        pass

    def locked_recv_multipart(self):
        while self.running:
            with self.socket_lock:
                try:
                    return self.socket.recv_multipart(zmq.NOBLOCK)
                except zmq.error.Again:
                    pass
            time.sleep(0.1)

    def stop(self):
        self.running = False

    def __exit__(self, ex_type, ex_message, ex_trace):
        print('hit exit of ZMQ Runner')
        code = CLOSE_GOING_AWAY
        if not ex_type:
            reason = 'shutdown'
        else:
            import traceback # pragma: no cover
            traceback.print_tb(ex_trace) # pragma: no cover
            reason = '%s:%s' % (ex_type, ex_message) # pragma: no cover
            print(reason) # pragma: no cover
        for (client, app_instance) in list(self.instances.items()):
            self.app_close(client, reason)
            app_instance.closed(code, reason)
        with self.socket_lock:
            self.socket.close()
            del self.socket
        del self.instances
        return True

    def command_error(self, client, message): 
        print('Could not find command "%s" (client id=%s)' \
              % (message, client)) # pragma: no cover

    def ws_recv(self, client, message):
        if not client in self.instances:
            self.instances[client] = AppInstance(client, self, message)
        else:
            self.instances[client].recv(message)
            
    def ws_send(self, client, message):
        (front, client) = client
        self.locked_send([front, client, 'ws_send', message])

    def locked_send(self, message_list):
        if sys.version_info >= (3,0,0):
            message_list = [self.encode(message) for message in message_list]
        with self.socket_lock:
            self.socket.send_multipart(message_list)

    def encode(self, message):
        if isinstance(message, str):
            return message.encode()
        return message

    def ws_close(self, client, message):
        json_msg = json.loads(message)
        code = json_msg['code']
        reason = json_msg['reason']
        if client in self.instances:
            self.instances[client].closed(code, reason)
            del self.instances[client]

    def app_close(self, client, reason):
        (front, client) = client
        self.locked_send([front, client, 'shutdown', reason])
        if client in self.instances:
            del self.instances[client]

    def get_app_name(self, client, message):
        json_msg = dict()
        json_msg['app_name'] = self.app_name()
        (front, client) = client
        self.locked_send([front, json.dumps(json_msg)])

    def read_file(self, client, message):
        (path, file_name) = json.loads(message)
        (local_path, local_file) = self.manifest[(path, file_name)]
        file_name = join(abspath(local_path),local_file)
        with open(file_name, 'rb') as read_file:
            contents = read_file.read()
        json_msg = dict()
        json_msg['blob'] = 'file_contents'
        raw_message = json.dumps(json_msg)
        (front, client) = client
        self.locked_send([front, raw_message])
        self.locked_send([front, contents])

    def list_directory(self, client, message):
        (path,) = json.loads(message)
        listing = self.manifest[path]
        json_msg = dict()
        json_msg['directory_listing'] = listing
        (front, client) = client
        self.locked_send([front, json.dumps(json_msg)])

