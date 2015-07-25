"""Copyright (c) 2015 TBillTech.  All rights reserved."""

from os.path import abspath
from os.path import join
import os
from domsocket.basic_widgets.html_widget import HTMLWidget
from domsocket.event import Event


class InstallButton(HTMLWidget):

    def __init__(self, install_handler):
        install_button_HTML_file_name = abspath(join('apps',
                                               'config',
                                               'widgets',
                                               'install_button.html'))

        with open(install_button_HTML_file_name, 'r') as install_button_HTML_file:
            super(InstallButton, self).__init__(install_button_HTML_file.read(), None)

        self._install_handler = install_handler
            
    def get_install_event(self):
        install_event = Event()
        install_event.add_observer(self, InstallButton.on_install_click)
        return install_event

    def on_install_click(self, theLoginButton, msg):
        self._install_handler.on_install()

    def dom_insert(self, name, parentNode, index):
        super(InstallButton, self).dom_insert(name, parentNode, index)
        self._Button.click = self.get_install_event()
        
