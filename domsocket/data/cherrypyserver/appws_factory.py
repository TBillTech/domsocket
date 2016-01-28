"""Copyright (c) 2015 TBillTech.  

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

import logging
from app_websocket import AppWebSocket


class AppWSFactory(object):

    """ AppWSFactory creates an app_websocket application to handle websocket requests
    """

    def __init__(self, app_name, server_id):
        self.app_name = app_name
        self.server_id = server_id

    def __call__(self, *args, **kw):
        return AppWebSocket(self.app_name, self.server_id, *args, **kw)
