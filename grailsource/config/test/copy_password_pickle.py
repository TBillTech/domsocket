"""Copyright (c) 2015 TBillTech.  All rights reserved."""
import shutil
import os
from os.path import join, abspath

def run_test_method(self):
    shutil.copyfile(abspath(join('apps', 'config', 'test', 'passwords.pkl')), 
                    abspath(join('apps', 'config', 'passwords.pkl')))
    self.increment_pass()
