#!/bin/bash

install etc/modprobe.d/ec_sys.conf /etc/modprobe.d/ec_sys.conf
install etc/modules-load.d/ec_sys.conf /etc/modules-load.d/ec_sys.conf
modprobe ec_sys write_support=1
apt install python3-pip - y
apt-get install python3-tk -y
pip3 install psutil -y
apt-get install gir1.2-appindicator3-0.1 -y
GRUB_CMDLINE_LINUX_DEFAULT="quiet ec_sys.write_support=1"
