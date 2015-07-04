"""Copyright (c) 2015 TBillTech.  All rights reserved."""

from message import Message
import sys


class InsertChildMessage(Message):

    def __init__(self, parent_node, index, node):
        self.index = self.get_index(parent_node, index)
        self.parent_id = self.get_parent_id(parent_node) 
        self.msg_dict = {'type': 'insertChild', 
                         'childTag': node.tag, 
                         'parentId': self.parent_id, 
                         'index': self.index,
                         'childId': node.id }
