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
from server_info import ServerInfo

def run_server():
    os.system('./updateconfigipaddresses.sh')
    os.system('./genkey.sh')

    WebSocketPlugin(cherrypy.engine).subscribe()
    cherrypy.tools.websocket = WebSocketTool()

    parser = argparse.ArgumentParser(description='Serve a domsocket application.')
    parser.add_argument('--server_ip','-i', dest='server_ip', default='*',
                        help='the ip address where the zmq domsocket app is listening') 

    args = parser.parse_args()
    server_info = ServerInfo(args)
    root_factory = RootFactory(server_info)

    try:
        root = root_factory.create_root()
        root_conf = root_factory.get_conf()
        cherrypy.quickstart(root, '/', config=root_conf)
    finally:
        logging.info('finally clause kicked out of cherrypy.quickstart')

if __name__ == '__main__':
    run_server()
