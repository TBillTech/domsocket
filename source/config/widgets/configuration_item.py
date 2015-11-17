"""Copyright (c) 2015 TBillTech.  All rights reserved."""

from os.path import abspath
from os.path import join
import os
from domsocket.basic_widgets.html_widget import HTMLWidget
from domsocket.event import Event
from domsocket.text_node import TextNode


class ConfigurationItem(HTMLWidget):

    def __init__(self, app_info):
        super(ConfigurationItem, self).__init__()

        self._app_info = app_info

    def on_create(self, name, parentNode, index):
        super(ConfigurationItem, self).on_create(name, parentNode, index)
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

