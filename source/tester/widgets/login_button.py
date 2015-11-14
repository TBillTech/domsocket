"""Copyright (c) 2015 TBillTech.  All rights reserved."""

from os.path import abspath
from os.path import join
import os
from domsocket.basic_widgets.html_widget import HTMLWidget


class LoginButton(HTMLWidget):

    _widget_html_id = 'loginButton'
    _html_source_filename = 'login_dialog.html'

    def __init__(self):
        super(LoginButton, self).__init__()
