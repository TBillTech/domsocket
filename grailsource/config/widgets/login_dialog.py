"""Copyright (c) 2015 TBillTech.  All rights reserved."""

from os.path import abspath
from os.path import join
import os
from domsocket.basic_widgets.html_widget import HTMLWidget
from domsocket.event import Event


class LoginDialog(HTMLWidget):

    def __init__(self, login_handler):
        login_dialog_HTML_file_name = abspath(join('apps',
                                               'config',
                                               'widgets',
                                               'login_dialog.html'))

        with open(login_dialog_HTML_file_name, 'r') as login_dialog_HTML_file:
            super(LoginDialog, self).__init__(login_dialog_HTML_file.read(), None)

        self._login_handler = login_handler
            
    def get_login_event(self):
        login_event = Event()
        login_event.add_argument(self._username, 'value')
        login_event.add_argument(self._password, 'value')
        login_event.add_observer(self, LoginDialog.on_login)
        return login_event

    def on_login(self, theLoginButton, msg):
        self._login_handler.on_login(self._username.value, self._password.value)

    def dom_insert(self, name, parentNode, index):
        super(LoginDialog, self).dom_insert(name, parentNode, index)
        self._loginButton.click = self.get_login_event()
        