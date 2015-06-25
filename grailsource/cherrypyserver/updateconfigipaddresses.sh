cat server.conf | awk '{ sub(/10.0.0.8/, "'$1'" ); print }' > server.conf.new
mv -f server.conf.new server.conf
cat server_openssl.conf | awk '{ sub(/10.0.0.8/, "'$1'" ); print }' > server_openssl.conf.new
mv -f server_openssl.conf.new server_openssl.conf

if [ -e ../test/testbase.trailer.js ]
    then
    cat ../test/testbase.trailer.js | awk '{ sub(/10.0.0.8/, "'$1'" ); print }' > ../test/testbase.trailer.js.new
    mv -f ../test/testbase.trailer.js.new ../test/testbase.trailer.js
fi
