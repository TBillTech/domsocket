"""Copyright (c) 2015 TBillTech.  All rights reserved."""

import cherrypy
import os
import shutil
import file_finder
from string import Template

temp_index_path = os.path.join(os.path.abspath('temp'), 'index.html')


def create_temp_index_method(html_file_names):
    return get_index_lambda(html_file_names)

def get_index_lambda(html_file_names):
    if len(html_file_names) == 1:
        return get_app_lambda(html_file_names[0])
    else:
        return get_all_apps_lambda(html_file_names)

def get_app_lambda(html_file_name):
    with open(html_file_name, 'r') as html_file:
        html_str = Template(html_file.read())
    app_name = get_app_name(html_file_name)
    html_sub_str = html_str.safe_substitute(appName=app_name)
    @cherrypy.expose
    def temp_index_method(self, *args):
        cherrypy.log.error_log.info(
            "%s html with args = %s requested." % (app_name, args))
        return html_sub_str
        
    return temp_index_method

def get_all_apps_lambda(html_file_names):
    all_apps_html_str = '<!doctype html>\n'\
    '<head>\n'\
    '    <title>Currently Available Apps</title>\n'\
    '</head>\n'\
    '<body>\n'\
    '<ul>\n'
    for app_name in get_app_names(html_file_names):
        all_apps_html_str += '    <li><a href="/apps/%s" title="%s">%s</a></li>\n' % (app_name, app_name, app_name)
    all_apps_html_str += '</ul>\n'

    @cherrypy.expose
    def temp_index_method(self, *args):
        cherrypy.log.error_log.info(
            "%s html with args = %s requested." % (app_name, args))
        return all_apps_html_str
    
    return temp_index_method

def get_app_names(html_file_names):
    return [get_app_name(html_file_name) for html_file_name in html_file_names]

def get_app_name(html_file_name):
    return os.path.split(
        file_finder.remove_h_t_m_l_extension(html_file_name))[-1:][0]
