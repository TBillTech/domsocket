"""Copyright (c) 2015 TBillTech.  All rights reserved."""

from domsocket.event import Event
from domsocket.basic_widgets.html_tag import HTMLTag
from domsocket.basic_widgets.text import Text
from domsocket.element import Node
from widgets.login_dialog import LoginDialog
from widgets.login_button import LoginButton

class SomeText(object):
    def __init__(self, text):
        self.text = text

class App(Node):

    def __init__(self, nodeid, parent_node, ws):
        self.called_init('div', nodeid, parent_node, ws, index=None)

        self.first_paragraph_show()
        self.sub_body_show()
        self.login_button_show()
        self.login_dialog_show()
        
    def first_paragraph_show(self):
        first_paragraph_kwargs = dict()
        first_paragraph_kwargs['first_child'] = 'Hello World!'
        first_paragraph_kwargs['class'] = 'first'
        first_paragraph_kwargs['toremove'] = 'remove_this'
        self.first_paragraph = HTMLTag('p', first_paragraph_kwargs)
        del self.first_paragraph.toremove
        self.first_paragraph.first_child = SomeText('Hello World!')
        self.first_paragraph.first_child = 'Hello World! -- changed!'

    def sub_body_show(self):
        sub_body_kwargs = dict()
        sub_body_kwargs['class'] = 'sub_body_class'
        sub_body_kwargs['first_child'] = self.sub_paragraph_child()
        sub_body_kwargs['sub_body_divA'] = self.sub_body_divA_child()
        sub_body_kwargs['sub_body_divB'] = self.sub_body_divA_child()
        self.sub_body = HTMLTag('body', sub_body_kwargs)
        self.sub_body.sub_body_divA.remove_child(1)
        self.sub_body.sub_body_divA.insert_child(2, HTMLTag('span'))
        self.sub_body.sub_body_divA.set_child(3, HTMLTag('li'), 'mylist')
        del self.sub_body.sub_body_divB

    def sub_paragraph_child(self):
        text_child = 'Hello World! -- from the sub paragraph'
        return HTMLTag('p', text_child)
    
    def sub_body_divA_child(self):
        return HTMLTag('div', HTMLTag('div'), HTMLTag('div'), 
                       [HTMLTag('p'), HTMLTag('p'), HTMLTag('div')],
                       custom_class='custom_class_info', 
                       keyword2='keyword2_info')

    def login_button_show(self):
        self.test_login_button = LoginButton()

    def login_dialog_show(self):
        self.login = LoginDialog()
        login_event = Event()
        login_event.add_argument(self.login._username, 'value')
        self.login._loginButton.click = login_event
        self.login._loginButton.click.add_listener(self, App.login)
        self.login._loginButton.click.add_argument(self.login._password, 'value')
    
    def login(self, theLoginButton, msg):
        authenticated = self.authenticate()
        if authenticated:
            try:
                del self.invalid
            except AttributeError:
                pass
            self.valid = HTMLTag('p', 'username and password is valid')
            self.login._loginButton.click.remove_listener(self, App.login)
            del self.login._loginButton.click
            self.login._loginButton.click = Event()
            self.login._loginButton.click.add_listener(self, App.colorize_valid)
        else:
            self.invalid = HTMLTag('p', 'username and/or password is invalid')
            self.login._loginButton.click.remove_argument(self.login._password, 'value')

    def authenticate(self):
        if self.login._username.value == "bad" or self.login._password.value == "bad":
            return False
        return True

    def colorize_valid(self, theLoginButton, msg):
        self.valid.style = 'color:green'
        
