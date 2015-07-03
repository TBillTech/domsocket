"""Copyright (c) 2015 TBillTech.  All rights reserved."""

from domsocket.element import Element
from widget_initializer import WidgetInitializer
from html_widget_parser import HTMLWidgetParser


class HTMLWidget(Element):

    def __init__(self, html_source, widget_html_id):
        object.__setattr__(self, '_html_source', html_source)
        object.__setattr__(self, '_widget_html_id', widget_html_id)
        super(HTMLWidget, self).__init__('widget')

    def create_node(self, name, parent_node, index):
        if self.is_active_on_client():
            raise AttributeError()

        node_init = WidgetInitializer(self, name, parent_node, parent_node.get_w_s(), index)
        HTMLWidgetParser(self._html_source, self._widget_html_id, node_init)
        return self
        

