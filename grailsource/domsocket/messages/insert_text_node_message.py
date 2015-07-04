"""Copyright (c) 2015 TBillTech.  All rights reserved."""

from message import Message
import sys


class InsertTextNodeMessage(Message):

    def __init__(self, parent_node, index, node):
        self.index = self.get_index(parent_node, index)
        self.msg_dict = {'type': 'insertTextNode', 
                         'childTag': node.tag, 
                         'parentId': parent_node.id, 
                         'index': self.index,
                         'text': node.text }

