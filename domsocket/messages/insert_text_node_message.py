"""Copyright (c) 2015 TBillTech.  

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

from .message import Message
import sys


class InsertTextNodeMessage(Message):

    def __init__(self, text_node, index):
        self.index = self.get_index(text_node.parentNode, index)
        self.msg_dict = {'type': 'insertTextNode', 
                         'childTag': text_node.tag, 
                         'parentId': text_node.parentNode.id, 
                         'index': self.index,
                         'text': text_node.text }

