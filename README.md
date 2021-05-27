# MSI Dragon Center for Linux
# )fficial name :- OpenFreezeCenter

- This project will be weekly Updated!
- For more features do comment and share your views!
- Well if you like my work, a cup of coffee would be nice!!

For Those running Linux Distro on MSI laptops. This is the Graphic User Interface application meant for Fan control in Linux.
- This Application can run on any Linux distro with python3 installed!!
- Installation is very easy with almost one click solution!!

# What is Pre-Required For this to install properly?
- run this command before getting any module installed ```sudo apt update```
### Nautilus-admin
- get it by :-> ```sudo apt install nautilus-admin```
### python3 
- get it by :-> ```sudo apt-get install python3.8```
### tkinter python3 library
- get it by :-> ```sudo apt-get install python3-tk```
### crontab python3 library
- get it by :-> ```sudo apt-get install python3-crontab```
### Disable SECURE BOOT because it interferes with the permission of the script to read/write to EC file.

# NO NEED TO UNINSTALL THE PREVIOUS VERSION OF MY SOFTWARE. JUST REPLACE THE MAIN ```GUI-MSI-DC-L.PY``` FILE AND YOU ARE GOOD TO GO!!
# DO INCLUDE OTHER FILES IN SAME DIRECTORY AS ```GUI-MSI-DC-L.PY```

# How To Install GUI app?
- Download the .zip from the github and extract it wherever you want
- After making the above requirements available manually. open terminal inside the extracted folder ```MSI-Deagon-Center-for-Linux``` directory and run.
- ```./at_startup.sh```
- This will open the GUI app for the first time.
- App will create ```conf.txt``` file. it will contain all your configurations and fan curve values. deleting that file will reset all your fan curves.

# For any issue and query comment!

# Working on models
- MSI GE66 (Ubuntu based OS)
- MSI GS65 (Ubuntu based OS)
- HELP ME ADD MORE MODELS. TEST AND REPORT ME

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
  - Making Pre-required installs automatic             In Beta Testing
  - Graph to monitor Temps and speeds                  In alpha Testing
  - integrating it in a widget in power menu           In alpha Testing
```

# Known Bugs :- 4
## Unfixed :- 0
-
## Fixed :- 4
- (CLOSED) Battery indicator shown 0 When applying fan modes
- (CLOSED) Button was not visible
- (CLOSED) Install errors
- (CLOSED) Installation on other distro like fedora and arch now working
