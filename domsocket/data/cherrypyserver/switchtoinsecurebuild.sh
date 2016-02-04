chmod a+x *.sh
mv server.insecure.conf server.conf
cat build.sh | awk '{ sub(/cherrypyserver/, "cherrypyinsecureserver" ); print }' > build.sh.new
mv -f build.sh.new build.sh
cat run.sh | awk '{ sub(/cherrypyserver/, "cherrypyinsecureserver" ); print }' > run.sh.new
mv -f run.sh.new run.sh
cat interactive_run.sh | awk '{ sub(/cherrypyserver/, "cherrypyinsecureserver" ); print }' > interactive_run.sh.new
mv -f interactive_run.sh.new interactive_run.sh
chmod a+x *.sh
