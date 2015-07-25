rm -rf deployed/test

./mkdeployed.sh
cp -rf source/tester deployed/apps
mv deployed/apps/tester/tester.conf deployed/apps
mv deployed/apps/tester/tester.html deployed/apps

cp -rf source/test deployed

cd deployed/cherrypyserver
ip="$(ifconfig | grep -A 1 'eth0' | tail -1 | cut -d ':' -f 2 | cut -d ' ' -f 1)"
./updateconfigipaddresses.sh $ip
./switchtoport8443.sh
cd ..

mv test/runtests.py .
./runtests.py
