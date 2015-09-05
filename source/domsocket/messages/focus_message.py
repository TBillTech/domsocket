""" Copyright (c) 2015 TBillTech.  All rights reserved. """

from message import Message

class FocusMessage(Message):

    def __init__(self, node):
        self.msg_dict = {'type': 'setFocus', 'id': node.id}
