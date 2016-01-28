"""Copyright (c) 2015 TBillTech.  

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

import os
from string import Template

temp_conf_path = os.path.join(os.path.abspath('temp'), 'server.conf')
cherrypy_conf_path = os.path.join('server.conf')


def reset_temp_conf(app_name, server_ip):
    try:
        os.unlink(get_temp_conf_path())
    except OSError:  # pragma: no cover
        pass         # pragma: no cover
    append_to_temp_conf(cherrypy_conf_path, app_name, server_ip)


def append_to_temp_conf(from_file_name, app_name, server_ip):
    with open(get_temp_conf_path(), 'a+') as to_file:
        append_conf(to_file, from_file_name, app_name, server_ip)


def append_conf(to_file, from_file_name, app_name, server_ip):
    conf_str = get_conf_str(from_file_name, app_name, server_ip)
    to_file.seek(0, os.SEEK_END)
    to_file.write(conf_str)


def get_conf_str(from_file_name, app_name, server_ip):
    with open(from_file_name, 'r') as from_file:
        conf_str = from_file.read()
    if app_name:
        conf_str_template = Template(conf_str)
        conf_str = conf_str_template.safe_substitute(appName=app_name, serverIp=server_ip)    
    return conf_str

def get_temp_conf_path():
    return temp_conf_path
