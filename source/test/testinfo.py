#!/usr/bin/python
"""Copyright (c) 2015 TBillTech.  

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

import os
from os.path import isfile, join, isdir, abspath
import shutil
import imp

class TestInfo(object):
    def __init__(self, app_name, test_name):
        self.app_name = app_name
        self.test_name = test_name

    def relative_test_dir(self, file_name):
        return join('apps', self.app_name, 'test', file_name)

    def relative_file_name(self):
        return self.relative_test_dir(self.test_name)

    def get_args(self):
        return [abspath('/home/thomas/node_modules/.bin/slimerjs'),
            '--error-log-file=%s' % ('jslog.txt',),
            '-P', 'AllowSSL', self.relative_file_name()]
 
    def find_module(self):
        return imp.find_module(self.py_module_name(), [self.relative_test_dir('')])

    def py_module_name(self):
        return self.test_name[:-3]
   
