"""Copyright (c) 2015 TBillTech.  

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

from domsocket.node import Node
from domsocket.element import Element

class HTMLTag(Element):

    def __init__(self, tag, *args, **kw):
        super(HTMLTag, self).__init__(*args, **kw)
        self.tag = tag

    def on_create(self, name, parentNode, index):
        super(HTMLTag,self).on_create(name, parentNode, index)
        self.dom_insert_args()

    def dom_insert_args(self):
        if self._kw:
            self._set_arg(self._kw)
        for arg in self._args:
            self._set_arg(arg)

    def _set_arg(self, arg):
        try:
            self._set_kw_arg(arg)
        except AttributeError:
            self._set_not_kw_arg(arg)

    def _set_kw_arg(self, arg):
        for (key, value) in arg.items():
            setattr(self, key, value)

    def _set_not_kw_arg(self, arg):
        try:
            self._set_iterable_arg(arg)
        except TypeError:
            self._set_not_iterable_arg(arg)

    def _set_iterable_arg(self, arg):
        if isinstance(arg, Node):
            raise TypeError("Nodes must be added as whole units")
        for child in arg:
            self._set_arg(child)

    def _set_not_iterable_arg(self, arg):
        self += [arg]
