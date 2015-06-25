"""
Module:  detach_event_message.py

Description:
  Constructs an dettach event message

Copyright (c) 2015 TBillTech.  All rights reserved.

"""

from message import Message


class DetachEventMessage(Message):

    def __init__(self, node, name):
        self.msg_dict = {'type': 'detachEvent', 'id': node.id, 'name': name}
