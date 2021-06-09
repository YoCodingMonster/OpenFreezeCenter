#! /usr/bin/python3

import os

EC_IO_FILE = '/sys/kernel/debug/ec/ec0/io'
path_to_script = os.path.dirname(os.path.abspath(__file__))
my_filename = os.path.join(path_to_script, "conf.txt")

conf_file_b = open(my_filename, "r")
all_lines = conf_file_b.readlines()
mode_f = int(all_lines[0])
battery_threshold = int(all_lines[3]) + 128
conf_file_b.close()

def write_EC(v, battery_threshold):
	with open(EC_IO_FILE, 'r+b') as file:
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
		file.seek(239)
		file.write(bytes((battery_threshold,)))
	return

def get_temp_list(val):
	vr = []
	vr_2 = []
	vr_1 = []
	vr_1 = all_lines[val]
	vr_2 = vr_1.split (",")
	count = 0
	for i in vr_2:
		count = count + 1
		if count < 16:
			vr.append(int(i))
	return vr

if int(mode_f) == 1:
	vr = get_temp_list(5)
	write_EC(vr, battery_threshold)
elif int(mode_f) == 2:
	offset_official = int(all_lines[1])
	vr = get_temp_list(5)
	vr_new = []
	vr_new.append(140)
	for i in range(1, 15):
		if ((vr[i] + offset_official) >= 0) & ((vr[i] + offset_official) <= 100):
			vr_new.append(vr[i] + offset_official)
		if ((vr[i] + offset_official) < 0):
			vr_new.append(0)
		if ((vr[i] + offset_official) > 100):
			vr_new.append(100)
	write_EC(vr_new, battery_threshold)
elif int(mode_f) == 3:
	vr = get_temp_list(2)
	write_EC(vr, battery_threshold)
else:
	with open(EC_IO_FILE,'w+b') as file:
		file.seek(0x98)
		file.write(bytes((128,)))
		file.seek(0xef)
		file.write(bytes((battery_threshold,)))
