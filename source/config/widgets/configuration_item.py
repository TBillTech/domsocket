"""Copyright (c) 2015 TBillTech.  All rights reserved."""

from os.path import abspath
from os.path import join
import os
from domsocket.basic_widgets.html_widget import HTMLWidget
from domsocket.event import Event
from domsocket.text_node import TextNode


class ConfigurationItem(HTMLWidget):

    def __init__(self, app_info):
        configuration_item_HTML_file_name = abspath(join('apps',
                                               'config',
                                               'widgets',
                                               'configuration_item.html'))

        with open(configuration_item_HTML_file_name, 'r') as configuration_item_HTML_file:
            super(ConfigurationItem, self).__init__(configuration_item_HTML_file.read(), None)

        self._app_info = app_info

    def dom_insert(self, name, parentNode, index):
        super(ConfigurationItem, self).dom_insert(name, parentNode, index)
        self._AppName.name = TextNode(self._app_info.app_name)
        self._URL.href = '/apps/' + self._app_info.app_name
        self._URL.name = TextNode(self._app_info.app_name)
        self._LoginControl += [TextNode('testuser')]
        self._Enabled.click = self.get_enabled_checkbox_event()
        if self._app_info.exposed:
            self._Enabled.checked = 'True'

    def get_enabled_checkbox_event(self):
        checkbox_event = Event()
        checkbox_event.add_observer(self, ConfigurationItem.on_enabled_checkbox_click)
        return checkbox_event

    def on_enabled_checkbox_click(self, theCheckBox, msg):
        self._app_info.toggle_enabled()
        if self._app_info.exposed:
            self._Enabled.checked = 'True'
        else:
            del self._Enabled.checked

