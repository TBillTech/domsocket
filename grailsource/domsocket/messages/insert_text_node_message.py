"""Copyright (c) 2015 TBillTech.  All rights reserved."""

from message import Message
import sys


class InsertTextNodeMessage(Message):

    def __init__(self, text_node, index):
        self.index = self.get_index(text_node.parent_node, index)
        self.msg_dict = {'type': 'insertTextNode', 
                         'childTag': text_node.tag, 
                         'parentId': text_node.parent_node.id, 
                         'index': self.index,
                         'text': text_node.text }

