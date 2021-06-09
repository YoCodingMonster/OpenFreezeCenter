#!/bin/bash
if [[ ! -f conf.txt ]]
then
	sudo GRUB_CMDLINE_LINUX_DEFAULT="quiet ec_sys.write_support=1"
	sudo install -Dm 644 etc/modprobe.d/ec_sys.conf $(pwd)/etc/modprobe.d/ec_sys.conf
	sudo install -Dm 644 etc/modules-load.d/ec_sys.conf $(pwd)/etc/modules-load.d/ec_sys.conf
	sudo modprobe ec_sys write_support=1
	sudo apt install nautilus -y
    sudo apt install nautilus-admin -y
	sudo apt-get install python3.8 -y
	sudo apt-get install python3.8-tk -y
	sudo apt-get install gir1.2-appindicator3-0.1 -y
fi
