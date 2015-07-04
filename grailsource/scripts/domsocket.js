// --------------------------------------------- Begin domsocket namespace -------------------------------------------------
var domsocket = domsocket = domsocket || {}

with(domsocket)
{
  var EventListeners = new Array();
  var debug = true;
  var wsInfoObjs = new Object();

  Bootstrap = function(web_socket_url, nodeid) 
  {
      if ("WebSocket" in window) 
	  BootstrapDomSocket(web_socket_url, nodeid);  
      else  
	  alert("This web browser lacks WebSocket capabilities.  Please run the with a web browser that supports WebSockets.");
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
      DetachAllEvents(ws);
      DropAllElementIds(ws);
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
      return err.stringify();      
  };

  GetErrorStack = function(err)
  {
      if(err.hasOwnProperty("stack"))
          return err.stack;
      return "Unknown stack";
  };

  wsInfoAddListener = function(ws, theElement, eventName, theListener)
  {
    var wsInfo = wsInfoObjs[ws];
    if(!(theElement.id in wsInfo.events))
    {
      wsInfo.events[theElement.id] = new Object();
    }
    var nodeEvents = wsInfo.events[theElement.id];
    if(eventName in nodeEvents)
      throw new Error(eventName + " is already defined for node " + theElement.id);
    nodeEvents[eventName] = theListener;
    theElement.addEventListener(theListener.eventName, theListener);
  };

  wsInfoGetListener = function(ws, theElement, eventName)
  {
    var wsInfo = wsInfoObjs[ws];
    if(!(theElement.id in wsInfo.events))
    {
      throw new Error(theElement.id + " is not defined.");
    }
    var nodeEvents = wsInfo.events[theElement.id];
    if(!(eventName in nodeEvents))
      throw new Error(eventName + " is not defined for node " + theElement.id);
    return nodeEvents[eventName];
  };

  wsInfoRemoveListener = function(ws, theElement, eventName)
  {
    var wsInfo = wsInfoObjs[ws];
    if(!(theElement.id in wsInfo.events))
    {
      throw new Error(theElement.id + " is not defined.");
    }
    var nodeEvents = wsInfo.events[theElement.id];
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
        var theListener = nodeEvents[eventName];
        theElement.removeEventListener(theListener);
      }
    }
    delete wsInfo.events;
  };

  wsInfoAddElement = function(ws, theElement)
  {
    var wsInfo = wsInfoObjs[ws];
    if(!(theElement.id in wsInfo.nodeids))
    {
      wsInfo.nodeids[theElement.id] = theElement;
    }
  };

  wsInfoRemoveElement = function(ws, theElement)
  {
    var wsInfo = wsInfoObjs[ws];
    if(!(theElement.id in wsInfo.nodeids))
    {
      throw new Error(theElement.id + " is not defined.");
    }
    delete wsInfo.nodeids[theElement.id];
  };

  wsInfoRemoveAllElements = function(ws)
  {
    var wsInfo = wsInfoObjs[ws];
    for(var theElementId in wsInfo.nodeids)
    {
      if(!(wsInfoOtherOwners(theElementId, ws)))
      {
        var theElement = document.getElementById(msg.id);
        theElement.parentNode.removeChild(theElement);
      }
    }
    delete wsInfo.nodeids;
  };

  wsInfoOtherOwners = function(theElementId, notws)
  {
    for(var ws in wsInfoObjs)
    {
      if(ws == notws)
        continue;
      alert(ws == notws);
      if(theElementId in wsInfoObjs[ws].nodeids)
        return true;
    }
    return false;
  };

  AppendChild = function(msg, ws)
  {
    if(msg.childTag !== "text")
    {
      var child = document.getElementById(msg.childId);
      if(child === null)
        child = document.createElement(msg.childTag);
      else
        child.tagName = msg.childTag;
      child.id = msg.childId;
      var parent = document.getElementById(msg.parentId);
      if(child.parentNode === null)
      {
        parent.appendChild(child);
      }
      else
      {
        if(child.parentNode !== parent)
          throw new Error("child parentnode is wrong: parent(" + child.parentNode.id + ")!=msg(" + msg.parentId + ")");
      }
      wsInfoAddElement(ws, child);
    }
    else
    {
      var parent = document.getElementById(msg.parentId);
      var child = document.createTextNode(msg.text);
      parent.appendChild(child);
    }
  };

  SetChild = function(msg, ws)
  {
    if(msg.childTag !== "text")
    {
      RemoveChild(msg, ws);
      InsertChild(msg, ws);
    }
    else
    {
      var parent = document.getElementById(msg.parentId);
      var child = parent.childNodes[msg.index];
      child.nodeValue = msg.text;
    }
  };

  InsertChild = function(msg, ws)
  {
    if(msg.childTag !== "text")
    {
      var child = document.getElementById(msg.childId);
      if(child === null)
        child = document.createElement(msg.childTag);
      else
        child.tagName = msg.childTag;
      child.id = msg.childId;
      var parent = document.getElementById(msg.parentId);
      if(msg.index == parent.childNodes.length)
        parent.appendChild(child);
      else
        parent.insertBefore(child, parent.childNodes[msg.index])
      wsInfoAddElement(ws, child);
    }
    else
    {
      var parent = document.getElementById(msg.parentId);
      var child = document.createTextNode(msg.text);
      if(msg.index == parent.childNodes.length)
        parent.appendChild(child);
      else
        parent.insertBefore(child, parent.childNodes[msg.index])
    }
  };

  RemoveChild = function(msg, ws)
  {
    var parent = document.getElementById(msg.parentId);
    var child = parent.childNodes[msg.index];
    if(!(wsInfoOtherOwners(child.id, ws)))
    {
      wsInfoRemoveElement(ws, child);
      parent.removeChild(child);
      child.id = "";
    }
  };

  SetAttribute = function(msg, ws)
  {
    var theElement = document.getElementById(msg.id);
    if(theElement.getAttribute(msg.name) instanceof Function)
    {
      theElement.getAttribute(msg.name)(msg.value);
    }
    else if(msg.name === "value")
    {
      theElement.value = msg.value;
    }
    else
    {
      theElement.setAttribute(msg.name, msg.value);
    }
    return msg.value;
  };

  GetAttribute = function(msg)
  {
    var theElement = document.getElementById(msg.id);
    if(theElement.getAttribute(msg.name) instanceof Function)
    {
      return theElement.getAttribute(msg.name)();
    }
    else if(msg.name === "value")
    {
      return theElement.value;
    }
    else
    {
      return theElement.getAttribute(msg.name);
    }
  };

  RemoveAttribute = function(msg, ws)
  {
    var theElement = document.getElementById(msg.id);
    theElement.removeAttribute(msg.name);
  };

  HandleEvent = function(event)
  {
    var theListener = this;
    var msg = new Object();
    msg.type = "event";
    msg.nodeid = theListener.nodeid;
    msg.eventName = theListener.eventName;
    if(theListener.hasOwnProperty("attributeArgs"))
    {
      var results = new Array();
      for(var i = 0; i < theListener.attributeArgs.length; i++)
      {
        var attributeArg = theListener.attributeArgs[i];
        var result = new Object();
        result.id = attributeArg.id;
        result.name = attributeArg.name;
        result.value = GetAttribute(attributeArg);
        results.push(result);
      }
      msg.attributeArgs = results;
    }
    theListener.ws.send(JSON.stringify(msg)); theListener.ws.send("flush");
  };
 
  AttachEvent = function(msg, ws)
  {
    var theElement = document.getElementById(msg.id);
    var theListener = new Object();
    theListener.nodeid = msg.id;
    theListener.eventName = msg.name;
    if(msg.hasOwnProperty("attributeArgs"))
    {
      theListener.attributeArgs = msg.attributeArgs;
    }
    theListener.handleEvent = HandleEvent;
    theListener.ws = ws;
    wsInfoAddListener(ws, theElement, msg.name, theListener);
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
    {
      theListener.attributeArgs = msg.attributeArgs;
    }
    else if(theListener.hasOwnProperty("attributeArgs"))
    {
      theListener.removeAttribute("attributeArgs");
    }
  };

  DetachAllEvents = function(msg, ws)
  {
    wsInfoRemoveAllListeners(ws);
  };

  wsOnMessageHandlers.appendChild = AppendChild;
  wsOnMessageHandlers.setChild = SetChild;
  wsOnMessageHandlers.insertChild = InsertChild;
  wsOnMessageHandlers.removeChild = RemoveChild;
  wsOnMessageHandlers.setAttribute = SetAttribute;
  wsOnMessageHandlers.removeAttribute = RemoveAttribute;
  wsOnMessageHandlers.attachEvent = AttachEvent;
  wsOnMessageHandlers.detachEvent = DetachEvent;
  wsOnMessageHandlers.updateEvent = UpdateEvent;
};
// --------------------------------------------- end domsocket namespace -------------------------------------------------

