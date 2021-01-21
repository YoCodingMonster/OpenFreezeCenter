#! /usr/bin/python3

from tkinter import *
from tkinter import messagebox
import os
import sys
import subprocess

############################################################################################## Variables

EC_IO_FILE = '/sys/kernel/debug/ec/ec0/io'
v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, cb, fm, offset, y = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 12, 0, 100
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

install_check = "/etc/modprobe.d/GUI-MSI-DC-L-ec_sys.conf"
check2 = os.path.exists(install_check)

if check2 == True:
    file = open(EC_IO_FILE, "r+b")
    with open(EC_IO_FILE,'r+b') as file:
        file.seek(114)
        v1 = int(file.read(1).hex(),16)
        file.seek(115)
        v2 = int(file.read(1).hex(),16)
        file.seek(116)
        v3 = int(file.read(1).hex(),16)
        file.seek(117)
        v4 = int(file.read(1).hex(),16)
        file.seek(118)
        v5 = int(file.read(1).hex(),16)
        file.seek(119)
        v6 = int(file.read(1).hex(),16)
        file.seek(120)
        v7 = int(file.read(1).hex(),16)
        file.seek(138)
        v8 = int(file.read(1).hex(),16)
        file.seek(139)
        v9 = int(file.read(1).hex(),16)
        file.seek(140)
        v10 = int(file.read(1).hex(),16)
        file.seek(141)
        v11 = int(file.read(1).hex(),16)
        file.seek(142)
        v12 = int(file.read(1).hex(),16)
        file.seek(143)
        v13 = int(file.read(1).hex(),16)
        file.seek(144)
        v14 = int(file.read(1).hex(),16)
        file.seek(0xf4)
        fm = int(file.read(1).hex(),16)
        file.seek(0x98)
        cb = int(file.read(1).hex(),16)

def null():
    return

window = Tk()
window.title('MSI Dragon Center for Linux')
window.geometry('370x210')
canvas = Canvas(window)

############################################################################################## Section 1

lable1 = Label(window, text = "Creator :-> Aditya Kumar Bajpai", fg = 'red', font=("Helvetica", 16))
lable1.place(x = 30, y = 10)

lable2 = Label(window, text = "Version 1.0.0", fg = 'black', font=("Helvetica", 16))
lable2.place(x = 122, y = 50)

def install():
    os.system("gnome-terminal -e 'bash -c \"sudo install -Dm 644 etc/modprobe.d/GUI-MSI-DC-L-ec_sys.conf \"${pkgdir}/etc/modprobe.d/GUI-MSI-DC-L-ec_sys.conf\" && sudo install -Dm 644 etc/modules-load.d/GUI-MSI-DC-L-ec_sys.conf \"${pkgdir}/etc/modules-load.d/GUI-MSI-DC-L-ec_sys.conf\" && reboot; exec bash\"'")
    button5.config(fg = 'black', command = uninstall)
    button2.config(fg = 'grey', command = null)
    messagebox.showinfo("Installation Complete!", "Please Reboot your system to enable EC module write capablities of script") 
    return

button2 = Button(window, text = "Install", width = 20, fg = 'black', command = install)
button2.place(x = 90, y = 80)

def startup():
    return

button3 = Button(window, text = "Run at Startup", width = 20, fg = 'black', command = startup)
button3.place(x = 90, y = 110)

def monitor():
    return

button4 = Button(window, text = "Monitor", width = 20, fg = 'black', command = monitor)
button4.place(x = 90, y = 140)

def uninstall():
    os.system("gnome-terminal -e 'bash -c \"sudo rm /etc/modprobe.d/GUI-MSI-DC-L-ec_sys.conf /etc/modules-load.d/GUI-MSI-DC-L-ec_sys.conf; exec bash\"'")
    button2.config(fg = 'black', command = install)
    button5.config(fg = 'grey', command = null)
    return

button5 = Button(window, text = "Uninstall", width = 20, fg = 'grey')
button5.place(x = 90, y = 170)

if check2 == False:
    button2.config(fg = 'black', command = install)
    button5.config(fg = 'grey', command = null)
else:
    button2.config(fg = 'grey', command = null)
    button5.config(fg = 'black', command = uninstall)

canvas.create_line(0, 210, 370, 210, dash=(10, 4), fill = "grey")

############################################################################################## Section 2
if check2 == True:
    window.geometry('370x270')
    cb = Label(window, text = "Fan Mode", fg = 'red', font=("Helvetica", 12))
    cb.place(x = 150, y = 215)

