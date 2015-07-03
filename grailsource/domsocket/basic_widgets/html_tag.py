"""Copyright (c) 2015 TBillTech.  All rights reserved."""

from domsocket.element import Element

class HTMLTag(Element):

    def __init__(self, tag, *args, **kw):
        super(HTMLTag, self).__init__(tag, *args, **kw)
        object.__setattr__(self, '_node_class', HTMLTag)

    def called_init(self, nodeid, parent_node, ws, index, *args, **kw):
        Element.called_init(self, self.tag, nodeid, parent_node, ws, index)

        self._set_arg(kw)
        for arg in args:
            self._set_arg(arg)

    def _set_arg(self, arg):
        if isinstance(arg, str):
            self._set_not_iterable_arg(arg)
            return
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
        for child in arg:
            self._set_arg(child)

    def _set_not_iterable_arg(self, arg):
        self.append_child(arg)

