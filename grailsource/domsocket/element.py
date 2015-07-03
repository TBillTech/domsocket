"""Copyright (c) 2015 TBillTech.  All rights reserved.

Description:
  domsocket base Element class, Text class, and EventCapture class implemented for python.

domsocket is a pattern designed to simplify dealing with GUI application client/server interactions.  
Instead of defining back-end services and painstakingly modifying client/server interfaces whenever code changes are needed, 
the domsocket pattern keeps a model of the GUI tree and automatically updates individual attributes of elements in the tree as they change.

Normally, a domsocket application starts up and bootstraps without even a div section in the web page.  Typically, the application Element is a
div tag, and appends itself to the end of the body tree.  However, if the correct div tag already exists with the correct application
id, the domsocket application will transparently use it.

The Element class is the first pillar of the domsocket pattern.  The Element class constructor requires a node tag, the node id, and the parent node.
These values are used to construct the tag in the GUI as the child of the proper DOM element, and used to subsequencly identify and
interact with the new DOM element.  The Element class atomatically intercepts attempts to set member variables of the Element class, 
and forwards changes across the web socket to the GUI DOM element attribute that corresponds with the member variable name that was modified.

Forwarded changes include adding children to the element, and adding event handlers.

Event handling is controlled by the second pillar of the domsocket pattern:  The EventCapture object.  The EventCapture object sets up a
corresponding event listener on the corresponding DOM element of the Element attribute where the EventCapture object is assigned.  This
allows for seamlessly and transparently setting up and triggering event handlers from within the server side code without needing to
create explicit event handling within the GUI.

Putting it all together, the domsocket pattern permits the programmer to write a web application that semantically is a single simple
GUI application.  With domsocket, the programmer is not forced to implement communication code for interfacing the back end and the
front end pieces of the application across the IP network.  The communication link is abstracted away and does not explicitly appear
in a domsocket application.


"""

import json
from messages.append_child_message import AppendChildMessage
from messages.attach_event_message import AttachEventMessage
from messages.set_attribute_message import SetAttributeMessage
from messages.remove_attribute_message import RemoveAttributeMessage
from messages.detach_event_message import DetachEventMessage
from messages.remove_message import RemoveMessage
from messages.remove_child_message import RemoveChildMessage
from messages.set_child_message import SetChildMessage
from messages.insert_child_message import InsertChildMessage
from event import Event
from text_node import TextNode
from node import Node

import logging
from element_error import ElementError
from messages.message_error import MessageError


