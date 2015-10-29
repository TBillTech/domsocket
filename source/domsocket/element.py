"""Copyright (c) 2015 TBillTech.  All rights reserved.

Description:
  domsocket base Element class, Text class, and EventCapture class implemented for python.

domsocket is a pattern designed to simplify dealing with GUI application client/server interactions.  
Instead of defining back-end services and painstakingly modifying client/server interfaces whenever code changes are needed, 
the domsocket pattern keeps a model of the GUI tree and automatically updates individual attributes of elements in the tree 
as they change.

Normally, a domsocket application starts up and bootstraps without even a div section in the web page.  
Typically, the application Element is a div tag, and appends itself to the end of the body tree.  
However, if the correct div tag already exists with the correct application id, 
the domsocket application will transparently use it.

The Element class is the first pillar of the domsocket pattern.  
The Element class is used to construct the GUI and proper DOM elements, and is also used to subsequently identify and
interact with the DOM elements.  The Element class atomatically intercepts attempts to set member variables of 
the Element class, and forwards changes across the web socket to the GUI DOM element attribute that corresponds with 
the member variable name that was modified.

Forwarded changes include controlling children elements, attributes, and event handlers.

Event handling is controlled by the second pillar of the domsocket pattern:  The EventCapture object.  
The EventCapture object sets up a corresponding event listener on the corresponding DOM element of the Element 
attribute where the EventCapture object is assigned.  This allows for seamlessly and transparently setting up and 
triggering event handlers from within the server side code without needing to create explicit event handling within the GUI.

Putting it all together, the domsocket pattern permits the programmer to write a web application that semantically is a simple
GUI application.  With domsocket, the programmer is not forced to implement communication code for interfacing the back end and the
front end pieces of the application across the IP network.  The communication link is abstracted away and does not explicitly appear
in a domsocket application.

"""

import json
from messages.attach_event_message import AttachEventMessage
from messages.set_attribute_message import SetAttributeMessage
from messages.remove_attribute_message import RemoveAttributeMessage
from messages.detach_event_message import DetachEventMessage
from messages.remove_message import RemoveMessage
from messages.remove_child_message import RemoveChildMessage
from messages.insert_child_message import InsertChildMessage
from messages.focus_message import FocusMessage
from event import Event
from text_node import TextNode
from node import Node
from operator import index
import sys
import traceback

import logging
from element_error import ElementError
from messages.message_error import MessageError

#messageLog = open('messageLog.txt', 'w+')

