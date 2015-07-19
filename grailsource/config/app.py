"""Copyright (c) 2015 TBillTech.  All rights reserved."""

from domsocket.element import Element
from widgets.login_dialog import LoginDialog
from domsocket.text_node import TextNode
from domsocket.basic_widgets.html_tag import HTMLTag
import hashlib
import pickle
import os
from os.path import join

class App(Element):

    def __init__(self, nodeid, parentNode, ws):
        self._nodeid = nodeid
        self.dom_insert_element('div', nodeid, parentNode, ws, child_index=None)

        self.login_dialog_show()

    def login_dialog_show(self):
        self.login = LoginDialog(login_handler=self)
    
    def on_login(self, username, password):
        authenticated = self.authenticate(username, password)
        if authenticated:
            self.on_authenticated()
        else:
            self.on_not_authenticated()

    def on_authenticated(self):
        self.authenticated_cleanup()
        #self.config = Configuration()

    def on_not_authenticated(self):
        self.invalid = HTMLTag('p', TextNode('username and/or password is invalid'))

    def authenticate(self, username, password):
        correct = self.get_correct_hashed_password(username)
        provided = self.get_provided_hashed_password(username, password)
        return correct == provided

    def get_correct_hashed_password(self, username):
        passwords = self.get_passwords()
        if username in passwords:
            return passwords[username]
        return None

    def get_provided_hashed_password(self, username, password):
        m = hashlib.sha256()
        m.update('%s.%s' % (username, password))
        return m.hexdigest().upper()
        
    def get_passwords(self):
        try:
            return self.load_pickle_file(join('apps', 'config', 'passwords.pkl'))
        except IOError as e:
            self.error = HTMLTag('p', TextNode('Could not load credentials file (%s).  Run set_config_password.py to initialize.' \
                                                 % (e,)))
            return dict()

    def load_pickle_file(self, filename):            
        with open(filename, 'r') as password_pickle:
            return pickle.load(password_pickle)

    def authenticated_cleanup(self):
        if hasattr(self, 'error'):
            del self.error
        if hasattr(self, 'invalid'):
            del self.invalid
        del self.login
