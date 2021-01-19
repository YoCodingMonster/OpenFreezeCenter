#! /usr/bin/python3

from tkinter import *
from tkinter import messagebox
import getpass
import os
import sys
import subprocess
import git

if os.geteuid() == 0:
    print("We're root!")
else:
    print("We're not root.")
    os.system('gksudo ls')

v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, cb_flag = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 140

username = getpass.getuser()
path_check = "/home/" + username + "/MSI-Dragon-Center-Linux"
install_check = "/etc/modprobe.d/GUI-MSI-DC-L-ec_sys.conf"
check = os.path.exists(path_check)
check2 = os.path.exists(install_check)
path = "/home/" + username
if check2 == True:
	EC_IO_FILE = '/sys/kernel/debug/ec/ec0/io'

def ec_write(v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, cb_flag):
	file = open(EC_IO_FILE, "r+b")
	list_cta = [106, 107, 108, 109, 110, 111]
	list_ct = [40, 50, 60, 70, 80, 90]
	list_cfsa = [114, 115, 116, 117, 118, 119, 120]
	list_cfs = [v1, v2, v3, v4, v5, v6, v7]
	list_gta = [130, 131, 132, 133, 134, 135]
	list_gt = [40, 50, 60, 70, 80, 90]
	list_gfsa = [138, 139, 140, 141, 142, 143, 144]
	list_gfs = [v8, v9, v10, v11, v12, v13, v14]
	ap = "MSI_ADDRESS_DEFAULT"
	fma = 244
	fm = cb_flag 
	with open(EC_IO_FILE,'r+b') as file:
		file.seek(fma)
		file.write(bytes((fm,)))
		for i in range(6):
			file.seek(list_cta[i])
			file.write(bytes((list_ct[i],)))
			file.seek(list_gta[i])
			file.write(bytes((list_gt[i],)))
		for i in range(7):
			file.seek(list_cfsa[i])
			file.write(bytes((list_cfs[i],)))
			file.seek(list_gfsa[i])
			file.write(bytes((list_gfs[i],)))

