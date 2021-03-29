#! /usr/bin/python3

from tkinter import *
from tkinter import messagebox
import os
import sys
import subprocess
from crontab import CronTab
import getpass
import threading
import time

"""############ Variables & Defaults"""

username = getpass.getuser()
EC_IO_FILE = '/sys/kernel/debug/ec/ec0/io'
fm, offset, y = 12, 0, 100
monitoring = 0
temp_c = 0
temp_g = 0
temp_c_m = 100
temp_g_m = 100
v = []
check = os.path.exists("/etc/modprobe.d/GUI-MSI-DC-L-ec_sys.conf")
window = Tk()
canvas = Canvas(window)

def read_EC():
	vr = []
	with open(EC_IO_FILE,'r+b') as file:
		file.seek(0x98)
		if int(file.read(1).hex(),16) == 128:
			file.seek(0x98)
			vr.insert(0, int(file.read(1).hex(),16))
		else:
			file.seek(0xf4)
			vr.insert(0, int(file.read(1).hex(),16))
		file.seek(114)
		vr.insert(1, int(file.read(1).hex(),16))
		file.seek(115)
		vr.insert(2, int(file.read(1).hex(),16))
		file.seek(116)
		vr.insert(3, int(file.read(1).hex(),16))
		file.seek(117)
		vr.insert(4, int(file.read(1).hex(),16))
		file.seek(118)
		vr.insert(5, int(file.read(1).hex(),16))
		file.seek(119)
		vr.insert(6, int(file.read(1).hex(),16))
		file.seek(120)
		vr.insert(7, int(file.read(1).hex(),16))
		file.seek(138)
		vr.insert(8, int(file.read(1).hex(),16))
		file.seek(139)
		vr.insert(9, int(file.read(1).hex(),16))
		file.seek(140)
		vr.insert(10, int(file.read(1).hex(),16))
		file.seek(141)
		vr.insert(11, int(file.read(1).hex(),16))
		file.seek(142)
		vr.insert(12, int(file.read(1).hex(),16))
		file.seek(143)
		vr.insert(13, int(file.read(1).hex(),16))
		file.seek(144)
		vr.insert(14, int(file.read(1).hex(),16))
	return vr
    
def write_EC(v):
	with open(EC_IO_FILE,'w+b') as file:
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

def null():
    return
    
"""######################################################################################################################## Canvas layout"""

window.title('MSI Dragon Center for Linux')
window.geometry('370x210')

lable1 = Label(window, text = "Creator :-> Aditya Kumar Bajpai", fg = 'red', font=("Helvetica", 16))
lable1.place(x = 30, y = 10)

lable2 = Label(window, text = "Version 1.2", fg = 'black', font=("Helvetica", 16))
lable2.place(x = 122, y = 50)

"""#################################################################################### Install - Uninstall"""

def install():
    os.system("gnome-terminal -e 'bash -c \"sudo install -Dm 644 etc/modprobe.d/GUI-MSI-DC-L-ec_sys.conf \"${pkgdir}/etc/modprobe.d/GUI-MSI-DC-L-ec_sys.conf\" && sudo install -Dm 644 etc/modules-load.d/GUI-MSI-DC-L-ec_sys.conf \"${pkgdir}/etc/modules-load.d/GUI-MSI-DC-L-ec_sys.conf\"; exec bash\"'")
    button1.config(text = "Uninstall", fg = 'grey', command = uninstall)
    messagebox.showinfo("Installation Complete!", "Please Reboot your system to enable EC module write capablities of script") 
    return
    
def uninstall():
	os.system("gnome-terminal -e 'bash -c \"sudo rm /etc/modprobe.d/GUI-MSI-DC-L-ec_sys.conf /etc/modules-load.d/GUI-MSI-DC-L-ec_sys.conf /usr/share/GUI-MSI-DC-L.py; exec bash\"'")
	if os.path.exist("/usr/share/GUI-MSI-DC-L.py") == True:
		os.system("gnome-terminal -e 'bash -c \"sudo rm /usr/share/GUI-MSI-DC-L.py; exec bash\"'")
	my_cron = CronTab(user = username)
	for job in my_cron:
		if job.comment == '@reboot python3 /usr/share/GUI-MSI-DC-L.py':
			my_cron.remove(job)
			my_cron.write()
	button1.config(text = "Install", fg = 'black', command = install)
	return
	
