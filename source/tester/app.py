"""Copyright (c) 2015 TBillTech.  All rights reserved."""

from domsocket.event import Event
from domsocket.basic_widgets.html_tag import HTMLTag
from domsocket.element import Element
from widgets.login_dialog import LoginDialog
from widgets.login_button import LoginButton
from domsocket.text_node import TextNode
from domsocket.element_error import ElementError
from operator import index

class App(Element):

    def __init__(self):
        super(App, self).__init__()

    def dom_insert(self, nodetag, nodeid, parentNode, ws, child_index):
        super(App, self).dom_insert(nodetag, nodeid, parentNode, ws, child_index)

        self.first_paragraph_show()
        self.sub_body_show()
        self.login_button_show()
        self.login_dialog_show()
        
    def first_paragraph_show(self):
        self.create_first_paragraph()
        self._attribute_removal_test()
        self._text_node_test()
        self._immutable_attribute_test()

    def create_first_paragraph(self):
        first_paragraph_kwargs = dict()
        first_paragraph_kwargs['text_node'] = TextNode('Hello World!')
        first_paragraph_kwargs['class'] = 'first'
        first_paragraph_kwargs['useful'] = 'true'
        first_paragraph_kwargs['toremove'] = 'remove_this'
        self.first_paragraph = HTMLTag('p', first_paragraph_kwargs)

    def _attribute_removal_test(self):
        self.first_paragraph.toremove = 'remove_this_instead'
        del self.first_paragraph.toremove
        self.first_paragraph._toremove = 'hidden data'
        del self.first_paragraph._toremove
        try:
            if self.first_paragraph._toremove == 'hidden data':
                pass
            raise ElementError('Could not remove hidden data _toremove')
        except AttributeError:
            pass

    def _text_node_test(self):
        self.first_paragraph.text_node = TextNode('Hello World!')
        self.first_paragraph.text_node.text = 'Hello World! -- changed!'
        self.first_paragraph.text_node = TextNode('Hello World! -- changed!')

    def _immutable_attribute_test(self):
        try:
            self.first_paragraph.useful = None
            raise Error('attribute useful should not be allowed to set to None!')
        except ElementError:
            pass
        try:
            self.first_paragraph.id = 'wrong.name'
            raise Error('Should not be allowed to modify id!')
        except ElementError:
            pass
        try:
            del self.first_paragraph.id
            raise Error('Should not be allowed to delete id!')
        except ElementError:
            pass

    def sub_body_show(self):
        self.create_sub_body()
        self._slice_tests()
        self._item_tests()

    def create_sub_body(self):
        sub_body_kwargs = dict()
        sub_body_kwargs['class'] = 'sub_body_class'
        sub_body_kwargs['subp_child'] = self.sub_paragraph_child()
        sub_body_kwargs['sub_body_divA'] = self.sub_body_divA_child()
        sub_body_kwargs['sub_body_divB'] = self.sub_body_divA_child()
        self.sub_body = HTMLTag('body', sub_body_kwargs)

    def _slice_tests(self):
        del self.sub_body.sub_body_divA[1:2]
        self.sub_body.sub_body_divA[2:2] = [HTMLTag('span')]
        self.sub_body.sub_body_divA[3] = [HTMLTag('li')]

    def _item_tests(self):
        del self.sub_body.sub_body_divB 
        self.sub_body.sub_body_divB = self.sub_body_divA_child()
        self.sub_body.sub_body_divB = self.sub_body_divA_child()
        del self.sub_body[self.sub_body.sub_body_divB]

    def sub_paragraph_child(self):
        text_child = TextNode('Hello World! -- from the sub paragraph')
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
        self._test_event_out_of_order()

    def _test_event_out_of_order(self):
        login_event = Event()
        login_event.add_argument(self.login._username, 'value')
        self.login._loginButton.click = login_event
        login_event.add_observer(self, App.on_login)
        login_event.add_argument(self.login._password, 'value')

    def on_login(self, theLoginButton, msg):
        authenticated = self.authenticate()
        if authenticated:
            self.on_authenticated()
        else:
            self.on_not_authenticated()

    def on_authenticated(self):
        if 'invalid' in self:
            del self.invalid
        self.valid = HTMLTag('p', TextNode('username and password is valid'))
        self._test_replace_event()

    def on_not_authenticated(self):
        if 'valid' in self:
            del self.invalid
        self.invalid = HTMLTag('p', TextNode('username and/or password is invalid'))
        self._test_remove_event_argument()

    def _test_remove_event_argument(self):
        self.login._loginButton.click.remove_argument(self.login._password, 'value')

    def _test_replace_event(self):
        self.login._loginButton.click.remove_observer(self, App.on_login)
        del self.login._loginButton.click
        self.login._loginButton.click = Event()
        self.login._loginButton.click.add_observer(self, App.colorize_valid)

    def authenticate(self):
        if self.login._username.value == "bad" or self.login._password.value == "bad":
            return False
        return True

    def colorize_valid(self, theLoginButton, msg):
        self.valid.style = 'color:green'
        
