"""Copyright (c) 2015 TBillTech.  

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

from os.path import abspath
from os.path import join
import os
from domsocket.basic_widgets.html_widget import HTMLWidget


class LoginButton(HTMLWidget):

    _widget_html_id = 'loginButton'
    _html_source_filename = 'login_dialog.html'

    def __init__(self):
        super(LoginButton, self).__init__()
