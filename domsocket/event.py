"""Copyright (c) 2015 TBillTech.  

  This Source Code Form is subject to the terms of the Mozilla Public
  License, v. 2.0. If a copy of the MPL was not distributed with this
  file, You can obtain one at http://mozilla.org/MPL/2.0/.

See more information on the node class in the doc of node.py.

Event handling is controlled by the second pillar of the REDOWL pattern:  The EventCapture object.  The EventCapture object sets up a
corresponding event observer on the corresponding DOM element of the Element attribute where the EventCapture object is assigned.  This
allows for seamlessly and transparently setting up and triggering event handlers from within the server side code without needing to
create explicit event handling within the GUI.

Putting it all together, the REDOWL pattern permits the programmer to write a web application that semantically is a single simple
GUI application.  With REDOWL, the programmer is not forced to implement communication code for interfacing the back end and the
front end pieces of the application across the IP network.  The communication link is abstracted away and does not explicitly appear
in a REDOWL application.

"""

from messages.update_event_message import UpdateEventMessage
from messages.attach_event_message import AttachEventMessage
from messages.detach_event_message import DetachEventMessage
from element_error import ElementError
import json
import logging


class Event(object):

    """ The Event class encapsulates handling GUI events.  Whenever it is desireable to trap and act on an event that occurs
    in the web GUI, a new Event object should be created and assigned to the variable of the Element with the name that exactly
    corresponds to the name of the event in the GUI.  

    Here is an example: suppose we have a button Element assigned to the local variable 'my_button'.  
    The click event in the GUI for this button could be captured by this code:
        my_button.click = Event()
    Consequently, whenever there is a click of the button in the GUI, the __call__ method of the Event class assigned 
    in the previous line to my_button.click will be called.

    The __call__ method of the Event class iterates through the observers that have registered with the Event class, 
    and calls the observer back using the observer's callback method.  A observer registers/deregisters with the Event class 
    by using the add_observer and remove_observer methods.

    Here is an example, again using the my_button Element: suppose we have a SpecialList Element called 'my_special_list' 
    that wants to get a callback method callback when my_button is clicked in the GUI.  For example, suppose the 
    SpecialList has an on_my_button_click method:

    class SpecialList(Element):
        ...
        def on_my_button_click(self, my_button, msg):
            #Do something useful with self and my_button, and optionally access the info in msg

    Now, the my_special_list Element can register with the my_button.click Event object like so:
        my_button.click.add_observer(my_special_list, on_my_button_click)
    Consequently, whenever there is a click of the button in the GUI, the on_my_button_click method will get called up.

    The msg passed into the callback has the following properties:
    msg.type # This always == "event"
    msg.nodeid # This is the id of the Element that initiated the event
    msg.event_name # This is the name of the event property, such as 'click' from the my_button example above
    msg.event # This is a JSON -> python loads version of the actual javascript event
    msg.attribute_args # This is an array of data structures with additional information passed back with the event handler

    An element from the attribute_args data structure has the following elements:
    attribute_arg.id # This is the id of the Element from which the attribute was read
    attribute_arg.name # This is the name of the attribute read
    attribute_arg.value # This is the value of the attribute of the Element at the time the event was handled

    Before iterating over the observers, the Event object will iterate through the attribute_arg list and update the state of
    the corresponding attributes in the server version of the GUI tree.  This ensures that when the callback is called on the
    observer, the state on the server is synchronized with the state in the GUI for all the attributes listed in the attribute_args.
    This means it is normally not necessary to examine the attribute_arg information in the event handler method.

    New and/or existing attribute synchronization elements can be added and/or removed by using the add_argument and 
    remove_argument methods of the Event object.  For example:
        my_button.click.add_argument(a_paragraph_node_id, 'text')
    Consequently, after the click event of the my_button object is called, the value of the a_text_field_node would be 
    automatically updated before the callbacks are executed.
    }
    """

    def __init__(self, client_no_bubble = False, normal_key_only_bubble = False):
        """Constructs an Event(client_no_bubble, normal_key_only_bubble) 
        flag client_no_bubble stops the GUI from processing the event normally
        flag normal_key_only_bubble stops the GUI from processing F-keys, Ctrl, Meta, or Alt
        """
        self.arguments = list()
        self.observers = set()
        self.owner_node = None
        self.name = None
        self.client_no_bubble = client_no_bubble
        self.normal_key_only_bubble = normal_key_only_bubble

    def construct_argument(self, node, parameter):
        event_argument = dict()
        event_argument['id'] = node.id
        event_argument['name'] = parameter
        return event_argument

    def add_argument(self, node, parameter):
        event_argument = self.construct_argument(node, parameter)
        self.arguments.append(event_argument)
        self.update_event()

    def remove_argument(self, node, parameter):
        event_argument = self.construct_argument(node, parameter)
        self.arguments.remove(event_argument)
        self.update_event()

    def update_event(self):
        if self.owner_node:
            msg = UpdateEventMessage(self.owner_node, self.name, self.arguments)
            self.owner_node._send_msg_to_client(msg)

    def add_observer(self, observer, observer_callback):
        self.observers.add((observer, observer_callback))

    def remove_observer(self, observer, observer_callback):
        self.observers.remove((observer, observer_callback))

    def __call__(self, msg):
        if 'attributeArgs' in msg:
            self.update_server_attributes(msg['attributeArgs'])
        for (observer, observer_callback) in list(self.observers):
            observer_callback(observer, self.owner_node, msg)

    def update_server_attributes(self, attributeArgs):
        for attribute_arg in attributeArgs:
            node = self.owner_node.document_get_element_by_id(attribute_arg['id'])
            object.__setattr__(node, attribute_arg['name'], attribute_arg['value'])

    def __len__(self):
        return len(self.observers)

    def set_element_attribute(self, element, name):
        self.owner_node = element
        self.name = name
        msg = AttachEventMessage(element, name, self.arguments, self.client_no_bubble, self.normal_key_only_bubble)
        element._send_msg_to_client(msg)
        object.__setattr__(element, name, self)

    def del_element_attribute(self, element, name):
        msg = DetachEventMessage(element, name)
        element._send_msg_to_client(msg)
        object.__delattr__(element, name)

