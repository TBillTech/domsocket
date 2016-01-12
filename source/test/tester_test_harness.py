"""Copyright (c) 2015 TBillTech.  

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

from subprocess import Popen
import thread
import time

class Harness(object):

    def __init__(self, test_info):
        self.test_info = test_info
        self.app_name = test_info.app_name
        self.run()

    def __enter__(self):
        time.sleep(0.1)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            self.p.terminate()
        except Exception as ex:
            print(ex)
        return False

    def run(self):
        args = ['coverage', 
                'run', 
                '--rcfile=apps/%s/test/.coveragerc'%(self.app_name), 
                './cherrypyserver/serve.py', 
                self.app_name]
        self.p = Popen(args)
