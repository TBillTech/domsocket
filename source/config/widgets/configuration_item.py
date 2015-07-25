"""Copyright (c) 2015 TBillTech.  All rights reserved."""

from os.path import abspath
from os.path import join
import os
from domsocket.basic_widgets.html_widget import HTMLWidget
from domsocket.event import Event


class ConfigurationItem(HTMLWidget):

    def __init__(self):
        configuration_item_HTML_file_name = abspath(join('apps',
                                               'config',
                                               'widgets',
                                               'configuration_item.html'))

        with open(configuration_item_HTML_file_name, 'r') as configuration_item_HTML_file:
            super(ConfigurationItem, self).__init__(configuration_item_HTML_file.read(), None)

