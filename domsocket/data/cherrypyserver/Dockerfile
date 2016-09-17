FROM alpine:3.3
LABEL Description="This image runs a simple websocket server with a domsocket app back end."
EXPOSE 80 443 8443 8444 8445 8446 8080 8081 8082 8083 5555 5556 5557 5558
RUN apk add --update \
    python \
    openssl \
 && apk add --update \
    --repository http://dl-4.alpinelinux.org/alpine/edge/community \
    --repository http://dl-4.alpinelinux.org/alpine/edge/testing \
    py2-zmq \
    py-cherrypy \
 && rm -rf /var/cache/apk/* \
 && mkdir /opt \
 && mkdir /opt/server \
 && mkdir /opt/server/css \
 && mkdir /opt/server/keys \
 && mkdir /keys_volume \
 && mkdir /opt/server/scripts \
 && mkdir /opt/server/static \
 && mkdir /opt/server/style \
 && mkdir /opt/server/temp \
 && mkdir /opt/server/toolkits \
 && mkdir /tmp/tarballs \
 && mkdir /tmp/tarballs/CherryPy \
 && mkdir /tmp/tarballs/WebSocket \
 && adduser -D webserver 
ADD WebSocket-for-Python-0.3.4.tar.gz /tmp/tarballs/WebSocket/
WORKDIR /tmp/tarballs/WebSocket/WebSocket-for-Python-0.3.4/
#VOLUME ["/keys_volume"]
RUN python setup.py install \ 
 && rm -rf /tmp/tarballs/* 
COPY *.sh /opt/server/
COPY *.conf /opt/server/
COPY *.conf.template /opt/server/
COPY *.py /opt/server/
RUN chown webserver /opt/server \
 && chgrp webserver /opt/server \
 && chown webserver /opt/server/* \
 && chgrp webserver /opt/server/* 
USER webserver
WORKDIR /opt/server
CMD ["python", "serve.py"]
