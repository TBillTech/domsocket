"""Copyright (c) 2015 TBillTech.  All rights reserved."""

from domsocket.element import Element

class WidgetInitializer(object):

    def __init__(self, widget, nodeid, parentNode, ws, index):
        self.widget = widget
        self.nodeid = nodeid
        self.parentNode = parentNode
        self.ws = ws
        self.index = index

    def initialize(self, tag):
        Element.dom_insert(self.widget, tag, self.nodeid, self.parentNode, self.ws, self.index)
        return self.widget

    def add_helper_property(self, id, sub_node):
        setattr(self.widget, '_' + id, sub_node)
