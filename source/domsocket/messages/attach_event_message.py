"""
Module:  attach_event_message.py

Description:
  Constructs an attach event message

Copyright (c) 2015 TBillTech.  All rights reserved.

"""

from message import Message


class AttachEventMessage(Message):

    def __init__(self, node, name, attribute_args):
        self.msg_dict = {'type': 'attachEvent', 'id': node.id, 'name': name}
        if attribute_args:
            self.msg_dict['attributeArgs'] = attribute_args
