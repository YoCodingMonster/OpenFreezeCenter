#! /usr/bin/python3

import imports_manager
from tkinter import *

EC_IO_FILE = '/sys/kernel/debug/ec/ec0/io'

path_to_script = imports_manager.os.path.dirname(imports_manager.os.path.abspath(__file__))
my_filename = imports_manager.os.path.join(path_to_script, "conf.txt")

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
dpi_base = 100
dpi = window_m.winfo_fpixels('1i')
dpi_scale = round(dpi/dpi_base)
window_m.geometry(f'{dpi_scale * 320}x{dpi_scale * 130}')
canvas = Canvas(window_m)
canvas.configure(bg = 'black')

def monitoring_int(label_c11, label_c22, label_c33, label_g11, label_g22, label_g33, label_m44, label_m55, label_m444, label_m555, label_battery_threshold, label_battery_threshold_value):
	global monitoring
	monitoring = 1
	global timer
	timer = imports_manager.threading.Timer(1, monitoring_int, args = (label_c11, label_c22, label_c33, label_g11, label_g22, label_g33, label_m44, label_m55, label_m444, label_m555, label_battery_threshold, label_battery_threshold_value))
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
		file.seek(0xef)
		battery_threshold = (int(file.read(1).hex(),16)) - 128
		label_battery_threshold_value.config(text = str(battery_threshold) + "%")
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
			color(temp_c, label_c22)
		if gpu_cur_temp > temp_g:
			temp_g = gpu_cur_temp
			color(temp_c, label_g22)
		if cpu_cur_temp < temp_c_m:
			temp_c_m = cpu_cur_temp
			color(temp_c_m, label_c33)
		if gpu_cur_temp < temp_g_m:
			temp_g_m = gpu_cur_temp
			color(temp_g_m, label_g33)
		color(cpu_cur_temp, label_c11)
		color(gpu_cur_temp, label_g11)
		label_m44.config(text = cpu_fan)
		label_m55.config(text = gpu_fan)
		label_m444.config(text = str(cpu_fan_s) + "%")
		label_m555.config(text = str(gpu_fan_s) + "%")
	return
	
def color(temp, label):
	if temp <= 45:
		label.config(text = temp, fg = 'green', bg = 'black')
	elif (temp > 45) & (temp <= 60):
		label.config(text = temp, fg = 'yellow', bg = 'black')
	elif (temp > 60) & (temp <= 75):
		label.config(text = temp, fg = 'orange', bg = 'black')
	else:
		label.config(text = temp, fg = 'red', bg = 'black')
	return
	

label_c1 = Label(window_m, text = "CPU Temperature (Celcius) : ", fg = 'white', bg = 'black', font=("Helvetica", 10))
label_c1.place(x = dpi_scale * 10, y = dpi_scale * 27)
label_c11 = Label(window_m, text = "", fg = 'white', bg = 'black', font=("Helvetica", 11))
label_c11.place(x = dpi_scale * 190, y = dpi_scale * 27)

label_c2 = Label(window_m, text = "Max", fg = 'white', bg = 'black', font=("Helvetica", 10))
label_c2.place(x = dpi_scale * 245, y = dpi_scale * 10)
label_c22 = Label(window_m, text = "", fg = 'white', bg = 'black', font=("Helvetica", 11))
label_c22.place(x = dpi_scale * 250, y = dpi_scale * 27)

label_c3 = Label(window_m, text = "Min", fg = 'white', bg = 'black', font=("Helvetica", 10))
label_c3.place(x = dpi_scale * 285, y = dpi_scale * 10)
label_c33 = Label(window_m, text = "", fg = 'white', bg = 'black', font=("Helvetica", 11))
label_c33.place(x = dpi_scale * 290, y = dpi_scale * 27)

label_g1 = Label(window_m, text = "GPU Temperature (Celcius) : ", fg = 'white', bg = 'black', font=("Helvetica", 10))
label_g1.place(x = dpi_scale * 10, y = dpi_scale * 47)
label_g11 = Label(window_m, text = "", fg = 'white', bg = 'black', font=("Helvetica", 11))
label_g11.place(x = dpi_scale * 190, y = dpi_scale * 47)

label_g22 = Label(window_m, text = "", fg = 'white', bg = 'black', font=("Helvetica", 11))
label_g22.place(x = dpi_scale * 250, y = dpi_scale * 47)

label_g33 = Label(window_m, text = "", fg = 'white', bg = 'black', font=("Helvetica", 11))
label_g33.place(x = dpi_scale * 290, y = dpi_scale * 47)

label_m4 = Label(window_m, text = "CPU fan RPM : ", fg = 'white', bg = 'black', font=("Helvetica", 10))
label_m4.place(x = dpi_scale * 10, y = dpi_scale * 67)
label_m44 = Label(window_m, text = "", fg = 'white', bg = 'black', font=("Helvetica", 11))
label_m44.place(x = dpi_scale * 190, y = dpi_scale * 67)
label_m444 = Label(window_m, text = "", fg = 'white', bg = 'black', font=("Helvetica", 11))
label_m444.place(x = dpi_scale * 250, y = dpi_scale * 67)

label_m5 = Label(window_m, text = "GPU fan RPM : ", fg = 'white', bg = 'black', font=("Helvetica", 10))
label_m5.place(x = dpi_scale * 10, y = dpi_scale * 87)
label_m55 = Label(window_m, text = "", fg = 'white', bg = 'black', font=("Helvetica", 11))
label_m55.place(x = dpi_scale * 190, y = dpi_scale * 87)
label_m555 = Label(window_m, text = "", fg = 'white', bg = 'black', font=("Helvetica", 11))
label_m555.place(x = dpi_scale * 250, y = dpi_scale * 87)

label_battery_threshold = Label(window_m, text = "Battery_Threshold : ", fg = 'white', bg = 'black', font=("Helvetica", 10))
label_battery_threshold.place(x = dpi_scale * 10, y = dpi_scale * 107)
label_battery_threshold_value = Label(window_m, text = "", fg = 'white', bg = 'black', font=("Helvetica", 11))
label_battery_threshold_value.place(x = dpi_scale * 190, y = dpi_scale * 107)

monitoring_int(label_c11, label_c22, label_c33, label_g11, label_g22, label_g33, label_m44, label_m55, label_m444, label_m555, label_battery_threshold, label_battery_threshold_value)

def on_closing():
	timer.cancel()
	window_m.destroy()
	return

canvas.pack(fill = BOTH, expand = 1)
window_m.protocol("WM_DELETE_WINDOW", on_closing)
window_m.mainloop()
