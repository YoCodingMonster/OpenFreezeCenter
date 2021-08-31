#! /usr/bin/python3

import os
import fileinput

EC_IO_FILE = '/sys/kernel/debug/ec/ec0/io'
path_to_script = os.path.dirname(os.path.abspath(__file__))
my_filename = os.path.join(path_to_script, "conf.txt")

conf_file = open(my_filename, "r")
all_lines = conf_file.readlines()
conf_file.close()
lines = all_lines[0] + "\n" + all_lines[1] + "\n" + all_lines[2] + "\n" + all_lines[3] + "\n"

with open(EC_IO_FILE,'r+b') as file:
    file.seek(0x6a)
    lines = lines + str(int(file.read(1).hex(),16)) + ","
    file.seek(0x6b)
    lines = lines + str(int(file.read(1).hex(),16)) + ","
    file.seek(0x6c)
    lines = lines + str(int(file.read(1).hex(),16)) + ","
    file.seek(0x6d)
    lines = lines + str(int(file.read(1).hex(),16)) + ","
    file.seek(0x6e)
    lines = lines + str(int(file.read(1).hex(),16)) + ","
    file.seek(0x6f)
    lines = lines + str(int(file.read(1).hex(),16)) + ","
    file.seek(0x82)
    lines = lines + str(int(file.read(1).hex(),16)) + ","
    file.seek(0x83)
    lines = lines + str(int(file.read(1).hex(),16)) + ","
    file.seek(0x84)
    lines = lines + str(int(file.read(1).hex(),16)) + ","
    file.seek(0x85)
    lines = lines + str(int(file.read(1).hex(),16)) + ","
    file.seek(0x86)
    lines = lines + str(int(file.read(1).hex(),16)) + ","
    file.seek(0x87)
    lines = lines + str(int(file.read(1).hex(),16)) + ","
    lines = lines + "\n12,"
    file.seek(0x72)
    lines = lines + str(int(file.read(1).hex(),16)) + ","
    file.seek(0x73)
    lines = lines + str(int(file.read(1).hex(),16)) + ","
    file.seek(0x74)
    lines = lines + str(int(file.read(1).hex(),16)) + ","
    file.seek(0x75)
    lines = lines + str(int(file.read(1).hex(),16)) + ","
    file.seek(0x76)
    lines = lines + str(int(file.read(1).hex(),16)) + ","
    file.seek(0x77)
    lines = lines + str(int(file.read(1).hex(),16)) + ","
    file.seek(0x78)
    lines = lines + str(int(file.read(1).hex(),16)) + ","
    file.seek(0x8a)
    lines = lines + str(int(file.read(1).hex(),16)) + ","
    file.seek(0x8b)
    lines = lines + str(int(file.read(1).hex(),16)) + ","
    file.seek(0x8c)
    lines = lines + str(int(file.read(1).hex(),16)) + ","
    file.seek(0x8d)
    lines = lines + str(int(file.read(1).hex(),16)) + ","
    file.seek(0x8e)
    lines = lines + str(int(file.read(1).hex(),16)) + ","
    file.seek(0x8f)
    lines = lines + str(int(file.read(1).hex(),16)) + ","
    file.seek(0x90)
    lines = lines + str(int(file.read(1).hex(),16)) + ","
 
conf_file = open(my_filename, "w")
conf_file.writelines(lines)
conf_file.close()
str_1 = ''
for line in fileinput.FileInput(my_filename, inplace=1):
    if line.rstrip():
        str_1 = str_1 + line
conf_file = open(my_filename, "w")
conf_file.writelines(str_1)
conf_file.close()