#! /usr/bin/python3

from tkinter import *
import threading
import os

EC_IO_FILE = '/sys/kernel/debug/ec/ec0/io'

path_to_script = os.path.dirname(os.path.abspath(__file__))
my_filename = os.path.join(path_to_script, "conf.txt")

conf_file_a = open(my_filename, "r")
mode = int(conf_file_a.read(1))
all_lines = conf_file_a.readlines()
flip_board = int(all_lines[6])
conf_file_a.close()

monitoring = 0
temp_c = 0
temp_g = 0
temp_c_m = 100
temp_g_m = 100
temp_m = 0

window_m = Tk()
window_m.title('Monitering')
dpi_base = 76
dpi = window_m.winfo_fpixels('1i')
dpi_scale = round(dpi/dpi_base)
window_m.geometry(f'{dpi_scale * 320}x{dpi_scale * 110}')
canvas = Canvas(window_m)
canvas.configure(bg = 'black')

def monitoring_int(lable_c11, lable_c22, lable_c33, lable_g11, lable_g22, lable_g33, lable_m44, lable_m55, lable_m444, lable_m555):
	global monitoring
	monitoring = 1
	global timer
	timer = threading.Timer(1, monitoring_int, args = (lable_c11, lable_c22, lable_c33, lable_g11, lable_g22, lable_g33, lable_m44, lable_m55, lable_m444, lable_m555))
	timer.start()
	global temp_m
	temp_m = mode
	global temp_c
	global temp_g
	global temp_c_m
	global temp_g_m
	with open(EC_IO_FILE,'r+b') as file:
		file.seek(0x68)
		cpu_cur_temp = (int(file.read(1).hex(),16))
		file.seek(0x80)
		gpu_cur_temp = (int(file.read(1).hex(),16))
		file.seek(0x71)
		cpu_fan_s = (int(file.read(1).hex(),16))
		file.seek(0x89)
		gpu_fan_s = (int(file.read(1).hex(),16))
		if flip_board == 0:
			file.seek(0xca)
		else:
			file.seek(0xc8)
		cpu_fan = (int(file.read(2).hex(),16))
		if cpu_fan != 0:
			cpu_fan = 478000//cpu_fan
		file.seek(0xca)
		gpu_fan = (int(file.read(2).hex(),16))
		if gpu_fan != 0:
			gpu_fan = 478000//gpu_fan
		if cpu_cur_temp > temp_c:
			temp_c = cpu_cur_temp
			color(temp_c, lable_c22)
		if gpu_cur_temp > temp_g:
			temp_g = gpu_cur_temp
			color(temp_c, lable_g22)
		if cpu_cur_temp < temp_c_m:
			temp_c_m = cpu_cur_temp
			color(temp_c_m, lable_c33)
		if gpu_cur_temp < temp_g_m:
			temp_g_m = gpu_cur_temp
			color(temp_g_m, lable_g33)
		color(cpu_cur_temp, lable_c11)
		color(gpu_cur_temp, lable_g11)
		lable_m44.config(text = cpu_fan)
		lable_m55.config(text = gpu_fan)
		lable_m444.config(text = str(cpu_fan_s) + "%")
		lable_m555.config(text = str(gpu_fan_s) + "%")
	return
	
def color(temp, lable):
	if temp <= 45:
		lable.config(text = temp, fg = 'green', bg = 'black')
	elif (temp > 45) & (temp <= 60):
		lable.config(text = temp, fg = 'yellow', bg = 'black')
	elif (temp > 60) & (temp <= 75):
		lable.config(text = temp, fg = 'orange', bg = 'black')
	else:
		lable.config(text = temp, fg = 'red', bg = 'black')
	return
	

lable_c1 = Label(window_m, text = "CPU Temperature (Celcius) : ", fg = 'white', bg = 'black', font=("Helvetica", 10))
lable_c1.place(x = dpi_scale * 10, y = dpi_scale * 27)
lable_c11 = Label(window_m, text = "", fg = 'white', bg = 'black', font=("Helvetica", 11))
lable_c11.place(x = dpi_scale * 190, y = dpi_scale * 27)

lable_c2 = Label(window_m, text = "Max", fg = 'white', bg = 'black', font=("Helvetica", 10))
lable_c2.place(x = dpi_scale * 245, y = dpi_scale * 10)
lable_c22 = Label(window_m, text = "", fg = 'white', bg = 'black', font=("Helvetica", 11))
lable_c22.place(x = dpi_scale * 250, y = dpi_scale * 27)

lable_c3 = Label(window_m, text = "Min", fg = 'white', bg = 'black', font=("Helvetica", 10))
lable_c3.place(x = dpi_scale * 285, y = dpi_scale * 10)
lable_c33 = Label(window_m, text = "", fg = 'white', bg = 'black', font=("Helvetica", 11))
lable_c33.place(x = dpi_scale * 290, y = dpi_scale * 27)

lable_g1 = Label(window_m, text = "GPU Temperature (Celcius) : ", fg = 'white', bg = 'black', font=("Helvetica", 10))
lable_g1.place(x = dpi_scale * 10, y = dpi_scale * 47)
lable_g11 = Label(window_m, text = "", fg = 'white', bg = 'black', font=("Helvetica", 11))
lable_g11.place(x = dpi_scale * 190, y = dpi_scale * 47)

lable_g22 = Label(window_m, text = "", fg = 'white', bg = 'black', font=("Helvetica", 11))
lable_g22.place(x = dpi_scale * 250, y = dpi_scale * 47)

lable_g33 = Label(window_m, text = "", fg = 'white', bg = 'black', font=("Helvetica", 11))
lable_g33.place(x = dpi_scale * 290, y = dpi_scale * 47)

lable_m4 = Label(window_m, text = "CPU fan RPM : ", fg = 'white', bg = 'black', font=("Helvetica", 10))
lable_m4.place(x = dpi_scale * 10, y = dpi_scale * 67)
lable_m44 = Label(window_m, text = "", fg = 'white', bg = 'black', font=("Helvetica", 11))
lable_m44.place(x = dpi_scale * 190, y = dpi_scale * 67)
lable_m444 = Label(window_m, text = "", fg = 'white', bg = 'black', font=("Helvetica", 11))
lable_m444.place(x = dpi_scale * 250, y = dpi_scale * 67)

lable_m5 = Label(window_m, text = "GPU fan RPM : ", fg = 'white', bg = 'black', font=("Helvetica", 10))
lable_m5.place(x = dpi_scale * 10, y = dpi_scale * 87)
lable_m55 = Label(window_m, text = "", fg = 'white', bg = 'black', font=("Helvetica", 11))
lable_m55.place(x = dpi_scale * 190, y = dpi_scale * 87)
lable_m555 = Label(window_m, text = "", fg = 'white', bg = 'black', font=("Helvetica", 11))
lable_m555.place(x = dpi_scale * 250, y = dpi_scale * 87)

monitoring_int(lable_c11, lable_c22, lable_c33, lable_g11, lable_g22, lable_g33, lable_m44, lable_m55, lable_m444, lable_m555)

def on_closing():
	timer.cancel()
	window_m.destroy()
	return

canvas.pack(fill = BOTH, expand = 1)
window_m.protocol("WM_DELETE_WINDOW", on_closing)
window_m.mainloop()
