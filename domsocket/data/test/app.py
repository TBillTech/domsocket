#!/usr/bin/python
"""Copyright (c) 2015 TBillTech.  

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

from domsocket.zmq_runner import ZMQRunner, domsocket_js_path
from domsocket.event import Event
from domsocket.basic_widgets.html_tag import HTMLTag
from domsocket.element import Element
from widgets.login_dialog import LoginDialog
from widgets.login_button import LoginButton
from widgets.increment_widget import IncrementWidget
from domsocket.text_node import TextNode
from domsocket.element_error import ElementError
from operator import index

theRunner = None

class App(Element):

    _html_source_app_name = 'tester'

    def __init__(self):
        super(App, self).__init__()
        self.tag = 'div'

    def on_create(self, nodeid, ws, child_index):
        super(App, self).on_create(nodeid, ws, child_index)

        self.first_paragraph_show()
        self.sub_body_show()
        self.login_button_show()
        self.login_dialog_show()
        self.longlist_show()
        self.increment_widget_show()
        self.noop = lambda x: x
        
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
        self.first_paragraph.text_node.text = 'Hello World! -- changed to!'
        self.first_paragraph.text_node = TextNode('Hello World! -- changed to!')
        self.first_paragraph.text_node = TextNode('Hello World! -- changed!')
        self.first_paragraph += [TextNode('A'), TextNode('B'), TextNode('C')]
        self.first_paragraph[-3:] = []

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
        sub_body_kwargs['class'] = 'sub_body_class_tochange'
        sub_body_kwargs['subp_child'] = self.sub_paragraph_child()
        sub_body_kwargs['sub_body_divA'] = self.sub_body_divA_child()
        sub_body_kwargs['sub_body_divB'] = self.sub_body_divA_child()
        self.sub_body = HTMLTag('body', sub_body_kwargs)
        if self.sub_body.getattr_class() != 'sub_body_class_tochange':
            raise Error('getattr_class return is wrong')
        self.sub_body.setattr_class('sub_body_class')
        if not self.sub_body.get_html_source_app_name() == 'tester':
            raise Error('source app name is not tester!')        

    def _slice_tests(self):
        del self.sub_body.sub_body_divA[1:2]
        self.sub_body.sub_body_divA[2:2] = [HTMLTag('span')]
        self.sub_body.sub_body_divA[3] = [HTMLTag('li')]
        self.sub_body.sub_body_divA[self.sub_body.sub_body_divA[4]] = [HTMLTag('span')]
        self.sub_body.sub_body_divA[-1] = [HTMLTag('span')]
        self.sub_body.sub_body_divA[7:13:2] = [HTMLTag('p'), HTMLTag('p'), HTMLTag('p')]

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
                       [HTMLTag('p'), HTMLTag('p'), HTMLTag('div'),
                        HTMLTag('div'), HTMLTag('div'), HTMLTag('div'),
                        HTMLTag('div'), HTMLTag('div'), HTMLTag('div'),
                        HTMLTag('div'), HTMLTag('div'), HTMLTag('div'),
                        HTMLTag('div'), HTMLTag('div'), HTMLTag('div')],
                       custom_class='custom_class_info', 
                       keyword2='keyword2_info')

    def login_button_show(self):
        self.test_login_button = LoginButton()
        on_focus = Event()
        on_focus.add_observer(self, App.on_focus)
        self.test_login_button.focus = on_focus
        self.test_login_button.set_focus()

    def on_focus(self, theLoginButton, msg):
        if msg['event']['target'] != self.test_login_button.id:
            raise Error('on_focus target "%s" != test_login_button id "%s"' %
                        (msg['event']['target'], self.test_login_button.id))
        self.focus_found = HTMLTag('p', TextNode('on focus event returned'))

    def login_dialog_show(self):
        self.login = LoginDialog()
        self._test_event_out_of_order()

    def _test_event_out_of_order(self):
        login_event = Event(client_no_bubble=True)
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
        
    def longlist_show(self):
        self.longlist = HTMLTag('ul')
        for index in range(100):
            self.longlist += [self.new_list_element()]
            self.add_select(self.longlist[-1])
        self.longlist[10:90] = []
        for index in range(100):
            self.longlist += [self.new_list_element()]
            self.add_select(self.longlist[-1])
        self.longlist[:] = []
        for index in range(50):
            self.longlist += [self.new_list_element()]
            self.add_select(self.longlist[-1])            
        self.longlist[10:] = []

    def new_list_element(self):
        return HTMLTag('li', count=len(self.longlist))

    def add_select(self, the_li):
        if not the_li.find_parent(App) == self:
            raise ElementError('Child the_li is not a descendant of self')
        if not the_li.find_handler('on_select') == self.on_select:
            raise ElementError('could not find on_select handler for the_li')

        the_li.selector = HTMLTag('input', { 'type': 'checkbox' } )
        select_click = Event()
        select_click.add_observer(self, App.on_select)
        the_li.selector.click = select_click

    def on_select(self, the_checkbox, msg):
        pass

    def client_has_closed_ws(self, code, reason):
        print('Test client has closed')
        theRunner.stop()

    def increment_widget_show(self):
        self.incrementor = IncrementWidget(self.on_increment)
        self._increment_expected_value = 3
        self.incrementor.do_increment(3)

    def on_increment(self, current_value):
        if self._increment_expected_value != current_value:
            raise ElementError('on increment expected %s != current %s' % \
                               (self._increment_expected_value, current_value))
        self._increment_expected_value += 3
        if current_value > 3:
            del self.incrementor


if __name__ == '__main__':
    manifest = {
        ('.','app.html') : ('.','app.html'),
        ('.','app.conf') : ('.','app.conf'),
        'css' : (),
        'scripts' : ('domsocket.js','increment_widget.js'),
        ('scripts', 'domsocket.js') : (domsocket_js_path, 'domsocket.js'), 
        ('scripts', 'increment_widget.js') : ('widgets', 'increment_widget.js'), 
        'static' : (),
        'style' : (),
        'toolkits' : ()
        }
    with ZMQRunner(App, manifest) as runner:
        theRunner = runner
        runner.run()
