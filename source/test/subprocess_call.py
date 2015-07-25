"""Copyright (c) 2015 TBillTech.  All rights reserved."""

import subprocess

sub_process_std_err_name = 'subprocessstderr.txt'
sub_process_std_out_name = 'subprocessstdout.txt'


def sub_process_call_with_temp_file_i_o(args):
    with open(sub_process_std_out_name, 'w+') as substdout:
        with open(sub_process_std_err_name, 'w+') as substderr:
            substdoutstr = subprocess.call(
                args, stdout=substdout, stderr=substderr)
    with open(sub_process_std_out_name, 'r') as substdout:
        with open(sub_process_std_err_name, 'r') as substderr:
            return (substdout.read(), substderr.read())
