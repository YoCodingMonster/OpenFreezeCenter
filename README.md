# OpenFreezeCenter
###### *MSI Dragon Center for Linux*
---
##### Notice: Next version is planned for the 20th of January. It should resolve most of the issues.

## Features
---
- Lives in system tray
- Allows setting static fan speed
- Allows setting fan curves
- Allows setting battery charge limit

## Screenshots
---
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


## Important notices
- Disable secure boot because it interferes with the permission of the script to read/write to EC file.
- Packages comming soon
- Deleting `conf.txt` will delete your fan curves and other configuration data.

## How to install?
You can't install this application yet, see below!

## How to run?
Open a terminal inside the extracted folder and run `sudo python3 indicator.py`

## Reporting bugs
- Specify your system information
  - Example: *MSI GF75 Thin 9SC, i7-9750h, GTX 1650*
- Describe your issue
- Attach relevant screenshots

## Known working models
- MSI GE66
- MSI GS65
- MSI GF63
- MSI GP76 (11th Gen Intel)
- MSI GF75 Thin 9SC (partial: no fan control besides cooler boost, fan speed is wrong)
- *If the application works on yours and isn't listed, let me know!*

## Known working distros
- Ubuntu
- Pop OS
- Mint
- Kubuntu
- *If the application works on yours and isn't listed, let me know!*

## Goals
```
  - [x] Basic GUI
  - [x] Fan Control with GUI
  - [x] Auto, Basic, Advanced, Cooler Booster
  - [x] Basic temperature and RPM monitoring
  - [x] One click install
  - [x] Dark Mode
  - [x] Configuration file
  - [x] Back version support
  - [x] Making Pre-required installs automatic
  - [x] Integrating it as an app indicator
  - [x] EC Map View
  - [ ] Debian Package (in beta testing, thanks @Special-Niewbie)
  - [ ] Graph to monitor Temps and speeds (In beta testing)
  - [ ] Dual GPU support (in beta testing)
  - 
```
## Known Bugs
- If you are not able to see the Speed of CPU fan but the percentage is showing perfectely fine, then do enable the ```Intel 11th gen``` and let me know and tell the generation of your processor!!. The 11th gen tag is alone write now, 10th gen please do check and confirm!!
