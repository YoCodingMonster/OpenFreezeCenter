# OpenFreezeCenter (OFC)
- Provides a UI and automated scripts in order to control MSI Laptops
- Made for Linux, as MSI does not have a native Linux client.
- if you do now want to run the GUI or if it is not working for you then try
  # OpenFreezeCenter-Lite (OFC-l)
  - Same thing just without GUI
  - https://github.com/YoCodingMonster/OpenFreezeCenter-Lite

# INSTALLATION
- Creating virtual environment. the path i will be using is ```/home/pm/Desktop/OFC```. Here ```OFC``` is the folder with script.
  ```
  python3 -m pip install --user virtualenv
  python3 -m venv /home/pm/Desktop/OFC
  cd /home/pm/Desktop/OFC
  ```
- Install ```ECTweaker``` library
  ```
  bin/pip3 install ectweaker
  ```
- Install ```PyGObject``` library
  ```
  sudo apt install libgirepository1.0-dev gcc libcairo2-dev pkg-config python3-dev gir1.2-gtk-4.0
  bin/pip3 install pycairo
  bin/pip3 install PyGObject
  ```
- Make sure ```secure boot``` is disabled.

# First time prepration
- Opening virtual environment. the path i will be using is ```/home/pm/Desktop/OFC```. Here ```OFC``` is the folder with script.
  ```
  cd /home/pm/Desktop/OFC
  sudo nohup bin/python3 OFC.py
  ```
- There are 2 outcomes.
  - If the EC read/write is not enabled on your OS, the system will enable it and restart and follow up with the second point.
  - If the EC read/write is enabled on your OS, the script will generate ```config.py``` file, which contains the configuration for fan curves and their addresses.
- DONE!

# Running after first time
- Opening virtual environment. the path i will be using is ```/home/pm/Desktop/OFC```. Here ```OFC``` is the folder with script.
  ```
  cd /home/pm/Desktop/OFC
  sudo nohup bin/python3 OFC.py
  ```
- Close the terminal and enjoy!!

## Supported Laptop models (tested)
- MSI GP76 11UG

## Supported Linux Distro (tested)
- Ubuntu

## Issue format
- ISSUE # [CPU] - [LAPTOP MODEL] - [LINUX DISTRO]
  - ```Example``` ISSUE # i7-11800H - MSI GP76 11UG - UBUNTU 23.05

## Feedback
- Please provide suggestions under the Feedback discussion tab!

## Goals
- [X] Fan Control GUI
- [X] Basic temperature and RPM monitoring
- [ ] Advanced and Basic GUI curve control
- [ ] Battery Threshold
- [ ] Webcam control
