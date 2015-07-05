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
from event import Event
from text_node import TextNode
from node import Node

import logging
from element_error import ElementError
from messages.message_error import MessageError


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
        object.__setattr__(self, '_active_on_client', False)
        object.__setattr__(self, '_children', list())

    def show_element(self, nodetag, nodeid, parentNode, ws, index):
        object.__setattr__(self, '_active_on_client', False)
        object.__setattr__(self, 'tag', nodetag)
        object.__setattr__(self, '_children', list())
        object.__setattr__(self, '_ws', ws)
        object.__setattr__(self, 'parentNode', parentNode)
        object.__setattr__(self, 'id', self._element_get_id(nodeid))
        object.__setattr__(self, '_append_count',  0)

        msg = InsertChildMessage(self.parentNode, index, self)
        self.send_msg(msg)

        object.__setattr__(self, '_active_on_client',  True)

    def __setattr__(self, name, value):
        if value == None:
            raise ElementError('attributes and children may not be set to None.  Use del to remove them.')
        if name in self.immutable_names:
            raise ElementError('%s is immutable and may not be changed' % (name,))

        if name[0] == '_':
            object.__setattr__(self, name, value)
            return 

        if not self.is_active_on_client():
            raise ElementError('Attributes, children and events may not be set until the element is active on the client.') # pragma: no cover 
        try:
            current_value = getattr(self, name)
            try:
                index = self.child_index(current_value)
            except ValueError:
                index = len(self._children)
            if current_value == value:
                return
            if isinstance(current_value, TextNode) and isinstance(value, str):
                current_value.text = value
                return
            delattr(self, name)
        except AttributeError:
            index = len(self._children)

        if isinstance(value, Event):
            msg = AttachEventMessage(self, name, value.arguments)
            value.owner_node = self
            value.name = name
        elif isinstance(value, Node):
            value = self.set_child(index, value, name)
            msg = None
        else:
            msg = SetAttributeMessage(self, name, value)
        self.send_msg(msg)
        object.__setattr__(self, name, value)

    def __delattr__(self, name):
        if name[0] == '_':
            object.__delattr__(self, name)
            return
        value = getattr(self, name)
        if name in self.immutable_names:
            raise ElementError('%s is immutable, and may not be deleted' % (name,))
        elif isinstance(value, Event):
            if len(value):
                raise ElementError('Trying to delete an event = %s from the node, '\
                                   'but there are still listeners attached.' % (name,))
            msg = DetachEventMessage(self, name)
        elif isinstance(value, Node):
            self.remove_child(value)
            msg = None
        else:
            msg = RemoveAttributeMessage(self, name)
        self.send_msg(msg)
        object.__delattr__(self, name)

    def __len__(self):
        return len(self._children)

    def get_child(self, index):
        return self._children[index]

    def append_child(self, child_node):
        try:
            child_node = child_node.create_node(
                str(self._append_count), self, None)
        except AttributeError:
            if isinstance(child_node, str):
                value = TextNode(text=child_node)
                child_node = value.create_node(
                    str(self._append_count), self, None)
        self._children.append(child_node)
        # this is not a real count, but just an anti-name collision value
        self._append_count += 1
        return child_node

    def remove_child(self, child_node):
        try:
            index = self._children.index(child_node)
        except ValueError:
            index = child_node
            child_node = self._children[index]
        self._children[index]._stop_observations()
        msg = RemoveMessage(child_node)
        del self._children[index]
        self.send_msg(msg)

    def insert_child(self, index, child_node):
        try:
            index = self.child_index(index)
        except ValueError:
            pass
        try:
            child_node = child_node.create_node(str(self._append_count), self, index)
        except AttributeError:
            pass
        self._children.insert(index, child_node)
        self._append_count += 1
        return child_node

    def set_child(self, index, child_node, name):
        if index == len(self._children):
            return self.append_child(child_node.create_node(name, self, index))
        if index > len(self._children):
            raise ElementError('Cannot set child at index = %s, since that would create a gap in the '\
                               'child array of len(children)=%s' % (index, len(self._children))) # pragma: no cover

        former_child = self.get_child(index)

        self.remove_child(former_child)
        child_node = self.insert_child(
            index, child_node.create_node(name, self, index))
        return child_node

    def is_active_on_client(self):
        return self._active_on_client

    def _element_get_id(self, nodeid):
        try:
            return self.parentNode.id + '.' + nodeid
        except AttributeError:
            return nodeid

    def _stop_observations(self):
        for child in self._children:
            child._stop_observations()

    def child_index(self, child_node):
        return self._children.index(child_node)

    def send_msg(self, msg):
        if not msg:
            return
        self._ws.send(msg.jsonstring(), False)

    def get_element_by_id(self, nodeid):
        if nodeid == self.id:
            return self
        if nodeid[:len(self.id)] == self.id:
            for child in self._children:
                try:
                    return child.get_element_by_id(nodeid)
                except:
                    continue
        raise ElementError('nodeid %s could not be found' % (nodeid,))

    def document_get_element_by_id(self, nodeid):
        return self.get_w_s().app.get_element_by_id(nodeid)

    def get_w_s(self):
        return self._ws

    def process_msg(self, ws, msg):
        if msg['type'] == 'event':
            node = self.get_element_by_id(msg['nodeid'])
            try:
                onevent = getattr(node, msg['eventName'])
            except AttributeError: # pragma: no cover
                raise MessageError('Event handler %s is not defined in node class %s with nodeid %s'\
                                   % (msg['eventName'], node.__class__.__name__, msg['nodeid'])) # pragma: no cover
            onevent(msg)
        elif msg['type'] == 'exception': # pragma: no cover
            raise MessageError('Exception raised from GUI: %s\noriginal message: %s\n GUI Stack: %s'\
                               % (msg['message'], msg['original'], msg['stack'])) # pragma: no cover
        else: # pragma: no cover
            raise MessageError('Event type %s not defined' % (msg['type'])) # pragma: no cover

    def closed(self, code, reason):
        pass
