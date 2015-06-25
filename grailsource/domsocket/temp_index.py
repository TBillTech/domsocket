"""Copyright (c) 2015 TBillTech.  All rights reserved."""

import cherrypy
import os
import shutil
import file_finder
from string import Template

temp_index_path = os.path.join(os.path.abspath('temp'), 'index.html')


def create_temp_index_method(html_file_names):
    update_temp_index_h_t_m_l(html_file_names)
    return temp_index_method


def update_temp_index_h_t_m_l(html_file_names):
    if len(html_file_names) == 1:
        with open(html_file_names[0], 'r') as html_file:
            html_str = Template(html_file.read())
        app_name = os.path.split(
            file_finder.remove_h_t_m_l_extension(html_file_names[0]))[-1:][0]
        html_sub_str = html_str.safe_substitute(appName=app_name)
        with open(temp_index_path, 'w+') as html_file:
            html_file.write(html_sub_str)
    else:
        raise Exception('Multiple applications not yet supported.') # pragma: no cover


@cherrypy.expose
def temp_index_method(self, *args):
    cherrypy.log.error_log.info(
        "Index html with args = %s requested." % (args,))
    with open(temp_index_path, 'r') as index_h_t_m_l:
        return index_h_t_m_l.read()
