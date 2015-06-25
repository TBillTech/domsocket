"""
Module:  set_attribute_message.py

Description:
  Constructs a set attribute message

Copyright (c) 2015 TBillTech.  All rights reserved.

"""

from message import Message


class SetAttributeMessage(Message):

    def __init__(self, node, name, value):
        self.msg_dict = {
            'type': 'setAttribute', 'id': node.id, 'name': name, 'value': value}
