#!/usr/bin/python
"""Copyright (c) 2015 TBillTech.  

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

import logging
import cherrypy
import argparse
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool

import sys
import os
sys.path.append('.')
from domsocket import root_factory as root_factory_module
from domsocket import appws_factory

WebSocketPlugin(cherrypy.engine).subscribe()
cherrypy.tools.websocket = WebSocketTool()

parser = argparse.ArgumentParser(
    description='Serve some websocket applications.')
parser.add_argument('applications', metavar='Apps', type=str, nargs='*',
                    help='applications to run')

if __name__ == '__main__':
    args = parser.parse_args()
    root_factory = root_factory_module.RootFactory(args.applications)

    try:
        root = root_factory.create_root()
        root_conf = root_factory.get_conf()
        cherrypy.quickstart(root, '/', config=root_conf)
    finally:
        logging.info('finally clause kicked out of cherrypy.quickstart')
