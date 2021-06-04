#!/bin/bash
cd $(pwd)
if [[ ! -f conf.txt ]]
then
    sudo apt install nautilus-admin -y
	sudo apt-get install python3.8 -y
	sudo apt-get install python3-tk -y
	sudo apt-get install python3-crontab -y
	sudo apt-get install gir1.2-appindicator3-0.1 -y
	sudo install -Dm 644 etc/modprobe.d/ec_sys.conf $(pwd)/etc/modprobe.d/ec_sys.conf
	sudo install -Dm 644 etc/modules-load.d/ec_sys.conf $(pwd)/etc/modules-load.d/ec_sys.conf
fi
