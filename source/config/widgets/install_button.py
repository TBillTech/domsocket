"""Copyright (c) 2015 TBillTech.  All rights reserved."""

from os.path import abspath
from os.path import join
import os
from domsocket.basic_widgets.html_widget import HTMLWidget
from domsocket.event import Event


class InstallButton(HTMLWidget):

    def __init__(self, install_handler):
        super(InstallButton, self).__init__()

        self._install_handler = install_handler
            
    def get_install_event(self):
        install_event = Event()
        install_event.add_observer(self, InstallButton.on_install_click)
        return install_event

    def on_install_click(self, theLoginButton, msg):
        self._install_handler.on_install()

    def on_create(self, name, parentNode, index):
        super(InstallButton, self).on_create(name, parentNode, index)
        self._Button.click = self.get_install_event()
        
