#!/usr/bin/python
"""Copyright (c) 2015 TBillTech.  All rights reserved."""

import os
from os.path import isfile, join, isdir, abspath
import shutil

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
 
    def setup_coverage(self):
        pass
   