model = {"14A1EMS1": "GS40_6QE",
         "14A3EMS1": "GS43_7RE",
         "16F4EMS1": "GT60_2PE",
         "16J1EMS1": "GE62_2QF",
         "16J5EMS1": "GE62_6QE",
         "16J6EMS1": "GL62_6QD",
         "16J9EMS1": "GE62_7RD",
         "16J9EMS1": "GE62_7RE",
         "16J9EMS1": "GF62_7RD",
         "16J9EMS1": "GF62_7RE",
         "16J9EMS1": "GL62_7RD",
         "16J9EMS1": "GL62_7RDX",
         "16J9EMS1": "GL62M_7RD",
         "16J9EMS1": "GL62M_7RDX",
         "16J9EMS1": "GL62M_7RE",
         "16J9EMS1": "GL62M_7REX",
         "16J9EMS1": "GP62_7RD",
         "16J9EMS1": "GP62_7RDX",
         "16J9EMS1": "GP62_7RE",
         "16J9EMS1": "GP62_7REX",
         "16J9EMS1": "GP62M_7RD",
         "16J9EMS1": "GP62M_7RDX",
         "16J9EMS1": "GP62M_7REX",
         "16J9EMS1": "GV62_7RD",
         "16J9EMS1": "GV62_7RE",
         "16J9EMS1": "PE60_7RD",
         "16J9EMS1": "PE62_7RD",
         "16JBEMS1": "GE62_6RF",
         "16JBEMS1": "GE62_7RF",
         "16JBEMS1": "GL62_7RFX",
         "16JBEMS1": "GP62_7RF",
         "16JBEMS1": "GP62M_6RF",
         "16JBEMS1": "GP62M_7RF",
         "16JBEMS1": "GV62_7RF",
         "16JEEMS1": "GF62_8RE",
         "16JEEMS1": "GV62_8RE",
         "16JFEMS1": "GF62_8RC",
         "16JFEMS1": "GF62_8RD",
         "16JFEMS1": "GP62_8RD",
         "16JFEMS1": "GV62_8RC",
         "16JFEMS1": "GV62_8RD",
         "16JFEMS1": "PE62_8RC",
         "16JFEMS1": "PE62_8RD",
         "16K2EMS1": "GS63_7RF",
         "16K5EMS1": "GS63_8RE",
         "16L1ED61": "MSI_16L13/TORNADO_F5",
         "16L2EMS1": "GT62_6RD",
         "16L2EMS1": "GT62_6RE",
         "16L2EMS1": "GT62_7RD",
         "16L2EMS1": "GT62_7RE",
         "16P6EMS1": "GL63_8RC",
         "16P6EMS1": "GL63_8RD",
         "16P6EMS1": "GP63_8RD",
         "16Q2EMS1": "GS65_8RE",
         "16Q2EMS1": "GS65_8RF",
         "16Q2EMS2": "P65_8RF",
         "16Q2EWS1": "WS65_8SK",
         "16Q3EMS1": "P65_8RE",
         "16Q3EMS1": "P65_8RD",
         "16Q4EMS1": "GS65_8SE",
         "16Q4EMS1": "GS65_8SF",
         "16Q4EMS1": "GS65_8SG",
         "16Q4EMS1": "GS65_9SD",
         "16Q4EMS1": "GS65_9SE",
         "16Q4EMS1": "GS65_9SF",
         "16Q4EMS1": "GS65_9SG",
         "16R1EMS1": "GF63_8RC",
         "16R1EMS1": "GF63_8RD",
         "16R3EMS1": "GF63_8RCS",
         "16R3EMS1": "GF63_9RC",
         "16R3EMS1": "GF63_9RCX",
         "16R3EMS1": "GF63_9SC",
         "16S2EMS1": "PS63_8SC",
         "16S3EMS1": "P15_A10RC",
         "16S3EMS1": "P15_A10SC",
         "16U4EMS1": "GL65_9SCK",
         "16U5EMS1": "GL65_9SD",
         "16U5EMS1": "GL65_9SDK",
         "16U5EMS1": "GL65_9SE",
         "16U5EMS1": "GL65_9SEK",
         "16W1EMS1": "15M_A9SD",
         "16W1EMS1": "15M_A9SE",
         "16W1EMS1": "GF65_9SD",
         "16W1EMS1": "GF65_9SE",
         "1791EMS1": "GE72_2QF",
         "179CEMS1": "GE72M_7RG",
         "17A6EMS1": "GT75_8SF",
         "17A6EMS1": "GT75_8SG",
         "17B1EMS1": "GS73_7RF",
         "17B5EMS1": "GS73_8RE",
         "17C6EMS1": "GL73_8RC",
         "17C6EMS1": "GL73_8RD",
         "17C6EMS1": "GP73_8RD",
         "17E2EMS1": "GE75_8SE",
         "17E2EMS1": "GE75_8SF",
         "17E2EMS1": "GE75_8SG",
         "17E2EMS1": "GE75_9SG",
         "17G1EMS1": "GS75_8SE",
         "17G1EMS1": "GS75_8SF",
         "17G1EMS1": "GS75_8SG",
         "17G1EMS1": "GS75_9SD",
         "17G1EMS1": "GS75_9SE",
         "17G1EMS1": "GS75_9SF",
         "17G1EMS1": "GS75_9SG"}

window = Tk()
window.title('MSI Dragon Center for Linux')
window.geometry('370x210')
canvas = Canvas(window)

lable1 = Label(window, text = "Creator :-> Aditya Kumar Bajpai", fg = 'red', font=("Helvetica", 16))
lable1.place(x = 30, y = 10)

def clone_git():
    path = "/home/" + username + "/"
    git.Git(path).clone('https://github.com/AdityaKumarBajpai/MSI-Dragon-Center-Linux.git')
    messagebox.showinfo('GUI-MSI-DC-L', 'MSI Dragon Center for Linux is copied to HOME folder from GIT page!\nClick on Install to set it up.\nSystem will reboot after install is over!!')
    return

