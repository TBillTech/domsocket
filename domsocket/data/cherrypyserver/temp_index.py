"""Copyright (c) 2015 TBillTech.  

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

import cherrypy
import os
import shutil
from string import Template

temp_index_path = os.path.join(os.path.abspath('temp'), 'index.html')


def create_temp_index_method(app_name, app_index_name):
    return get_app_lambda(app_name, app_index_name)

def get_app_lambda(app_name, app_index_name):
    with open(app_index_name, 'r') as html_file:
        html_str = Template(html_file.read())
    html_sub_str = html_str.safe_substitute(appName=app_name)
    with open(temp_index_path, 'w+') as index_file:
        index_file.write(html_sub_str)

    @cherrypy.expose
    def temp_index_method(self, *args):
        cherrypy.log.error_log.info(
            "%s html with args = %s requested." % (app_name, args))
        return html_sub_str
        
    return temp_index_method

