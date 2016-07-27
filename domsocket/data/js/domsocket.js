// --------------------------------------------- Begin domsocket namespace -------------------------------------------------
//Copyright (c) 2015 TBillTech.  

//This Source Code Form is subject to the terms of the Mozilla Public
//License, v. 2.0. If a copy of the MPL was not distributed with this
//file, You can obtain one at http://mozilla.org/MPL/2.0/.

var domsocket = domsocket = domsocket || {}

with(domsocket)
{
  var EventListeners = new Array();
  var debug = true;
  var wsInfoObjs = new Object();
  var widgetConstructors = new Object();

  Bootstrap = function(web_socket_url, nodeid) 
  {
      if ("WebSocket" in window) 
          BootstrapDomSocket(web_socket_url, nodeid);  
      else  
          alert("This web browser lacks WebSocket capabilities.  Please run the with a web browser that supports WebSockets.");
  };

  SetWidgetClass = function(className, classConstructor)
  {
      widgetConstructors[className] = classConstructor;
  };

  BootstrapDomSocket = function(web_socket_url, nodeid)
  {
      var ws = NewWebSocket(web_socket_url);
      ws.onopen = function() { WSOnOpen(ws, nodeid); };
      ws.onmessage = function (evt) { WSOnMessage(ws, evt); };
      ws.onclose = function() { WSOnClose(ws); };
      ws.onerror = function(evt) { WSOnError(ws, evt); };
      ws.sendmsg = function(msg) { WSSendMsg(ws, msg); };
  };

  NewwsInfo = function(ws)
  { 
      wsInfo = new Object();
      wsInfo.ws = ws;
      wsInfo.events = new Object();
      wsInfo.nodeids = new Object();
      wsInfo.widgets = new Object();
      return wsInfo
  };

  NewWebSocket = function(web_socket_url)
  {
      var ws = new WebSocket(web_socket_url);
      wsInfoObjs[ws] = NewwsInfo(ws);
      return ws;
  };

  DeleteWebSocket = function(ws)
  {
      if(ws in wsInfoObjs)
          delete wsInfoObjs[ws];
  };

  WSOnOpen = function(ws, nodeid)
  {
      var msg = new Object();
      msg.type = "event";
      msg.nodeid = nodeid;
      msg.eventName = "init";
      ws.sendmsg(msg);
  };

  var wsOnMessageHandlers = new Object();
  WSOnMessage = function(ws, evt)
  { 
      try
      {
          var msg = JSON.parse(evt.data);
          wsOnMessageHandlers[msg.type](msg, ws);
      }
      catch(err)
      {
          var errmsg = NewErrorMessage(err);
          errmsg.original = evt.data;
          ws.sendmsg(errmsg);
      }
  };

  WSOnClose = function(ws)
  {
      DetachAllWidgets(ws);
      DetachAllEvents(ws);
      DeleteWebSocket(ws);
  };

  WSOnError = function(ws, evt)
  { 
      alert("Error communicating with server... closing down web socket and logging out.");
      ws.onclose();
  };     

  WSSendMsg = function(ws, msg)
  {
      ws.send(JSON.stringify(msg)); ws.send("flush");      
  };

  NewErrorMessage = function(err)
  {
      var msg = new Object();
      msg.type = "exception";
      msg.message = GetBestErrorString(err);
      msg.stack = GetErrorStack(err);
      return msg;
  }; 

  GetBestErrorString = function(err)
  {
      if(err.hasOwnProperty("message"))
          return err.message;
      else if(err.hasOwnProperty("description"))
          return err.description;
      return String(err);      
  };

  GetErrorStack = function(err)
  {
      return String(err.stack);
  };

  wsInfoAddListener = function(theElement, theListener)
  {
      var nodeEvents = createNodeEvents(theListener.ws, theElement);
      if(theListener.eventName in nodeEvents)
          throw new Error(theListener.eventName + " is already defined for node " + theElement.id);
      nodeEvents[theListener.eventName] = theListener;
      theElement.addEventListener(theListener.eventName, theListener);
  };

  wsInfoGetListener = function(ws, theElement, eventName)
  {
      var nodeEvents = getNodeEvents(ws, theElement);
      if(eventName in nodeEvents)
          return nodeEvents[eventName];
      throw new Error(eventName + " is not defined for node " + theElement.id);
  };

  wsInfoRemoveListener = function(ws, theElement, eventName)
  {
      var nodeEvents = getNodeEvents(ws, theElement);
      if(eventName in nodeEvents)
      {
          var theListener = nodeEvents[eventName];
          theElement.removeEventListener(theListener.eventName, theListener);
          delete nodeEvents[eventName];
      }
  };

  wsInfoRemoveAllListeners = function(ws)
  {
      var wsInfo = wsInfoObjs[ws];
      for(var theElementId in wsInfo.events)
      {
          var nodeEvents = wsInfo.events[theElementId];
          for(var eventName in nodeEvents)
          {
              var theElement = document.getElementById(theElementId);
              wsInfoRemoveListener(ws, theElement, eventName);  
          }
      }
      delete wsInfo.events;
  };

  eventListenerIsMissing = function(theElement, wsInfo)
  {
      return !(theElement.id in wsInfo.events);
  };

  getNodeEvents = function(ws, theElement)
  {
      var wsInfo = wsInfoObjs[ws];
      if(eventListenerIsMissing(theElement, wsInfo))
          throw new Error(theElement.id + " is not defined.");
      return wsInfo.events[theElement.id];      
  };

  createNodeEvents = function(ws, theElement)
  {
      var wsInfo = wsInfoObjs[ws];
      if(eventListenerIsMissing(theElement, wsInfo))
          wsInfo.events[theElement.id] = new Object();
      return getNodeEvents(ws, theElement);
  };

  wsInfoAddElement = function(ws, theElement)
  {
      var wsInfo = wsInfoObjs[ws];
      if(!(theElement.id in wsInfo.nodeids))
          wsInfo.nodeids[theElement.id] = theElement;
  };

  wsInfoRemoveElement = function(ws, theElement)
  {
      var wsInfo = wsInfoObjs[ws];
      if(!(theElement.id in wsInfo.nodeids))
          throw new Error(theElement.id + " is not defined.");
      if(!(wsInfoOtherOwners(ws, theElement.id)))
         theElement.parentNode.removeChild(theElement);
      delete wsInfo.nodeids[theElement.id];
  };

  wsInfoRemoveAllElements = function(ws)
  {
      var wsInfo = wsInfoObjs[ws];
      for(var theElementId in wsInfo.nodeids)
      {
          if(!(wsInfoOtherOwners(ws, theElementId)))
          {
              var theElement = document.getElementById(msg.id);
              theElement.parentNode.removeChild(theElement);
          }
      }
      delete wsInfo.nodeids;
  };

  wsInfoOtherOwners = function(thisws, theElementId)
  {
      for(var ws in wsInfoObjs)
      {
          if(ws == thisws)
              continue;
          if(theElementId in wsInfoObjs[ws].nodeids)
              return true;
      }
      return false;
  };

  InsertChild = function(msg, ws)
  {
      var child = CreateChild(msg);
      AdoptChild(msg, child);
      wsInfoAddElement(ws, child);
  };

  CreateChild = function(msg)
  {
      var child = document.getElementById(msg.childId);
      if(child === null)
        child = document.createElement(msg.childTag);
      else
        child.tagName = msg.childTag;
      child.id = msg.childId;
      return child;
  };

  AdoptChild = function(msg, child)
  {
      var parent = document.getElementById(msg.parentId);
      if((msg.index < 0) || (msg.index == parent.childNodes.length))
        parent.appendChild(child);
      else
        parent.insertBefore(child, parent.childNodes[msg.index])
  };

  RemoveChild = function(msg, ws)
  {
      var parent = document.getElementById(msg.parentId);
      var child = parent.childNodes[msg.index];
      wsInfoRemoveElement(ws, child);
  };

  SetTextNode = function(msg, ws)
  {
      var parent = document.getElementById(msg.parentId);
      var child = parent.childNodes[msg.index];
      child.textContent = msg.text;
  };

  InsertTextNode = function(msg, ws)
  {
      var parent = document.getElementById(msg.parentId);
      var child = document.createTextNode(msg.text);
      if(msg.index == parent.childNodes.length)
          parent.appendChild(child);
      else
          parent.insertBefore(child, parent.childNodes[msg.index])
  };

  SetAttribute = function(msg, ws)
  {
      var theElement = document.getElementById(msg.id);
      if(theElement.getAttribute(msg.name) instanceof Function)
           theElement.getAttribute(msg.name)(msg.value);
      else if(msg.name === "value")
          theElement.value = msg.value;
      else
          theElement.setAttribute(msg.name, msg.value);
      return msg.value;
  };

  GetAttribute = function(msg)
  {
      var theElement = document.getElementById(msg.id);
      if(theElement.getAttribute(msg.name) instanceof Function)
          return theElement.getAttribute(msg.name)();
      else if(msg.name === "value")
          return theElement.value;
      return theElement.getAttribute(msg.name);
  };

  RemoveAttribute = function(msg, ws)
  {
      var theElement = document.getElementById(msg.id);
      theElement.removeAttribute(msg.name);
  };

  HandleEvent = function(event)
  {
      var theListener = this;
      var msg = CreateEventMessage(theListener, event);
      if(theListener.clientNoBubble)
          disabledEventPropagation(event);
      theListener.ws.sendmsg(msg);
      return false;
  };

  disabledEventPropagation = function(event)
  {
      event.returnValue = false;
      if(event.stopPropagation)
      {
          event.stopPropagation();
      } else if(window.event)
      {
          window.event.cancelBubble = true;
      }
      event.preventDefault();
  }

  var eventPropertyNames = [
  "currentTarget", "target", "timeStamp", "type", "view",
  "altKey", "button", "buttons", "clientX", "clientY", "ctrlKey", "detail", "metaKey",
      "relatedTaget", "screenX", "screenY", "shiftKey", "which",
  "charCode", "key", "keyCode", "location", 
  "newURL", "oldURL", "from", "to",
  "persisted",
  "animationName", "elapsedTime",
  "propertyName",
  "deltaX", "deltaY", "deltaZ", "deltaMode"]

  eventProperties = function(event) 
  {
    var msgProperties = new Object();
    for (var i = 0; i < eventPropertyNames.length; i++)
    {
        propertyName = eventPropertyNames[i];
        try {
            if((propertyName === "currentTarget") || 
               (propertyName === "target") || 
               (propertyName === "relatedTarget") ||
               (propertyName === "view"))
            {
                msgProperties[propertyName] = event[propertyName].id;
            }
            else
            {
                msgProperties[propertyName] = event[propertyName];
            }
        } catch (e) {
        }
    }
    return msgProperties;
  };

  CreateEventMessage = function(theListener, event)
  {
      var msg = new Object();
      msg.type = "event";
      msg.nodeid = theListener.nodeid;
      msg.eventName = theListener.eventName;
      if(theListener.hasOwnProperty("attributeArgs"))
          msg.attributeArgs = GetAttributeResults(theListener);
      msg.event = eventProperties(event);
      return msg;
  };

  GetAttributeResults = function(theListener)
  {
      var results = new Array();
      var attributeArgs = theListener.attributeArgs;
      for(var i = 0; i < attributeArgs.length; i++)
      {
          var result = GetAttributeResult(attributeArgs[i]);
          results.push(result);
      }
      return results;
  };
 
  GetAttributeResult = function(attributeArg)
  {
      var result = new Object();
      result.id = attributeArg.id;
      result.name = attributeArg.name;
      result.value = GetAttribute(attributeArg);
      return result;      
  };

  AttachEvent = function(msg, ws)
  {
      var theElement = document.getElementById(msg.id);
      var theListener = CreateListener(msg, ws);
      wsInfoAddListener(theElement, theListener);
  };

  CreateListener = function(msg, ws)
  {
      var theListener = new Object();
      theListener.nodeid = msg.id;
      theListener.eventName = msg.name;
      if(msg.hasOwnProperty("attributeArgs"))
          theListener.attributeArgs = msg.attributeArgs;
      theListener.clientNoBubble = false;
      if(msg.hasOwnProperty("clientNoBubble"))
          if(msg.clientNoBubble != false)
              theListener.clientNoBubble = true;
      theListener.handleEvent = HandleEvent;
      theListener.ws = ws;
      return theListener;
  };

  DetachEvent = function(msg, ws)
  {
      var theElement = document.getElementById(msg.id);
      wsInfoRemoveListener(ws, theElement, msg.name);
  };

  UpdateEvent = function(msg, ws)
  {
      var theElement = document.getElementById(msg.id);
      var theListener = wsInfoGetListener(ws, theElement, msg.name);
      if(msg.hasOwnProperty("attributeArgs"))
          theListener.attributeArgs = msg.attributeArgs;
      else 
          theListener.removeAttribute("attributeArgs");
  };

  SetFocus = function(msg, ws)
  {
      var theElement = document.getElementById(msg.id);
      theElement.focus();
  };

  CreateWidget = function(msg, ws)
  {
      var widget = new Object();
      wsInfoObjs[widget] = NewwsInfo(widget);
      widget.ws = ws;
      widget.theElement = document.getElementById(msg.id);
      widget.stop = false;
      widget.idleSleep = 10;
      widget.eventHandlers = new Object();
      widget.HaveListener = function(eventName)
      {
          if(eventName in getNodeEvents(this.ws, this.theElement))
              return true;
          return false;
      };
      widget.GetListener = function(eventName)
      {
          return wsInfoGetListener(this.ws, this.theElement, eventName);
      };
      widget.Run = function()
      {
          if(this.stop)
              return;
          if(this.HaveWork())
          {
              try
              {
                  this.DoWork();
              }
              catch(err)
              {
                  var errmsg = NewErrorMessage(err);
                  errmsg.original = 'Error in javascript widget';
                  this.ws.sendmsg(errmsg);
              }
          }
          setTimeout(function() { this.Run(); }.bind(this), this.SleepTime());
      };
      widget.SleepTime = function()
      {
          if(this.HaveWork())
              return 0;
          else
              return this.idleSleep;
      };
      widget.Attach = function()
      {
          this.Run();
      };
      widget.Detach = function()
      {
          this.Destructor();
          this.stop = true;
          delete wsInfoObjs[this];
      };
      widget.SendEvent = function(eventName, event) 
      {
           var theListener = this.GetListener(eventName);
           theListener.handleEvent(event);
      };
      widget.FireEvent = function(eventName, event)
      {
          if(this.HaveListener(eventName))
          {
              event.target = this.theElement;
              event.timeStamp = Date.now();
              this.SendEvent(eventName, event)
          }
      };
      // a javascript event handler is invoked by the domsocket HandleEvent function
      // Which expects to call ws.sendmsg(msg), but here the ws is actually: this
      // due to a prior call to AttachEvent(msg, this);
      widget.sendmsg = function(msg)
      {
          if(msg.eventName in this.eventHandlers)
              this.eventHandlers[msg.eventName](this, msg);
      };
      widget.AttachEvent = function(eventName, eventHandler, clientNoBubble)
      {
          msg = new Object();
          msg.id = this.theElement.id;
          msg.name = eventName;
          msg.clientNoBubble = clientNoBubble;
          AttachEvent(msg, this);
          this.eventHandlers[eventName] = eventHandler;
      };
      widget.DetachEvent = function(eventName)
      {
          msg = new Object();
          msg.id = this.theElement.id;
          msg.name = eventName;
          DetachEvent(msg, this);
          delete this.eventHandlers[eventName];
      };
      widget.HaveWork = function() { return false; };
      widget.DoWork = function() { };
      widget.Destructor = function() { };
      widget.Receive = function(msg) { };
      widget.Construct = widgetConstructors[msg.className];
      widget.Construct(msg);
      return widget;
  };

  AttachWidget = function(msg, ws)
  {
      var widget = CreateWidget(msg, ws);
      wsInfoObjs[ws].widgets[msg.id] = widget;
      widget.Attach();
  };

  DetachWidget = function(msg, ws)
  {
      if(msg.id in wsInfoObjs[ws].widgets)
      {
          var widget = wsInfoObjs[ws].widgets[msg.id];
          widget.Detach();
          delete wsInfoObjs[ws].widgets[msg.id];
      }
  };

  SendToWidget = function(msg, ws)
  {
      if(msg.id in wsInfoObjs[ws].widgets)
      {
          var widget = wsInfoObjs[ws].widgets[msg.id];
          widget.Receive(msg.msg);
      }
  };
  
  DetachAllWidgets = function(ws)
  {
      for(var widget in wsInfoObjs[ws].widgets)
          if(widget.hasOwnProperty('Detach'))
              widget.Detach();
      wsInfoObjs[ws].widgets = [];
  };

  DetachAllEvents = function(ws)
  {
    wsInfoRemoveAllListeners(ws);
  };

  wsOnMessageHandlers.insertChild = InsertChild;
  wsOnMessageHandlers.removeChild = RemoveChild;
  wsOnMessageHandlers.setTextNode = SetTextNode;
  wsOnMessageHandlers.insertTextNode = InsertTextNode;
  wsOnMessageHandlers.setAttribute = SetAttribute;
  wsOnMessageHandlers.removeAttribute = RemoveAttribute;
  wsOnMessageHandlers.attachEvent = AttachEvent;
  wsOnMessageHandlers.detachEvent = DetachEvent;
  wsOnMessageHandlers.updateEvent = UpdateEvent;
  wsOnMessageHandlers.setFocus = SetFocus;
  wsOnMessageHandlers.attachWidget = AttachWidget;
  wsOnMessageHandlers.detachWidget = DetachWidget;
  wsOnMessageHandlers.sendToWidget = SendToWidget;
};
// --------------------------------------------- end domsocket namespace -------------------------------------------------

