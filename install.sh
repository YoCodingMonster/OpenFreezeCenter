#!/bin/bash

install -Dm 644 etc/modprobe.d/GUI-MSI-DC-L-ec_sys.conf /etc/modprobe.d/GUI-MSI-DC-L-ec_sys.conf
install -Dm 644 etc/modules-load.d/GUI-MSI-DC-L-ec_sys.conf /etc/modules-load.d/GUI-MSI-DC-L-ec_sys.conf

mkdir -p /opt/OpenFreezeCenter

cp -rv *.py /opt/OpenFreezeCenter/