"""Copyright (c) 2015 TBillTech.  All rights reserved."""

import sys
from html_tag import HTMLTag

import logging
from HTMLParser import HTMLParser
from domsocket.text_node import TextNode
from domsocket.element import Element

class HTMLImporterException(Exception):
    pass


class HTMLWidgetParser(HTMLParser):

    def __init__(self, html_source, widget_html_id, node_init):
        HTMLParser.__init__(self)

        self.html_source = html_source

        if widget_html_id:
            self.widget_html_id = widget_html_id
        self.node_init = node_init
        self.have_found_first_tag = False
        self.xml_parse_stack = list()
        self.feed(self.html_source)
        self.close()

    def handle_starttag(self, tag, xml_attrs):
        if self.tag_needs_processing(tag, xml_attrs):
            self.process_tag(tag, xml_attrs)

    def handle_endtag(self, tag):
        self.process_end_tag(tag)

    def handle_data(self, data):
        if self.data_is_whitespace(data):
            return
        self.process_data(data)

    def data_is_whitespace(self, data):
        return not data.strip()

    def tag_needs_processing(self, tag, xml_attrs):
        if self.before_first_tag(xml_attrs):
            return False
        if self.after_last_tag():
            return False
        return True

    def before_first_tag(self, xml_attrs):
        if self.have_found_first_tag:
            return False
        if self.is_widget_start_tag(xml_attrs):
            return False
        return True

    def after_last_tag(self):
        if self.have_found_first_tag and self.stack_is_empty():
            return True
        return False

    def stack_is_empty(self):
        return not self.xml_parse_stack

    def this_is_the_first_tag(self):
        return len(self.xml_parse_stack) == 0

    def is_widget_start_tag(self, xml_attrs):
        id = self.get_id(xml_attrs)
        try:
            return id == self.widget_html_id
        except AttributeError:
            return self.this_is_the_first_tag()

    def process_tag(self, tag, xml_attrs):
        if self.is_widget_start_tag(xml_attrs):
            self.process_first_tag(tag, xml_attrs)
        else:
            self.process_sub_tag(tag, xml_attrs)

    def process_first_tag(self, tag, xml_attrs):
        self.have_found_first_tag = True
        widget = self.setup_first_widget(tag)
        self.add_widget(widget, xml_attrs)

    def process_sub_tag(self, tag, xml_attrs):
        widget = self.create_sub_widget(tag, xml_attrs)
        self.add_widget(widget, xml_attrs)

    def add_widget(self, widget, xml_attrs):
        self.set_top_widget(widget)
        self.set_top_widget_attributes_except_id(xml_attrs)

    def set_top_widget(self, widget):
        self.xml_parse_stack.append(widget)

    def process_end_tag(self, tag):
        if not self.have_found_first_tag or self.after_last_tag():
            return
        self.pop_stack(tag)

    def pop_stack(self, tag):
        if self.top_is_tag(tag):
            self.pop_stack_top()
            return
        if self.prior_is_tag(tag):
            self.pop_stack_prior()
            return
        raise HTMLImporterException("end tag (%s) does not match current start tag (%s) on the stack at position %s",
                                    tag, self.get_end_tag(), self.getpos())  # pragma: no cover

    def top_is_tag(self, tag):
        return self.get_end_tag() == tag

    def prior_is_tag(self, tag):
        return self.get_prior_end_tag() == tag

    def pop_stack_top(self):
        self.xml_parse_stack.pop()

    def pop_stack_prior(self):
        self.pop_stack_top()
        self.pop_stack_top()

    def get_id(self, xml_attrs):
        for (attr_name, attr_value) in xml_attrs:
            if attr_name == 'id':
                return attr_value

    def set_top_widget_attributes_except_id(self, xml_attrs):
        for (attr_name, attr_value) in xml_attrs:
            if attr_name == 'id':
                continue
            self.set_top_widget_attribute(attr_name, attr_value)

    def set_top_widget_attribute(self, attr_name, attr_value):
        widget = self.get_top_widget()
        setattr(widget, attr_name, attr_value)

    def get_end_tag(self):
        return self.get_top_widget().tag

    def get_prior_end_tag(self):
        try:
            return self.get_prior_widget().tag
        except IndexError: # pragma: no cover
            pass # pragma: no cover
        except AttributeError: # pragma: no cover
            pass # pragma: no cover
        return None # pragma: no cover

    def get_top_widget(self):
        return self.xml_parse_stack[-1]

    def get_prior_widget(self):
        return self.xml_parse_stack[-2]

    def setup_first_widget(self, tag):
        return self.node_init.initialize(tag)

    def create_sub_widget(self, tag, xml_attrs):
        child_tag = HTMLTag(tag)
        id = self.get_id(xml_attrs)
        if id:
            return self.create_sub_widget_with_id(child_tag, id)
        else:
            return self.create_sub_widget_anonymous(child_tag)

    def create_sub_widget_with_id(self, child_tag, id):
        cur_parent = self.get_top_widget()
        setattr(cur_parent, id, child_tag)
        widget = getattr(cur_parent, id)
        self.node_init.add_helper_property(id, widget)
        return widget

    def create_sub_widget_anonymous(self, child_tag):
        cur_parent = self.get_top_widget()
        widget = cur_parent.append_child(child_tag)
        return widget

    def process_data(self, data):
        if self.use_child_data():
            child_text = Element(TextNode, data)
            cur_parent = self.get_top_widget()
            cur_parent.append_child(child_text)

    def use_child_data(self):
        return self.have_found_first_tag and self.xml_parse_stack
