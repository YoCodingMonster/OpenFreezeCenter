#!/usr/bin/env python3

# Handles setting and reading EC values and setting fan profiles

import sys
import os

# Constants
EC_IO_FILE = "/sys/kernel/debug/ec/ec0/io"
DEFAULT_MODE = 0
DEFAULT_OFFSET = 0
DEFAULT_VR_AUTO = [12, 0, 20, 40, 45, 50, 60, 70, 0, 20, 40, 45, 50, 60, 70]
DEFAULT_VR_BASIC = [140, 0, 20, 40, 45, 50, 60, 70, 0, 20, 40, 45, 50, 60, 70]
DEFAULT_VR_COOLERBOOST = [0]

MODE_AUTO = 0
MODE_BASIC = 1
MODE_ADVANCED = 2
MODE_COOLERBOOST = 3


def read_EC():
    vr = []
    try:
        with open(EC_IO_FILE, "r+b") as file:
            file.seek(0x98)
            if int(file.read(1).hex(), 16) == 128:
                file.seek(0x98)
                vr.insert(0, int(file.read(1).hex(), 16))
            else:
                file.seek(0xF4)
                vr.insert(0, int(file.read(1).hex(), 16))
            file.seek(114)
            vr.insert(1, int(file.read(1).hex(), 16))
            file.seek(115)
            vr.insert(2, int(file.read(1).hex(), 16))
            file.seek(116)
            vr.insert(3, int(file.read(1).hex(), 16))
            file.seek(117)
            vr.insert(4, int(file.read(1).hex(), 16))
            file.seek(118)
            vr.insert(5, int(file.read(1).hex(), 16))
            file.seek(119)
            vr.insert(6, int(file.read(1).hex(), 16))
            file.seek(120)
            vr.insert(7, int(file.read(1).hex(), 16))
            file.seek(138)
            vr.insert(8, int(file.read(1).hex(), 16))
            file.seek(139)
            vr.insert(9, int(file.read(1).hex(), 16))
            file.seek(140)
            vr.insert(10, int(file.read(1).hex(), 16))
            file.seek(141)
            vr.insert(11, int(file.read(1).hex(), 16))
            file.seek(142)
            vr.insert(12, int(file.read(1).hex(), 16))
            file.seek(143)
            vr.insert(13, int(file.read(1).hex(), 16))
            file.seek(144)
            vr.insert(14, int(file.read(1).hex(), 16))

        file.close()
    except:
        print("Error reading EC")

    return vr


def write_EC(v):
    MIN_VR_LENGTH = 14
    # Make sure v is valid - Default to cooler boost
    try:
        if len(v) < MIN_VR_LENGTH:
            v = None
    except TypeError:
        v = None

    try:
        with open(EC_IO_FILE, "w+b") as file:
            if v == None:
                file.seek(0x98)
                file.write(bytes((128,)))
                return
            elif v[0] == 128:
                file.seek(0x98)
                file.write(bytes((128,)))
                file.seek(0xF4)
                file.write(bytes((0,)))
            else:
                file.seek(0x98)
                file.write(bytes((0,)))
                file.seek(0xF4)
                file.write(bytes((v[0],)))
            file.seek(114)
            file.write(bytes((v[1],)))
            file.seek(115)
            file.write(bytes((v[2],)))
            file.seek(116)
            file.write(bytes((v[3],)))
            file.seek(117)
            file.write(bytes((v[4],)))
            file.seek(118)
            file.write(bytes((v[5],)))
            file.seek(119)
            file.write(bytes((v[6],)))
            file.seek(120)
            file.write(bytes((v[7],)))
            file.seek(138)
            file.write(bytes((v[8],)))
            file.seek(139)
            file.write(bytes((v[9],)))
            file.seek(140)
            file.write(bytes((v[10],)))
            file.seek(141)
            file.write(bytes((v[11],)))
            file.seek(142)
            file.write(bytes((v[12],)))
            file.seek(143)
            file.write(bytes((v[13],)))
            file.seek(144)
            file.write(bytes((v[14],)))

        file.close()
    except:
        print("Error reading EC")

    return


def enable_mode(mode=MODE_AUTO, vr=DEFAULT_VR_AUTO, offset=DEFAULT_OFFSET):
    """Changes the current fan mode.

    Args:
        mode (int, optional): The mode to use. Defaults to 'Auto'
        vr (list of int, optional): The VR values to set fan speed profile. Defaults to 'Auto'
        offset (int, optional): The offset value to use. Defaults to 'Auto'
    """
    # Auto
    if mode == MODE_AUTO:
        vr_new = DEFAULT_VR_AUTO
        write_EC(vr_new)

    # Basic
    elif mode == MODE_BASIC:
        offset_official = offset
        vr_b = DEFAULT_VR_BASIC
        vr_new = DEFAULT_VR_BASIC
        vr_new.append(140)
        for i in range(1, 15):
            if ((vr_b[i] + offset_official) >= 0) & (
                (vr_b[i] + offset_official) <= 100
            ):
                vr_new.append(vr_b[i] + offset_official)
            if (vr_b[i] + offset_official) < 0:
                vr_new.append(0)
            if (vr_b[i] + offset_official) > 100:
                vr_new.append(100)
        write_EC(vr_new)

    # Advanced
    elif mode == MODE_ADVANCED:
        vr_3 = []
        vr_2 = []
        vr_1 = []
        vr_2 = vr
        count = 0
        for i in vr_2:
            count = count + 1
            if count < 16:
                vr_3.append(int(i))
        write_EC(vr_3)

    # Coolser Boost
    else:
        vr_new = DEFAULT_VR_COOLERBOOST
        write_EC(vr_new)


def get_stats():
    stats = dict()
    try:
        with open(EC_IO_FILE, "r+b") as file:
            file.seek(0x68)
            cpu_cur_temp = int(file.read(1).hex(), 16)
            file.seek(0x80)
            gpu_cur_temp = int(file.read(1).hex(), 16)
            file.seek(0xCC)
            cpu_fan = int(file.read(2).hex(), 16)
            if cpu_fan != 0:
                cpu_fan = 478000 // cpu_fan
            file.seek(0xCA)
            gpu_fan = int(file.read(2).hex(), 16)
            if gpu_fan != 0:
                gpu_fan = 478000 // gpu_fan

            stats = {
                "CPU_RPM": cpu_fan,
                "GPU_RPM": gpu_fan,
                "CPU_TEMP": cpu_cur_temp,
                "GPU_TEMP": gpu_cur_temp,
            }
        file.close()

    except:
        print("Error reading EC")
        stats = {
            "CPU_RPM": 0,
            "GPU_RPM": 0,
            "CPU_TEMP": 0,
            "GPU_TEMP": 0,
        }

    return stats
