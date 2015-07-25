"""
Module:  remove_message.py

Description:
  Constructs a remove element message

Copyright (c) 2015 TBillTech.  All rights reserved.

"""

from message import Message


class RemoveMessage(Message):

    def __init__(self, node):
        from remove_child_message import RemoveChildMessage
        msg = RemoveChildMessage(node.parentNode, node)
        self.msg_dict = msg.msg_dict
