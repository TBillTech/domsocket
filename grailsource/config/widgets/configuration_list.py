"""Copyright (c) 2015 TBillTech.  All rights reserved."""

from os.path import abspath
from os.path import join
import os
from domsocket.basic_widgets.html_widget import HTMLWidget
from domsocket.event import Event
from configuration_item import ConfigurationItem
from install_button import InstallButton


class ConfigurationList(HTMLWidget):

    def __init__(self):
        configuration_list_HTML_file_name = abspath(join('apps',
                                               'config',
                                               'widgets',
                                               'configuration_list.html'))

        with open(configuration_list_HTML_file_name, 'r') as configuration_list_HTML_file:
            super(ConfigurationList, self).__init__(configuration_list_HTML_file.read(), None)

    def dom_insert(self, name, parentNode, index):
        super(ConfigurationList, self).dom_insert(name, parentNode, index)
        self.insert_apps()
        self.append_install_button()

    def insert_apps(self):
        self += [ConfigurationItem()]

    def append_install_button(self):
        self.install_button = InstallButton(install_handler=self)

    def on_install(self):
        #del self.install_button._Button.click
        del self.install_button
        self += [ConfigurationItem()]
        self.append_install_button()
        
