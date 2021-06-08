#!/bin/sh
cd $(pwd)
sudo modprobe ec_sys write_support=1
nohup ./install_deps.sh >/dev/null 2>&1
nohup python3 indicator.py >/dev/null 2>&1 & exit
