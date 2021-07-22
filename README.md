# Open Freeze Center

An MSI Dragon Center replacement for Linux. Used to control fan speed profiles
on some MSI Laptops as well battery charging threshold.

- Well if you like my work, a cup of coffee would be nice!!
- This Application can run with python3 installed!!

# Warning
* **Use it at your own risk!**
* Secure boot can prevent access to the EC.
* Check that your EC (Embedded Controler) work the same way, you can find documentation on the
  [YoyPa's project](https://github.com/YoyPa/isw/wiki/MSI-G-laptop-EC---Rosetta).

# Working on
```
System:    Kernel: 5.8.0-55-generic x86_64 bits: 64 compiler: N/A Desktop: Cinnamon 4.8.6 Distro: Linux Mint 20.1 Ulyssa
           base: Ubuntu 20.04 focal
Machine:   Type: Laptop System: Micro-Star product: Modern 14 B4MW v: REV:1.0 serial: <filter>
           Mobo: Micro-Star model: MS-14DK v: REV:1.0 serial: <filter> UEFI: American Megatrends v: E14DKAMS.112
           date: 01/25/2021
Battery:   ID-1: BAT1 charge: 27.4 Wh condition: 38.7/37.8 Wh (102%) model: MSI BIF0_9 status: Discharging
CPU:       Topology: 6-Core model: AMD Ryzen 5 4500U with Radeon Graphics bits: 64 type: MCP arch: Zen rev: 1
           L2 cache: 3072 KiB
           flags: avx avx2 lm nx pae sse sse2 sse3 sse4_1 sse4_2 sse4a ssse3 svm bogomips: 28446
           Speed: 1397 MHz min/max: 1400/2375 MHz Core speeds (MHz): 1: 1397 2: 1401 3: 1410 4: 1397 5: 1397 6: 1397
Graphics:  Device-1: Advanced Micro Devices [AMD/ATI] Renoir vendor: Micro-Star MSI driver: amdgpu v: kernel bus ID: 03:00.0
           Display: x11 server: X.Org 1.20.9 driver: amdgpu,ati unloaded: fbdev,modesetting,vesa resolution: 1920x1080~60Hz
           OpenGL: renderer: AMD RENOIR (DRM 3.38.0 5.8.0-55-generic LLVM 11.0.0) v: 4.6 Mesa 20.2.6 direct render: Yes
Audio:     Device-1: Advanced Micro Devices [AMD/ATI] driver: snd_hda_intel v: kernel bus ID: 03:00.1
           Device-2: Advanced Micro Devices [AMD] Raven/Raven2/FireFlight/Renoir Audio Processor vendor: Micro-Star MSI
           driver: N/A bus ID: 03:00.5
           Device-3: Advanced Micro Devices [AMD] Family 17h HD Audio vendor: Micro-Star MSI driver: snd_hda_intel v: kernel
           bus ID: 03:00.6
           Sound Server: ALSA v: k5.8.0-55-generic
Network:   Device-1: Realtek RTL8822CE 802.11ac PCIe Wireless Network Adapter vendor: AzureWave driver: rtw_8822ce v: N/A
           port: f000 bus ID: 02:00.0
           IF: wlp2s0 state: down mac: <filter>
           IF-ID-1: usb0 state: unknown speed: N/A duplex: N/A mac: <filter>
Drives:    Local Storage: total: 476.94 GiB used: 58.45 GiB (12.3%)
           ID-1: /dev/nvme0n1 vendor: Kingston model: OM8PCP3512F-AI1 size: 476.94 GiB
Partition: ID-1: / size: 93.37 GiB used: 15.10 GiB (16.2%) fs: ext4 dev: /dev/nvme0n1p2
           ID-2: /home size: 374.49 GiB used: 43.34 GiB (11.6%) fs: ext4 dev: /dev/nvme0n1p3
Sensors:   System Temperatures: cpu: 37.5 C mobo: N/A gpu: amdgpu temp: 36 C
           Fan Speeds (RPM): N/A
Info:      Processes: 271 Uptime: 2h 21m Memory: 7.24 GiB used: 2.61 GiB (36.0%) Init: systemd runlevel: 5 Compilers:
           gcc: 9.3.0 Shell: bash v: 5.0.17 inxi: 3.0.38
```

# Installation

* Secure boot must be disabled for this to function correctly
* Preferably disable fastboot as well.
* Download / clone the project
* Install dependencies `$ pip install -r requirements.txt`
* Run `Sudo ./install.sh` script to load kernel module at start up.
* Reboot machine to load module.

# Usage

_Note : This application runs in `root` mode. On running it will prompt for root password_

## For help

```bash
$ python main.py --help
# or
$ python main.py -h
```

## To launch the GUI.

```bash
$ python main.py --gui
# or
$ python main.py -g
```

## To change mode

```bash
$ python main.py --mode {MODE}
# or
$ python main.py -m {MODE}
```

## To check status

```bash
$ python main.py --stats
# or
$ python main.py -s
```

## To set charging threshold

```bash
$ python main.py --battery <value>
# or
$ python main.py -b <value>
```

***The charging threshold need to be between 20 and 100***

# Configuration

The configuration file can be found in `config.toml`

```
[settings]
mode = 0
offset = 0
vr_custom = [13, 45, 50, 60, 72, 80, 85, 100, 0, 50, 60, 72, 80, 85, 100]
four = 4
battery_threshold = 80

[ui]
dark_mode_enabled = false
update_freq = 10
```

Avaliable modes:

- 0 - Auto
- 1 - Basic
- 2 - Advanced/custom
- 3 - Cooler Boost

# Info
* Some fan_speed value are ignored by laptops, they will trigger the closest valid RPM speed.
* The RPM value displayed is not exact but close (+-50RPM).
* fan_mode can be 140, 76 or 12, for Advanced, Basic or Auto.
Advanced seems to work better with suspend/hibernate.
* cooler_boost seems to be triggered by any value >= 128.
* battery_threshold below 20 and above 100 are not allowed.
* battery_threshold apply after reboot and isn't reset by it.

## Thanks to [YoCodingMonster](https://github[.com/YoCodingMonster), [llalon](https://github.com/llalon) and [YoyPa](https://github.com/YoyPa)