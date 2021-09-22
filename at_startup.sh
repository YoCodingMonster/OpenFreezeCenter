#!/bin/sh
BASEDIR=$(dirname $0)
python3 ${BASEDIR}/indicator.py >/dev/null 2>&1 & exit
