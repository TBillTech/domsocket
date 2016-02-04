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
from summary import Summary, summary_from_std_strs
from test_runner import TestRunner
from tester_test_harness import Harness
from subprocess_call import sub_process_call_with_temp_file_i_o
from testinfo import TestInfo

import imp
import sys
import argparse

py_extension = '.py'
js_extension = '.js'
test_path = abspath('tests')
path = abspath('.')

def full_test_path(filename):
    return join(test_path, filename)

def full_apps_path(filename):
    return join(path, filename)

def is_test_file(filename):
    return isfile(full_test_path(filename))

def has_extension(name, extension):
    return name[-len(extension):] == extension

def remove_extension(name, extension):
    return name[:-len(extension)]

def has_py_extension(name):
    return has_extension(name, py_extension)

def has_js_extension(name):
    return has_extension(name, js_extension)

def get_test_dir_list():
    return listdir(test_path)

def get_test_file_list():
    return [f for f in get_test_dir_list() if is_test_file(f)]

def get_all_test_py_file_list():
    return [f for f in get_test_file_list() if has_py_extension(f)]

def get_all_testnames_from(path_name, ext_test):
    return [f for f in listdir(path_name) if ext_test(f)]

def get_test_js_file_list(args):
    test_info_list = list()
    for test_name in get_all_testnames_from(test_path, has_js_extension):
        test_info_list += [TestInfo(test_name, args)]
    return test_info_list

def run_test(run_test_method):
    with TestRunner(run_test_method) as runner:
        return runner.run()

def perform_subprocess_test(test_info):
    with Harness(test_info) as harness:
        stdstrs = sub_process_call_with_temp_file_i_o(test_info.get_args())
        return summary_from_std_strs(stdstrs)

def append_test_base_trailer(test_info):
    with open(test_info.relative_file_name(), 'r') as to_copy:
        with open(test_info.relative_temp_name(), 'w+') as to_write:
            to_write.write(to_copy.read())
    with open(test_info.relative_temp_name(), 'a') as append_to:
        append_to.write('var url = "http://%s:8080";\n\n' % (test_info.get_server_ip(),)) 
        with open('testbase.trailer.js', 'r') as append_from:
            append_to.write(append_from.read())

def test_js_module(test_info):
    append_test_base_trailer(test_info)
    return perform_subprocess_test(test_info)

def perform_js_tests(args):
    return [test_js_module(test_info) for test_info in get_test_js_file_list(args)]

def merge_summaries(summaries):
    merged_summary = Summary()
    for summary in summaries:
        merged_summary.merge(summary)
    return merged_summary

def perform_all_tests(args):
    return perform_js_tests(args)

def run():
    parser = argparse.ArgumentParser(description='Run domsocket tests.')
    parser.add_argument('--server_ip', '-i', dest='server_ip', default='*',
                        help='the ip address where the cherrpyserver is listening')
    args = parser.parse_args()

    print("\n\nRunning all Unit Tests...\n")

    all_summaries = perform_all_tests(args)
    total_summary = merge_summaries(all_summaries)

    return total_summary

if __name__ == '__main__':
    total_summary = run()
    print(total_summary)
