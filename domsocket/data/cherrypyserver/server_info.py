"""Copyright (c) 2015 TBillTech.  

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""
import zmq
import os
import json
import subprocess
from os.path import join, abspath
from one_shot_message import OneShotMessage

class ServerInfo(object):
    def __init__(self, args):
        self.server_ip = args.server_ip
        self.zmq_port = args.zmq_port
        self.web_port = args.web_port
        self.setup_server()

    def setup_server(self):
        self.get_app_name()
        self.copy_file('.','app.html')
        self.copy_file('.','app.conf')
        self.copy_directory('css')
        self.copy_directory('scripts')
        self.copy_directory('static')
        self.copy_directory('style')
        self.copy_directory('toolkits')

    def get_app_name(self):
        with OneShotMessage(['get_app_name', 'None'], self.server_ip, self.zmq_port) as message:
            self.app_name = message.app_name
            print('message.app_name is %s' % message.app_name)

    def read_file(self, path, file_name):
        with OneShotMessage(['read_file', path, file_name], self.server_ip, self.zmq_port) as message:
            return message.file_contents

    def list_directory(self, path):
        with OneShotMessage(['list_directory', path], self.server_ip, self.zmq_port) as message:
            return message.directory_listing

    def copy_file(self, path, file_name):
        file_contents = self.read_file(path, file_name)
        if file_name[-len('.tar.gz'):] == '.tar.gz':
            self.write_zipped_contents(file_contents, abspath(path), file_name)
        else:
            with open(join(abspath(path),file_name), 'w+') as to_write:
                to_write.write(file_contents)

    def copy_directory(self, directory_name):
        directory_listing = self.list_directory(directory_name)
        print('directory_listing = %s' % (directory_listing,))
        for file_name in directory_listing:
            self.copy_file(directory_name, file_name)


    def write_zipped_contents(self, file_contents, path, file_name):
        temp_filepath = join(abspath('temp'),file_name)
        unzip_path = join(abspath(path), './')
        with open(temp_filepath, 'w+') as to_write:
            to_write.write(file_contents)
        subprocess.call(['gunzip', temp_filepath]) 
        temp_filepath = temp_filepath[0:-len('.gz')]
        untar_call = ['tar', '-xvf', temp_filepath, '-C', unzip_path]
        subprocess.call(untar_call)
        os.unlink(temp_filepath)

