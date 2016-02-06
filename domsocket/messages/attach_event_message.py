"""Copyright (c) 2015 TBillTech.  

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

from message import Message


class AttachEventMessage(Message):

    def __init__(self, node, name, attribute_args, client_no_bubble):
        self.msg_dict = {'type': 'attachEvent', 'id': node.id, 'name': name}
        if client_no_bubble:
            self.msg_dict['clientNoBubble'] = True
        if attribute_args:
            self.msg_dict['attributeArgs'] = attribute_args