if check == True:
	button1 = Button(window, text = "Uninstall", width = 20, fg = 'grey', command = uninstall)
else:
	button1 = Button(window, text = "Install", width = 20, fg = 'black', command = install)
button1.place(x = 90, y = 80)
    
"""#################################################################################### Startup - Unstartup"""
    
def startup():
	button2.config(fg = 'grey', text = 'Dont run at Startup', command = unstartup)
	os.system("gnome-terminal -e 'bash -c \"sudo install -Dm 644 GUI-MSI-DC-L.py \"${pkgdir}/usr/share/GUI-MSI-DC-L.py\"; exec bash\"'")
	my_cron = CronTab(user = username)
	job = my_cron.new(command = '@reboot python3 /usr/share/GUI-MSI-DC-L.py')
	my_cron.write()
	return
	
def unstartup():
	button2.config(fg = 'black', text = 'Run at Startup', command = startup)
	os.system("gnome-terminal -e 'bash -c \"sudo rm /usr/share/GUI-MSI-DC-L.py; exec bash\"'")
	my_cron = CronTab(user = username)
	for job in my_cron:
		if job.comment == '@reboot python3 /usr/share/GUI-MSI-DC-L.py':
			my_cron.remove(job)
			my_cron.write()
	return
	
button2 = Button(window, text = "Run at Startup", width = 20, fg = 'black', command = startup)
button2.place(x = 90, y = 110)

my_cron = CronTab(user = username)
for job in my_cron:
	if job.comment == '@reboot python3 /usr/share/GUI-MSI-DC-L.py':
		button2.config(fg = 'grey', text = 'Dont run at Startup', command = unstartup)
	else:
		button2.config(fg = 'black', text = 'Run at Startup', command = startup)

"""#################################################################################### Monitor - Unmonitor"""
def monitoring_int(lable_c11, lable_c22, lable_c33, lable_g11, lable_g22, lable_g33, lable_m44, lable_m55):
	global monitoring
	monitoring = 1
	global timer
	timer = threading.Timer(1, monitoring_int, args = (lable_c11, lable_c22, lable_c33, lable_g11, lable_g22, lable_g33, lable_m44, lable_m55))
	timer.start()
	global temp_c
	global temp_g
	global temp_c_m
	global temp_g_m
	with open(EC_IO_FILE,'r+b') as file:
		file.seek(0x68)
		cpu_cur_temp = (int(file.read(1).hex(),16))
		file.seek(0x80)
		gpu_cur_temp = (int(file.read(1).hex(),16))
		file.seek(0xcc)
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
	return
	
def color(temp, lable):
	if temp <= 45:
		lable.config(text = temp, fg = 'green')
	elif (temp > 45) & (temp <= 60):
		lable.config(text = temp, fg = 'yellow')
	elif (temp > 60) & (temp <= 75):
		lable.config(text = temp, fg = 'orange')
	else:
		lable.config(text = temp, fg = 'red')
	return

