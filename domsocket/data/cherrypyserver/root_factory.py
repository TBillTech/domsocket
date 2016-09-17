"""Copyright (c) 2015 TBillTech.  

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

import cherrypy
import temp_index
import temp_conf


class RootBase(object):
    pass

        
@cherrypy.expose
def app_method_prototype(self):
    pass


class RootFactory(object):
    index_method_name = 'index'
    app_method = app_method_prototype
    app_index_name = 'app.html'
    app_conf_name = 'app.conf'

    def __init__(self, server_info):
        self.app_name = server_info.app_name
        self.server_ip = server_info.server_ip
        self.web_port = server_info.web_port
        self.init_root_class()
        self.init_conf()

    def init_root_class(self):
        self.create_root_class()
        self.add_index_to_root_class()
        self.add_app_to_root_class()

    def create_root_class(self):
        self.root_class = RootBase

    def add_index_to_root_class(self):
        index_method = self.create_index_method()
        self.add_method_to_root_class(self.index_method_name, index_method)

    def create_index_method(self):
        return temp_index.create_temp_index_method(self.app_name, self.app_index_name)

    def add_app_to_root_class(self):
        self.add_method_to_root_class(self.app_name, self.app_method)

    def add_method_to_root_class(self, methodname, method):
        setattr(self.root_class, methodname, method)

    def create_root(self):
        return self.root_class()

    def get_conf(self):
        return temp_conf.get_temp_conf_path()

    def init_conf(self):
        temp_conf.reset_temp_conf(self.app_name, self.server_ip, self.web_port)
        temp_conf.append_to_temp_conf(self.app_conf_name, self.app_name, self.server_ip, self.web_port)

