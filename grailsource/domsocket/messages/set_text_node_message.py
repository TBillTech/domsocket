"""Copyright (c) 2015 TBillTech.  All rights reserved."""

from message import Message

class SetTextNodeMessage(Message):

    def __init__(self, parent_node, index, node):
        self.msg_dict = {'type': 'setTextNode', 
                         'childTag': node.tag, 
                         'parentId': parent_node.id, 
                         'index': index,
                         'text': node.text }
            
