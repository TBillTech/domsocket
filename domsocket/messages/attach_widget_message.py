"""Copyright (c) 2015 TBillTech.  

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

from .message import Message


class AttachWidgetMessage(Message):

    def __init__(self, node, className):
        self.msg_dict = {'type': 'attachWidget', 
                         'id': node.id, 
                         'className': className}
