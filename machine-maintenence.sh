#!/bin/bash

if [ $# -eq 0 ]; then

    cat << EOF
usage: machine-maintenance.sh [-h] [-m MODE] [-g] [-s] [-b BATTERY]

MSI Open Freeze Center

optional arguments:
  -h, --help            show this help message and exit
  -m MODE, --mode MODE  The fan profile mode to use. 0 for Auto, 1 for Basic, 2 for Advanced, and 3 for COOLER BOOST.
  -g, --gui             To launch the GUI.
  -s, --stats           Standard outs the stats
  -b BATTERY, --battery BATTERY
                        Set charging threshold between 20 and 100

Controls fan speed and battery threshold profiles
EOF

    exit 1
fi

PROJECT_PATH=$(cd $(dirname $(test -L "$0" && readlink "$0" || echo "$0")) && pwd)

cd "${PROJECT_PATH}"

source "./venv/bin/activate"

python main.py $@