"""Copyright (c) 2015 TBillTech.  

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

import json
import traceback
import sys
from domsocket.element_error import ElementError

class AppInstance(object):

    """ AppInstance bootstraps an app instance, and handles messaging to and
    from the app instance.
    The most important attribute members are:
    1) self.create_app function (which equals the App constructor)
    2) self.appid (which equals the top level div tag for the Gui application)
    """

    def __init__(self, client, runner, message):
        self.client = client
        self.runner = runner
        self.create_app = runner.app_cls
        json_msg = json.loads(message)
        self.app_init(json_msg)

    def recv(self, message):
        if self.runner.verbose: print('recieving message "%s"' % (message,))
        json_msg = json.loads(message)
        try:
            self.app.process_client_msg(self, json_msg)
        except AttributeError: # pragma: no cover
            raise  # pragma: no cover
        except ElementError as e: # pragma: no cover
            fex = traceback.format_exc().splitlines()
            self.app_element_error(json_msg, e, fex) # pragma: no cover
            
    def send(self, message, f):
        if self.runner.verbose: print('sending message "%s"' % (message,))
        self.runner.ws_send(self.client, message)

    def closed(self, code, reason):
        self.app.client_has_closed_ws(code, reason)
        
    def close(self, reason):
        self.runner.app_close(self.client, reason) # pragma: no cover

    def app_init(self, json_msg):
        self.appid = json_msg['nodeid']
        self.app = self.create_app()
        self.app.on_create(self.appid, self, child_index=None)

    def app_element_error(self, json_msg, e, fex):
        try: # pragma: no cover
            self.app.process_element_error(json_msg, e) # pragma: no cover
        except AttributeError: # pragma: no cover
            print('App failed to process message "%s" due to %s:\n%s' % # pragma: no cover
                  (json_msg, e, '\n'.join(fex))) # pragma: no cover
