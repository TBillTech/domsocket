"""Copyright (c) 2015 TBillTech.  

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

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
