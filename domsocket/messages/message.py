"""Copyright (c) 2015 TBillTech.  

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

import json

class Message(object):
    def jsonstring(self):
        return json.dumps(self.msg_dict)

    def get_index(self, parentNode, index):
        if parentNode is None:
            return 0
        if index is None:
            return len(parentNode)
        return index

    def get_parent_id(self, parentNode):
        return getattr(parentNode, 'id', 'body')
