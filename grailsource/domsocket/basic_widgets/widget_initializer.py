"""Copyright (c) 2015 TBillTech.  All rights reserved."""


class WidgetInitializer(object):

    def __init__(self, widget, nodeid, parent_node, ws, index):
        self.widget = widget
        self.nodeid = nodeid
        self.parent_node = parent_node
        self.ws = ws
        self.index = index

    def initialize(self, tag):
        from domsocket.element import Element
        Element.show(self.widget, tag, self.nodeid, self.parent_node, self.ws, self.index)
        return self.widget

    def add_helper_property(self, id, sub_node):
        setattr(self.widget, '_' + id, sub_node)
