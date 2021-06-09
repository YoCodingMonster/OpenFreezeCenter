#!/bin/sh
./install_deps.sh >/dev/null 2>&1
python3 indicator.py >/dev/null 2>&1 & exit