def auto_on():
    window.geometry('370x270')
    basic_slider.pack_forget()
    button_basic.pack_forget()
    with open(EC_IO_FILE,'r+b') as file:
        file.seek(0xf4)
        file.write(bytes((12,)))
        file.seek(0x98)
        file.write(bytes((0,)))
        file.seek(114)
        file.write(bytes((0,)))
        file.seek(115)
        file.write(bytes((20,)))
        file.seek(116)
        file.write(bytes((40,)))
        file.seek(117)
        file.write(bytes((45,)))
        file.seek(118)
        file.write(bytes((50,)))
        file.seek(119)
        file.write(bytes((60,)))
        file.seek(120)
        file.write(bytes((70,)))
        file.seek(138)
        file.write(bytes((0,)))
        file.seek(139)
        file.write(bytes((20,)))
        file.seek(140)
        file.write(bytes((40,)))
        file.seek(141)
        file.write(bytes((45,)))
        file.seek(142)
        file.write(bytes((50,)))
        file.seek(143)
        file.write(bytes((60,)))
        file.seek(144)
        file.write(bytes((70,)))
    a_on.config(fg = 'red', command = null)
    b_on.config(fg = 'black', command = basic_build)
    ad_on.config(fg = 'black', command = advanced_on)
    cb_on.config(fg = 'black', command = cooler_booster_on)
    return

if check2 == True:
    a_on = Button(window, text = "Auto", width = 6, fg = 'black', command = auto_on)
    a_on.place(x = 10, y = 235)
    
basic_slider = Scale(window, from_ = -30, to = 30, orient = HORIZONTAL, length = 200, showvalue = 1, tickinterval = 10, resolution = 10)
basic_slider.place(x = 10, y = 265)
basic_slider.set(offset)
button_basic = Button(window, text = "Apply", width = 10, fg = 'black', command = lambda: basic_on(basic_slider.get()))
button_basic.place(x = 235, y = 280)

def basic_build():
    window.geometry('370x330')
    a_on.config(fg = 'black', command = auto_on)
    b_on.config(fg = 'red', command = null)
    ad_on.config(fg = 'black', command = advanced_on)
    cb_on.config(fg = 'black', command = cooler_booster_on)
    return

def basic_on(offset_local):
    offset = offset_local
    with open(EC_IO_FILE,'r+b') as file:
        file.seek(0xf4)
        file.write(bytes((76,)))
        file.seek(0x98)
        file.write(bytes((0,)))
        if offset >= 0:
            file.seek(114)
            file.write(bytes((0 + offset,)))
        else:
            file.seek(114)
            file.write(bytes((0,)))
        if offset >= -20:
            file.seek(115)
            file.write(bytes((20 + offset,)))
        else:
            file.seek(115)
            file.write(bytes((20,)))
        file.seek(116)
        file.write(bytes((40 + offset,)))
        file.seek(117)
        file.write(bytes((45 + offset,)))
        file.seek(118)
        file.write(bytes((50 + offset,)))
        file.seek(119)
        file.write(bytes((60 + offset,)))
        file.seek(120)
        file.write(bytes((70 + offset,)))
        if offset >= 0:
            file.seek(138)
            file.write(bytes((0 + offset,)))
        else:
            file.seek(138)
            file.write(bytes((0,)))
        if offset >= -20:
            file.seek(139)
            file.write(bytes((20 + offset,)))
        else:
            file.seek(139)
            file.write(bytes((20,)))
        file.seek(140)
        file.write(bytes((40 + offset)))
        file.seek(141)
        file.write(bytes((45 + offset,)))
        file.seek(142)
        file.write(bytes((50 + offset,)))
        file.seek(143)
        file.write(bytes((60 + offset,)))
        file.seek(144)
        file.write(bytes((70 + offset,)))
    return

if check2 == True:
    b_on = Button(window, text = "Basic", width = 6, fg = 'black', command = basic_build)
    b_on.place(x = 90, y = 235)

