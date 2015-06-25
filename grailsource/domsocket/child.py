"""
Description:
  DOMSocket Child "Factory" class

The child "factory" class helps make the syntax of constructing a child node more convenient.  For example, it is most convenient
to be able to use syntax like:
new_button = Button('Click Me!')

In the above example, the Button class inherits from the Child class, and will construct an object inheriting from the Node class 
if and when it is assigned to either a property of a Node class, or in a call to append_child on a Node class.

"""

import json
from child_error import ChildError


class Child(object):

    """The Child object is a helper object to allow assignment syntax of child nodes to Node property variables.  This is to
    support thinking of Child objects as widget objects that MUST have a parent in the DOM, and keeping the id of the child object equal 
    to the name of the parent Node property.  For example, if my_node is an Node object currently in the DOM, then a child Button could be 
    assigned to the application using syntax like this:
        my_app.clickme_button = Child(Button, text_param='Click Me!')
    The clickme_button property of my_app need not even be defined before executing this code, and the new child Button Node will use the
    property name 'clickme_button' to construct the child Button Node id value.
    """

    def __init__(self, node_class, *args, **kw):
        object.__setattr__(self, 'node_class', node_class)
        object.__setattr__(self, 'args', args)
        object.__setattr__(self, 'kw', kw)

    def create_node(self, name, parent_node, index):
        return self.node_class(name, parent_node, parent_node.get_w_s(), index, *self.args, **self.kw)

    def __setattr__(self, name, value):
        """
        Child Node "Factories" which inherit from Child are not allowed to set public user properties.  This is to prevent unexpected
        behavior when accidentally assigning properties to the Child Node "Factory" instead of assigning properties to
        a Node.  Assigning properties to a Node is the intended behavior.  A Node is constructed only after one of two options is taken:
        1) Assign the Child object to a property of a Node, for example:
            my_widget_node.child_property = Button('Click Me!')
        2) call the append_child method of a Node, passing the Child object as the argument, for example:
            my_widget_node.append_child(Button('Click Me!'))
        """
        raise ChildError(
            'Child Node Factories do not permit setting properties. See the __setattr__ doc string in child.py')  # pragma: no cover
