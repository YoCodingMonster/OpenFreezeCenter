# OpenFreezeCenter (OFC)
- Provides a UI and automated scripts in order to control MSI Laptops. Check the #Supported section to see what models are supported.
- Made for Linux, as MSI does not have a native Linux client.
- if you don't want to run the GUI or if it is not working for you then try
  # OpenFreezeCenter-Lite (OFC-l)
  - Same thing just without GUI
  - https://github.com/YoCodingMonster/OpenFreezeCenter-Lite

# INSTALLATION
- apt-based distros
  ```
  sudo apt install libgirepository1.0-dev gcc libcairo2-dev pkg-config python3-dev gir1.2-gtk-4.0
  ```
- dnf-based distros
  ```
  sudo dnf install python3-gobject gobject-introspection gobject-introspection-devel gcc cairo-devel pkg-config python3-devel
  ```
  
- All distros
  ```
  python -m pip install pycairo PyGObject
  ```
- Make sure secure boot is disabled.
  ```
  cd ~/Desktop/OFC
  sudo nohup python OFC.py
  ```
  - If EC read/write is not enabled, the script will enable it and reboot.
  - If EC read/write is enabled, the script will generate the ```config.py``` file, which contains the configuration for fan curves and their addresses.

# UPDATING
- Save your AUTO and ADVANCED speeds, then delete ```config.py```.
  ```
  cd ~/Desktop/OFC
  python -m pip ectweaker -U
  sudo nohup bin/python3 OFC.py
  ```
- After you have run the script and the new ```config.py``` file is created, paste the new values in the AUTO_SPEED and ADV_SPEED vales place.

# RUNNING
  ```
  sudo nohup bin/python3 OFC.py
  ```
- Close the terminal and enjoy!!

## Issue format
- ISSUE # [CPU] - [LAPTOP MODEL] - [LINUX DISTRO]
  - ```Example``` ISSUE # i7-11800H - MSI GP76 11UG - UBUNTU 23.04

## Feedback
- Please provide suggestions under the Feedback discussion tab!

## Goals
- [X] Fan Control GUI
- [X] Basic temperature and RPM monitoring
- [ ] Advanced & Basic GUI control
- [X] Battery Threshold
- [ ] Webcam control
