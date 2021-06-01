#! /usr/bin/python3

import os

EC_IO_FILE = '/sys/kernel/debug/ec/ec0/io'

"""################################
read & write EC
################################"""


def read_EC():
    vr = []
    with open(EC_IO_FILE, 'r+b') as file:
        file.seek(0x98)
        if int(file.read(1).hex(), 16) == 128:
            file.seek(0x98)
            vr.insert(0, int(file.read(1).hex(), 16))
        else:
            file.seek(0xf4)
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
    return vr


def write_EC(v):
    with open(EC_IO_FILE, 'w+b') as file:
        if v[0] == 128:
            file.seek(0x98)
            file.write(bytes((128,)))
            file.seek(0xf4)
            file.write(bytes((0,)))
        else:
            file.seek(0x98)
            file.write(bytes((0,)))
            file.seek(0xf4)
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
    return


"""################################
reading conf file
################################"""

path_to_script = os.path.dirname(os.path.abspath(__file__))
my_filename = os.path.join(path_to_script, "conf.txt")

offset_official = 0
vr_3 = []
vr_2 = []
vr_1 = []

conf_file_b = open(my_filename, "r")
mode = int(conf_file_b.read(1))
all_lines = conf_file_b.readlines()
mode_f = all_lines[1]
conf_file_b.close()

# AUTO
if int(mode_f) == 1:
    vr = [12, 0, 20, 40, 45, 50, 60, 70, 0, 20, 40, 45, 50, 60, 70]
    write_EC(vr)

# BASIC
elif int(mode_f) == 2:
    conf_file_x = open(my_filename, "r")
    all_lines = conf_file_x.readlines()
    offset_official = int(all_lines[2])
    vr_b = [140, 0, 20, 40, 45, 50, 60, 70, 0, 20, 40, 45, 50, 60, 70]
    vr_new = []
    vr_new.append(140)
    for i in range(1, 15):
        if ((vr_b[i] + offset_official) >= 0) & ((vr_b[i] + offset_official) <= 100):
            vr_new.append(vr_b[i] + offset_official)
        if ((vr_b[i] + offset_official) < 0):
            vr_new.append(0)
        if ((vr_b[i] + offset_official) > 100):
            vr_new.append(100)
    write_EC(vr_new)

# Advanced
elif int(mode_f) == 3:
    vr_3 = []
    vr_2 = []
    vr_1 = []
    conf_file_x = open(my_filename, "r")
    all_lines = conf_file_x.readlines()
    vr_1 = all_lines[3]
    vr_2 = vr_1.split(",")
    count = 0
    for i in vr_2:
        count = count + 1
        if count < 16:
            vr_3.append(int(i))
    write_EC(vr_3)
    conf_file_x.close()

# Cooler boost
else:
    with open(EC_IO_FILE, 'w+b') as file:
        file.seek(0x98)
        file.write(bytes((128,)))
