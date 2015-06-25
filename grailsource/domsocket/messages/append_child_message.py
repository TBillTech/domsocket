"""Copyright (c) 2015 TBillTech.  All rights reserved."""

from message import Message
import sys


class AppendChildMessage(Message):

    def __init__(self, parent_node, node):
        sys.path.append('..')
        from domsocket.text_node import TextNode
        self.msg_dict = {'type': 'appendChild', 'childTag': node.tag}
        self.set_parent_node_id(parent_node)
        if isinstance(node, TextNode):
            self.msg_dict['text'] = node.text
        else:
            self.msg_dict['childId'] = node.id
