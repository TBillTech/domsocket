"""Copyright (c) 2015 TBillTech.  All rights reserved."""

from os.path import abspath
from os.path import join
import os
from domsocket.basic_widgets.html_widget import HTMLWidget
from domsocket.event import Event
from configuration_item import ConfigurationItem
from install_button import InstallButton
from domsocket.file_finder import get_all_app_info


class AppInfoLike(object):
    def __init__(self, app_name, exposed):
        self.app_name = app_name
        self.exposed = exposed

class ConfigurationList(HTMLWidget):

    def __init__(self):
        super(ConfigurationList, self).__init__()

    def on_create(self, name, parentNode, index):
        super(ConfigurationList, self).on_create(name, parentNode, index)
        self.insert_apps()
        self.append_install_button()

    def insert_apps(self):
        for app_info in get_all_app_info():
            self += [ConfigurationItem(app_info)]

    def append_install_button(self):
        self.install_button = InstallButton(install_handler=self)

    def on_install(self):
        del self.install_button
        self += [ConfigurationItem(AppInfoLike('bogus',True))]
        self.append_install_button()
        
