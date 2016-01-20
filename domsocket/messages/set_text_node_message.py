"""Copyright (c) 2015 TBillTech.  

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

from message import Message
from operator import index

class SetTextNodeMessage(Message):

    def __init__(self, text_node):
        self.index = index(text_node)
        self.msg_dict = {'type': 'setTextNode', 
                         'childTag': text_node.tag, 
                         'parentId': text_node.parentNode.id, 
                         'index': self.index,
                         'text': text_node.text }
            
