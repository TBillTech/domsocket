"""Copyright (c) 2015 TBillTech.  All rights reserved."""

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