def monitor():
	window.minsize(width = 700, height = 10)
	button3.config(fg = 'grey', text = 'Hide Monitering', command = unmonitor)
	
	lable_m = Label(window, text = "Monitering", fg = 'Black', font=("Helvetica", 16))
	lable_m.place(x = 470, y = 5)
	canvas.create_line(370, 0, 370, 920, dash = (10, 4), fill = "grey")
	canvas.create_line(370, 32, 700, 32, dash = (10, 4), fill = "grey")
	lable_c1 = Label(window, text = "CPU Temperature (Celcius) : ", fg = 'Black', font=("Helvetica", 10))
	lable_c1.place(x = 380, y = 50)
	lable_c11 = Label(window, text = "", fg = 'Black', font=("Helvetica", 10))
	lable_c11.place(x = 560, y = 50)
	
	lable_c2 = Label(window, text = "Max", fg = 'Black', font=("Helvetica", 10))
	lable_c2.place(x = 615, y = 35)
	lable_c22 = Label(window, text = "", fg = 'Black', font=("Helvetica", 10))
	lable_c22.place(x = 620, y = 50)
	
	lable_c3 = Label(window, text = "Min", fg = 'Black', font=("Helvetica", 10))
	lable_c3.place(x = 655, y = 35)
	lable_c33 = Label(window, text = "", fg = 'Black', font=("Helvetica", 10))
	lable_c33.place(x = 660, y = 50)
	
	lable_g1 = Label(window, text = "GPU Temperature (Celcius) : ", fg = 'Black', font=("Helvetica", 10))
	lable_g1.place(x = 380, y = 70)
	lable_g11 = Label(window, text = "", fg = 'Black', font=("Helvetica", 10))
	lable_g11.place(x = 560, y = 70)
	
	lable_g22 = Label(window, text = "", fg = 'Black', font=("Helvetica", 10))
	lable_g22.place(x = 620, y = 70)
	
	lable_g33 = Label(window, text = "", fg = 'Black', font=("Helvetica", 10))
	lable_g33.place(x = 660, y = 70)
	
	lable_m4 = Label(window, text = "CPU fan RPM : ", fg = 'Black', font=("Helvetica", 10))
	lable_m4.place(x = 380, y = 90)
	lable_m44 = Label(window, text = "", fg = 'Black', font=("Helvetica", 10))
	lable_m44.place(x = 480, y = 90)
	
	lable_m5 = Label(window, text = "GPU fan RPM : ", fg = 'Black', font=("Helvetica", 10))
	lable_m5.place(x = 380, y = 110)
	lable_m55 = Label(window, text = "", fg = 'Black', font=("Helvetica", 10))
	lable_m55.place(x = 480, y = 110)
	
	monitoring_int(lable_c11, lable_c22, lable_c33, lable_g11, lable_g22, lable_g33, lable_m44, lable_m55)
	return
	
def unmonitor():
	window.minsize(width = 370, height = 10)
	button3.config(fg = 'black', text = 'Monitor', command = monitor)
	timer.cancel()
	return

button3 = Button(window, text = "Monitor", width = 20, fg = 'black', command = monitor)
button3.place(x = 90, y = 140)

"""#################################################################################### Fan modes"""
"""########################################## Auto Mode"""

def auto_on():
	window.geometry('370x270')
	vr = [12,0,20,40,45,50,60,70,0,20,40,45,50,60,70]
	write_EC(vr)

	a_on.config(fg = 'red', command = null)
	b_on.config(fg = 'black', command = basic_build)
	ad_on.config(fg = 'black', command = advanced_on)
	cb_on.config(fg = 'black', command = cooler_booster_on)
	return

"""########################################## Baisc Mode"""

def basic_build():
	window.geometry('370x330')
	basic_slider = Scale(window, from_ = -30, to = 30, orient = HORIZONTAL, length = 200, showvalue = 1, tickinterval = 10, resolution = 10)
	basic_slider.place(x = 10, y = 265)
	
	def basic_on(offset):
		vr = [76,0,20,40,45,50,60,70,0,20,40,45,50,60,70]
		vr_new = []
		vr_new.append(76)
		for i in range(1, 15):
			if ((vr[i] + offset) >= 0) & ((vr[i] + offset) <= 100):
				vr_new.append(vr[i] + offset)
				print(vr_new[i])
			if ((vr[i] + offset) < 0):
				vr_new.append(0)
				print(vr_new[i])
			if ((vr[i] + offset) > 100):
				vr_new.append(100)
				print(vr_new[i])
		write_EC(vr_new)
		return
		
	button_basic = Button(window, text = "Apply", width = 10, fg = 'black', command = lambda: basic_on(basic_slider.get()))
	button_basic.place(x = 235, y = 280)
	
	a_on.config(fg = 'black', command = auto_on)
	b_on.config(fg = 'red', command = null)
	ad_on.config(fg = 'black', command = advanced_on)
	cb_on.config(fg = 'black', command = cooler_booster_on)
	return

"""########################################## Advanced Mode"""

