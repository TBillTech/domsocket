"""Copyright (c) 2015 TBillTech.  

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

from summary import Summary


class TestRunner(object):

    def __init__(self, run_test_method):
        self.summary = Summary()
        self.run_test = run_test_method
        self.exception_suppressed = False

    def run(self):
        self.run_test(self)
        return self.summary

    def run_test(self):
        raise Exception('Do not call this run_test method!')

    def test(self, test_value):
        self.summary.test(test_value)

    def increment_pass(self):
        self.summary.increment_pass()

    def increment_fail(self):
        self.summary.increment_fail()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type != None:
            self.summary.append_error(
                'Failed test with %s:%s\n%s\n' % (exc_type, exc_value, traceback))
            return self.exception_suppressed
        return True