def install():
    os.system("gnome-terminal -e 'bash -c \"sudo install -Dm 644 etc/modprobe.d/GUI-MSI-DC-L-ec_sys.conf \"${pkgdir}/etc/modprobe.d/GUI-MSI-DC-L-ec_sys.conf\" && sudo install -Dm 644 etc/modules-load.d/GUI-MSI-DC-L-ec_sys.conf \"${pkgdir}/etc/modules-load.d/GUI-MSI-DC-L-ec_sys.conf\" && sudo reboot; exec bash\"'")
    return

def startup():
    return

def monitor():
    return

def uninstall():
    os.system("gnome-terminal -e 'bash -c \"sudo rm /etc/modprobe.d/GUI-MSI-DC-L-ec_sys.conf /etc/modules-load.d/GUI-MSI-DC-L-ec_sys.conf; exec bash\"'")
    return

if (check == False) & (check2 == False):
    button1 = Button(window, text = "Clone GIT", width = 20, fg = 'black', command = clone_git)
    button1.place(x = 90, y = 50)
else:
    button1 = Button(window, text = "Clone GIT", width = 20, fg = 'grey')
    button1.place(x = 90, y = 50)

if check2 == False:
    button2 = Button(window, text = "Install", width = 20, fg = 'black', command = install)
    button2.place(x = 90, y = 80)
else:
    button2 = Button(window, text = "Install", width = 20, fg = 'grey')
    button2.place(x = 90, y = 80)

button3 = Button(window, text = "Run at Startup", width = 20, fg = 'black', command = startup)
button3.place(x = 90, y = 110)

button4 = Button(window, text = "Monitor", width = 20, fg = 'black', command = monitor)
button4.place(x = 90, y = 140)

if check2 == True:
    button5 = Button(window, text = "Uninstall ISW", width = 20, fg = 'black', command = uninstall)
    button5.place(x = 90, y = 170)
else:
    button5 = Button(window, text = "Uninstall ISW", width = 20, fg = 'grey')
    button5.place(x = 90, y = 170)

canvas.create_line(0, 210, 370, 210, dash=(10, 4), fill = "grey")