def advanced_on():
	v = []
	v = read_EC()
	window.geometry('370x920')
	
	offset = 50
	
	lable_ct8 = Label(window, text = "CPU fan Speeds" , fg = 'blue', font=("Helvetica", 10))
	lable_ct8.place(x = 135, y = offset + 280)
	
	lable_gt7 = Label(window, text = "GPU fan Speeds" , fg = 'blue', font=("Helvetica", 10))
	lable_gt7.place(x = 135, y = offset + 560)
	
	canvas.create_line(0, offset + 550, 370, offset + 550, dash=(10, 4), fill = "grey")

	lable_ct1 = Label(window, text = str(v[1]) + "%", fg = 'Black', font=("Helvetica", 10))
	lable_ct1.place(x = 35, y = offset + 300)
	lable_ct2 = Label(window, text = str(v[2]) + "%", fg = 'Black', font=("Helvetica", 10))
	lable_ct2.place(x = 85, y = offset + 300)
	lable_ct3 = Label(window, text = str(v[3]) + "%", fg = 'Black', font=("Helvetica", 10))
	lable_ct3.place(x = 135, y = offset + 300)
	lable_ct4 = Label(window, text = str(v[4]) + "%", fg = 'Black', font=("Helvetica", 10))
	lable_ct4.place(x = 185, y = offset + 300)
	lable_ct5 = Label(window, text = str(v[5]) + "%", fg = 'Black', font=("Helvetica", 10))
	lable_ct5.place(x = 235, y = offset + 300)
	lable_ct6 = Label(window, text = str(v[6]) + "%", fg = 'Black', font=("Helvetica", 10))
	lable_ct6.place(x = 285, y = offset + 300)
	lable_ct7 = Label(window, text = str(v[7]) + "%", fg = 'Black', font=("Helvetica", 10))
	lable_ct7.place(x = 335, y = offset + 300)
	lable_gt1 = Label(window, text = str(v[8]) + "%", fg = 'Black', font=("Helvetica", 10))
	lable_gt1.place(x = 35, y = offset + 580)
	lable_gt2 = Label(window, text = str(v[9]) + "%", fg = 'Black', font=("Helvetica", 10))
	lable_gt2.place(x = 85, y = offset + 580)
	lable_gt3 = Label(window, text = str(v[10]) + "%", fg = 'Black', font=("Helvetica", 10))
	lable_gt3.place(x = 135, y = offset + 580)
	lable_gt4 = Label(window, text = str(v[11]) + "%", fg = 'Black', font=("Helvetica", 10))
	lable_gt4.place(x = 185, y = offset + 580)
	lable_gt5 = Label(window, text = str(v[12]) + "%", fg = 'Black', font=("Helvetica", 10))
	lable_gt5.place(x = 235, y = offset + 580)
	lable_gt6 = Label(window, text = str(v[13]) + "%", fg = 'Black', font=("Helvetica", 10))
	lable_gt6.place(x = 285, y = offset + 580)
	lable_gt7 = Label(window, text = str(v[14]) + "%", fg = 'Black', font=("Helvetica", 10))
	lable_gt7.place(x = 335, y = offset + 580)
	
	lable_ct1_t = Label(window, text = "<40°C", fg = 'Green', font=("Helvetica", 10))
	lable_ct1_t.place(x = 30, y = offset + 527)
	lable_ct2_t = Label(window, text = "40°C", fg = 'Green', font=("Helvetica", 10))
	lable_ct2_t.place(x = 80, y = offset + 527)
	lable_ct3_t = Label(window, text = "50°C", fg = 'Yellow', font=("Helvetica", 10))
	lable_ct3_t.place(x = 130, y = offset + 527)
	lable_ct4_t = Label(window, text = "60°C", fg = 'Yellow', font=("Helvetica", 10))
	lable_ct4_t.place(x = 180, y = offset + 527)
	lable_ct5_t = Label(window, text = "70°C", fg = 'orange', font=("Helvetica", 10))
	lable_ct5_t.place(x = 230, y = offset + 527)
	lable_ct6_t = Label(window, text = "80°C", fg = 'Red', font=("Helvetica", 10))
	lable_ct6_t.place(x = 280, y = offset + 527)
	lable_ct7_t = Label(window, text = "90°C", fg = 'Red', font=("Helvetica", 10))
	lable_ct7_t.place(x = 330, y = offset + 527)
	lable_gt1_t = Label(window, text = "<40°C", fg = 'Green', font=("Helvetica", 10))
	lable_gt1_t.place(x = 30, y = offset + 810)
	lable_gt2_t = Label(window, text = "40°C", fg = 'Green', font=("Helvetica", 10))
	lable_gt2_t.place(x = 80, y = offset + 810)
	lable_gt3_t = Label(window, text = "50°C", fg = 'Yellow', font=("Helvetica", 10))
	lable_gt3_t.place(x = 130, y = offset + 810)
	lable_gt4_t = Label(window, text = "60°C", fg = 'Yellow', font=("Helvetica", 10))
	lable_gt4_t.place(x = 180, y = offset + 810)
	lable_gt5_t = Label(window, text = "70°C", fg = 'orange', font=("Helvetica", 10))
	lable_gt5_t.place(x = 230, y = offset + 810)
	lable_gt6_t = Label(window, text = "80°C", fg = 'red', font=("Helvetica", 10))
	lable_gt6_t.place(x = 280, y = offset + 810)
	lable_gt7_t = Label(window, text = "90°C", fg = 'red', font=("Helvetica", 10))
	lable_gt7_t.place(x = 330, y = offset + 810)
		
	def sct_val(val):
		lable_ct1.config(text = str(sct1.get()) + "%")
		lable_ct2.config(text = str(sct2.get()) + "%")
		lable_ct3.config(text = str(sct3.get()) + "%")
		lable_ct4.config(text = str(sct4.get()) + "%")
		lable_ct5.config(text = str(sct5.get()) + "%")
		lable_ct6.config(text = str(sct6.get()) + "%")
		lable_ct7.config(text = str(sct7.get()) + "%")
		lable_gt1.config(text = str(sgt1.get()) + "%")
		lable_gt2.config(text = str(sgt2.get()) + "%")
		lable_gt3.config(text = str(sgt3.get()) + "%")
		lable_gt4.config(text = str(sgt4.get()) + "%")
		lable_gt5.config(text = str(sgt5.get()) + "%")
		lable_gt6.config(text = str(sgt6.get()) + "%")
		lable_gt7.config(text = str(sgt7.get()) + "%")
		return

	sct1 = Scale(window, from_ = 150, to = 0, orient = VERTICAL, length = 200, showvalue = 0, tickinterval = 5, resolution = 5, command = sct_val)
	sct1.place(x = 10, y = offset + 320)
	sct1.set(v[1])
	sct2 = Scale(window, from_ = 150, to = 0, orient = VERTICAL, length = 200, showvalue = 0, tickinterval = 5, resolution = 5, command = sct_val)
	sct2.place(x = 60, y = offset + 320)
	sct2.set(v[2])
	sct3 = Scale(window, from_ = 150, to = 0, orient = VERTICAL, length = 200, showvalue = 0, tickinterval = 5, resolution = 5, command = sct_val)
	sct3.place(x = 110, y = offset + 320)
	sct3.set(v[3])
	sct4 = Scale(window, from_ = 150, to = 0, orient = VERTICAL, length = 200, showvalue = 0, tickinterval = 5, resolution = 5, command = sct_val)
	sct4.place(x = 160, y = offset + 320)
	sct4.set(v[4])
	sct5 = Scale(window, from_ = 150, to = 0, orient = VERTICAL, length = 200, showvalue = 0, tickinterval = 5, resolution = 5, command = sct_val)
	sct5.place(x = 210, y = offset + 320)
	sct5.set(v[5])
	sct6 = Scale(window, from_ = 150, to = 0, orient = VERTICAL, length = 200, showvalue = 0, tickinterval = 5, resolution = 5, command = sct_val)
	sct6.place(x = 260, y = offset + 320)
	sct6.set(v[6])
	sct7 = Scale(window, from_ = 150, to = 0, orient = VERTICAL, length = 200, showvalue = 0, tickinterval = 5, resolution = 5, command = sct_val)
	sct7.place(x = 310, y = offset + 320)
	sct7.set(v[7])
	sgt1 = Scale(window, from_ = 150, to = 0, orient = VERTICAL, length = 200, showvalue = 0, tickinterval = 5, resolution = 5, command = sct_val)
	sgt1.place(x = 10, y = offset + 600)
	sgt1.set(v[8])
	sgt2 = Scale(window, from_ = 150, to = 0, orient = VERTICAL, length = 200, showvalue = 0, tickinterval = 5, resolution = 5, command = sct_val)
	sgt2.place(x = 60, y = offset + 600)
	sgt2.set(v[9])
	sgt3 = Scale(window, from_ = 150, to = 0, orient = VERTICAL, length = 200, showvalue = 0, tickinterval = 5, resolution = 5, command = sct_val)
	sgt3.place(x = 110, y = offset + 600)
	sgt3.set(v[10])
	sgt4 = Scale(window, from_ = 150, to = 0, orient = VERTICAL, length = 200, showvalue = 0, tickinterval = 5, resolution = 5, command = sct_val)
	sgt4.place(x = 160, y = offset + 600)
	sgt4.set(v[11])
	sgt5 = Scale(window, from_ = 150, to = 0, orient = VERTICAL, length = 200, showvalue = 0, tickinterval = 5, resolution = 5, command = sct_val)
	sgt5.place(x = 210, y = offset + 600)
	sgt5.set(v[12])
	sgt6 = Scale(window, from_ = 150, to = 0, orient = VERTICAL, length = 200, showvalue = 0, tickinterval = 5, resolution = 5, command = sct_val)
	sgt6.place(x = 260, y = offset + 600)
	sgt6.set(v[13])
	sgt7 = Scale(window, from_ = 150, to = 0, orient = VERTICAL, length = 200, showvalue = 0, tickinterval = 5, resolution = 5, command = sct_val)
	sgt7.place(x = 310, y = offset + 600)
	sgt7.set(v[14])

	def adv_apply():
		vr = [140, sct1.get(), sct2.get(), sct3.get(), sct4.get(), sct5.get(), sct6.get(), sct7.get(), sgt1.get(), sgt2.get(), sgt3.get(), sgt4.get(), sgt5.get(), sgt6.get(), sgt7.get()]
		write_EC(vr)
		return
	
	adv = Button(window, text = "Apply", width = 20, fg = 'black', command = adv_apply)
	adv.place(x = 90, y = offset + 830)
	
	a_on.config(fg = 'black', command = auto_on)
	b_on.config(fg = 'black', command = basic_build)
	ad_on.config(fg = 'red', command = null)
	cb_on.config(fg = 'black', command = cooler_booster_on)
	return

