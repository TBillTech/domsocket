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
        self.run()

    def __enter__(self):
        time.sleep(1.0)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            start_time = time.time()
            while self.p.poll() is None:
                time.sleep(0.1)
                if time.time() - start_time > 2.0:
                    break
            if self.p.poll() is None:
                print('Terminating client after timeout')
                self.p.terminate()
        except Exception as ex:
            print(ex)
        return False

    def get_ip(self):
        return self.test_info.args.server_ip

    def run(self):
        args = ['coverage', 
                'run', 
                '--rcfile=coveragerc', 
                './app.py', 
                '-p5555',
                '-i%s'%self.get_ip(),
                '-v',]
        self.p = Popen(args)
