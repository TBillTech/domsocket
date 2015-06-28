"""Copyright (c) 2015 TBillTech.  All rights reserved."""

from domsocket.element import Node


class Text(Node):

    def __init__(self, *args, **kw):
        from domsocket.text_node import TextNode
        super(Text, self).__init__(TextNode, *args, **kw)
