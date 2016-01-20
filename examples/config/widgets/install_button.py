"""Copyright (c) 2015 TBillTech.  

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

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
        
