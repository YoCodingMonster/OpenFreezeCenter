#! /usr/bin/python3

from tkinter import *
import os
import fileinput
from math import pow

path_to_script = os.path.dirname(os.path.abspath(__file__))
my_filename = os.path.join(path_to_script, "conf.txt")

def reading():
    conf_file = open(my_filename, "r")
    all_lines = conf_file.readlines()
    conf_file.close()
    return all_lines

def corrections(lines):
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
    os.system("konsole -e 'bash -c \"sudo python3 ${pkgdir}write_EC.py\"'")
    return

window = Tk()
dpi_base = 76
dpi = window.winfo_fpixels('1i')
dpi_scale = round(dpi/dpi_base)
dpi_scale_reducer = 0
if dpi_scale == 1:
    dpi_scale_reducer = 0
else:
    dpi_scale_reducer = dpi_scale
canvas = Canvas(window)
canvas.configure(bg = 'black')
window.title('OpenFreezeCenter - Advanced Fan Curve')
window.geometry(f'{dpi_scale * 370}x{dpi_scale * 610}')

all_lines = reading()
v_temp = all_lines[2].split (",")
count = 0
v = []
for i in v_temp:
    count = count + 1
    if count < 16:
        v.append(int(i))
w_temp = all_lines[4].split (",")
count_w = 0
w = []
for j in w_temp:
    if count_w < 12:
        print(j)
        w.append(int(j))
        count_w = count_w + 1
lable_ct8 = Label(window, text = "CPU fan Speeds" , fg = 'blue', bg = 'black', font=("Helvetica", 10))
lable_ct8.place(x = dpi_scale * 135 , y = dpi_scale * 10)

lable_gt7 = Label(window, text = "GPU fan Speeds" , fg = 'blue', bg = 'black', font=("Helvetica", 10))
lable_gt7.place(x = dpi_scale * 135, y = dpi_scale * 290)

canvas.create_line(dpi_scale * 0, dpi_scale * 280, dpi_scale * 370, dpi_scale * 280, dash=(10, 4), fill = "grey")

lable_ct1 = Label(window, text = str(v[1]) + "%", fg = 'white', bg = 'black', font=("Helvetica", 10))
lable_ct1.place(x = (dpi_scale * 25) - pow(3, dpi_scale_reducer), y = dpi_scale * 30)
lable_ct2 = Label(window, text = str(v[2]) + "%", fg = 'white', bg = 'black', font=("Helvetica", 10))
lable_ct2.place(x = (dpi_scale * 75) - pow(4, dpi_scale_reducer), y = dpi_scale * 30)
lable_ct3 = Label(window, text = str(v[3]) + "%", fg = 'white', bg = 'black', font=("Helvetica", 10))
lable_ct3.place(x = (dpi_scale * 125) - pow(4, dpi_scale_reducer), y = dpi_scale * 30)
lable_ct4 = Label(window, text = str(v[4]) + "%", fg = 'white', bg = 'black', font=("Helvetica", 10))
lable_ct4.place(x = (dpi_scale * 175) - pow(4, dpi_scale_reducer), y = dpi_scale * 30)
lable_ct5 = Label(window, text = str(v[5]) + "%", fg = 'white', bg = 'black', font=("Helvetica", 10))
lable_ct5.place(x = (dpi_scale * 225) - pow(4, dpi_scale_reducer), y = dpi_scale * 30)
lable_ct6 = Label(window, text = str(v[6]) + "%", fg = 'white', bg = 'black', font=("Helvetica", 10))
lable_ct6.place(x = (dpi_scale * 275) - pow(4, dpi_scale_reducer), y = dpi_scale * 30)
lable_ct7 = Label(window, text = str(v[7]) + "%", fg = 'white', bg = 'black', font=("Helvetica", 10))
lable_ct7.place(x = (dpi_scale * 325) - pow(4, dpi_scale_reducer), y = dpi_scale * 30)
lable_gt1 = Label(window, text = str(v[8]) + "%", fg = 'white', bg = 'black', font=("Helvetica", 10))
lable_gt1.place(x = (dpi_scale * 25) - pow(3, dpi_scale_reducer), y = dpi_scale * 310)
lable_gt2 = Label(window, text = str(v[9]) + "%", fg = 'white', bg = 'black', font=("Helvetica", 10))
lable_gt2.place(x = (dpi_scale * 75) - pow(4, dpi_scale_reducer), y = dpi_scale * 310)
lable_gt3 = Label(window, text = str(v[10]) + "%", fg = 'white', bg = 'black', font=("Helvetica", 10))
lable_gt3.place(x = (dpi_scale * 125) - pow(4, dpi_scale_reducer), y = dpi_scale * 310)
lable_gt4 = Label(window, text = str(v[11]) + "%", fg = 'white', bg = 'black', font=("Helvetica", 10))
lable_gt4.place(x = (dpi_scale * 175) - pow(4, dpi_scale_reducer), y = dpi_scale * 310)
lable_gt5 = Label(window, text = str(v[12]) + "%", fg = 'white', bg = 'black', font=("Helvetica", 10))
lable_gt5.place(x = (dpi_scale * 225) - pow(4, dpi_scale_reducer), y = dpi_scale * 310)
lable_gt6 = Label(window, text = str(v[13]) + "%", fg = 'white', bg = 'black', font=("Helvetica", 10))
lable_gt6.place(x = (dpi_scale * 275) - pow(4, dpi_scale_reducer), y = dpi_scale * 310)
lable_gt7 = Label(window, text = str(v[14]) + "%", fg = 'white', bg = 'black', font=("Helvetica", 10))
lable_gt7.place(x = (dpi_scale * 325) - pow(4, dpi_scale_reducer), y = dpi_scale * 310)

