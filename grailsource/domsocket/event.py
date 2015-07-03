"""
Copyright (c) 2015 TBillTech.  All rights reserved.

See more information on the node class in the doc of node.py.

Event handling is controlled by the second pillar of the REDOWL pattern:  The EventCapture object.  The EventCapture object sets up a
corresponding event listener on the corresponding DOM element of the Element attribute where the EventCapture object is assigned.  This
allows for seamlessly and transparently setting up and triggering event handlers from within the server side code without needing to
create explicit event handling within the GUI.

Putting it all together, the REDOWL pattern permits the programmer to write a web application that semantically is a single simple
GUI application.  With REDOWL, the programmer is not forced to implement communication code for interfacing the back end and the
front end pieces of the application across the IP network.  The communication link is abstracted away and does not explicitly appear
in a REDOWL application.

"""

from messages.update_event_message import UpdateEventMessage
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

    The __call__ method of the Event class iterates through the listeners that have registered with the Event class, 
    and calls the listener back using the listener's callback method.  A listener registers/deregisters with the Event class 
    by using the add_listener and remove_listener methods.

    Here is an example, again using the my_button Element: suppose we have a SpecialList Element called 'my_special_list' that wants to get 
    a callback method callback when my_button is clicked in the GUI.  For example, suppose the SpecialList has an on_my_button_click method:

    class SpecialList(Element):
        ...
        def on_my_button_click(self, my_button, msg):
            #Do something useful with self and my_button, and optionally access the info in msg

    Now, the my_special_list Element can register with the my_button.click Event object like so:
        my_button.click.add_listener(my_special_list, on_my_button_click)
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

    Before iterating over the listeners, the Event object will iterate through the attribute_arg list and update the state of
    the corresponding attributes in the server version of the GUI tree.  This ensures that when the callback is called on the
    listener, the state on the server is synchronized with the state in the GUI for all the attributes listed in the attribute_args.
    This means it is normally not necessary to examine the attribute_arg information in the event handler method.

    New and/or existing attribute synchronization elements can be added and/or removed by using the add_argument and remove_argument methods
    of the Event object.  For example:
        my_button.click.add_argument(a_paragraph_node_id, 'text')
    Consequently, after the click event of the my_button object is called, the value of the a_text_field_node would be automatically updated
    before the callbacks are executed.
    }
    """

    def __init__(self):
        self.arguments = list()
        self.listeners = set()
        self.owner_node = None
        self.name = None

    def construct_argument(self, nodeid, parameter):
        event_argument = dict()
        event_argument['id'] = nodeid
        event_argument['name'] = parameter
        return event_argument

    def add_argument(self, node, parameter):
        nodeid = node.id
        event_argument = self.construct_argument(nodeid, parameter)
        self.arguments.append(event_argument)
        if self.owner_node:
            msg = UpdateEventMessage(self.owner_node, self.name, self.arguments)
            self.owner_node.send_msg(msg)

    def remove_argument(self, node, parameter):
        nodeid = node.id
        event_argument = self.construct_argument(nodeid, parameter)
        self.arguments.remove(event_argument)
        if self.owner_node:
            msg = UpdateEventMessage(self.owner_node, self.name, self.arguments)
            self.owner_node.send_msg(msg)

    def add_listener(self, listener, listener_callback):
        self.listeners.add((listener, listener_callback))

    def remove_listener(self, listener, listener_callback):
        self.listeners.remove((listener, listener_callback))

    def __call__(self, msg):
        try:
            attribute_args = msg['attributeArgs']
        except KeyError:
            attribute_args = list()
        for attribute_arg in attribute_args:
            the_node = self.owner_node.document_get_element_by_id(attribute_arg['id'])
            # Don't trigger updating the GUI:  Just directly update the value
            # in the server tree
            object.__setattr__(
                the_node, attribute_arg['name'], attribute_arg['value'])
        if self.listeners:
            for (listener, listener_callback) in list(self.listeners):
                listener_callback(listener, self.owner_node, msg)

    def __len__(self):
        return len(self.listeners)
