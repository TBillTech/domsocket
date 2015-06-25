// --------------------------------------------- Begin domsocket namespace -------------------------------------------------
var domsocket = domsocket = domsocket || {}
// Put all the DOM websocket login into the domsocket namespace
with(domsocket)
{
  var EventListeners = new Array();
  var debug = true;
  var wsInfoObjs = new Object();

  AddwsInfo = function(ws)
  {
    // wsInfo prototype:
    wsInfo = new Object();
    wsInfo.ws = ws;
    wsInfo.events = new Object();
    wsInfo.nodeids = new Object();
    wsInfoObjs[ws] = wsInfo;
  };

  RemovewsInfo = function(ws)
  {
    // wsInfo prototype:
    if(ws in wsInfoObjs)
      delete wsInfoObjs[ws];
  };

  wsInfoAddListener = function(ws, theNode, eventName, theListener)
  {
    var wsInfo = wsInfoObjs[ws];
    if(!(theNode.id in wsInfo.events))
    {
      wsInfo.events[theNode.id] = new Object();
    }
    var nodeEvents = wsInfo.events[theNode.id];
    if(eventName in nodeEvents)
      throw new Error(eventName + " is already defined for node " + theNode.id);
    nodeEvents[eventName] = theListener;
    theNode.addEventListener(theListener.eventName, theListener);
  };

  wsInfoGetListener = function(ws, theNode, eventName)
  {
    var wsInfo = wsInfoObjs[ws];
    if(!(theNode.id in wsInfo.events))
    {
      throw new Error(theNode.id + " is not defined.");
    }
    var nodeEvents = wsInfo.events[theNode.id];
    if(!(eventName in nodeEvents))
      throw new Error(eventName + " is not defined for node " + theNode.id);
    return nodeEvents[eventName];
  };

  wsInfoRemoveListener = function(ws, theNode, eventName)
  {
    var wsInfo = wsInfoObjs[ws];
    if(!(theNode.id in wsInfo.events))
    {
      throw new Error(theNode.id + " is not defined.");
    }
    var nodeEvents = wsInfo.events[theNode.id];
    if(eventName in nodeEvents)
    {
      var theListener = nodeEvents[eventName];
      theNode.removeEventListener(theListener.eventName, theListener);
      delete nodeEvents[eventName];
    }
  };

  wsInfoRemoveAllListeners = function(ws)
  {
    var wsInfo = wsInfoObjs[ws];
    for(var theNodeId in wsInfo.events)
    {
      var nodeEvents = wsInfo.events[theNodeId];
      for(var eventName in nodeEvents)
      {
        var theListener = nodeEvents[eventName];
        theNode.removeEventListener(theListener);
      }
    }
    delete wsInfo.events;
  };

  wsInfoAddNode = function(ws, theNode)
  {
    var wsInfo = wsInfoObjs[ws];
    if(!(theNode.id in wsInfo.nodeids))
    {
      wsInfo.nodeids[theNode.id] = theNode;
    }
  };

  wsInfoRemoveNode = function(ws, theNode)
  {
    var wsInfo = wsInfoObjs[ws];
    if(!(theNode.id in wsInfo.nodeids))
    {
      throw new Error(theNode.id + " is not defined.");
    }
    delete wsInfo.nodeids[theNode.id];
  };

  wsInfoRemoveAllNodes = function(ws)
  {
    var wsInfo = wsInfoObjs[ws];
    for(var theNodeId in wsInfo.nodeids)
    {
      if(!(wsInfoOtherOwners(theNodeId, ws)))
      {
        var theNode = document.getElementById(msg.id);
        theNode.parentNode.removeChild(theNode);
      }
    }
    delete wsInfo.nodeids;
  };

  wsInfoOtherOwners = function(theNodeId, notws)
  {
    for(var ws in wsInfoObjs)
    {
      if(ws == notws)
        continue;
      alert(ws == notws);
      if(theNodeId in wsInfoObjs[ws].nodeids)
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
      wsInfoAddNode(ws, child);
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
      wsInfoAddNode(ws, child);
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
      wsInfoRemoveNode(ws, child);
      parent.removeChild(child);
      child.id = "";
    }
  };

  AccessAttribute = function(msg)
  {
    if(msg.hasOwnProperty("value"))
      return SetAttribute(msg);
    return GetAttribute(msg);
  };

  SetAttribute = function(msg)
  {
    var theNode = document.getElementById(msg.id);
    if(theNode.getAttribute(msg.name) instanceof Function)
    {
      theNode.getAttribute(msg.name)(msg.value);
    }
    else if(msg.name === "value")
    {
      theNode.value = msg.value;
    }
    else
    {
      theNode.setAttribute(msg.name, msg.value);
    }
    return msg.value;
  };

  GetAttribute = function(msg)
  {
    var theNode = document.getElementById(msg.id);
    if(theNode.getAttribute(msg.name) instanceof Function)
    {
      return theNode.getAttribute(msg.name)();
    }
    else if(msg.name === "value")
    {
      return theNode.value;
    }
    else
    {
      return theNode.getAttribute(msg.name);
    }
  };

  RemoveAttribute = function(msg)
  {
    var theNode = document.getElementById(msg.id);
    theNode.removeAttribute(msg.name);
  };

  HandleEvent = function(event)
  {
    var theListener = this;
    var msg = new Object();
    msg.type = "event";
    msg.nodeid = theListener.nodeid;
    msg.eventName = theListener.eventName;
    //msg.event = JSON.stringify(event);
    if(theListener.hasOwnProperty("attributeArgs"))
    {
      var results = new Array();
      for(var i = 0; i < theListener.attributeArgs.length; i++)
      {
        var attributeArg = theListener.attributeArgs[i];
        var result = new Object();
        result.id = attributeArg.id;
        result.name = attributeArg.name;
        result.value = AccessAttribute(attributeArg);
        results.push(result);
      }
      msg.attributeArgs = results;
    }
    theListener.ws.send(JSON.stringify(msg)); theListener.ws.send("flush");
  };
 
  AttachEvent = function(msg, ws)
  {
    var theNode = document.getElementById(msg.id);
    // if(debug)
    // {
    //   for(var i=0; i < EventListeners.length; i++)
    //   {
    //     var aListener = EventListeners[i];
    //     if(aListener.nodeid === msg.id)
    //       if(aListener.eventName === msg.name)
    //         if(aListener.ws === ws)
    //         {
    //           throw new Error("Trying to attach an event, but the event listenter already exists");
    //         }
    //   }
    // }

    // Attach and detach events are actually implemented using add and remove EventListeners
    var theListener = new Object();
    theListener.nodeid = msg.id;
    theListener.eventName = msg.name;
    if(msg.hasOwnProperty("attributeArgs"))
    {
      theListener.attributeArgs = msg.attributeArgs;
    }
    theListener.handleEvent = HandleEvent;
    theListener.ws = ws;
    //EventListeners.push(theListener);
    wsInfoAddListener(ws, theNode, msg.name, theListener);
    //theNode.addEventListener(theListener.eventName, theListener);
  };

  DetachEvent = function(msg, ws)
  {
    var theNode = document.getElementById(msg.id);
    wsInfoRemoveListener(ws, theNode, msg.name);
    // for(var i=0; i < EventListeners.length; i++)
    // {
    //   var aListener = EventListeners[i];
    //   if(aListener.nodeid === msg.id)
    //     if(aListener.eventName === msg.name)
    //       if(aListener.ws === ws)
    //       {
    //         theNode.removeEventListener(aListener);
    //         EventListeners.splice(i,1);
    //         return;       
    //       }
    // }
    // throw new Error("Could not find the event listenter to detach it");
  };

  UpdateEvent = function(msg, ws)
  {
    var theNode = document.getElementById(msg.id);
    var theListener = wsInfoGetListener(ws, theNode, msg.name);
    if(msg.hasOwnProperty("attributeArgs"))
    {
      theListener.attributeArgs = msg.attributeArgs;
    }
    else if(theListener.hasOwnProperty("attributeArgs"))
    {
      theListener.removeAttribute("attributeArgs");
    }
    // var theNode = document.getElementById(msg.id);
    // for(var i=0; i < EventListeners.length; i++)
    // {
    //   var aListener = EventListeners[i];
    //   if(aListener.nodeid === msg.id)
    //     if(aListener.eventName === msg.name)
    //       if(aListener.ws === ws)
    //       {
    //         if(msg.hasOwnProperty("attributeArgs"))
    //         {
    //           aListener.attributeArgs = msg.attributeArgs;
    //         }
    //         else if(aListener.hasOwnProperty("attributeArgs"))
    //         {
    //           aListener.removeAttribute("attributeArgs");
    //         }
    //         return;       
    //       }
    // }
    // throw new Error("Could not find the event listenter to update it");
  };

  DetachAllEvents = function(msg, ws)
  {
    wsInfoRemoveAllListeners(ws);
    // for(var i=EventListeners.length-1; i >= 0; i--)
    // {
    //   var aListener = EventListeners[i];
    //   if(aListener.ws === ws)
    //   {
    //     theNode.removeEventListener(aListener);
    //     EventListeners.splice(i,1);
    //     return;       
    //   }
    // }
  };

  Bootstrap = function(web_socket_url, nodeid)
  {
    if ("WebSocket" in window)
    {
      var ws = new WebSocket(web_socket_url);
      AddwsInfo(ws);
      ws.onopen = function()
      {
        var msg = new Object();
        msg.type = "event";
        msg.nodeid = nodeid;
        msg.eventName = "init";
        this.send(JSON.stringify(msg)); this.send("flush");
      };
      ws.onmessage = function (evt) 
      { 
        try
        {
          var msg = JSON.parse(evt.data);
          switch(msg.type)
          {
            case "appendChild":
              AppendChild(msg, this);
              break;
            case "setChild":
              SetChild(msg, this);
              break;
            case "insertChild":
              InsertChild(msg, this);
              break;
            case "removeChild":
              RemoveChild(msg, this);
              break;
            case "setAttribute":
              SetAttribute(msg);
              break;
            case "removeAttribute":
              RemoveAttribute(msg);
              break;
            case "attachEvent":
              AttachEvent(msg, this);
              break; 
            case "detachEvent":
              DetachEvent(msg, this);
              break; 
            case "updateEvent":
              UpdateEvent(msg, this);
              break; 
          }
        }
        catch(err)
        {
          var msg = new Object();
          msg.type = "exception";
          if(err.hasOwnProperty("message"))
            msg.message = err.message;
          else if(err.hasOwnProperty("description"))
            msg.message = err.description;
          else
            msg.message = err.stringify();
          msg.stack = "Unknown stack";
          if(err.hasOwnProperty("stack"))
            msg.stack = err.stack;
          msg.original = evt.data;
          this.send(JSON.stringify(msg)); this.send("flush");
        }
      };
      ws.onclose = function()
      { 
        DetachAllEvents(this);
        DropAllNodeIds(this);
        RemovewsInfo(this);
        //alert("Connection to server has been lost..."); 
      };
      ws.onerror = function(evt) 
      { 
        alert("Error communicating with server... closing down socket and logging out.");
        this.onclose();
      }; 
    }
    else
    {
      alert("This web browser lacks WebSocket capabilities.  Please run the with a web browser that supports WebSockets.");
    }
  };
};
// --------------------------------------------- end domsocket namespace -------------------------------------------------

