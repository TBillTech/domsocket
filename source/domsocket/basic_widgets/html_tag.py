"""Copyright (c) 2015 TBillTech.  All rights reserved."""

from domsocket.node import Node
from domsocket.element import Element

class HTMLTag(Element):

    def __init__(self, tag, *args, **kw):
        super(HTMLTag, self).__init__(*args, **kw)
        object.__setattr__(self, 'tag', tag)

    def dom_insert(self, name, parentNode, index):
        if self.is_active_on_client():
            raise AttributeError() # pragma: no cover
        self.dom_insert_element(name, parentNode, index)
        return self

    def dom_insert_element(self, nodeid, parentNode, index):
        super(HTMLTag,self).dom_insert_element(self.tag, nodeid, parentNode, parentNode._get_ws(), index)

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