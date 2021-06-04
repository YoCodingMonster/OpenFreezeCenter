#!/bin/sh
cd $(pwd)
nohup ./install_deps.sh >/dev/null 2>&1
nohup python3 indicator.py >/dev/null 2>&1 & exit