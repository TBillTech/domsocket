"""Copyright (c) 2015 TBillTech.  All rights reserved."""

from message import Message

class SetChildMessage(Message):

    def __init__(self, parent_node, index, node):
        from domsocket.text_node import TextNode
        self.msg_dict = {'type': 'setChild', 
                         'childTag': node.tag, 
                         'parentId': parent_node.id, 
                         'index': index}
        self.set_parent_node_id(parent_node)
        if isinstance(node, TextNode):
            self.msg_dict['text'] = node.text
        else:
            self.msg_dict['childId'] = node.id # pragma: no cover
            
