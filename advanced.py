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
    os.system("sudo python3 write_EC.py")
    return

window = Tk()
dpi_base = 100
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

label_ct1=label_ct2=label_ct3=label_ct4=label_ct5=label_ct6=label_ct7=label_gt1=label_gt2=label_gt3=label_gt4=label_gt5=label_gt6=label_gt7 = Label()
label_ct = [label_ct1, label_ct2, label_ct3, label_ct4, label_ct5, label_ct6, label_ct7]
label_gt = [label_gt1, label_gt2, label_gt3, label_gt4, label_gt5, label_gt6, label_gt7]
dpi_scale_x_label_factor = [0, 25, 75, 125, 175, 225, 275, 325]

label_ct1_t=label_ct2_t=label_ct3_t=label_ct4_t=label_ct5_t=label_ct6_t=label_ct7_t=label_gt1_t=label_gt2_t=label_gt3_t=label_gt4_t=label_gt5_t=label_gt6_t=label_gt7_t = Label()
label_ct_t = [label_ct1_t, label_ct2_t, label_ct3_t, label_ct4_t, label_ct5_t, label_ct6_t, label_ct7_t]
label_gt_t = [label_gt1_t, label_gt2_t, label_gt3_t, label_gt4_t, label_gt5_t, label_gt6_t, label_gt7_t]
dpi_scale_x_label_t_factor = [0, 15, 70, 120, 170, 220, 270, 320]

sct1=sct2=sct3=sct4=sct5=sct6=sct7=sgt1=sgt2=sgt3=sgt4=sgt5=sgt6=sgt7 = Scale()
sct = [sct1, sct2, sct3, sct4, sct5, sct6, sct7]
sgt = [sgt1, sgt2, sgt3, sgt4, sgt5, sgt6, sgt7]
dpi_scale_x_scale_factor = [0, 10, 60, 110, 160, 210, 260, 310]

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

def sct_val(val):
    for i in range (0, 14):
        if i < 7:
            label_ct[i - 1].config(text = str(sct[i - 1].get()) + "%")
        else:
            label_gt[i - 7].config(text = str(sgt[i - 7].get()) + "%")
    return

for i in range (0, 14):
    if i < 7:
        label_ct[i] = Label(window, text = str(v[i + 1]) + "%", fg = 'white', bg = 'black', font=("Helvetica", 10))
        label_ct[i].place(x = (dpi_scale * dpi_scale_x_label_factor[i + 1]) - pow(3, dpi_scale_reducer), y = dpi_scale * 30)
        sct[i] = Scale(window, from_ = 150, to = 0, orient = VERTICAL, length = dpi_scale * 200, showvalue = 0, tickinterval = 5, resolution = 5, fg = 'white', bg = 'black', command = sct_val)
        sct[i].place(x = dpi_scale * dpi_scale_x_scale_factor[i + 1], y = dpi_scale * 50)
        sct[i].set(v[i + 1])
        if i == 0:
            label_ct_t[i] = Label(window, text = str("<" + str(w[i]) + "°C"), fg = 'Green', bg = 'black', font=("Helvetica", 10))
            label_ct_t[i].place(x = (dpi_scale * dpi_scale_x_label_t_factor[i + 1]) - pow(3, dpi_scale_reducer), y = dpi_scale * 257)
        else:
            label_ct_t[i] = Label(window, text = str(str(w[i - 1]) + "°C"), fg = 'Green', bg = 'black', font=("Helvetica", 10))
            label_ct_t[i].place(x = (dpi_scale * dpi_scale_x_label_t_factor[i + 1]) - pow(3, dpi_scale_reducer), y = dpi_scale * 257)
    else:
        label_gt[i - 7] = Label(window, text = str(v[i + 1]) + "%", fg = 'white', bg = 'black', font=("Helvetica", 10))
        label_gt[i - 7].place(x = (dpi_scale * dpi_scale_x_label_factor[i - 6]) - pow(3, dpi_scale_reducer), y = dpi_scale * 310)
        sgt[i - 7] = Scale(window, from_ = 150, to = 0, orient = VERTICAL, length = dpi_scale * 200, showvalue = 0, tickinterval = 5, resolution = 5, fg = 'white', bg = 'black', command = sct_val)
        sgt[i - 7].place(x = dpi_scale * dpi_scale_x_scale_factor[i - 6], y = dpi_scale * 330)
        sgt[i - 7].set(v[i + 1])
        if i == 7:
            label_gt_t[i - 7] = Label(window, text = str("<" + str(w[i - 1]) + "°C"), fg = 'Green', bg = 'black', font=("Helvetica", 10))
            label_gt_t[i - 7].place(x = (dpi_scale * dpi_scale_x_label_t_factor[i - 6]) - pow(3, dpi_scale_reducer), y = dpi_scale * 540)
        else:
            label_gt_t[i - 7] = Label(window, text = str(str(w[i - 2]) + "°C"), fg = 'Yellow', bg = 'black', font=("Helvetica", 10))
            label_gt_t[i - 7].place(x = (dpi_scale * dpi_scale_x_label_t_factor[i - 6]) - pow(3, dpi_scale_reducer), y = dpi_scale * 540)

def adv_apply():
    vr = [140]
    for i in range(0, 14):
        if i < 7:
            vr.append(int (sct[i].get()))
        else:
            vr.append(int (sgt[i - 7].get()))
    all_lines = reading()
    lines = str(3) + "\n" + all_lines[1] + "\n"
    for val in vr:
        lines = lines + str(val) + ","
    lines = lines + "\n" + all_lines[3] + "\n" + all_lines[4] + "\n" + all_lines[5] + "\n" + all_lines[6]
    corrections(lines)

adv = Button(window, text = "Apply", width = 20, fg = 'white', bg = 'black', command = adv_apply)
adv.place(x = dpi_scale * 90, y = dpi_scale * 560)

def on_closing():
	window.destroy()
	return

canvas.pack(fill = BOTH, expand = 1)
window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()