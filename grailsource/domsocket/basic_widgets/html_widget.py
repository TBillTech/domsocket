"""Copyright (c) 2015 TBillTech.  All rights reserved."""

from domsocket.child import Child
from node_initializer import NodeInitializer
from html_widget_parser import HTMLWidgetParser


class HTMLWidget(Child):

    def __init__(self, html_source, widget_html_id):
        from domsocket.element import Node

        class HTMLWidgetNode(Node):

            def __init__(self, nodeid, parent_node, ws, index):
                node_init = NodeInitializer(self, nodeid, parent_node, ws, index)

                HTMLWidgetParser(html_source, widget_html_id, node_init)

        super(HTMLWidget, self).__init__(HTMLWidgetNode)
