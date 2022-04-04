# Next version release on jan 20th at 12:00PM should resolve most of the issues!!

# ```Working on MSI Center software and making laptops with this software respond to calls from same script!!```

# Brand New UI. Now work as App Indicator
# SCREENSHOTS
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

# MSI Dragon Center for Linux
# Official name :- OpenFreezeCenter

- This project will be weekly Updated!
- For more features do comment and share your views!
- Well if you like my work, do follow me for more awesome projects!!

For those running a Linux distro on MSI laptops. This is the Graphic User Interface application meant for fan control and monitoring in Linux.
- This Application can run on any Linux distro!!
- Installation is very easy with one command solution!!

### Disable SECURE BOOT because it interferes with the permission of the script to read/write to EC file.

# .DEB package comming soon, till then delete previous versions of the application by deleting the directory and replacing it with the new release you download. Reinstall is not required and will be only done the first time automatically! thanks to # @Special-Niewbie

# How To Install GUI app?
- Download the .zip from the github and extract it wherever you want
- Open terminal inside the extracted folder and run ```./at_startup.sh```
- This will install all the dependencies which are missing and open the GUI app for the first time.
- App will create ```conf.txt``` file. it will contain all your configurations and fan curve values. deleting that file will reset all your fan curves.

# How To Run GUI app?
- Open terminal inside the extracted folder and run ```./at_startup.sh```

# For any issue follow the guideline below
- Specify the System Specifications [CPU, GPU] and Model Number [MSI GP76 11UG].
- Write the problem with some description.
- Attach relevant screenshots.

# Working on models
- MSI GE66
- MSI GS65
- MSI GF63
- MSI GP76 (11th Gen Intel)
- HELP ME ADD MORE MODELS. TEST AND REPORT ME

# Working on Linux distro
- Ubuntu
- Pop OS
- Mint
- Kubuntu
- HELP ME ADD MORE DISTROS. TEST AND REPORT ME

# Goals
```
  - Basic GUI                                          Done
  - Fan Control with GUI                               Done
  - Auto, Basic, Advanced, Cooler Booster              Done
  - Basic temperature and RPM monitoring               Done
  - One click install                                  Done
  - Dark Mode                                          Done
  - Configuration file                                 Done
  - Back version support                               Done
  - Making Pre-required installs automatic             Done
  - Integrating it as an app indicator           	     Done
  - EC Map View                                        Done
  - Debian Package                                     In Beta Testing -> thanks to @Special-Niewbie
  - Graph to monitor Temps and speeds                  In beta Testing
  - Dual GPU support                                   In beta Testing
  - 
```
# Known Bugs :- 1
- If you are not able to see the Speed of CPU fan but the percentage is showing perfectely fine, then do enable the ```Intel 11Th gen``` and report me and tell the generation of your processor!!. The 11th gen tag is alone write now, 10th gen please do check and confirm!!
