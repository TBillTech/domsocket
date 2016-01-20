cat server.conf | awk '{ sub(/443/, "8443" ); print }' > server.conf.new
mv -f server.conf.new server.conf

