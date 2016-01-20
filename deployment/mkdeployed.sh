rm -rf tempoldsource
mkdir tempoldsource
cp -rf deployed/cherrypyserver/keys tempoldsource
rm -rf deployed/cherrpyserver
rm -rf deployed/domsocket
rm -rf deployed/scripts
rm -rf deployed/style
rm -rf deployed/apps
rm -rf deployed/temp

if [ ! -e deployed ]
    then mkdir deployed
fi
if [ ! -e deployed/cherrypyserver ]
    then mkdir deployed/cherrypyserver
fi
if [ ! -e deployed/cherrypyserver/keys ]
    then mkdir deployed/cherrypyserver/keys
fi
mkdir deployed/domsocket
mkdir deployed/scripts
mkdir deployed/style
mkdir deployed/apps
if [ ! -e deployed/toolkits ]
    then mkdir deployed/toolkits
fi
mkdir deployed/temp

cp -rf source/cherrypyserver/* deployed/cherrypyserver/
cp -rf source/config deployed/apps
mv deployed/apps/config/config.conf deployed/apps
mv deployed/apps/config/config.html deployed/apps
cp -rf source/domsocket deployed
cp -rf source/scripts deployed

cp -rf tempoldsource/keys deployed/cherrypyserver

cd deployed/cherrypyserver
ip="$(ifconfig | grep -A 1 'eth0' | tail -1 | cut -d ':' -f 2 | cut -d ' ' -f 1)"
./updateconfigipaddresses.sh $ip

if [ ! -e keys/server.crt ]
    then ./genkey.sh
else
    echo "Not regenerating keys"
fi