lable_ct1_t = Label(window, text = str("<" + str(w[0]) + "°C"), fg = 'Green', bg = 'black', font=("Helvetica", 10))
lable_ct1_t.place(x = (dpi_scale * 15) - pow(3, dpi_scale_reducer), y = dpi_scale * 257)
lable_ct2_t = Label(window, text = str(str(w[0]) + "°C"), fg = 'Green', bg = 'black', font=("Helvetica", 10))
lable_ct2_t.place(x = (dpi_scale * 70) - pow(3, dpi_scale_reducer), y = dpi_scale * 257)
lable_ct3_t = Label(window, text = str(str(w[1]) + "°C"), fg = 'Yellow', bg = 'black', font=("Helvetica", 10))
lable_ct3_t.place(x = (dpi_scale * 120) - pow(3, dpi_scale_reducer), y = dpi_scale * 257)
lable_ct4_t = Label(window, text = str(str(w[2]) + "°C"), fg = 'Yellow', bg = 'black', font=("Helvetica", 10))
lable_ct4_t.place(x = (dpi_scale * 170) - pow(3, dpi_scale_reducer), y = dpi_scale * 257)
lable_ct5_t = Label(window, text = str(str(w[3]) + "°C"), fg = 'orange', bg = 'black', font=("Helvetica", 10))
lable_ct5_t.place(x = (dpi_scale * 220) - pow(3, dpi_scale_reducer), y = dpi_scale * 257)
lable_ct6_t = Label(window, text = str(str(w[4]) + "°C"), fg = 'Red', bg = 'black', font=("Helvetica", 10))
lable_ct6_t.place(x = (dpi_scale * 270) - pow(3, dpi_scale_reducer), y = dpi_scale * 257)
lable_ct7_t = Label(window, text = str(str(w[5]) + "°C"), fg = 'Red', bg = 'black', font=("Helvetica", 10))
lable_ct7_t.place(x = (dpi_scale * 320) - pow(3, dpi_scale_reducer), y = dpi_scale * 257)
lable_gt1_t = Label(window, text = str("<" + str(w[6]) + "°C"), fg = 'Green', bg = 'black', font=("Helvetica", 10))
lable_gt1_t.place(x = (dpi_scale * 15) - pow(3, dpi_scale_reducer), y = dpi_scale * 540)
lable_gt2_t = Label(window, text = str(str(w[6]) + "°C"), fg = 'Green', bg = 'black', font=("Helvetica", 10))
lable_gt2_t.place(x = (dpi_scale * 70) - pow(3, dpi_scale_reducer), y = dpi_scale * 540)
lable_gt3_t = Label(window, text = str(str(w[7]) + "°C"), fg = 'Yellow', bg = 'black', font=("Helvetica", 10))
lable_gt3_t.place(x = (dpi_scale * 120) - pow(3, dpi_scale_reducer), y = dpi_scale * 540)
lable_gt4_t = Label(window, text = str(str(w[8]) + "°C"), fg = 'Yellow', bg = 'black', font=("Helvetica", 10))
lable_gt4_t.place(x = (dpi_scale * 170) - pow(3, dpi_scale_reducer), y = dpi_scale * 540)
lable_gt5_t = Label(window, text = str(str(w[9]) + "°C"), fg = 'orange', bg = 'black', font=("Helvetica", 10))
lable_gt5_t.place(x = (dpi_scale * 220) - pow(3, dpi_scale_reducer), y = dpi_scale * 540)
lable_gt6_t = Label(window, text = str(str(w[10]) + "°C"), fg = 'red', bg = 'black', font=("Helvetica", 10))
lable_gt6_t.place(x = (dpi_scale * 270) - pow(3, dpi_scale_reducer), y = dpi_scale * 540)
lable_gt7_t = Label(window, text = str(str(w[11]) + "°C"), fg = 'red', bg = 'black', font=("Helvetica", 10))
lable_gt7_t.place(x = (dpi_scale * 320) - pow(3, dpi_scale_reducer), y = dpi_scale * 540)
    
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

