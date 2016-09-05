"""Copyright (c) 2015 TBillTech.  

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

from .message import Message
import sys


class InsertChildMessage(Message):

    def __init__(self, parentNode, index, node):
        self.index = self.get_index(parentNode, index)
        self.parent_id = self.get_parent_id(parentNode) 
        self.msg_dict = {'type': 'insertChild', 
                         'childTag': node.tag, 
                         'parentId': self.parent_id, 
                         'index': self.index,
                         'childId': node.id }
