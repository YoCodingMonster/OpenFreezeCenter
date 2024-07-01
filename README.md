# OpenFreezeCenter (OFC)
- Provides a UI and automated scripts in order to control MSI Laptops. Check the #Supported section to see what models are supported.
- Made for Linux, as MSI does not have a native Linux client.
- if you do now want to run the GUI or if it is not working for you then try
  # OpenFreezeCenter-Lite (OFC-l)
  - Same thing just without GUI
  - https://github.com/YoCodingMonster/OpenFreezeCenter-Lite

# INSTALLATION / UPDATING
- ```cd``` into the download folder and execute (UBUNTU)
  - ```chmod +x file_1.sh```
  - ```chmod +x file_2.sh```
  - ```chmod +x install.sh```
- Now run the ```install.sh```, That will install all the dependencies and create a virtual python environment on desktop for the script to work.
- (ONLY FOR INSTALLATION) ```Reboot``` after the script complete the first run.

# RUNNING
- Run ```install.sh``` from the desktop folder. 

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
- [ ] Advanced & Basic GUI control
- [X] Battery Threshold
- [ ] Webcam control
