"""
The DOMSocket Text Node class is a special case of the Node class because it is based upon the javascript Text Node.

Text Nodes must be handled specially because they are not Elements.

Copyright (c) 2015 TBillTech.  All rights reserved.
"""

import json
from messages.append_child_message import AppendChildMessage
from messages.insert_child_message import InsertChildMessage
from messages.set_child_message import SetChildMessage

from element_error import ElementError
from node import Node

class TextNode(Node):

    def __init__(self, *args, **kw):
        object.__setattr__(self, '_args', args)
        object.__setattr__(self, '_kw', kw)
        object.__setattr__(self, '_active_on_client', False)

    def create_node(self, name, parent_node, index):
        if self.is_active_on_client():
            raise AttributeError()
        new_class = TextNode(*self._args, **self._kw)
        new_class.called_init(name, parent_node, parent_node.get_w_s(), index, *self._args, **self._kw)
        return new_class

    def called_init(self, nodeid, parent_node, ws, index, text=''):
        object.__setattr__(self, 'tag', 'text')
        object.__setattr__(self, 'text', text)
        object.__setattr__(self, '_ws', ws)
        object.__setattr__(self, 'parent_node', parent_node)
        if index == None:
            msg = AppendChildMessage(self.parent_node, self)
        else:
            msg = InsertChildMessage(self.parent_node, index, self)
        self.send_msg(msg)

        object.__setattr__(self, '_active_on_client', True)

    def is_active_on_client(self):
        return self._active_on_client

    def __setattr__(self, name, value):
        if name != 'text':
            raise ElementError('Only the text field of the Text Node can be modified') # pragma: no cover
        object.__setattr__(self, name, value)
        msg = SetChildMessage(self.parent_node, 
                              self.parent_node.child_index(self), 
                              self)
        self.send_msg(msg)

    def __getattribute__(self, name):
        try:
            return object.__getattribute__(self, name)
        except AttributeError:
            if name == 'text':
                if self._args:
                    return self._args[0]
                elif 'text' in self._kw:
                    return self._kw['text']
            raise

    def stop_observations(self):
        pass # pragma: no cover

    def __eq__(self, other):
        if other is None:
            return False
        if isinstance(other, str):
            return self.text == other
        return self.text == other.text

    def send_msg(self, msg):
        self._ws.send(msg.jsonstring(), False)

