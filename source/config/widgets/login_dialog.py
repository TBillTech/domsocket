"""Copyright (c) 2015 TBillTech.  All rights reserved."""

from os.path import abspath
from os.path import join
import os
from domsocket.basic_widgets.html_widget import HTMLWidget
from domsocket.event import Event


class LoginDialog(HTMLWidget):

    def __init__(self, login_handler):
        super(LoginDialog, self).__init__()

        self._login_handler = login_handler
            
    def get_login_event(self):
        login_event = Event()
        login_event.add_argument(self._username, 'value')
        login_event.add_argument(self._password, 'value')
        login_event.add_observer(self, LoginDialog.on_login)
        return login_event

    def on_login(self, theLoginButton, msg):
        self._login_handler.on_login(self._username.value, self._password.value)

    def on_create(self, name, parentNode, index):
        super(LoginDialog, self).on_create(name, parentNode, index)
        self._loginButton.click = self.get_login_event()
        
