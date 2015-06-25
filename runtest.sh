rm -rf grail/test

./deploy.sh
cp -rf grailsource/tester grail/apps
mv grail/apps/tester/tester.conf grail/apps
mv grail/apps/tester/tester.html grail/apps

cp -rf grailsource/test grail

cd grail/cherrypyserver
ip="$(ifconfig | grep -A 1 'eth0' | tail -1 | cut -d ':' -f 2 | cut -d ' ' -f 1)"
./updateconfigipaddresses.sh $ip
./switchtoport8443.sh
cd ..

mv test/runtests.py .
mv test/.coveragerc .
rm -rf .coverage
./runtests.py
