"""Copyright (c) 2015 TBillTech.  

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

from .html_tag import HTMLTag
from domsocket.text_node import TextNode
from domsocket.element import Element

class WidgetInitializer(object):
    
    tag_class = HTMLTag
    text_node_class = TextNode

    def __init__(self, widget, nodeid, parentNode, index):
        self.widget = widget
        self.nodeid = nodeid
        self.parentNode = parentNode
        self.index = index

    def initialize(self, tag):
        self.widget.tag = tag
        Element.on_create(self.widget, self.nodeid, self.parentNode, self.index)
        return self.widget

    def add_helper_property(self, id, sub_node):
        key = '_' + id
        if hasattr(self.widget, key):
            prior = getattr(self.widget, key)
            try:
                _ = prior.tag
                setattr(self.widget, key, [prior, sub_node])
            except AttributeError:
                prior += [sub_node]
        else:
            setattr(self.widget, key, sub_node)
                
        
