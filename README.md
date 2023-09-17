# OpenFreezeCenter-Lite
- Same thing without much hassle
- https://github.com/YoCodingMonster/OpenFreezeCenter-Lite

# OpenFreezeCenter

## Overview
**OpenFreezeCenter** provides a UI and automated scripts in order to control MSI Laptops. Check the #Supported section to see what models are supported.

Mainly made for Linux, as MSI does not have a native Linux client.

## Screenshots
<details>
<summary>Screenshots</summary>

## Main Application
![Screenshot from 2021-06-10 04-16-03.png](https://github.com/YoCodingMonster/OpenFreezeCenter/blob/a9af1fe3d027d6e2af8ceef4a0c62e2735c12e83/Screenshot%20from%202021-06-10%2004-16-03.png)

## Expanded Basic Menu
![Screenshot from 2021-06-10 04-16-07.png](https://github.com/YoCodingMonster/OpenFreezeCenter/blob/a9af1fe3d027d6e2af8ceef4a0c62e2735c12e83/Screenshot%20from%202021-06-10%2004-16-07.png)

## Expanded Battery Menu
![Screenshot from 2021-06-10 04-16-10.png](https://github.com/YoCodingMonster/OpenFreezeCenter/blob/a9af1fe3d027d6e2af8ceef4a0c62e2735c12e83/Screenshot%20from%202021-06-10%2004-16-10.png)

## Advanced Fan curve Window
![Screenshot from 2021-06-10 04-44-41.png](https://github.com/YoCodingMonster/OpenFreezeCenter/blob/f1905b95af32f66c629c22eb68a1ce6130c9164f/Screenshot%20from%202021-06-10%2004-44-41.png)

## Monitoring Window
![Screenshot from 2021-06-10 04-16-24.png](https://github.com/YoCodingMonster/OpenFreezeCenter/blob/a9af1fe3d027d6e2af8ceef4a0c62e2735c12e83/Screenshot%20from%202021-06-10%2004-16-24.png)

## EC Map Window
![Screenshot from 2021-06-10 04-16-36.png](https://github.com/YoCodingMonster/OpenFreezeCenter/blob/a9af1fe3d027d6e2af8ceef4a0c62e2735c12e83/Screenshot%20from%202021-06-10%2004-16-36.png)
</details>

## Supported Laptop models (tested)
- MSI GE66
- MSI GS65
- MSI GF63
- MSI GP76
- MSI GS65 8RF
- MSI GF75 Thin 9SCXR

## Supported Linux Distro (tested)
- Ubuntu
- debian
- Pop os!
- Fedora
- Cent OS
- Rhel
- Open Sesu
- Sles
- Arch

*More models are actively added, if your model isn't listed, check the issues tab, if there isn't a request for it already, make one.*

## Usage
### **Secure Boot MUST** be disabled, otherwise it interferes with the permission of the script to read/write to EC file.

# How To Install GUI app?
- Download the .zip from the github and extract it wherever you want
- Mark the file ```at_startup.sh``` as executable
- Open terminal inside the extracted folder and run ```sudo ./at_startup.sh```
- This will install all the dependencies which are missing and open the GUI app for the first time.
  - If the ```GUI did not open``` or ```something seems to not work``` follow the steps below
  - Disable the Secure Boot
  - Manually install Python Libraries like
    - pip
    - subprocess
    - signal
    - webbrowser
    - fileinput
    - threading
    - os
    - math
    - psutil
    - warnings
    - tkinter
  - Check weather your Linux Kernal has ```ec_sys``` support
      - If ```no``` then copy the file from inside the [DOWNLOADED ZIP] ```modprobe.d``` and ```modules-lode.d``` to [SYSTEM] ```etc/modprobe.d/``` and ```etc/modules-load.d/ec_sys.conf```, then restart
      - If ```yes``` then add ```ec_sys write_support = 1``` line in file ```/etc/default/grub```, save and in terminal run command ```update-grub``` then reboot
- App will create ```conf.txt``` file. it will contain all your configurations and fan curve values. deleting that file will reset all your fan curves.

# Updating 
- Just delete the older folder and work in new folder

## Bugs
- Advanced fan profile seems to have a lower RPM than set in GUI.

## Issue format
- Find if there is alreadfy an issue avilable for your ```LINUX DISTRO```. and comment your issue inside that with steps below.
  - If your ```LINUX DISTRO``` is not listed then make a issue with heading exactly as below.
    - ```LINUX DISTRO``` issue!
- Specify the System Specifications [CPU, GPU] and Model Number [MSI GP76 11UG] while reporting the issue.
- Write the problem with some description.
- Attach relevant screenshots.


## Goals
- [X] Fan Control with GUI
- [X] Auto, Basic, Advanced, Cooler Booster
- [X] Basic temperature and RPM monitoring
- [X] Configuration file
- [ ] Making Pre-required installs automatic for major linux branches 
- [X] Integrating it as an app indicator
- [X] EC Map View
- [ ] CPU Profiles
- [ ] Battery Threshold

