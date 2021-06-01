# OpenFreezeCenter - WIP

An MSI Dragon Center replacement for Linux. Used to control fan speed profiles on some MSI Laptops.

- This project will be weekly Updated!
- For more features do comment and share your views!
- Well if you like my work, a cup of coffee would be nice!!

- This Application can run on any Linux distro with python3 installed!!
- Installation is very easy with almost one click solution!!

# Installation

Install dependencies and clone/download this repository.

```bash
sudo apt get update && sudo apt install python3 python3-ttkthemes python3-tk
```

```bash
git pull https://github.com/YoCodingMonster/MSI-Dragon-Center-for-Linux-OpenFreezeCenter
```

### Secure boot must be disabled for this to function correctly

# Usage

OpenFreezeCenter can be run through the command line, or through the GUI.

```bash
python main.py --help
```

To launch the GUI.

```bash
python main.py --gui
```

To change the current mode. See configuration for avaliable modes. Requires root.

```bash
sudo python main.py --mode {MODE}
```

To get the current system stats GPU/CPU fan RPMs and Temps. Requires root.

```bash
sudo python main.py --stats
```

# Configuration

The configuration file can be found in ~/.config/OpenFreezeCenter/config.toml

```
[settings]
mode = 0
offset = 0
vr_custom = [13, 45, 50, 60, 72, 80, 85, 100, 0, 50, 60, 72, 80, 85, 100]

[ui]
dark_mode_enabled = false
```

Avaliable modes:

- 0 - Auto
- 1 - Basic
- 2 - Advanced/custom
- 3 - Cooler Boost

# For any issue and query comment!

# Working on models

- MSI GE66 (Ubuntu based OS)
- MSI GS65 (Ubuntu based OS)
- HELP ME ADD MORE MODELS. TEST AND REPORT ME

# Goals

```

- Basic GUI Done
- Fan Control with GUI Done
- Auto, Basic, Advanced, Cooler Booster Done
- Basic temperature and RPM monitoring Done
- One click install Done
- Dark Mode Done
- Configuration file Done
- Back version support Done
- Making Pre-required installs automatic In Beta Testing
- Graph to monitor Temps and speeds In alpha Testing
- integrating it in a widget in power menu In alpha Testing

```

# Known Bugs :- 4

## Unfixed :- 0

-

## Fixed :- 4

- (CLOSED) Battery indicator shown 0 When applying fan modes
- (CLOSED) Button was not visible
- (CLOSED) Install errors
- (CLOSED) Installation on other distro like fedora and arch now working

```

```
