"""Copyright (c) 2015 TBillTech.  

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

The DOMSocket Text Node class is a special case of the Node class because it is based upon the javascript Text Node.

Text Nodes must be handled specially because they are not Elements.
"""

import json
from .messages.insert_text_node_message import InsertTextNodeMessage
from .messages.set_text_node_message import SetTextNodeMessage
from .messages.remove_message import RemoveMessage

from .node import Node

class TextNode(Node):

    def __init__(self, text=''):
        object.__setattr__(self, '_active_on_client', False) 
        object.__setattr__(self, 'tag', 'text')
        self.text = text

    def on_create(self, name, parentNode, index):
        object.__setattr__(self, '_ws', parentNode._get_ws())
        object.__setattr__(self, 'parentNode', parentNode)
        self.show_text_node(index)    
        return self

    def is_active_on_client(self):
        return self._active_on_client

    def set_active_on_client(self):
        object.__setattr__(self, '_active_on_client', True)

    def __setattr__(self, name, value):
        if name != 'text':
            raise AttributeError('Only the text field of the Text Node can be modified') # pragma: no cover
        object.__setattr__(self, 'text', str(value))
        self.update()

    def set_element_attribute(self, element, name):
        if hasattr(element, name):
            current_value = getattr(element, name)
            if hasattr(current_value, 'text'):
                current_value.text = self.text
                return
        super(TextNode, self).set_element_attribute(element, name)

    def _set_nodeid(self, name):
        pass

    def _stop_observations(self):
        pass # pragma: no cover

    def __index__(self):
        return self.parentNode._get_index_of_child(self)

    def __eq__(self, other):
        other_text = getattr(other, 'text', other)
        return self.text == other_text

    def __str__(self):
        return self.text # pragma: no cover

    def _send_msg_to_client(self, msg):
        self._ws.send(msg.jsonstring(), False)

    def show_text_node(self, index): 
        if self.is_active_on_client():
            raise AttributeError() # pragma: no cover

        msg = InsertTextNodeMessage(self, index)
        self._send_msg_to_client(msg)

        self.set_active_on_client()
       
    def update(self):
        if self.is_active_on_client():
            msg = SetTextNodeMessage(self)
            self._send_msg_to_client(msg)

    def _remove_element_from_client(self):
        self.text = ''
        if self.is_active_on_client():
            self.update()
        else:
            raise AttributeError() # pragma: no cover
        

