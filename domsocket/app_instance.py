"""Copyright (c) 2015 TBillTech.  

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

import json

class AppInstance(object):

    """ AppInstance bootstraps an app instance, and handles messaging to and
    from the app instance.
    The most important attribute members are:
    1) self.create_app function (which equals the App constructor)
    2) self.appid (which equals the top level div tag for the Gui application)
    """

    def __init__(self, ws_id, runner):
        self.ws_id = ws_id
        self.runner = runner
        self.create_app = runner.app_cls

    def recv(self, json_msg):
        try:
            self.app.process_client_msg(self, json_msg)
        except AttributeError:
            if json_msg['eventName'] == 'init':
                self.appid = json_msg['nodeid']:
                self.app = self.create_app()
                self.app.on_create(self.appid, self, child_index=None)
            else:
                raise  # pragma: no cover

    def send(self, message, f):
        self.runner.ws_send(self.ws_id, message)

    def closed(self, code, reason):
        self.app.client_has_closed_ws(code, reason)