"""Copyright (c) 2015 TBillTech.  All rights reserved."""

from os.path import abspath
from os.path import join
import os
from domsocket.basic_widgets.html_widget import HTMLWidget


class LoginDialog(HTMLWidget):

    def __init__(self):
        login_dialog_HTML_file_name = abspath(join('apps',
                                               'tester',
                                               'widgets',
                                               'login_dialog.html'))

        with open(login_dialog_HTML_file_name, 'r') as login_dialog_HTML_file:
            super(LoginDialog, self).__init__(login_dialog_HTML_file.read(), None)
