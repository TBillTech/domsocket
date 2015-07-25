"""Copyright (c) 2015 TBillTech.  All rights reserved."""

from message import Message
from operator import index

class SetTextNodeMessage(Message):

    def __init__(self, text_node):
        self.index = index(text_node)
        self.msg_dict = {'type': 'setTextNode', 
                         'childTag': text_node.tag, 
                         'parentId': text_node.parentNode.id, 
                         'index': self.index,
                         'text': text_node.text }
            
