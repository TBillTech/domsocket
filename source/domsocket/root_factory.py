"""Copyright (c) 2015 TBillTech.  All rights reserved."""

import cherrypy
import temp_index
import temp_conf
import file_finder


class RootBase(object):
    def __init__(self, applinks):
        self.apps = applinks
        self.apps.expose = True
        
@cherrypy.expose
def app_method_prototype(self):
    pass

class RootFactory(object):
    index_method_name = 'index'
    apps_base_name = 'apps'
    app_method = app_method_prototype

    def create_root(self):
        return self.root_class(self.applinks)

    def get_conf(self):
        return temp_conf.get_temp_conf_path()

    def __init__(self, applications):
        self.init_app_names(applications)
        self.init_app_links()
        self.init_root_class()
        self.init_conf()

    def init_app_names(self, applications):
        if not applications: 
            self.app_names = file_finder.get_exposed_app_names() # pragma: no cover
        else:
            self.app_names = applications

    def init_app_links(self):
        class AppLinks(object):
            pass

        for (app_name, index_method) in self.get_app_index_methods():
            setattr(AppLinks, app_name, index_method)

        self.applinks = AppLinks()

    def get_app_index_methods(self):
        return [(app_name, self.get_index_method(app_name)) for app_name in self.app_names]

    def get_index_method(self, app_name):
        return temp_index.get_app_lambda(file_finder.full_path(file_finder.add_h_t_m_l_extension(app_name)))

    def init_root_class(self):
        self.create_root_class()
        self.add_index_to_root_class()
        self.add_apps_to_root_class()

    def create_root_class(self):
        self.root_class = RootBase

    def add_index_to_root_class(self):
        index_method = self.create_index_method()
        self.add_method_to_root_class(self.index_method_name, index_method)

    def add_method_to_root_class(self, methodname, method):
        setattr(self.root_class, methodname, method)

    def create_index_method(self):
        html_files = file_finder.get_app_h_t_m_l_paths(self.app_names)
        return temp_index.create_temp_index_method(html_files)

    def add_apps_to_root_class(self):
        for app_name in self.app_names:
            self.add_app_to_root_class(app_name)

    def add_app_to_root_class(self, app_name):
        self.add_method_to_root_class(app_name, self.app_method)

    def init_conf(self):
        temp_conf.reset_temp_conf()
        for app_conf_file_name in file_finder.get_app_conf_paths(self.app_names):
            temp_conf.append_to_temp_conf(app_conf_file_name)