if check2 == True:
    window.geometry('370x900')
    def cpu_adv_apply():
        with open(EC_IO_FILE,'r+b') as file:
            file.seek(0x72)
            file.write(bytes((sct1.get(),)))
            file.seek(0x73)
            file.write(bytes((sct2.get(),)))
            file.seek(0x74)
            file.write(bytes((sct3.get(),)))
            file.seek(0x75)
            file.write(bytes((sct4.get(),)))
            file.seek(0x76)
            file.write(bytes((sct5.get(),)))
            file.seek(0x77)
            file.write(bytes((sct6.get(),)))
            file.seek(0x78)
            file.write(bytes((sct7.get(),)))
            file.seek(0x6a)
            file.write(bytes((40,)))
            file.seek(0x6b)
            file.write(bytes((50,)))
            file.seek(0x6c)
            file.write(bytes((60,)))
            file.seek(0x6d)
            file.write(bytes((70,)))
            file.seek(0x6e)
            file.write(bytes((80,)))
            file.seek(0x6f)
            file.write(bytes((90,)))
        return
        
    def gpu_adv_apply():
        with open(EC_IO_FILE,'r+b') as file:
            file.seek(0x8a)
            file.write(bytes((sct1.get(),)))
            file.seek(0x8b)
            file.write(bytes((sct2.get(),)))
            file.seek(0x8c)
            file.write(bytes((sct3.get(),)))
            file.seek(0x8d)
            file.write(bytes((sct4.get(),)))
            file.seek(0x8e)
            file.write(bytes((sct5.get(),)))
            file.seek(0x8f)
            file.write(bytes((sct6.get(),)))
            file.seek(0x90)
            file.write(bytes((sct7.get(),)))
            file.seek(0x82)
            file.write(bytes((40,)))
            file.seek(0x83)
            file.write(bytes((50,)))
            file.seek(0x84)
            file.write(bytes((60,)))
            file.seek(0x85)
            file.write(bytes((70,)))
            file.seek(0x86)
            file.write(bytes((80,)))
            file.seek(0x87)
            file.write(bytes((90,)))
        return
        
    def sct1_val(v):
        lable_ct1.config(text = v + "%")
        return

    def sct2_val(v):
        lable_ct2.config(text = v + "%")
        return

    def sct3_val(v):
        lable_ct3.config(text = v + "%")
        return

    def sct4_val(v):
        lable_ct4.config(text = v + "%")
        return

    def sct5_val(v):
        lable_ct5.config(text = v + "%")
        return

    def sct6_val(v):
        lable_ct6.config(text = v + "%")
        return

    def sct7_val(v):
        lable_ct7.config(text = v + "%")
        return

    def sgt1_val(v):
        lable_gt1.config(text = v + "%")
        return

    def sgt2_val(v):
        lable_gt2.config(text = v + "%")
        return

    def sgt3_val(v):
        lable_gt3.config(text = v + "%")
        return

    def sgt4_val(v):
        lable_gt4.config(text = v + "%")
        return

    def sgt5_val(v):
        lable_gt5.config(text = v + "%")
        return

    def sgt6_val(v):
        lable_gt6.config(text = v + "%")
        return

    def sgt7_val(v):
        lable_gt7.config(text = v + "%")
        return
        
    lable_ct7 = Label(window, text = "CPU fan Speeds" , fg = 'blue', font=("Helvetica", 10))
    lable_ct7.place(x = 135, y = 220)
    
    lable_ct1 = Label(window, text = str(v1) + "%", fg = 'Black', font=("Helvetica", 10))
    lable_ct1.place(x = 35, y = 240)
    lable_ct2 = Label(window, text = str(v2) + "%", fg = 'Black', font=("Helvetica", 10))
    lable_ct2.place(x = 85, y = 240)
    lable_ct3 = Label(window, text = str(v3) + "%", fg = 'Black', font=("Helvetica", 10))
    lable_ct3.place(x = 135, y = 240)
    lable_ct4 = Label(window, text = str(v4) + "%", fg = 'Black', font=("Helvetica", 10))
    lable_ct4.place(x = 185, y = 240)
    lable_ct5 = Label(window, text = str(v5) + "%", fg = 'Black', font=("Helvetica", 10))
    lable_ct5.place(x = 235, y = 240)
    lable_ct6 = Label(window, text = str(v6) + "%", fg = 'Black', font=("Helvetica", 10))
    lable_ct6.place(x = 285, y = 240)
    lable_ct7 = Label(window, text = str(v7) + "%", fg = 'Black', font=("Helvetica", 10))
    lable_ct7.place(x = 335, y = 240)
    
    lable_ct1_t = Label(window, text = "<40°C", fg = 'Green', font=("Helvetica", 10))
    lable_ct1_t.place(x = 30, y = 470)
    lable_ct2_t = Label(window, text = "40°C", fg = 'Green', font=("Helvetica", 10))
    lable_ct2_t.place(x = 80, y = 470)
    lable_ct3_t = Label(window, text = "50°C", fg = 'Yellow', font=("Helvetica", 10))
    lable_ct3_t.place(x = 130, y = 470)
    lable_ct4_t = Label(window, text = "60°C", fg = 'Yellow', font=("Helvetica", 10))
    lable_ct4_t.place(x = 180, y = 470)
    lable_ct5_t = Label(window, text = "70°C", fg = 'Red', font=("Helvetica", 10))
    lable_ct5_t.place(x = 230, y = 470)
    lable_ct6_t = Label(window, text = "80°C", fg = 'Red', font=("Helvetica", 10))
    lable_ct6_t.place(x = 280, y = 470)
    lable_ct7_t = Label(window, text = "90°C", fg = 'Red', font=("Helvetica", 10))
    lable_ct7_t.place(x = 330, y = 470)

    cpu_adv = Button(window, text = "Apply", width = 20, fg = 'black', command = cpu_adv_apply)
    cpu_adv.place(x = 90, y = 490)

    canvas.create_line(0, 530, 370, 530, dash=(10, 4), fill = "grey")

    lable_gt7 = Label(window, text = "GPU fan Speeds" , fg = 'blue', font=("Helvetica", 10))
    lable_gt7.place(x = 135, y = 540)

    lable_gt1 = Label(window, text = str(v8) + "%", fg = 'Black', font=("Helvetica", 10))
    lable_gt1.place(x = 35, y = 560)
    lable_gt2 = Label(window, text = str(v9) + "%", fg = 'Black', font=("Helvetica", 10))
    lable_gt2.place(x = 85, y = 560)
    lable_gt3 = Label(window, text = str(v10) + "%", fg = 'Black', font=("Helvetica", 10))
    lable_gt3.place(x = 135, y = 560)
    lable_gt4 = Label(window, text = str(v11) + "%", fg = 'Black', font=("Helvetica", 10))
    lable_gt4.place(x = 185, y = 560)
    lable_gt5 = Label(window, text = str(v12) + "%", fg = 'Black', font=("Helvetica", 10))
    lable_gt5.place(x = 235, y = 560)
    lable_gt6 = Label(window, text = str(v13) + "%", fg = 'Black', font=("Helvetica", 10))
    lable_gt6.place(x = 285, y = 560)
    lable_gt7 = Label(window, text = str(v14) + "%", fg = 'Black', font=("Helvetica", 10))
    lable_gt7.place(x = 335, y = 560)
    
    lable_gt1_t = Label(window, text = "<40°C", fg = 'Green', font=("Helvetica", 10))
    lable_gt1_t.place(x = 30, y = 790)
    lable_gt2_t = Label(window, text = "40°C", fg = 'Green', font=("Helvetica", 10))
    lable_gt2_t.place(x = 80, y = 790)
    lable_gt3_t = Label(window, text = "50°C", fg = 'Yellow', font=("Helvetica", 10))
    lable_gt3_t.place(x = 130, y = 790)
    lable_gt4_t = Label(window, text = "60°C", fg = 'Yellow', font=("Helvetica", 10))
    lable_gt4_t.place(x = 180, y = 790)
    lable_gt5_t = Label(window, text = "70°C", fg = 'red', font=("Helvetica", 10))
    lable_gt5_t.place(x = 230, y = 790)
    lable_gt6_t = Label(window, text = "80°C", fg = 'red', font=("Helvetica", 10))
    lable_gt6_t.place(x = 280, y = 790)
    lable_gt7_t = Label(window, text = "90°C", fg = 'red', font=("Helvetica", 10))
    lable_gt7_t.place(x = 330, y = 790)
    
    gpu_adv = Button(window, text = "Apply", width = 20, fg = 'black', command = gpu_adv_apply)
    gpu_adv.place(x = 90, y = 810)

    canvas.create_line(0, 850, 370, 850, dash=(10, 4), fill = "grey")

    cb = Label(window, text = "Cooler Booster :->", fg = 'red', font=("Helvetica", 12))
    cb.place(x = 30, y = 866)

    sct1 = Scale(window, from_ = 150, to = 0, orient = VERTICAL, length = 200, showvalue = 0, tickinterval = 5, resolution = 5, command = sct1_val)
    sct1.place(x = 10, y = 260)
    sct1.set(v1)
    sct2 = Scale(window, from_ = 150, to = 0, orient = VERTICAL, length = 200, showvalue = 0, tickinterval = 5, resolution = 5, command = sct2_val)
    sct2.place(x = 60, y = 260)
    sct2.set(v2)
    sct3 = Scale(window, from_ = 150, to = 0, orient = VERTICAL, length = 200, showvalue = 0, tickinterval = 5, resolution = 5, command = sct3_val)
    sct3.place(x = 110, y = 260)
    sct3.set(v3)
    sct4 = Scale(window, from_ = 150, to = 0, orient = VERTICAL, length = 200, showvalue = 0, tickinterval = 5, resolution = 5, command = sct4_val)
    sct4.place(x = 160, y = 260)
    sct4.set(v4)
    sct5 = Scale(window, from_ = 150, to = 0, orient = VERTICAL, length = 200, showvalue = 0, tickinterval = 5, resolution = 5, command = sct5_val)
    sct5.place(x = 210, y = 260)
    sct5.set(v5)
    sct6 = Scale(window, from_ = 150, to = 0, orient = VERTICAL, length = 200, showvalue = 0, tickinterval = 5, resolution = 5, command = sct6_val)
    sct6.place(x = 260, y = 260)
    sct6.set(v6)
    sct7 = Scale(window, from_ = 150, to = 0, orient = VERTICAL, length = 200, showvalue = 0, tickinterval = 5, resolution = 5, command = sct7_val)
    sct7.place(x = 310, y = 260)
    sct7.set(v7)

    sgt1 = Scale(window, from_ = 150, to = 0, orient = VERTICAL, length = 200, showvalue = 0, tickinterval = 5, resolution = 5, command = sgt1_val)
    sgt1.place(x = 10, y = 580)
    sgt1.set(v8)
    sgt2 = Scale(window, from_ = 150, to = 0, orient = VERTICAL, length = 200, showvalue = 0, tickinterval = 5, resolution = 5, command = sgt2_val)
    sgt2.place(x = 60, y = 580)
    sgt2.set(v9)
    sgt3 = Scale(window, from_ = 150, to = 0, orient = VERTICAL, length = 200, showvalue = 0, tickinterval = 5, resolution = 5, command = sgt3_val)
    sgt3.place(x = 110, y = 580)
    sgt3.set(v10)
    sgt4 = Scale(window, from_ = 150, to = 0, orient = VERTICAL, length = 200, showvalue = 0, tickinterval = 5, resolution = 5, command = sgt4_val)
    sgt4.place(x = 160, y = 580)
    sgt4.set(v11)
    sgt5 = Scale(window, from_ = 150, to = 0, orient = VERTICAL, length = 200, showvalue = 0, tickinterval = 5, resolution = 5, command = sgt5_val)
    sgt5.place(x = 210, y = 580)
    sgt5.set(v12)
    sgt6 = Scale(window, from_ = 150, to = 0, orient = VERTICAL, length = 200, showvalue = 0, tickinterval = 5, resolution = 5, command = sgt6_val)
    sgt6.place(x = 260, y = 580)
    sgt6.set(v13)
    sgt7 = Scale(window, from_ = 150, to = 0, orient = VERTICAL, length = 200, showvalue = 0, tickinterval = 5, resolution = 5, command = sgt7_val)
    sgt7.place(x = 310, y = 580)
    sgt7.set(v14)

    def cb_turbo_on():
        with open(EC_IO_FILE,'r+b') as file:
            file.seek(0x98)
            file.write(bytes((128,)))
        return

    def cb_turbo_off():
        with open(EC_IO_FILE,'r+b') as file:
            file.seek(0x98)
            file.write(bytes((140,)))
        return

    with open(EC_IO_FILE,'r+b') as file:
        file.seek(0x98)
        cb_flag = int(file.read(1).hex(),16)
    
    if (cb_flag == 128):
        cb_on = Button(window, text = "ON", width = 5, fg = 'grey')
        cb_on.place(x = 180, y = 860)
        cb_off = Button(window, text = "OFF", width = 5, fg = 'black', command = cb_turbo_off)
        cb_off.place(x = 260, y = 860)
    if (cb_flag != 128):
        cb_on = Button(window, text = "ON", width = 5, fg = 'black', command = cb_turbo_on)
        cb_on.place(x = 180, y = 860)
        cb_off = Button(window, text = "OFF", width = 5, fg = 'grey')
        cb_off.place(x = 260, y = 860)

canvas.pack(fill = BOTH, expand = 1)
window.mainloop()
    
