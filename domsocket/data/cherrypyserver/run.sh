sudo docker run -v $PWD/keys:/keys_volume:ro --net="host" tbilltechrep/cherrypyserver ./serve.py --server_ip 0.0.0.0 --zmq_bind_ip "*" --server_port 8443 --zmq_port 5555
