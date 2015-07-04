"""Copyright (c) 2015 TBillTech.  All rights reserved."""

import json


class Message(object):
    def jsonstring(self):
        return json.dumps(self.msg_dict)

    def get_index(self, parent_node, index):
        if parent_node is None:
            return 0
        if index is None:
            return len(parent_node)
        return index

    def get_parent_id(self, parent_node):
        return getattr(parent_node, 'id', 'body')