sct1 = Scale(window, from_ = 150, to = 0, orient = VERTICAL, length = dpi_scale * 200, showvalue = 0, tickinterval = 5, resolution = 5, fg = 'white', bg = 'black', command = sct_val)
sct1.place(x = dpi_scale * 10, y = dpi_scale * 50)
sct1.set(v[1])
sct2 = Scale(window, from_ = 150, to = 0, orient = VERTICAL, length = dpi_scale * 200, showvalue = 0, tickinterval = 5, resolution = 5, fg = 'white', bg = 'black', command = sct_val)
sct2.place(x = dpi_scale * 60, y = dpi_scale * 50)
sct2.set(v[2])
sct3 = Scale(window, from_ = 150, to = 0, orient = VERTICAL, length = dpi_scale * 200, showvalue = 0, tickinterval = 5, resolution = 5, fg = 'white', bg = 'black', command = sct_val)
sct3.place(x = dpi_scale * 110, y = dpi_scale * 50)
sct3.set(v[3])
sct4 = Scale(window, from_ = 150, to = 0, orient = VERTICAL, length = dpi_scale * 200, showvalue = 0, tickinterval = 5, resolution = 5, fg = 'white', bg = 'black', command = sct_val)
sct4.place(x = dpi_scale * 160, y = dpi_scale * 50)
sct4.set(v[4])
sct5 = Scale(window, from_ = 150, to = 0, orient = VERTICAL, length = dpi_scale * 200, showvalue = 0, tickinterval = 5, resolution = 5, fg = 'white', bg = 'black', command = sct_val)
sct5.place(x = dpi_scale * 210, y = dpi_scale * 50)
sct5.set(v[5])
sct6 = Scale(window, from_ = 150, to = 0, orient = VERTICAL, length = dpi_scale * 200, showvalue = 0, tickinterval = 5, resolution = 5, fg = 'white', bg = 'black', command = sct_val)
sct6.place(x = dpi_scale * 260, y = dpi_scale * 50)
sct6.set(v[6])
sct7 = Scale(window, from_ = 150, to = 0, orient = VERTICAL, length = dpi_scale * 200, showvalue = 0, tickinterval = 5, resolution = 5, fg = 'white', bg = 'black', command = sct_val)
sct7.place(x = dpi_scale * 310, y = dpi_scale * 50)
sct7.set(v[7])
sgt1 = Scale(window, from_ = 150, to = 0, orient = VERTICAL, length = dpi_scale * 200, showvalue = 0, tickinterval = 5, resolution = 5, fg = 'white', bg = 'black', command = sct_val)
sgt1.place(x = dpi_scale * 10, y = dpi_scale * 330)
sgt1.set(v[8])
sgt2 = Scale(window, from_ = 150, to = 0, orient = VERTICAL, length = dpi_scale * 200, showvalue = 0, tickinterval = 5, resolution = 5, fg = 'white', bg = 'black', command = sct_val)
sgt2.place(x = dpi_scale * 60, y = dpi_scale * 330)
sgt2.set(v[9])
sgt3 = Scale(window, from_ = 150, to = 0, orient = VERTICAL, length = dpi_scale * 200, showvalue = 0, tickinterval = 5, resolution = 5, fg = 'white', bg = 'black', command = sct_val)
sgt3.place(x = dpi_scale * 110, y = dpi_scale * 330)
sgt3.set(v[10])
sgt4 = Scale(window, from_ = 150, to = 0, orient = VERTICAL, length = dpi_scale * 200, showvalue = 0, tickinterval = 5, resolution = 5, fg = 'white', bg = 'black', command = sct_val)
sgt4.place(x = dpi_scale * 160, y = dpi_scale * 330)
sgt4.set(v[11])
sgt5 = Scale(window, from_ = 150, to = 0, orient = VERTICAL, length = dpi_scale * 200, showvalue = 0, tickinterval = 5, resolution = 5, fg = 'white', bg = 'black', command = sct_val)
sgt5.place(x = dpi_scale * 210, y = dpi_scale * 330)
sgt5.set(v[12])
sgt6 = Scale(window, from_ = 150, to = 0, orient = VERTICAL, length = dpi_scale * 200, showvalue = 0, tickinterval = 5, resolution = 5, fg = 'white', bg = 'black', command = sct_val)
sgt6.place(x = dpi_scale * 260, y = dpi_scale * 330)
sgt6.set(v[13])
sgt7 = Scale(window, from_ = 150, to = 0, orient = VERTICAL, length = dpi_scale * 200, showvalue = 0, tickinterval = 5, resolution = 5, fg = 'white', bg = 'black', command = sct_val)
sgt7.place(x = dpi_scale * 310, y = dpi_scale * 330)
sgt7.set(v[14])

def adv_apply():
    vr = [140, sct1.get(), sct2.get(), sct3.get(), sct4.get(), sct5.get(), sct6.get(), sct7.get(), sgt1.get(), sgt2.get(), sgt3.get(), sgt4.get(), sgt5.get(), sgt6.get(), sgt7.get()]
    all_lines = reading()
    lines = str(3) + "\n" + all_lines[1] + "\n"
    for val in vr:
        lines = lines + str(val) + ","
    lines = lines + "\n" + all_lines[3] + "\n" + all_lines[4] + "\n" + all_lines[5] + "\n" + all_lines[6]
    corrections(lines)
    return

adv = Button(window, text = "Apply", width = 20, fg = 'white', bg = 'black', command = adv_apply)
adv.place(x = dpi_scale * 90, y = dpi_scale * 560)

def on_closing():
	window.destroy()
	return

canvas.pack(fill = BOTH, expand = 1)
window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()
