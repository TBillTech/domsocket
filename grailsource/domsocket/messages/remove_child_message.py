"""
Module:  remove_child_message.py

Description:
  Constructs a remove child element message

Copyright (c) 2015 TBillTech.  All rights reserved.

"""

from message import Message


class RemoveChildMessage(Message):

    def __init__(self, parent_node, node):
        index = parent_node.child_index(node)
        self.msg_dict = {
            'type': 'removeChild', 'parentId': parent_node.id, 'index': index}