def advanced_on():
    window.geometry('370x1000')
    basic_slider.pack_forget()
    button_basic.pack_forget()
    
    lable_ct8 = Label(window, text = "CPU fan Speeds" , fg = 'blue', font=("Helvetica", 10))
    lable_ct8.place(x = 135, y = y + 240)

    lable_ct1 = Label(window, text = str(v1) + "%", fg = 'Black', font=("Helvetica", 10))
    lable_ct1.place(x = 35, y = y + 260)
    lable_ct2 = Label(window, text = str(v2) + "%", fg = 'Black', font=("Helvetica", 10))
    lable_ct2.place(x = 85, y = y + 260)
    lable_ct3 = Label(window, text = str(v3) + "%", fg = 'Black', font=("Helvetica", 10))
    lable_ct3.place(x = 135, y = y + 260)
    lable_ct4 = Label(window, text = str(v4) + "%", fg = 'Black', font=("Helvetica", 10))
    lable_ct4.place(x = 185, y = y + 260)
    lable_ct5 = Label(window, text = str(v5) + "%", fg = 'Black', font=("Helvetica", 10))
    lable_ct5.place(x = 235, y = y + 260)
    lable_ct6 = Label(window, text = str(v6) + "%", fg = 'Black', font=("Helvetica", 10))
    lable_ct6.place(x = 285, y = y + 260)
    lable_ct7 = Label(window, text = str(v7) + "%", fg = 'Black', font=("Helvetica", 10))
    lable_ct7.place(x = 335, y = y + 260)

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

    sct1 = Scale(window, from_ = 150, to = 0, orient = VERTICAL, length = 200, showvalue = 0, tickinterval = 5, resolution = 5, command = sct1_val)
    sct1.place(x = 10, y = y + 280)
    sct1.set(v1)
    sct2 = Scale(window, from_ = 150, to = 0, orient = VERTICAL, length = 200, showvalue = 0, tickinterval = 5, resolution = 5, command = sct2_val)
    sct2.place(x = 60, y = y + 280)
    sct2.set(v2)
    sct3 = Scale(window, from_ = 150, to = 0, orient = VERTICAL, length = 200, showvalue = 0, tickinterval = 5, resolution = 5, command = sct3_val)
    sct3.place(x = 110, y = y + 280)
    sct3.set(v3)
    sct4 = Scale(window, from_ = 150, to = 0, orient = VERTICAL, length = 200, showvalue = 0, tickinterval = 5, resolution = 5, command = sct4_val)
    sct4.place(x = 160, y = y + 280)
    sct4.set(v4)
    sct5 = Scale(window, from_ = 150, to = 0, orient = VERTICAL, length = 200, showvalue = 0, tickinterval = 5, resolution = 5, command = sct5_val)
    sct5.place(x = 210, y = y + 280)
    sct5.set(v5)
    sct6 = Scale(window, from_ = 150, to = 0, orient = VERTICAL, length = 200, showvalue = 0, tickinterval = 5, resolution = 5, command = sct6_val)
    sct6.place(x = 260, y = y + 280)
    sct6.set(v6)
    sct7 = Scale(window, from_ = 150, to = 0, orient = VERTICAL, length = 200, showvalue = 0, tickinterval = 5, resolution = 5, command = sct7_val)
    sct7.place(x = 310, y = y + 280)
    sct7.set(v7)

    lable_ct1_t = Label(window, text = "<40°C", fg = 'Green', font=("Helvetica", 10))
    lable_ct1_t.place(x = 30, y = y + 490)
    lable_ct2_t = Label(window, text = "40°C", fg = 'Green', font=("Helvetica", 10))
    lable_ct2_t.place(x = 80, y = y + 490)
    lable_ct3_t = Label(window, text = "50°C", fg = 'Yellow', font=("Helvetica", 10))
    lable_ct3_t.place(x = 130, y = y + 490)
    lable_ct4_t = Label(window, text = "60°C", fg = 'Yellow', font=("Helvetica", 10))
    lable_ct4_t.place(x = 180, y = y + 490)
    lable_ct5_t = Label(window, text = "70°C", fg = 'Red', font=("Helvetica", 10))
    lable_ct5_t.place(x = 230, y = y + 490)
    lable_ct6_t = Label(window, text = "80°C", fg = 'Red', font=("Helvetica", 10))
    lable_ct6_t.place(x = 280, y = y + 490)
    lable_ct7_t = Label(window, text = "90°C", fg = 'Red', font=("Helvetica", 10))
    lable_ct7_t.place(x = 330, y = y + 490)

    def cpu_adv_apply():
        with open(EC_IO_FILE,'r+b') as file:
            v1, v2, v3, v4, v5, v6, v7 =  sct1.get(), sct2.get(), sct3.get(), sct4.get(), sct5.get(), sct6.get(), sct7.get()
            file.seek(114)
            file.write(bytes((sct1.get(),)))
            file.seek(115)
            file.write(bytes((sct2.get(),)))
            file.seek(116)
            file.write(bytes((sct3.get(),)))
            file.seek(117)
            file.write(bytes((sct4.get(),)))
            file.seek(118)
            file.write(bytes((sct5.get(),)))
            file.seek(119)
            file.write(bytes((sct6.get(),)))
            file.seek(120)
            file.write(bytes((sct7.get(),)))
            file.seek(106)
            file.write(bytes((40,)))
            file.seek(107)
            file.write(bytes((50,)))
            file.seek(108)
            file.write(bytes((60,)))
            file.seek(109)
            file.write(bytes((70,)))
            file.seek(110)
            file.write(bytes((80,)))
            file.seek(111)
            file.write(bytes((90,)))
        return

    cpu_adv = Button(window, text = "Apply", width = 20, fg = 'black', command = cpu_adv_apply)
    cpu_adv.place(x = 90, y = y + 510)

    canvas.create_line(0, y + 550, 370, y + 550, dash=(10, 4), fill = "grey")

    lable_gt7 = Label(window, text = "GPU fan Speeds" , fg = 'blue', font=("Helvetica", 10))
    lable_gt7.place(x = 135, y = y + 560)

    lable_gt1 = Label(window, text = str(v8) + "%", fg = 'Black', font=("Helvetica", 10))
    lable_gt1.place(x = 35, y = y + 580)
    lable_gt2 = Label(window, text = str(v9) + "%", fg = 'Black', font=("Helvetica", 10))
    lable_gt2.place(x = 85, y = y + 580)
    lable_gt3 = Label(window, text = str(v10) + "%", fg = 'Black', font=("Helvetica", 10))
    lable_gt3.place(x = 135, y = y + 580)
    lable_gt4 = Label(window, text = str(v11) + "%", fg = 'Black', font=("Helvetica", 10))
    lable_gt4.place(x = 185, y = y + 580)
    lable_gt5 = Label(window, text = str(v12) + "%", fg = 'Black', font=("Helvetica", 10))
    lable_gt5.place(x = 235, y = y + 580)
    lable_gt6 = Label(window, text = str(v13) + "%", fg = 'Black', font=("Helvetica", 10))
    lable_gt6.place(x = 285, y = y + 580)
    lable_gt7 = Label(window, text = str(v14) + "%", fg = 'Black', font=("Helvetica", 10))
    lable_gt7.place(x = 335, y = y + 580)

    sgt1 = Scale(window, from_ = 150, to = 0, orient = VERTICAL, length = 200, showvalue = 0, tickinterval = 5, resolution = 5, command = sgt1_val)
    sgt1.place(x = 10, y = y + 600)
    sgt1.set(v8)
    sgt2 = Scale(window, from_ = 150, to = 0, orient = VERTICAL, length = 200, showvalue = 0, tickinterval = 5, resolution = 5, command = sgt2_val)
    sgt2.place(x = 60, y = y + 600)
    sgt2.set(v9)
    sgt3 = Scale(window, from_ = 150, to = 0, orient = VERTICAL, length = 200, showvalue = 0, tickinterval = 5, resolution = 5, command = sgt3_val)
    sgt3.place(x = 110, y = y + 600)
    sgt3.set(v10)
    sgt4 = Scale(window, from_ = 150, to = 0, orient = VERTICAL, length = 200, showvalue = 0, tickinterval = 5, resolution = 5, command = sgt4_val)
    sgt4.place(x = 160, y = y + 600)
    sgt4.set(v11)
    sgt5 = Scale(window, from_ = 150, to = 0, orient = VERTICAL, length = 200, showvalue = 0, tickinterval = 5, resolution = 5, command = sgt5_val)
    sgt5.place(x = 210, y = y + 600)
    sgt5.set(v12)
    sgt6 = Scale(window, from_ = 150, to = 0, orient = VERTICAL, length = 200, showvalue = 0, tickinterval = 5, resolution = 5, command = sgt6_val)
    sgt6.place(x = 260, y = y + 600)
    sgt6.set(v13)
    sgt7 = Scale(window, from_ = 150, to = 0, orient = VERTICAL, length = 200, showvalue = 0, tickinterval = 5, resolution = 5, command = sgt7_val)
    sgt7.place(x = 310, y = y + 600)
    sgt7.set(v14)

    lable_gt1_t = Label(window, text = "<40°C", fg = 'Green', font=("Helvetica", 10))
    lable_gt1_t.place(x = 30, y = y + 810)
    lable_gt2_t = Label(window, text = "40°C", fg = 'Green', font=("Helvetica", 10))
    lable_gt2_t.place(x = 80, y = y + 810)
    lable_gt3_t = Label(window, text = "50°C", fg = 'Yellow', font=("Helvetica", 10))
    lable_gt3_t.place(x = 130, y = y + 810)
    lable_gt4_t = Label(window, text = "60°C", fg = 'Yellow', font=("Helvetica", 10))
    lable_gt4_t.place(x = 180, y = y + 810)
    lable_gt5_t = Label(window, text = "70°C", fg = 'red', font=("Helvetica", 10))
    lable_gt5_t.place(x = 230, y = y + 810)
    lable_gt6_t = Label(window, text = "80°C", fg = 'red', font=("Helvetica", 10))
    lable_gt6_t.place(x = 280, y = y + 810)
    lable_gt7_t = Label(window, text = "90°C", fg = 'red', font=("Helvetica", 10))
    lable_gt7_t.place(x = 330, y = y + 810)

    def gpu_adv_apply():
        with open(EC_IO_FILE,'r+b') as file:
            v8, v9, v10, v11, v12, v13, v14 =  sgt1.get(), sgt2.get(), sgt3.get(), sgt4.get(), sgt5.get(), sgt6.get(), sgt7.get()
            file.seek(138)
            file.write(bytes((sgt1.get(),)))
            file.seek(139)
            file.write(bytes((sgt2.get(),)))
            file.seek(140)
            file.write(bytes((sgt3.get(),)))
            file.seek(141)
            file.write(bytes((sgt4.get(),)))
            file.seek(142)
            file.write(bytes((sgt5.get(),)))
            file.seek(143)
            file.write(bytes((sgt6.get(),)))
            file.seek(144)
            file.write(bytes((sgt7.get(),)))
            file.seek(130)
            file.write(bytes((40,)))
            file.seek(131)
            file.write(bytes((50,)))
            file.seek(132)
            file.write(bytes((60,)))
            file.seek(133)
            file.write(bytes((70,)))
            file.seek(134)
            file.write(bytes((80,)))
            file.seek(135)
            file.write(bytes((90,)))
        return

    gpu_adv = Button(window, text = "Apply", width = 20, fg = 'black', command = gpu_adv_apply)
    gpu_adv.place(x = 90, y = y + 830)
    
    with open(EC_IO_FILE,'r+b') as file:
        file.seek(0xf4)
        file.write(bytes((140,)))
        file.seek(0x98)
        file.write(bytes((0,)))
    a_on.config(fg = 'black', command = auto_on)
    b_on.config(fg = 'black', command = basic_build)
    ad_on.config(fg = 'red', command = null)
    cb_on.config(fg = 'black', command = cooler_booster_on)
    return

