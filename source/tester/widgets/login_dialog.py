"""Copyright (c) 2015 TBillTech.  All rights reserved."""

from os.path import abspath
from os.path import join
import os
from domsocket.basic_widgets.html_widget import HTMLWidget


class LoginDialog(HTMLWidget):

    def __init__(self):
        super(LoginDialog, self).__init__()
