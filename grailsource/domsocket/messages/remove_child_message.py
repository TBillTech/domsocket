"""
Module:  remove_child_message.py

Description:
  Constructs a remove child element message

Copyright (c) 2015 TBillTech.  All rights reserved.

"""

from message import Message


class RemoveChildMessage(Message):

    def __init__(self, parentNode, node):
        index = parentNode.child_index(node)
        self.msg_dict = {'type': 'removeChild', 
                         'parentId': parentNode.id, 
                         'index': index }