class Element(Node):
    """The Element class is the basis for all domsocket Gui elements. 

    The Element class automatically tries to mirror any property update in the GUI DOM.  
    The exception to this rule is private variables with leading underscores, which are never mirrored in the DOM.

    id, tag, and parentNode are considered immutable once the Element exists on the client, and may not be modified.
    In addition, these three fields are handled specially when the Element gets shown on the GUI, and are considered
    fully mirrored.  (This is why the parentNode element is Camel case as opposed to normal python PEP 8).
    """

    immutable_names = set(['tag', 'id', 'parentNode', '_ws', '_active_on_client', '_children'])

    def __init__(self, *args, **kw):
        object.__setattr__(self, '_args', args)
        object.__setattr__(self, '_kw', kw)
        object.__setattr__(self, '_children', list())
        object.__setattr__(self, '_nodeid', None)

    def dom_insert(self, nodetag, nodeid, parentNode, ws, child_index):
        if self.is_active_on_client():
            raise ElementError('Cannot make element active because it is already active') # pragma: no cover
       
        object.__setattr__(self, 'tag', nodetag)
        object.__setattr__(self, '_children', list())
        object.__setattr__(self, '_ws', ws)
        object.__setattr__(self, 'parentNode', parentNode)
        object.__setattr__(self, 'id', self._element_get_id(nodeid))
        object.__setattr__(self, '_serial_no',  0)

        msg = InsertChildMessage(self.parentNode, child_index, self)
        self._send_msg_to_client(msg)

        object.__setattr__(self, '_active_on_client',  True)

    def is_active_on_client(self):
        return getattr(self, '_active_on_client', False)

    def __setattr__(self, name, value):
        if self._is_underscored_name(name):
            return object.__setattr__(self, name, value)

        if self._value_is_valid(name, value):
            try:
                value.set_element_attribute(self, name)
            except AttributeError:
                self._set_named_attribute(name, value)

    def _value_is_valid(self, name, value):
        if value == None:
            raise ElementError('attributes and children may not be set to None.  Use del to remove them.')
        current_value = getattr(self, name, None) 
        if current_value == value:
            return False
        return True

    def _set_named_attribute(self, name, value):
        msg = SetAttributeMessage(self, name, value)
        self._send_msg_to_client(msg)
        object.__setattr__(self, name, value)

    def __delattr__(self, name):
        if self._is_underscored_name(name):
            return object.__delattr__(self, name)

        value = getattr(self, name)
        try:
            value.del_element_attribute(self, name)
        except AttributeError:
            self._del_named_attribute(name)

    def _del_named_attribute(self, name):
        msg = RemoveAttributeMessage(self, name)
        self._send_msg_to_client(msg)
        object.__delattr__(self, name)

    def _is_underscored_name(self, name):
        if name in self.immutable_names:
            raise ElementError('%s is immutable, and may not be deleted' % (name,))
        if name[0] == '_':
            return True
        if not self.is_active_on_client():
            raise ElementError('Attributes, children and events may not be set or deleted until '\
                               'the element is active on the client.') # pragma: no cover 
        return False

    def _set_nodeid(self, name):
        self._nodeid = name

    def _remove_element_from_client(self):
        if self.is_active_on_client():
            self._stop_observations()
            msg = RemoveMessage(self)
            self._send_msg_to_client(msg)
        object.__setattr__(self, '_active_on_client', False)            

    def __len__(self):
        return len(self._children)

    def __getitem__(self, child):
        return self._children[child] # pragma: no cover

    def __iadd__(self, child_node_list): 
        for child_node in child_node_list:
            self._element_append_child_node(child_node)
        return self

    def _element_append_child_node(self, child_node):
        self._child_node_dom_insert(child_node, None)
        self._children.append(child_node)
        self._serial_no += 1

    def _child_node_dom_insert(self, child_node, first_index):
        try:
            child_node.dom_insert(str(self._serial_no), self, first_index)
        except AttributeError, e: # pragma: no cover
            if hasattr(child_node, 'dom_insert'): # pragma: no cover
                type_, value_, traceback_ = sys.exc_info() # pragma: no cover
                raise ElementError('%s in %s.dom_insert: %s' % \
                                   (repr(e), repr(child_node), traceback.format_tb(traceback_))) # pragma: no cover
            else: # pragma: no cover
                raise ElementError('%s does not possess dom_insert' % (repr(child_node),)) # pragma: no cover

    def __delitem__(self, sliceobj):
        self._remove_slice_from_client(sliceobj)
            
        del self._children[sliceobj]

    def __setitem__(self, sliceobj, child_list):
        if isinstance(sliceobj, Node):
            sliceobj = index(sliceobj)

        self._remove_slice_from_client(sliceobj)
        self._add_list_to_client(sliceobj, child_list)
        if isinstance(sliceobj, int):
            self._children[sliceobj:sliceobj+1] = child_list
        else:
            self._children[sliceobj] = child_list
            
    def _remove_slice_from_client(self, sliceobj):
        slice_list = self._get_slice_children_list(sliceobj)
        for child_node in reversed(slice_list):
            child_node._remove_element_from_client()

    def _add_list_to_client(self, first_index, child_list):
        if not isinstance(first_index, int):
            first_index = self._get_first_index_of_slice(first_index)
        for child_node in child_list:
            self._child_node_dom_insert(child_node, first_index)
            first_index += 1
            self._serial_no += 1

    def _get_first_index_of_slice(self, sliceobj):
        try:
            return index(self._get_slice_children_list(sliceobj)[0])
        except IndexError:
            return 0

    def _get_slice_children_list(self, sliceobj):
        slice_list = self._children[sliceobj]
        if isinstance(slice_list, Node):
            return [slice_list]
        return slice_list

    def __index__(self):
        return self.parentNode._get_index_of_child(self)

    def _element_get_id(self, nodeid):
        if self._nodeid:
            nodeid = self._nodeid
        try:
            return self.parentNode.id + '.' + nodeid
        except AttributeError:
            return nodeid

    def _stop_observations(self):
        for (key, value) in self.__dict__.items():
            if isinstance(value, Event):
                delattr(self, key)
        for child in self._children:
            child._stop_observations()

    def _get_index_of_child(self, child_node):
        index = 0
        for other_child in self._children:
            if child_node == other_child:
                return index
            index += 1
        raise IndexError('Child Node not found in _children list') # pragma: no cover

    def _send_msg_to_client(self, msg):
        #messageLog.write(str(msg.msg_dict)+'\n')
        self._get_ws().send(msg.jsonstring(), False)

    def get_element_by_id(self, nodeid):
        if nodeid == self.id:
            return self
        if nodeid[:len(self.id)] == self.id:
            for child in self._children:
                try:
                    return child.get_element_by_id(nodeid)
                except ElementError, AttributeError:
                    continue
        raise ElementError('nodeid %s could not be found' % (nodeid,))

    def document_get_element_by_id(self, nodeid):
        return self._get_ws().app.get_element_by_id(nodeid)

    def _get_ws(self):
        return self._ws

    def process_client_msg(self, ws, msg):
        if msg['type'] == 'event':
            self._process_client_event(msg)
        elif msg['type'] == 'exception': # pragma: no cover
            self._process_client_exception(msg)
        else: # pragma: no cover
            raise MessageError('Event type %s not defined' % (msg['type'])) # pragma: no cover

    def _process_client_event(self, msg):
        node = self.get_element_by_id(msg['nodeid'])
        onevent = getattr(node, msg['eventName'], None)
        if not onevent:
            raise MessageError('Event handler %s is not defined in node class %s with nodeid %s'\
                               % (msg['eventName'], node.__class__.__name__, msg['nodeid'])) # pragma: no cover
        onevent(msg)
        
    def _process_client_exception(self, msg):
        raise MessageError('Exception raised from GUI: %s\noriginal message: %s\n GUI Stack: %s'\
                           % (msg['message'], msg['original'], msg['stack'])) # pragma: no cover

    def client_has_closed_ws(self, code, reason):
        pass

    def set_focus(self):
        msg = FocusMessage(self)
        self._send_msg_to_client(msg)

    def find_parent(self, cls):
        if not self.parentNode or not hasattr(self.parentNode, 'find_parent'):
            raise ElementError('No parent Node of class %s found' % (repr(cls))) #pragma: no cover
        if isinstance(self.parentNode, cls):
            return self.parentNode
        return self.parentNode.find_parent(cls)

    def find_handler(self, handler_name):
        return getattr(self, handler_name, 
                       self.find_parent_handler(handler_name))

    def find_parent_handler(self, handler_name):
        if not self.parentNode or not hasattr(self.parentNode, 'find_parent_handler'):
            raise ElementError('No parent Node of class %s found' % (repr(cls))) #pragma: no cover
        if hasattr(self.parentNode, handler_name):
            return getattr(self.parentNode, handler_name)
        return self.parentNode.find_parent_handler(handler_name)

    def getattr_class(self):
        return getattr(self, 'class', '')

    def setattr_class(self, value):
        setattr(self, 'class', value)
