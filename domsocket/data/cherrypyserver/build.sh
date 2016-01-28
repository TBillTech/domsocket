if [ -e CherryPy-4.0.0.tar.gz ] 
then
    if [ -e WebSocket-for-Python-0.3.4.tar.gz ] 
    then
	echo "CherryPy-4.0.0.tar.gz and WebSocket-for-Python-0.3.4.tar.gz found."
    else
        echo "WebSocket-for-Python-0.3.4.tar.gz must exist in current dir prior to building for first time.  Docker build may not succeed."
    fi
else
    echo "CherryPy-4.0.0.tar.gz must exist in current dir prior to building for first time.  Docker build may not succeed."
fi

sudo docker build -t cherrypyserver . 
