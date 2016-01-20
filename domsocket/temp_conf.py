"""Copyright (c) 2015 TBillTech.  

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

import os

temp_conf_path = os.path.join(os.path.abspath('temp'), 'server.conf')
cherrypy_conf_path = os.path.join(
    os.path.abspath('cherrypyserver'), 'server.conf')


def reset_temp_conf():
    try:
        os.unlink(get_temp_conf_path())
    except OSError:  # pragma: no cover
        pass         # pragma: no cover
    append_to_temp_conf(cherrypy_conf_path)


def append_to_temp_conf(from_file_name):
    with open(get_temp_conf_path(), 'a+') as to_file:
        append_conf(to_file, from_file_name)


def append_conf(to_file, from_file_name):
    with open(from_file_name, 'r') as from_file:
        to_file.seek(0, os.SEEK_END)
        to_file.write(from_file.read())


def get_temp_conf_path():
    return temp_conf_path
