#! /usr/bin/python3

import os
import fileinput



def read_range(file, range):
    file.seek(range.start)
    return ",".join('{:02X}'.format(x) for x in file.read(range.__len__()+1))

EC_IO_FILE = '/sys/kernel/debug/ec/ec0/io'
path_to_script = os.path.dirname(os.path.abspath(__file__))
my_filename = os.path.join(path_to_script, "conf.txt")

conf_file = open(my_filename, "r")
all_lines = conf_file.readlines()
conf_file.close()
lines = all_lines[0] + "\n" + all_lines[1] + "\n" + all_lines[2] + "\n" + all_lines[3] + "\n"

with open(EC_IO_FILE,'r+b') as file:
    file.seek(0xf4)
    file.write(bytes(12))
    lines += read_range(file, range(0x6a, 0x6f)) + ","
    lines += read_range(file, range(0x82, 0x87)) + ",\n12,"
    lines += read_range(file, range(0x72, 0x78)) + ","
    lines += read_range(file, range(0x8a, 0x90)) + ","
 
conf_file = open(my_filename, "w")
conf_file.writelines(lines)
conf_file.close()
str_1 = ''
for line in fileinput.FileInput(my_filename, inplace=1):
    if line.rstrip():
        str_1 = str_1 + line
conf_file = open(my_filename, "w")
conf_file.writelines(str_1)
conf_file.write("\n" + all_lines[6])
conf_file.close()