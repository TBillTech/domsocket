#!/usr/bin/python
"""Copyright (c) 2015 TBillTech.  

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

import os
from os.path import isfile, join, isdir, abspath, expanduser
import shutil
import imp

class TestInfo(object):
    def __init__(self, test_name, args):
        self.test_name = test_name
        self.args = args

    def relative_file_name(self):
        return join('tests', self.test_name)

    def relative_temp_name(self):
        return join('temp', self.test_name)

    def get_server_ip(self):
        return self.args.server_ip

    def get_args(self):
        return [abspath(expanduser('~/node_modules/.bin/slimerjs')),
            '--error-log-file=%s' % ('jslog.txt',),
            '-P', 'AllowSSL', self.relative_temp_name()]
 
