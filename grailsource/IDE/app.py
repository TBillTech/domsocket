"""Copyright (c) 2015 TBillTech.  All rights reserved."""

#from domsocket.event import Event
#from basic_widgets.button import Button
from basic_widgets.paragraph import Paragraph
#from basic_widgets.text import Text
from domsocket.element import Element
# Do an import of the module to ensure picking up the quick options (for
# the Storm db)
import ds_controls.ca_login_dialog
from ds_controls.ca_login_dialog import LoginDialog
#from ds_controls.ca_instrument_list import InstrumentList
#from ds_controls.ca_packet_sample_summary import PacketSampleSummary
#from ds_controls.ca_packet_sample_decode import PacketSampleDecode


class App(Element):

    def __init__(self, nodeid, parent_node, ws):
        super(App, self).__init__('div', nodeid, parent_node, ws, index=None)

        self.login = LoginDialog(App.authenticated)

    def remove_listeners(self):
        # This gets called by the websocket when the app goes away.
        # It is very important to call remove_listeners on all children that listen for
        # 0mq events so that the 0mq even handlers will not try to send dead
        # apps information.
        try:
            pass
            # self.packet_sample_summary.remove_listeners()
        except Exception:
            pass

    def authenticated(self):
        del self.login

        #self.instruments = InstrumentList()
        #self.packet_sample_summary = PacketSampleSummary()
        #self.packet_sample_decode = PacketSampleDecode()
