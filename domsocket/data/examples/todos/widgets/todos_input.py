"""Copyright (c) 2015 TBillTech.  

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

from domsocket.basic_widgets.html_widget import HTMLWidget
from domsocket.event import Event


class TodosInput(HTMLWidget):

    ENTER_KEY_CODE = 13

    def __init__(self):
        super(TodosInput, self).__init__()

    def on_create(self, name, parentNode, index):
        super(TodosInput, self).on_create(name, parentNode, index)
        self._TodosEntry.value = ''
        #self._TodosEntry.keydown = self.create_input_keydown_event()
        self._TodosEntry.set_focus()
        self._Add.click = self.create_add_press_event()

    def create_input_keydown_event(self):
        input_keydown_event = Event()
        input_keydown_event.add_observer(self, TodosInput.on_input_keydown)
        input_keydown_event.add_argument(self._TodosEntry, 'value')
        return input_keydown_event

    def create_add_press_event(self):
        add_press_event = Event()
        add_press_event.add_observer(self, TodosInput.on_add_press)
        add_press_event.add_argument(self._TodosEntry, 'value')
        return add_press_event

    def on_input_keydown(self, theInputControl, msg):
        if msg['event']['keyCode'] != self.ENTER_KEY_CODE:
            self._TodosEntry.value = self._TodosEntry.value + msg['event']['key']
            return
        else:
            self.add_todo()

    def on_add_press(self, theInputControl, msg):
        self.add_todo()

    def add_todo(self):
        self.parentNode.add_todos_item(self._TodosEntry.value)
        self._TodosEntry.value = ''
        self._TodosEntry.set_focus()

