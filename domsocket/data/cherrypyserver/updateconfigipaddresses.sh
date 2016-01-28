ip="$(ifconfig | grep -A 1 'eth0' | tail -1 | cut -d ':' -f 2 | cut -d ' ' -f 1)"
cat server.conf | awk '{ sub(/10.0.0.8/, "'$ip'" ); print }' > server.conf.new
mv -f server.conf.new server.conf
cat server_openssl.conf | awk '{ sub(/10.0.0.8/, "'$ip'" ); print }' > server_openssl.conf.new
mv -f server_openssl.conf.new server_openssl.conf
