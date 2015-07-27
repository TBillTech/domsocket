"""Copyright (c) 2015 TBillTech.  All rights reserved."""

import os
from os import listdir
from os.path import isfile, join

apps_path = os.path.abspath('apps')
conf_extension = '.conf'
html_extension = '.html'

class AppInfo(object):
    def __init__(self, conf_filename):
        self.app_name = remove_conf_extension(conf_filename)
        self.exposed = is_exposed(conf_filename)

    def toggle_enabled(self):
        filename = full_path(join(self.app_name,'exposed'))
        if self.exposed:
            os.remove(filename)
        else:
            with open(filename, 'w+') as exposed_file:
                exposed_file.write('True')
        self.exposed = not self.exposed

def full_path(filename):
    return join(apps_path, filename)


def is_apps_file(filename):
    return isfile(full_path(filename)) # pragma: no cover


def has_extension(name, extension):
    return name[-len(extension):] == extension # pragma: no cover


def add_extension(name, extension):
    return name + extension


def has_conf_extension(name):
    return has_extension(name, conf_extension) # pragma: no cover


def has_h_t_m_l_extension(name):
    return has_extension(name, html_extension) # pragma: no cover


def add_conf_extension(name):
    return add_extension(name, conf_extension)


def add_h_t_m_l_extension(name):
    return add_extension(name, html_extension)


def get_app_dir_list():
    return listdir(apps_path) 


def get_app_file_list():
    return [f for f in get_app_dir_list() if is_apps_file(f)] 


def get_app_conf_file_list(app_names):
    return [full_path(add_conf_extension(f)) for f in app_names if is_apps_file(add_h_t_m_l_extension(f))]


def get_app_h_t_m_l_file_list(app_names):
    return [full_path(add_h_t_m_l_extension(f)) for f in app_names if is_apps_file(add_h_t_m_l_extension(f))]


def remove_extension(name, extension):
    return name[:-len(extension)]


def remove_conf_extension(name):
    return remove_extension(name, conf_extension) 


def remove_h_t_m_l_extension(name):
    return remove_extension(name, conf_extension)

def is_exposed(name):
    if has_conf_extension(name):
        if is_apps_file(join(remove_conf_extension(name),'exposed')):
            return True
    return False

def get_exposed_app_names():
    return [remove_conf_extension(f) for f in get_app_file_list() if is_exposed(f)]

def get_all_app_info():
    return [AppInfo(f) for f in get_app_file_list() if has_conf_extension(f)]

def get_app_conf_paths(app_names):
    return [full_path(f) for f in get_app_conf_file_list(app_names)]


def get_app_h_t_m_l_paths(app_names):
    return [full_path(f) for f in get_app_h_t_m_l_file_list(app_names)]
