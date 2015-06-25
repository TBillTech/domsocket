"""Copyright (c) 2015 TBillTech.  All rights reserved."""

from message import Message
import sys


class InsertChildMessage(Message):

    def __init__(self, parent_node, index, node):
        sys.path.append('..')
        from domsocket.text_node import TextNode
        self.msg_dict = {'type': 'insertChild', 
                         'childTag': node.tag, 
                         'parentId': parent_node.id, 
                         'index': index}
        if isinstance(node, TextNode):
            self.msg_dict['text'] = node.text
        else:
            self.msg_dict['childId'] = node.id
