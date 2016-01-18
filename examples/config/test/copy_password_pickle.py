"""Copyright (c) 2015 TBillTech.  

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

import shutil
import os
from os.path import join, abspath

def run_test_method(self):
    shutil.copyfile(abspath(join('apps', 'config', 'test', 'passwords.pkl')), 
                    abspath(join('apps', 'config', 'passwords.pkl')))
    self.increment_pass()
