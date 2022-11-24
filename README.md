# OpenFreezeCenter
###### *MSI Dragon Center for Linux*
##### Notice: Next version is planned for the 20th of January. It should resolve most of the issues.
---
## Features
- Lives in system tray
- Allows setting static fan speed
- Allows setting fan curves
- Allows setting battery charge limit

---
## Screenshots
#### Main application
![Screenshot of main application](https://github.com/YoCodingMonster/OpenFreezeCenter/blob/a9af1fe3d027d6e2af8ceef4a0c62e2735c12e83/Screenshot%20from%202021-06-10%2004-16-03.png)

#### Expanded basic nenu
![Basic menu](https://github.com/YoCodingMonster/OpenFreezeCenter/blob/a9af1fe3d027d6e2af8ceef4a0c62e2735c12e83/Screenshot%20from%202021-06-10%2004-16-07.png)

#### Expanded battery nenu
![Battery menu](https://github.com/YoCodingMonster/OpenFreezeCenter/blob/a9af1fe3d027d6e2af8ceef4a0c62e2735c12e83/Screenshot%20from%202021-06-10%2004-16-10.png)

#### Advanced fan curve window
![Advanced fan curve control](https://github.com/YoCodingMonster/OpenFreezeCenter/blob/f1905b95af32f66c629c22eb68a1ce6130c9164f/Screenshot%20from%202021-06-10%2004-44-41.png)

#### Monitoring window
![Monitoring](https://github.com/YoCodingMonster/OpenFreezeCenter/blob/a9af1fe3d027d6e2af8ceef4a0c62e2735c12e83/Screenshot%20from%202021-06-10%2004-16-24.png)

#### EC map window
![EC map display](https://github.com/YoCodingMonster/OpenFreezeCenter/blob/a9af1fe3d027d6e2af8ceef4a0c62e2735c12e83/Screenshot%20from%202021-06-10%2004-16-36.png)

---
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
  - [x] Dark mode
  - [x] Configuration file
  - [x] Back version support
  - [x] Making pre-required installs automatic
  - [x] Integrating it as an app indicator
  - [x] EC Map View
  - [ ] Graph to monitor Temps and speeds (In beta testing)
  - [ ] Dual GPU support (in beta testing)
  - [ ] Debian package (in beta testing, thanks @Special-Niewbie)
  - [ ] AUR PKGBUILD (@TheArcaneBrony will do after refactor)
```
## Known Bugs
- If you're unable to see CPU fan speed, but the percentage is showing correctly, enable `Intel 11th gen` support in the menu and report back with your processor's generation!