#!/bin/bash

install etc/modprobe.d/ec_sys.conf /etc/modprobe.d/ec_sys.conf
install etc/modules-load.d/ec_sys.conf /etc/modules-load.d/ec_sys.conf
modprobe ec_sys write_support=1
sudo pacman -S python-pip tk --noconfirm
pip3 install psutil
#apt-get install gir1.2-appindicator3-0.1 -y
GRUB_CMDLINE_LINUX_DEFAULT="quiet ec_sys.write_support=1"
