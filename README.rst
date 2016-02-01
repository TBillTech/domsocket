===============
 domsocket 1.0
===============

--------------------------------------------------------
 Document Object Model Python Bindings over Web Sockets 
--------------------------------------------------------

Installation
============

Install Docker Engine
---------------------

If you wish to use the cherrpyserver to serve up a domsocket application, which is
currently the only supported configuration, you will need to have a running docker
engine to allow execution of the cherrypyserver docker container.

The docker web site explains how to install the docker engine on your OS.  You can 
navigate to other OS instructions from this page which shows how to install onto Ubuntu::
  https://docs.docker.com/engine/installation/ubuntulinux/


Install domsocket Python Library
--------------------------------

The source code may be obtained by either unzipping the source tar.gz or by
checking out the git source code.

In the root of the source tree, to install as a site-package, 
run python setup.py install.  For example on Ubuntu linux::
  sudo python setup.py install


You can now import the domsocket library in your source code::

  from domsocket.zmq_runner import ZMQRunner, domsocket_js_path
  from domsocket.element import Element
  from domsocket.event import Event
  from domsocket.basic_widgets.html_widget import HTMLWidget
  from domsocket.basic_widgets.html_tag import HTMLTag



Running the Example Todos App
=============================

Building the cherrpyserver Docker Container
-------------------------------------------

To build the cherrpyserver Docker Container, first create a new empty directory where
you will store the container build files.  Change to this directory, and then run::
  build_cherrypyserver

Executing this command will result in copying all the cherrypyserver files to the 
current directory, and building the Docker container called cherrpyserver.  This will
also "load" the container into the Docker Engine, and allow you to run the server.

Next, you may wish to update the genkeys.sh with your own information, and build the
keys that will be used by the cherrypyserver every time::

  update server_openssl.conf
  mkdir keys
  ./genkey.sh
  

If you make modifications, and wish to rebuild the cherrypyserver, then
from this directory, run::
  ./build.sh

Installing the Todos App Example
--------------------------------

To install the example, first create a new empty directory where you will store the 
app files.  Change to this directory, and then run::
  todos_app_example

This will copy the todos app into your directory, and it will be ready to run.

Running the Example
-------------------
    
To run the example, it is now necessary to run the two pieces of the server and then hit
the server with your web browser.  It does not matter what order you start the two web
server pieces in.

You may run the cherrypywebserver in two ways.  Change to the cherrypywebserver directory
from the earlier step where it was built, and execute either of the following two scripts::
  ./interactive_run.sh
  ./run.sh

If you run the interactive_run.sh script, you will need to start the web server in the
container manually by running::
  ./serve.py

In interactive mode you can also examine the files, and even make modifications to them
with vi.

To run the app piece of the example, change to the directory where you copied the todos
app files, and run::
  ./app.py -p5555 -i10.0.2.15

It is possible that the ip address will not match your docker container.  You should
change it to match eth0 from the ifconfig if it does not.

Now that the two pieces of the server are running, you can hit the app with your web 
browser.  Type the following url::
  https://10.0.2.15:8443/

Your ip address may vary.  It should match eth0 from your ifconfig.

Once you have hit the web page, you will get a self-signed certificate warning the first time.
If you have not done the "update the genkeys.sh" step, then every time you run the server it will regenerate
the self signed keys.  However, if you have performed that step, then the keys will be preserved
from run to run.

Resolve the certificate warning according to your web browsers instructions, and then
you should see an input box with a "Add Todo" button beside it::
  Type something
  press tab
  press enter

Your new todo item should appear at the top of the page!  Congratulations!

Stopping the Example
--------------------

To shut down the todos app, just press Ctrl-C.

To shut down the cherrypyserver container, it may be slightly more difficult.  It may not
stop with Ctrl-C.  This is another thing that needs to be looked at.  For the moment, 
you can kill it::
  sudo docker ps

There should be a hex number appearing at the beginning of the line showing cherrypyserver.
copy and paste this hex number into the docker kill command like so::
  sudo docker kill 5a347ceb9583


