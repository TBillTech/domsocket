#!/usr/bin/python
"""Copyright (c) 2015 TBillTech.  

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""
import subprocess
import logging
import cherrypy
import argparse
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool

import sys
import os
sys.path.append('.')
from root_factory import RootFactory
import appws_factory
import app_websocket
from server_info import ServerInfo

def shutdown():
    print('engine is calling shutdown')
    appws_factory.SHUTDOWN_SIGNAL = True
    exit()

def run_server():
    os.system('./updateconfigipaddresses.sh')
    os.system('./genkey.sh')

    WebSocketPlugin(cherrypy.engine).subscribe()
    cherrypy.tools.websocket = WebSocketTool()

    cherrypy.engine.subscribe('stop', shutdown)

    parser = argparse.ArgumentParser(description='Serve a domsocket application.')
    parser.add_argument('--server_ip','-i', dest='server_ip', default='*',
                        help='the ip address where the zmq domsocket app is listening')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', 
                        help='Turn on message debugging (which makes the server seem less responsive')

    args = parser.parse_args()
    app_websocket.parsed_args = args
    server_info = ServerInfo(args)
    root_factory = RootFactory(server_info)
    root = root_factory.create_root()
    root_conf = root_factory.get_conf()

    try:
        cherrypy.quickstart(root, '/', config=root_conf)
    finally:
        logging.info('finally clause kicked out of cherrypy.quickstart')

if __name__ == '__main__':
    run_server()