"""########################################## Cooler Booster Mode"""

def cooler_booster_on():
	window.geometry('370x270')
	with open(EC_IO_FILE,'w+b') as file:
	    file.seek(0x98)
	    file.write(bytes((128,)))
	a_on.config(fg = 'black', command = auto_on)
	b_on.config(fg = 'black', command = basic_build)
	ad_on.config(fg = 'black', command = advanced_on)
	cb_on.config(fg = 'red', command = null)
	return
	
cb = Label(window, text = "Fan Mode", fg = 'red', font=("Helvetica", 12))
cb.place(x = 150, y = 215)

a_on = Button(window, text = "Auto", width = 6, fg = 'black', command = auto_on)
a_on.place(x = 10, y = 235)
	
b_on = Button(window, text = "Basic", width = 6, fg = 'black', command = basic_build)
b_on.place(x = 90, y = 235)
	
ad_on = Button(window, text = "Advanced", width = 6, fg = 'black', command = advanced_on)
ad_on.place(x = 170, y = 235)
	
cb_on = Button(window, text = "Cooler Booster", width = 10, fg = 'black', command = cooler_booster_on)
cb_on.place(x = 250, y = 235)
	
"""########################################## Fan Mode Select"""
	
def fan_mode():
	v = read_EC()
	canvas.create_line(0, 210, 370, 210, dash=(10, 4), fill = "grey")
	window.geometry('370x270')

	if v[0] == 128:
		cb_on.config(fg = 'red')
	if v[0] == 12:
		a_on.config(fg = 'red')
	if v[0] == 76:
		b_on.config(fg = 'red')
	if v[0] == 140:
		ad_on.config(fg = 'red')
	return
    
button4 = Button(window, text = "Fan Modes", width = 20, fg = 'black', command = fan_mode)
button4.place(x = 90, y = 170)

def on_closing():
	if monitoring == 1:
		timer.cancel()
	window.destroy()
	return

canvas.pack(fill = BOTH, expand = 1)
window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()
