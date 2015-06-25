"""
Module:  remove_attribute_message.py

Description:
  Constructs a remove attribute message

Copyright (c) 2015 TBillTech.  All rights reserved.

"""

from message import Message


class RemoveAttributeMessage(Message):

    def __init__(self, node, name):
        self.msg_dict = {'type': 'removeAttribute', 'id': node.id, 'name': name}
