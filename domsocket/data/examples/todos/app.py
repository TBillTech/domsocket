#!/usr/bin/python
"""Copyright (c) 2015 TBillTech.  

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

from domsocket.zmq_runner import ZMQRunner, domsocket_js_path
from domsocket.element import Element
from widgets.todos_item import TodosItem
from widgets.todos_input import TodosInput
from domsocket.text_node import TextNode
import argparse
import os
from os.path import join

class App(Element):

    _html_source_app_name = 'todos'

    def __init__(self):
        super(App, self).__init__()
        self.tag = 'div'

    def on_create(self, nodeid, ws, child_index):
        super(App, self).on_create(nodeid, ws, child_index)

        self += [TodosInput()]

    def add_todos_item(self, todo_text):
        self[0:0] = [TodosItem(todo_text)]

if __name__ == '__main__':
    manifest = {
        ('.','app.html') : ('.','app.html'),
        ('.','app.conf') : ('.','app.conf'),
        'css' : (),
        'scripts' : ('domsocket.js',),
        ('scripts', 'domsocket.js') : (domsocket_js_path, 'domsocket.js'), 
        'static' : (),
        'style' : (),
        'toolkits' : ()
        }
    with ZMQRunner(App, manifest) as runner:
        runner.run()
