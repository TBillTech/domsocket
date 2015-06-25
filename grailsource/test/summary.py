"""Copyright (c) 2015 TBillTech.  All rights reserved."""

import json


def as_summary(dct):
    if '__Summary__' in dct:
        result = Summary()
        result.test_count = dct['test_count']
        result.success_count = dct['success_count']
        result.errors = dct['errors']
        if result.errors:
            if result.test_count == result.success_count:
                result.test_count += 1
        return result
    return dct


def get_safe_test_count(summary_info):
    try:
        return int(summary_info.test_count)
    except:
        return 1


def get_safe_success_count_from_bool(summary_info):
    if SummaryInfo:
        return 1
    else:
        return 0


def get_safe_success_count(summary_info):
    try:
        return int(summary_info.success_count)
    except:
        return get_safe_success_count_from_bool(summary_info)


def get_safe_error_list(summary_info):
    try:
        return list(summary_info.errors)
    except:
        return list()


def normal_summary_decode_from_std_strs(stdstrs):
    (substdout, substderr) = stdstrs
    js_summary = json.loads(substdout, object_hook=as_summary)
    js_summary.append_error(substderr)
    return js_summary


def error_summary_decode_from_std_strs(stdstrs):
    (substdout, substderr) = stdstrs
    error_summary = Summary()
    error_summary.increment_fail()
    error_summary.append_error(substdout)
    error_summary.append_error(substderr)
    return error_summary


def summary_from_std_strs(stdstrs):
    try:
        return normal_summary_decode_from_std_strs(stdstrs)
    except ValueError:
        return error_summary_decode_from_std_strs(stdstrs)


class Summary(object):

    def __init__(self, stdstrs=None):
        self.test_count = 0
        self.success_count = 0
        self.errors = list()

    def increment_pass(self):
        self.test_count += 1
        self.success_count += 1

    def increment_fail(self):
        self.test_count += 1

    def test(self, assertion_value):
        assert(assertion_value)
        self.increment_pass()

    def merge(self, summary_info):
        self.test_count += get_safe_test_count(summary_info)
        self.success_count += get_safe_success_count(summary_info)
        self.errors += get_safe_error_list(summary_info)

    def append_error(self, error_str):
        if error_str != '':
            self.errors.append(str(error_str))

    def get_fail_count(self):
        return self.test_count - self.success_count

    def __str__(self):
        if self.get_fail_count() == 0:
            return self.success_str()
        else:
            return self.failure_str()

    def success_str(self):
        return "All %s Tests Succeeded!\n" % (self.success_count)

    def failure_str(self):
        resultstr = self.errors_str()
        resultstr += "%s Failures out of %s tests" % (
            self.get_fail_count(), self.test_count)
        return resultstr

    def errors_str(self):
        resultstr = ''
        for error in self.errors:
            resultstr += "Error: %s\n" % (error,)
        return resultstr
