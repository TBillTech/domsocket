"""Copyright (c) 2015 TBillTech.  All rights reserved."""

from os.path import abspath, join
from domsocket.element import Element
from widget_initializer import WidgetInitializer
from html_widget_parser import HTMLWidgetParser


class HTMLWidget(Element):

    def __init__(self):
        super(HTMLWidget, self).__init__()

    def on_create(self, name, parentNode, index):
        if self.is_active_on_client():
            raise AttributeError() # pragma: no cover

        self._tempParentNodeRef = parentNode
        self._node_init = WidgetInitializer(self, name, parentNode, parentNode._get_ws(), index)
        HTMLWidgetParser(self)
        del self._tempParentNodeRef
        return self
        
    def get_widget_html_id(self):
        return getattr(self, '_widget_html_id', None)

    def get_html_source(self):
        try:
            return self._html_source
        except AttributeError:
            return self.read_html_source()

    def read_html_source(self):
        filename = self.get_html_source_path()
        with open(filename, 'r') as html_file:
            return html_file.read()

    def get_html_source_path(self):
        try:
            return self._html_source_path
        except AttributeError:
            return self.construct_html_source_path()

    def construct_html_source_path(self):
        app_name = self.get_html_source_app_name()
        file_name = self.get_html_source_filename()
        return abspath(join('apps',
                            app_name,
                            'widgets',
                            file_name))

    def get_html_source_filename(self):
        try:
            return self._html_source_filename
        except AttributeError:
            return '%s.%s' % (self.get_simple_module_name(),'html')
    
    def get_simple_module_name(self):
        return self.__class__.__module__.split('.')[-1]
