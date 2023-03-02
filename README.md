# Back on this Project from 1 March 2023!!

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
# Official name :- Open Freeze Center

- This project will be Monthly Updated!
- For more features do comment and share your views!
- Well if you like my work, Do follow me for more awesome projects!!

For Those running Linux Distro on MSI laptops. This is the Graphic User Interface application meant for Fan control and monitoring in Linux.
- This Application can run on any Linux distro!!
- Installation is very easy with one command solution!! (Most of the time XD)

### Disable SECURE BOOT because it interferes with the permission of the script to read/write to EC file.

# How To Install GUI app?
- Download the .zip from the github and extract it wherever you want
- Mark the file ```at_startup.sh``` as executable
- Open terminal inside the extracted folder and run ```sudo ./at_startup.sh```
- This will install all the dependencies which are missing and open the GUI app for the first time.
  - If the GUI did not open follow the steps below
  - Disable the Secure Boot
  - Manually install Python Libraries like
    - ```sudo apt install python3-pip -y```
    - ```sudo apt-get install python3-tk -y```
    - Check weather your Linux Kernal has ```ec_sys``` support
      - If ```no``` then copy the file from inside the [DOWNLOADED ZIP] ```modprobe.d``` and ```modules-lode.d``` to [SYSTEM] ```etc/modprobe.d/``` and ```etc/modules-load.d/ec_sys.conf```, then restart
      - If ```yes``` then add ```ec_sys write_support = 1``` line in file ```/etc/default/grub```, save and in terminal run command ```update-grub``` then reboot
- App will create ```conf.txt``` file. it will contain all your configurations and fan curve values. deleting that file will reset all your fan curves.

#How to Update?
- Just delete the older folder and work in new folder!!

# How To Run GUI app?
- Open terminal inside the extracted folder and run ```sudo ./at_startup.sh```

# Working on models
- MSI GE66
- MSI GS65
- MSI GF63
- MSI GP76
- MSI GS65 8RF
- MSI GF75 Thin 9SCXR
- HELP ME ADD MORE MODELS. TEST AND REPORT ME

# Working on Linux distro
- Ubuntu
- Pop OS
- Mint
- Kubuntu
- KDE Neon
- HELP ME ADD MORE DISTROS. TEST AND REPORT ME

# For any issue follow the guideline below
- Specify the System Specifications [CPU, GPU] and Model Number [MSI GP76 11UG].
- Write the problem with some description.
- Attach relevant screenshots.

# Goals
```
  - Basic GUI                                          Done
  - Fan Control with GUI                               Done
  - Auto, Basic, Advanced, Cooler Booster              Done
  - Basic temperature and RPM monitoring               Done
  - One click install                                  Almost Done
  - Configuration file                                 Done
  - Making Pre-required installs automatic             Almost Done
  - Integrating it as an app indicator                 Done
  - EC Map View                                        Done
  - CPU Profiles                                       Work in Progress!
  - Battery Threshold                                  Work in Progress!
```
# Unsolved Issues :- 1
- Advanced fan profile seems to not apply the curve to CPU, but GPU curve is applied but not above 90%.

# Solved Issues
- While monitoring the temps and fan speed, some of the sections are blank.
  - Turn ```on``` the 10th Gen and above option in GUI accordingly to your CPU.