class Element(Node):
    immutable_names = set(['tag', 'id', 'parent_node', '_ws', '_active_on_client', '_children'])

    """The Element class is the basis for all domsocket Gui elements.  The Element class constructor requires a tag, a nodeid, and the parent_node.
    These arguments allow the Element constructor to immediately add the mirror representation of the object into the DOM as an element
    with the proper tag and as a child of the proper parent.  The id permits the Element class to find it's mirror element and modify/update
    it as the program executes.

    The Element class automatically tries to mirror any property update in the GUI DOM.  The exception to this rule is private variables
    with leading underscores, which are never mirrored in the DOM.

    The Element class tree heiarchy can efficiently find sub nodes by comparing the id fields of the nodes.  In fact, any Element can easily
    locate and obtain a reference to any other Element via the other Element's id using the document_get_element_by_id method.
    """
    def __init__(self, node_class, *args, **kw):
        object.__setattr__(self, '_node_class', node_class)
        object.__setattr__(self, '_args', args)
        object.__setattr__(self, '_kw', kw)
        object.__setattr__(self, '_active_on_client', False)
        object.__setattr__(self, '_children', list())

    def create_node(self, name, parent_node, index):
        if self.is_active_on_client():
            raise AttributeError()
        new_class = self._node_class(self._node_class, *self._args, **self._kw)
        new_class.called_init(name, parent_node, parent_node.get_w_s(), index, *self._args, **self._kw)
        return new_class

    def called_init(self, nodetag, nodeid, parent_node, ws, index):
        object.__setattr__(self, '_active_on_client', False)
        object.__setattr__(self, 'tag', nodetag)
        object.__setattr__(self, '_children', list())
        object.__setattr__(self, '_ws', ws)
        object.__setattr__(self, 'parent_node', parent_node)
        if self.parent_node == None:
            object.__setattr__(self, 'id', nodeid)
        else:
            object.__setattr__(self, 'id', self.parent_node.id + '.' + nodeid)
        if index == None:
            msg = AppendChildMessage(self.parent_node, self)
        else:
            msg = InsertChildMessage(self.parent_node, index, self)
        self.send_msg(msg)

        self._append_count = 0
        object.__setattr__(self, '_active_on_client',  True)

    def is_active_on_client(self):
        return self._active_on_client

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

    def __del__(self):
        self.stop_observations()

    def stop_observations(self):
        for child in self._children:
            child.stop_observations()

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
        msg = RemoveMessage(child_node)
        del self._children[index]
        self.send_msg(msg)

    def insert_child(self, index, child_node):
        try:
            index = self.child_index(index)
        except ValueError:
            pass
        try:
            child_node = child_node.create_node(
                str(self._append_count), self, index)
        except AttributeError as e:
            if isinstance(child_node, str):
                value = TextNode(text=child_node)
                child_node = value.create_node(
                    str(self._append_count), self, index)
        self._children.insert(index, child_node)
        # this is not a real count, but just an anti-name collision value
        self._append_count += 1
        return child_node

    def __len__(self):
        return len(self._children)

    def child_count(self):
        return len(self)

    def get_child(self, index):
        return self._children[index]

    def child_index(self, child_node):
        return self._children.index(child_node)

    def set_child(self, index, child_node, name):
        if index == None:
            index = len(self._children)
        if index == len(self._children):
            return self.append_child(child_node.create_node(name, self, index))
        if index > len(self._children):
            raise ElementError('Cannot set child at index = %s, since that would create a gap in the child array of len(children)=%s' % (
                index, len(self._children)))

        try:
            former_child = self.get_child(index)
        except IndexError:
            former_child = index
            index = self.child_index(former_child)

        if isinstance(child_node, str) and isinstance(former_child, TextNode):
            former_child.text = child_node
            return former_child

        self.remove_child(former_child)
        child_node = self.insert_child(
            index, child_node.create_node(name, self, index))
        return child_node

    def send_msg(self, msg):
        if not msg:
            return
        self._ws.send(msg.jsonstring(), False)

    def get_element_by_id(self, nodeid):
        try:
            if nodeid == self.id:
                return self
        except:
            pass
        if nodeid[:len(self.id)] == self.id:
            for child in self._children:
                try:
                    return child.get_element_by_id(nodeid)
                except:
                    continue
        raise ElementError('nodeid could not be found')

    def get_element_by_partial_id(self, partial_nodeid):
        try:
            if nodeid[len(self.id) - len(partial_nodeid):] == partial_nodeid:
                return self
        except:
            pass
        for child in self._children:
            try:
                return child.get_element_by_partial_id(partial_nodeid)
            except:
                continue
        raise ElementError('partial nodeid could not be found')

    def get_element_by_text(self, text):
        try:
            if self.text == text:
                return self
        except:
            pass
        for child in self._children:
            try:
                return child.get_element_by_text(text)
            except:
                continue
        raise ElementError('partial nodeid could not be found')

    def document_get_element_by_id(self, nodeid):
        return self.get_w_s().app.get_element_by_id(nodeid)

    def get_w_s(self):
        return self._ws

    def process_msg(self, ws, msg):
        if msg['type'] == 'event':
            node = self.get_element_by_id(msg['nodeid'])
            if not node:
                raise MessageError(
                    'node with nodeid = %s could not be found' % (msg['nodeid'],))
            try:
                onevent = getattr(node, msg['eventName'])
            except AttributeError:
                raise MessageError('Event handler %s is not defined in node class %s with nodeid %s' % (
                    msg['eventName'], node.__class__.__name__, msg['nodeid']))
            onevent(msg)
        elif msg['type'] == 'exception':
            #self.logger.error('Exception raise from GUI: %s' % (msg))
            #self.logger.error('Exception raised from GUI: %s\n_original message: %s' % (msg['err'],msg['rootmessage']))
            raise MessageError('Exception raised from GUI: %s\n_original message: %s\n_g_u_i Stack: %s' % (
                msg['message'], msg['original'], msg['stack']))
        else:
            raise MessageError('Event type %s not defined' % (msg['type']))

    def closed(self, code, reason):
        pass
