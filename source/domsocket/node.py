"""Copyright (c) 2015 TBillTech.  All rights reserved."""

from operator import index

class Node(object):
    def set_element_attribute(self, element, name):
        self._set_nodeid(name)
        current_value = getattr(element, name, None)
        if current_value is None:
            element += [self]
        else:
            element[current_value] = [self]
        object.__setattr__(element, name, self)

    def del_element_attribute(self, element, name):
        del element[self]
        object.__delattr__(element, name)

