#!/bin/bash

# Is this a good idea? Shouldn't this be up to the package?
# Doesn't this depend on the distro using systemd?
install etc/modprobe.d/ec_sys.conf /etc/modprobe.d/ec_sys.conf
install etc/modules-load.d/ec_sys.conf /etc/modules-load.d/ec_sys.conf
# Shouldn't this be managed in the python code?
modprobe ec_sys write_support=1
if [ -f "/bin/pacman" ]; then 
    # Arch ships many popular python packages
    # These are generally preferred over installing through pip
    pacman -Sy python-psutil tk
else if [ -f "/bin/apt-get" ]; then
    #apt install -y 
    echo "apt packages unknown, please add to install_deps.sh!"
    # If apt has a package for python's psutil, this is preferred over pip!
    #pip install psutil
else
    echo "Unknown package manager, please add to install_deps.sh!"
fi