if check2 == True:
    ad_on = Button(window, text = "Advanced", width = 6, fg = 'black', command = advanced_on)
    ad_on.place(x = 170, y = 235)

def cooler_booster_on():
    window.geometry('370x270')
    basic_slider.pack_forget()
    button_basic.pack_forget()
    with open(EC_IO_FILE,'r+b') as file:
        file.seek(0x98)
        file.write(bytes((128,)))
    a_on.config(fg = 'black', command = auto_on)
    b_on.config(fg = 'black', command = basic_build)
    ad_on.config(fg = 'black', command = advanced_on)
    cb_on.config(fg = 'red', command = null)
    return

if check2 == True:
    cb_on = Button(window, text = "Cooler Booster", width = 10, fg = 'black', command = cooler_booster_on)
    cb_on.place(x = 250, y = 235)

if check2 == True:
	with open(EC_IO_FILE,'r+b') as file:
		file.seek(0xf4)
		fm = int(file.read(1).hex(),16)
		file.seek(0x98)
		cb = int(file.read(1).hex(),16)
		
if check2 == True:
	if cb == 128:
		cb_on.config(fg = 'red')
	if fm == 12:
		a_on.config(fg = 'red')
	if fm == 76:
		b_on.config(fg = 'red')
	if fm == 140:
		ad_on.config(fg = 'red')

canvas.create_line(0, y + 230, 370, y + 230, dash=(10, 4), fill = "grey")

############################################################################################## Section 3
        
canvas.pack(fill = BOTH, expand = 1)
window.mainloop()
