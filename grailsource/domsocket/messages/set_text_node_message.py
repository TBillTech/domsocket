"""Copyright (c) 2015 TBillTech.  All rights reserved."""

from message import Message

class SetTextNodeMessage(Message):

    def __init__(self, text_node):
        index = text_node.parent_node.child_index(text_node)
        self.msg_dict = {'type': 'setTextNode', 
                         'childTag': text_node.tag, 
                         'parentId': text_node.parent_node.id, 
                         'index': index,
                         'text': text_node.text }
            
