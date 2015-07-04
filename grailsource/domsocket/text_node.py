"""
The DOMSocket Text Node class is a special case of the Node class because it is based upon the javascript Text Node.

Text Nodes must be handled specially because they are not Elements.

Copyright (c) 2015 TBillTech.  All rights reserved.
"""

import json
from messages.insert_text_node_message import InsertTextNodeMessage
from messages.set_text_node_message import SetTextNodeMessage

from element_error import ElementError
from node import Node

class TextNode(Node):

    def __init__(self, text=''):
        object.__setattr__(self, '_active_on_client', False) 
        object.__setattr__(self, 'tag', 'text')
        self.text = text

    def create_node(self, name, parent_node, index):
        object.__setattr__(self, '_ws', parent_node.get_w_s())
        object.__setattr__(self, 'parent_node', parent_node)
        self.show(index)    
        return self

    def is_active_on_client(self):
        return self._active_on_client

    def set_active_on_client(self):
        object.__setattr__(self, '_active_on_client', True)

    def __setattr__(self, name, value):
        if name != 'text':
            raise ElementError('Only the text field of the Text Node can be modified') # pragma: no cover
        object.__setattr__(self, 'text', value)
        self.update()

    def stop_observations(self):
        pass # pragma: no cover

    def __eq__(self, other):
        other_text = getattr(other, 'text', other)
        return self.text == other_text

    def send_msg(self, msg):
        self._ws.send(msg.jsonstring(), False)

    def show(self, index): 
        if self.is_active_on_client():
            raise AttributeError()

        msg = InsertTextNodeMessage(self.parent_node, index, self)
        self.send_msg(msg)

        self.set_active_on_client()
       
    def update(self):
        if self.is_active_on_client():
            msg = SetTextNodeMessage(self.parent_node, 
                                  self.parent_node.child_index(self), 
                                  self)
            self.send_msg(msg)
        

