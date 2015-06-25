"""Copyright (c) 2015 TBillTech.  All rights reserved."""

import json


class Message(object):
    def jsonstring(self):
        return json.dumps(self.msg_dict)

    def set_parent_node_id(self, parent_node):
        try:
            self.msg_dict['parentId'] = parent_node.id
        except:
            self.msg_dict['parentId'] = 'body'
