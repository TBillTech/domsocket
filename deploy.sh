rm -rf tempoldgrail
mkdir tempoldgrail
cp -rf grail/cherrypyserver/keys tempoldgrail
rm -rf grail/cherrpyserver
rm -rf grail/domsocket
rm -rf grail/scripts
rm -rf grail/apps
rm -rf grail/temp

if [ ! -e grail ]
    then mkdir grail
fi
if [ ! -e grail/cherrypyserver ]
    then mkdir grail/cherrypyserver
fi
if [ ! -e grail/cherrypyserver/keys ]
    then mkdir grail/cherrypyserver/keys
fi
mkdir grail/domsocket
mkdir grail/scripts
mkdir grail/apps
if [ ! -e grail/toolkits ]
    then mkdir grail/toolkits
fi
mkdir grail/temp

cp -rf grailsource/cherrypyserver/* grail/cherrypyserver/
cp -rf grailsource/IDE grail/apps
mv grail/apps/IDE/IDE.conf grail/apps
mv grail/apps/IDE/IDE.html grail/apps
cp -rf grailsource/domsocket grail
cp -rf grailsource/scripts grail

cp -rf tempoldgrail/keys grail/cherrypyserver

if [ ! -e grail/toolkits/wrapbootstrapCoreAdmin ]
    then ./setupcoreadmintoolkit.sh
else
    echo "wrapbootstrap Core Admin already present"
fi

cd grail/cherrypyserver
ip="$(ifconfig | grep -A 1 'eth0' | tail -1 | cut -d ':' -f 2 | cut -d ' ' -f 1)"
./updateconfigipaddresses.sh $ip

if [ ! -e keys/server.crt ]
    then ./genkey.sh
else
    echo "Not regenerating keys"
fi


