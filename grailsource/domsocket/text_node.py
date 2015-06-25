"""
The DOMSocket Text Node class is a special case of the Node class because it is based upon the javascript Text Element.

Text Elements must be handled specially because they do not have id properties in the DOM.

Copyright (c) 2015 TBillTech.  All rights reserved.
"""

from node_error import NodeError
from messages.append_child_message import AppendChildMessage
from messages.insert_child_message import InsertChildMessage
from messages.set_child_message import SetChildMessage
from node import Node


class TextNode(Node):

    def __init__(self, nodeid, parent_node, ws, index, text=''):
        object.__setattr__(self, 'tag', 'text')
        object.__setattr__(self, 'text', text)
        object.__setattr__(self, '_ws', ws)
        object.__setattr__(self, 'parent_node', parent_node)
        if index == None:
            msg = AppendChildMessage(self.parent_node, self)
        else:
            msg = InsertChildMessage(self.parent_node, index, self)
        self.send_msg(msg)

    def __setattr__(self, name, value):
        if name != 'text':
            raise NodeError('Only the text field of the Text Node can be modified') # pragma: no cover
        object.__setattr__(self, name, value)
        msg = SetChildMessage(self.parent_node, 
                              self.parent_node.child_index(self), 
                              self)
        self.send_msg(msg)

    def __eq__(self, other):
        if isinstance(other, str):
            return self.text == other
        return self.text == other.text
