from subprocess import Popen
import thread
import time


class Harness(object):

    def __init__(self):
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
        args = ['coverage', 'run', './cherrypyserver/serve.py', 'tester']
        self.p = Popen(args)
