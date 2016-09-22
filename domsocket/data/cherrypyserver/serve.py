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
from string import Template
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool

import sys
import os
sys.path.append('.')
from root_factory import RootFactory
import appws_factory
import app_websocket
from server_info import ServerInfo
from zmq_backend import init_backend, get_backend

def shutdown():
    print('engine is calling shutdown')
    backend = get_backend()
    backend.stop()
    exit()

def get_default_ip():
    os.system('./detectipaddress.sh')
    with open('./temp/detected_ip.txt', 'r') as detected_ip_file:
        return detected_ip_file.read().strip()

def write_server_openssl_conf(server_ip):
    with open('./server_openssl.conf.template', 'r') as conf_template_file:
        conf_str_template = Template(conf_template_file.read())
    conf_str = conf_str_template.safe_substitute(serverIp=server_ip)
    with open('./server_openssl.conf', 'w+') as conf_file:
        conf_file.write(conf_str)

def config_server_openssl(server_ip):
    write_server_openssl_conf(server_ip)
    os.system('./genkey.sh')

def run_server():
    default_ip = get_default_ip()
    
    parser = argparse.ArgumentParser(description='Serve a domsocket application.')
    parser.add_argument('--server_ip','-s', dest='server_ip', default=default_ip,
                        help='the ip address where the zmq domsocket app is listening')
    parser.add_argument('--zmq_bind_ip','-i', dest='zmq_bind_ip', default='127.0.0.1',
                        help='the ip address where the zmq domsocket app is listening')
    parser.add_argument('--server_port','-p', dest='web_port', default=8443,
                        help='the port for the web server to listen')
    parser.add_argument('--zmq_port','-z', dest='zmq_port', default=5555,
                        help='the port for the zmq backend to listen')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', 
                        help='Turn on message debugging (which makes the server seem less responsive')

    args = parser.parse_args()
    app_websocket.parsed_args = args
    config_server_openssl(args.server_ip)

    WebSocketPlugin(cherrypy.engine).subscribe()
    cherrypy.tools.websocket = WebSocketTool()

    cherrypy.engine.subscribe('stop', shutdown)

    server_info = ServerInfo(args)
    backend = init_backend(args)
    backend.start()
    root_factory = RootFactory(server_info)
    root = root_factory.create_root()
    root_conf = root_factory.get_conf()

    try:
        cherrypy.quickstart(root, '/', config=root_conf)
    finally:
        logging.info('finally clause kicked out of cherrypy.quickstart')

if __name__ == '__main__':
    run_server()
