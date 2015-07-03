"""Copyright (c) 2015 TBillTech.  All rights reserved."""

from domsocket.element import Element
from widget_initializer import WidgetInitializer
from html_widget_parser import HTMLWidgetParser


class HTMLWidget(Element):

    def __init__(self, html_source, widget_html_id):
        class HTMLWidgetElement(Element):

            def called_init(self, nodeid, parent_node, ws, index):
                node_init = WidgetInitializer(self, nodeid, parent_node, ws, index)

                HTMLWidgetParser(html_source, widget_html_id, node_init)

        super(HTMLWidget, self).__init__()
        object.__setattr__(self, '_node_class', HTMLWidgetElement)
