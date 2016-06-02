"""Copyright (c) 2015 TBillTech.  

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

from os.path import abspath
from os.path import join
import os
from domsocket.event import Event
from domsocket.basic_widgets.javascript_widget import JavascriptWidget


class IncrementWidget(JavascriptWidget):

    def __init__(self, increment_handler):
        super(IncrementWidget, self).__init__()

        self._increment_handler = increment_handler

    def on_create(self, name, parentNode, index):
        super(IncrementWidget, self).on_create(name, parentNode, index)

        self.currentValue = "0"
        self.increment = self.get_increment_event()

    def do_increment(self, increment_by):
        self.incrementBy = str(increment_by)
        self.send('haveWork')

    def get_increment_event(self):
        increment_event = Event()
        increment_event.add_argument(self, 'currentValue')
        increment_event.add_argument(self, 'haveWork')
        increment_event.add_observer(self, IncrementWidget.on_increment)
        return increment_event

    def on_increment(self, self_, msg):
        if not msg['event']['detail'] == "done":
            raise Exception('message "increment" did not return detail=="done"')
        self._increment_handler(int(self.currentValue))
