#!/bin/bash

path_python3=$(which python3)
user=$(whoami)
line="$user ALL=(root) NOPASSWD:$path_python3"
file='/etc/sudoers'
line_num=$(sudo awk '/%sudo/{print NR}' $file)
line_num=`expr $line_num + 1` 
sudo sed -i "$line_num i $line" $file

path_nohup=$(which nohup)
line_="$user ALL=(root) NOPASSWD:$path_nohup"
file_='/etc/sudoers'
line_num_=$(sudo awk '/%sudo/{print NR}' $file_)
line_num_=`expr $line_num_ + 1` 
sudo sed -i "$line_num_ i $line_" $file_
