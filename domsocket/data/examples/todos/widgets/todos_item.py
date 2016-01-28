"""Copyright (c) 2015 TBillTech.  

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

from domsocket.basic_widgets.html_widget import HTMLWidget
from domsocket.event import Event
from domsocket.text_node import TextNode


class TodosItem(HTMLWidget):

    def __init__(self, item_text):
        super(TodosItem, self).__init__()

        self._item_text = item_text

    def on_create(self, name, parentNode, index):
        super(TodosItem, self).on_create(name, parentNode, index)

        self._ItemInfo.item_text = TextNode(self._item_text)

