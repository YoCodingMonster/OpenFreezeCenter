# OpenFreezeCenter (OFC)

Fan profiles, temperature monitoring and battery charge limiting for MSI
laptops on Linux, since MSI ships no Linux client of its own.

- **Fan profiles** — Auto, Basic (the auto curve shifted by an offset) and
  Advanced (your own curve), plus Cooler Booster as an independent toggle.
- **Fan curve editor** — set all seven CPU and seven GPU points in the app.
- **Live monitoring** — 60 seconds of CPU/GPU temperature history, with
  current, minimum, maximum and fan RPM.
- **Battery charge limit** — stop charging between 50% and 100%.

Prefer no GUI at all? [OpenFreezeCenter-Lite](https://github.com/YoCodingMonster/OpenFreezeCenter-Lite)
does the same job from the command line.

| | |
|---|---|
| ![Main window](screenshots/02-main-light.png) | ![Fan curve editor](screenshots/04-fan-curves.png) |

## Requirements

- Python 3.8+, PyGObject, **GTK 4.14 or newer**, **libadwaita 1.4 or newer**
- polkit (for the privilege prompt)
- A kernel with the `ec_sys` module (every mainstream kernel has it)
- Secure Boot disabled, so the module can be loaded
- `sudo`

GTK 4.14 is the binding constraint — the charts use the GSK path API added in
that release. In practice that means:

| Distribution | Works? |
|---|---|
| Ubuntu 24.04 LTS and newer | yes |
| Debian 13 (trixie) and newer | yes |
| Fedora 40 and newer | yes |
| Arch, openSUSE Tumbleweed | yes |
| Ubuntu 23.10, Fedora 39 | no — libadwaita is new enough, GTK is not |
| Ubuntu 22.04 LTS, Debian 12 | no — both too old |
| RHEL / Rocky / Alma 9 | no |

`install.sh` checks both versions and stops with an explanation rather than
installing something that would crash on the first redraw.

On anything older, use
[OpenFreezeCenter-Lite](https://github.com/YoCodingMonster/OpenFreezeCenter-Lite),
which has no GUI and therefore no GTK requirement at all.

## Installation

Download and unpack the release, then, **as your normal user**:

```bash
chmod +x install.sh
./install.sh
```

It installs the dependencies, enables EC read/write, and puts the application
in `/opt/openfreezecenter` with a launcher and a desktop entry. Re-run it any
time to update. If the EC could not be enabled without a reboot the script
says so — Disable SecureBoot, reboot, then start the app.

To remove everything it installed:

```bash
./install.sh --uninstall
```

## Running

Launch **Open Freeze Center** from your applications menu, or:

```bash
openfreezecenter
```

It asks for your password through polkit, because reading and writing the
embedded controller needs root.

To look around the interface on any machine, with no hardware involved:

```bash
openfreezecenter --simulate
```

## Settings

Settings live in `~/.config/openfreezecenter/config.json`, owned by you rather
than root. A `config.py` from an older version is migrated automatically on
first run and left behind as `config.py.migrated`.

The `hardware` section holds the EC register addresses. Only touch it if you
are porting a model that is not listed below — and please open a pull request
if you get one working.

## Upgrading from version 5 or earlier

- Your old `config.py` is imported automatically; nothing to do by hand.
- **Cooler Booster is now a switch, not a fourth profile.** It layers on top of
  whichever profile is selected, so you can leave Advanced set and still boost.
- **Basic now means "the auto curve plus an offset"**, which is what the old
  config comment described. The previous build applied the offset to an
  all-zero curve instead, so Basic drove the fans to roughly the offset value
  at every temperature — near-silent, and much hotter than intended.
- The virtual environment on the Desktop is gone; the app uses the system
  PyGObject. `install.sh --uninstall` does not remove the old `~/Desktop/OFC`
  folder, so delete that yourself once you are happy.

## Supported laptop models (tested)

- MSI GP76 11UG

## Supported Linux distributions (tested)

- Ubuntu

## Issue format

`ISSUE # [CPU] - [LAPTOP MODEL] - [LINUX DISTRO]`

Example: `ISSUE # i7-11800H - MSI GP76 11UG - UBUNTU 24.04`

## Feedback

Please put suggestions under the Feedback discussion tab.

## Goals

- [X] Fan control GUI
- [X] Temperature and RPM monitoring
- [X] Advanced & Basic GUI control
- [X] Battery threshold

## AI had been used to do proper documentations, script commenting and assisted in the UI layouts too!
