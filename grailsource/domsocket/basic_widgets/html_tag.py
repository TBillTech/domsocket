"""Copyright (c) 2015 TBillTech.  All rights reserved."""

from domsocket.child import Child


class HTMLTag(Child):

    def __init__(self, tag, *args, **kw):
        from domsocket.node import Node

        class HTMLTagNode(Node):

            def __init__(self, nodeid, parent_node, ws, index, *args, **kw):
                Node.__init__(self, tag, nodeid, parent_node, ws, index)

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

        super(HTMLTag, self).__init__(HTMLTagNode, *args, **kw)
