#!/bin/bash

path_python3=$(which python3)
user=$(whoami)
line="$user ALL=(root) NOPASSWD:$path_python3"
file='/etc/sudoers'
line_num=$(sudo awk '/%sudo/{print NR}' $file)
line_num=`expr $line_num + 1` 
sudo sed -i "$line_num i $line" $file
