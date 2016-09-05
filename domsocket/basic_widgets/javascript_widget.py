"""Copyright (c) 2015 TBillTech.  

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

from .html_widget import HTMLWidget
from domsocket.messages.attach_widget_message import AttachWidgetMessage
from domsocket.messages.detach_widget_message import DetachWidgetMessage
from domsocket.messages.send_to_widget_message import SendToWidgetMessage


class JavascriptWidget(HTMLWidget):

    def __init__(self):
        super(JavascriptWidget, self).__init__()

    def on_create(self, name, parentNode, index):
        super(JavascriptWidget, self).on_create(name, parentNode, index)

        class_name = type(self).__name__
        msg = AttachWidgetMessage(self, class_name)
        self._send_msg_to_client(msg)
        
        return self
        
    def del_element_attribute(self, element, name):
        msg = DetachWidgetMessage(self)
        self._send_msg_to_client(msg)
        super(JavascriptWidget, self).del_element_attribute(element, name)

    def _remove_element_from_client(self):
        msg = DetachWidgetMessage(self)
        self._send_msg_to_client(msg)
        super(JavascriptWidget, self)._remove_element_from_client()

    def send(self, msg_string):
        msg = SendToWidgetMessage(self, msg_string)
        self._send_msg_to_client(msg)
