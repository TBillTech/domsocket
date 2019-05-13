cp /keys_volume/* keys/
if [ -e keys/server.csr ]
    then
        echo "Not generating keys"
    else
        openssl genrsa -out keys/server.crtkey 1024
        openssl req -new -config server_openssl.conf -out keys/server.csr
        openssl x509 -req -days 365 -in keys/server.csr -signkey keys/server.crtkey -out keys/server.crt
fi
