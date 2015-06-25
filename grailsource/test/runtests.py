#!/usr/bin/python
"""Copyright (c) 2015 TBillTech.  All rights reserved."""

import os
from os import listdir
from os.path import isfile, join
import json
from test import __all__ as test_framework_module_files
from test.summary import Summary, summary_from_std_strs
from test.test_runner import TestRunner
from test.tester_test_harness import Harness
from test.subprocess_call import sub_process_call_with_temp_file_i_o

import imp
import sys
import domsocket
from domsocket import file_finder

py_extension = '.py'
js_extension = '.js'
test_framework_files = list(test_framework_module_files)
test_framework_files.append('__init__')
test_framework_files.append('testbase.trailer.js')
test_path = os.path.abspath('test')


def full_test_path(filename):
    return join(test_path, filename)

def is_test_file(filename):
    return isfile(full_test_path(filename))

def has_py_extension(name):
    return file_finder.has_extension(name, py_extension)

def has_js_extension(name):
    return file_finder.has_extension(name, js_extension)

def get_test_dir_list():
    return listdir(test_path)

def get_test_file_list():
    return [f for f in get_test_dir_list() if is_test_file(f)]

def get_all_test_py_file_list():
    return [f for f in get_test_file_list() if has_py_extension(f)]

def not_test_framework_file(name):
    return name not in test_framework_files and remove_py_extension(name) not in test_framework_files

def get_test_py_file_list():
    return [f for f in get_all_test_py_file_list() if not_test_framework_file(f)]

def get_all_test_js_file_list():
    return [f for f in get_test_file_list() if has_js_extension(f)]

def get_test_js_file_list():
    return [f for f in get_all_test_js_file_list() if not_test_framework_file(f)]

def remove_py_extension(name):
    return file_finder.remove_extension(name, py_extension)

def get_import_names():
    return [remove_py_extension(f) for f in get_test_py_file_list()]

def run_test(run_test_method):
    with TestRunner(run_test_method) as runner:
        return runner.run()

def get_test_module(modulename):
    (filename, pathname, description) = imp.find_module(modulename, [test_path])
    return imp.load_module(modulename, filename, pathname, description)

def test_py_module(modulename):
    test_module = get_test_module(modulename)
    return run_test(test_module.run_test_method)

def perform_py_tests():
    return [test_py_module(modulename) for modulename in get_import_names()]

def perform_subprocess_test(args):
    with Harness() as harness:
        stdstrs = sub_process_call_with_temp_file_i_o(args)
        return summary_from_std_strs(stdstrs)

def append_test_base_trailer(js_file_name):
    with open(os.path.join('test', js_file_name), 'a') as append_to:
        with open(os.path.join('test', 'testbase.trailer.js'), 'r') as append_from:
            append_to.write(append_from.read())

def test_js_module(js_file_name):
    append_test_base_trailer(js_file_name)
    args = [os.path.abspath('/home/thomas/node_modules/.bin/slimerjs'),
            '--error-log-file=%s' % ('jslog.txt',),
            '-P', 'AllowSSL', os.path.join('test', js_file_name)]
    return perform_subprocess_test(args)

def perform_js_tests():
    return [test_js_module(js_file_name) for js_file_name in get_test_js_file_list()]

def merge_summaries(summaries):
    merged_summary = Summary()
    for summary in summaries:
        merged_summary.merge(summary)
    return merged_summary

def perform_all_tests():
    return perform_py_tests() + perform_js_tests()


if __name__ == '__main__':

    print("\n\nRunning all Unit Tests...\n")

    all_summaries = perform_all_tests()
    total_summary = merge_summaries(all_summaries)

    print(total_summary)
