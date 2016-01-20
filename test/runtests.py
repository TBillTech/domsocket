#!/usr/bin/python
"""Copyright (c) 2015 TBillTech.  

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

import os
from os import listdir
from os.path import isfile, join, isdir, abspath
import json
from test import __all__ as test_framework_module_files
from test.summary import Summary, summary_from_std_strs
from test.test_runner import TestRunner
from test.tester_test_harness import Harness
from test.subprocess_call import sub_process_call_with_temp_file_i_o
from test.testinfo import TestInfo

import imp
import sys
import domsocket
from domsocket import file_finder

py_extension = '.py'
js_extension = '.js'
test_framework_files = list(test_framework_module_files)
test_framework_files.append('__init__')
test_framework_files.append('testbase.trailer.js')
test_path = abspath('test')
apps_path = abspath('apps')

def full_test_path(filename):
    return join(test_path, filename)

def full_apps_path(filename):
    return join(apps_path, filename)

def is_test_file(filename):
    return isfile(full_test_path(filename))

def has_py_extension(name):
    return file_finder.has_extension(name, py_extension)

def has_js_extension(name):
    return file_finder.has_extension(name, js_extension)

def get_test_dir_list():
    return listdir(test_path)

def get_apps_dir_list():
    return listdir(apps_path)

def get_test_file_list():
    return [f for f in get_test_dir_list() if is_test_file(f)]

def get_all_test_py_file_list():
    return [f for f in get_test_file_list() if has_py_extension(f)]

def not_test_framework_file(name):
    return name not in test_framework_files and remove_py_extension(name) not in test_framework_files

def get_all_appnames():
    return [f for f in get_apps_dir_list() if isdir(full_apps_path(f))]

def get_all_testnames_from(path_name, ext_test):
    return [f for f in listdir(path_name) if ext_test(f)]

def get_test_ext_file_list(ext_test):
    test_info_list = list()
    for app_name in get_all_appnames():
        for test_name in get_all_testnames_from(join(apps_path, app_name, 'test'), ext_test):
            test_info_list += [TestInfo(app_name, test_name)]
    return test_info_list

def get_test_js_file_list():
    return get_test_ext_file_list(has_js_extension)

def get_test_py_file_list():
    return get_test_ext_file_list(has_py_extension)

def remove_py_extension(name):
    return file_finder.remove_extension(name, py_extension)

def get_import_names():
    return [remove_py_extension(f) for f in get_test_py_file_list()]

def run_test(run_test_method):
    with TestRunner(run_test_method) as runner:
        return runner.run()

def get_test_module(test_info):
    (filename, pathname, description) = test_info.find_module()
    return imp.load_module(test_info.py_module_name(), filename, pathname, description)

def test_py_module(test_info):
    test_module = get_test_module(test_info)
    return run_test(test_module.run_test_method)

def perform_py_tests():
    return [test_py_module(test_info) for test_info in get_test_py_file_list()]

def perform_subprocess_test(test_info):
    with Harness(test_info) as harness:
        stdstrs = sub_process_call_with_temp_file_i_o(test_info.get_args())
        return summary_from_std_strs(stdstrs)

def append_test_base_trailer(test_info):
    with open(test_info.relative_file_name(), 'a') as append_to:
        with open(join('test', 'testbase.trailer.js'), 'r') as append_from:
            append_to.write(append_from.read())

def test_js_module(test_info):
    append_test_base_trailer(test_info)
    return perform_subprocess_test(test_info)

def perform_js_tests():
    return [test_js_module(test_info) for test_info in get_test_js_file_list()]

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
