#!/usr/bin/env python3

# Handles installing and checking for installation of the driver

import os
import sys


def is_installed():
    check = os.path.exists("/etc/modprobe.d/GUI-MSI-DC-L-ec_sys.conf")
    return check


def install():
    command = os.system(
        'x-terminal-emulator -e \'bash -c "sudo install -Dm 644 etc/modprobe.d/GUI-MSI-DC-L-ec_sys.conf "${pkgdir}/etc/modprobe.d/GUI-MSI-DC-L-ec_sys.conf" && sudo install -Dm 644 etc/modules-load.d/GUI-MSI-DC-L-ec_sys.conf "${pkgdir}/etc/modules-load.d/GUI-MSI-DC-L-ec_sys.conf"; exec bash"\''
    )

    if command == 0:
        return True
    else:
        return False


def uninstall():
    command = os.system(
        "x-terminal-emulator -e 'bash -c \"sudo rm /etc/modprobe.d/GUI-MSI-DC-L-ec_sys.conf /etc/modules-load.d/GUI-MSI-DC-L-ec_sys.conf; exec bash\"'"
    )

    if command == 0:
        return True
    else:
        return False
