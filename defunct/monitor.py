#! /usr/bin/python3

from tkinter import *
import threading
import os

EC_IO_FILE = "/sys/kernel/debug/ec/ec0/io"

path_to_script = os.path.dirname(os.path.abspath(__file__))
my_filename = os.path.join(path_to_script, "conf.txt")

conf_file_a = open(my_filename, "r")
mode = int(conf_file_a.read(1))
conf_file_a.close()

monitoring = 0
temp_c = 0
temp_g = 0
temp_c_m = 100
temp_g_m = 100
temp_m = 0

ORIGINAL_DPI = 96


def get_dpi():
    screen = Tk()
    current_dpi = screen.winfo_fpixels("1i")
    screen.destroy()
    return current_dpi


SCALE_1 = ORIGINAL_DPI / get_dpi()
SCALE_2 = get_dpi() / ORIGINAL_DPI


def scaled(original_width, val):
    if val == 1:
        val_fin = round(original_width * SCALE_1)
    if val == 2:
        val_fin = round(original_width * SCALE_2)
    return val_fin


window_m = Tk()
window_m.title("Monitering")
window_m.geometry(f"{scaled(320, 2)}x{scaled(110, 2)}")
canvas = Canvas(window_m)
canvas.configure(bg="black" if mode == 1 else "light grey")


def monitoring_int(
    lable_c11,
    lable_c22,
    lable_c33,
    lable_g11,
    lable_g22,
    lable_g33,
    lable_m44,
    lable_m55,
):
    global monitoring
    monitoring = 1
    global timer
    timer = threading.Timer(
        1,
        monitoring_int,
        args=(
            lable_c11,
            lable_c22,
            lable_c33,
            lable_g11,
            lable_g22,
            lable_g33,
            lable_m44,
            lable_m55,
        ),
    )
    timer.start()
    conf_file_a = open(my_filename, "r")
    global mode
    mode = int(conf_file_a.read(1))
    global temp_m
    conf_file_a.close()
    if int(temp_m) != int(mode):
        change_1(lable_c11)
        change_1(lable_c33)
        change_1(lable_g11)
        change_1(lable_g22)
        change_1(lable_g33)
        change_1(lable_c22)
        change(lable_m44)
        change(lable_m55)
        change(lable_c1)
        change(lable_c3)
        change(lable_g1)
        change(lable_m4)
        change(lable_m5)
        change(lable_c2)
        canvas.configure(bg="black" if mode == 1 else "light grey")
    temp_m = mode
    global temp_c
    global temp_g
    global temp_c_m
    global temp_g_m
    with open(EC_IO_FILE, "r+b") as file:
        file.seek(0x68)
        cpu_cur_temp = int(file.read(1).hex(), 16)
        file.seek(0x80)
        gpu_cur_temp = int(file.read(1).hex(), 16)
        file.seek(0xCC)
        cpu_fan = int(file.read(2).hex(), 16)
        if cpu_fan != 0:
            cpu_fan = 478000 // cpu_fan
        file.seek(0xCA)
        gpu_fan = int(file.read(2).hex(), 16)
        if gpu_fan != 0:
            gpu_fan = 478000 // gpu_fan
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
        lable_m44.config(text=cpu_fan)
        lable_m55.config(text=gpu_fan)
    return


def color(temp, lable):
    if temp <= 45:
        lable.config(text=temp, fg="green", bg="black" if mode == 1 else "light grey")
    elif (temp > 45) & (temp <= 60):
        lable.config(text=temp, fg="yellow", bg="black" if mode == 1 else "light grey")
    elif (temp > 60) & (temp <= 75):
        lable.config(text=temp, fg="orange", bg="black" if mode == 1 else "light grey")
    else:
        lable.config(text=temp, fg="red", bg="black" if mode == 1 else "light grey")
    return


def change(lable):
    lable.config(
        fg="black" if mode == 0 else "white", bg="black" if mode == 1 else "light grey"
    )
    return


def change_1(lable):
    lable.config(bg="black" if mode == 1 else "light grey")
    return


"""def batt_thresh():
	value = entry1.get()
	if ((value <= 100) & (value >= 20)):
		value = value + 128
		with open(EC_IO_FILE,'w+b') as file:
			file.seek(0xef)
			file.write(bytes((value,)))
	return"""

lable_c1 = Label(
    window_m,
    text="CPU Temperature (Celcius) : ",
    fg="black" if mode == 0 else "white",
    bg="black" if mode == 1 else "light grey",
    font=("Helvetica", scaled(10, 1)),
)
lable_c1.place(x=scaled(10, 2), y=scaled(27, 2))
lable_c11 = Label(
    window_m,
    text="",
    fg="black" if mode == 0 else "white",
    bg="black" if mode == 1 else "light grey",
    font=("Helvetica", scaled(11, 1)),
)
lable_c11.place(x=scaled(190, 2), y=scaled(27, 2))

lable_c2 = Label(
    window_m,
    text="Max",
    fg="black" if mode == 0 else "white",
    bg="black" if mode == 1 else "light grey",
    font=("Helvetica", scaled(10, 1)),
)
lable_c2.place(x=scaled(245, 2), y=scaled(10, 2))
lable_c22 = Label(
    window_m,
    text="",
    fg="black" if mode == 0 else "white",
    bg="black" if mode == 1 else "light grey",
    font=("Helvetica", scaled(11, 1)),
)
lable_c22.place(x=scaled(250, 2), y=scaled(27, 2))

lable_c3 = Label(
    window_m,
    text="Min",
    fg="black" if mode == 0 else "white",
    bg="black" if mode == 1 else "light grey",
    font=("Helvetica", scaled(10, 1)),
)
lable_c3.place(x=scaled(285, 2), y=scaled(10, 2))
lable_c33 = Label(
    window_m,
    text="",
    fg="black" if mode == 0 else "white",
    bg="black" if mode == 1 else "light grey",
    font=("Helvetica", scaled(11, 1)),
)
lable_c33.place(x=scaled(290, 2), y=scaled(27, 2))

lable_g1 = Label(
    window_m,
    text="GPU Temperature (Celcius) : ",
    fg="black" if mode == 0 else "white",
    bg="black" if mode == 1 else "light grey",
    font=("Helvetica", scaled(10, 1)),
)
lable_g1.place(x=scaled(10, 2), y=scaled(47, 2))
lable_g11 = Label(
    window_m,
    text="",
    fg="black" if mode == 0 else "white",
    bg="black" if mode == 1 else "light grey",
    font=("Helvetica", scaled(11, 1)),
)
lable_g11.place(x=scaled(190, 2), y=scaled(47, 2))

lable_g22 = Label(
    window_m,
    text="",
    fg="black" if mode == 0 else "white",
    bg="black" if mode == 1 else "light grey",
    font=("Helvetica", scaled(11, 1)),
)
lable_g22.place(x=scaled(250, 2), y=scaled(47, 2))

lable_g33 = Label(
    window_m,
    text="",
    fg="black" if mode == 0 else "white",
    bg="black" if mode == 1 else "light grey",
    font=("Helvetica", scaled(11, 1)),
)
lable_g33.place(x=scaled(290, 2), y=scaled(47, 2))

lable_m4 = Label(
    window_m,
    text="CPU fan RPM : ",
    fg="black" if mode == 0 else "white",
    bg="black" if mode == 1 else "light grey",
    font=("Helvetica", scaled(10, 1)),
)
lable_m4.place(x=scaled(10, 2), y=scaled(67, 2))
lable_m44 = Label(
    window_m,
    text="",
    fg="black" if mode == 0 else "white",
    bg="black" if mode == 1 else "light grey",
    font=("Helvetica", scaled(11, 1)),
)
lable_m44.place(x=scaled(190, 2), y=scaled(67, 2))

lable_m5 = Label(
    window_m,
    text="GPU fan RPM : ",
    fg="black" if mode == 0 else "white",
    bg="black" if mode == 1 else "light grey",
    font=("Helvetica", scaled(10, 1)),
)
lable_m5.place(x=scaled(10, 2), y=scaled(87, 2))
lable_m55 = Label(
    window_m,
    text="",
    fg="black" if mode == 0 else "white",
    bg="black" if mode == 1 else "light grey",
    font=("Helvetica", scaled(11, 1)),
)
lable_m55.place(x=scaled(190, 2), y=scaled(87, 2))

monitoring_int(
    lable_c11,
    lable_c22,
    lable_c33,
    lable_g11,
    lable_g22,
    lable_g33,
    lable_m44,
    lable_m55,
)

"""canvas.create_line(370, 135, 700, 135, dash = (10, 4), fill = "grey")

lable_b = Label(window, text = "Battery Thresholds", fg = 'Black' if mode == 0 else 'white', bg = 'black' if mode == 1 else 'light grey', font=("Helvetica", 16))
lable_b.place(x = 440, y = 140)

canvas.create_line(370, 166, 700, 166, dash = (10, 4), fill = "grey")

lable_b1 = Label(window, text = "Battery Charge : ", fg = 'Black' if mode == 0 else 'white', bg = 'black' if mode == 1 else 'light grey', font=("Helvetica", 10))
lable_b1.place(x = 380, y = 187)
lable_b2 = Label(window, text = "100%", fg = 'Black' if mode == 0 else 'white', bg = 'black' if mode == 1 else 'light grey', font=("Helvetica", 11))
lable_b2.place(x = 560, y = 187)

lable_b3 = Label(window, text = "Upper Limit", fg = 'Black' if mode == 0 else 'white', bg = 'black' if mode == 1 else 'light grey', font=("Helvetica", 10))
lable_b3.place(x = 615, y = 170)
global entry1
entry1 = Text(window, height = 1, width = 3, fg = 'Black' if mode == 0 else 'white', bg = 'black' if mode == 1 else 'light grey', font=("Helvetica", 10))
entry1.place(x = 620, y = 187)
lable_b4 = Label(window, text = "%", fg = 'Black' if mode == 0 else 'white', bg = 'black' if mode == 1 else 'light grey', font=("Helvetica", 11))
lable_b4.place(x = 655, y = 187)

lable_b5 = Label(window, text = "Battery Charge Threashold : ", fg = 'Black' if mode == 0 else 'white', bg = 'black' if mode == 1 else 'light grey', font=("Helvetica", 10))
lable_b5.place(x = 380, y = 207)
lable_b6 = Label(window, text = "", fg = 'Black' if mode == 0 else 'white', bg = 'black' if mode == 1 else 'light grey', font=("Helvetica", 11))
lable_b6.place(x = 560, y = 207)

button_b = Button(window, text = "Apply", width = 10, fg = 'black' if mode == 0 else 'white', bg = 'black' if mode == 1 else 'light grey', command = batt_thresh)
button_b.place(x = 480, y = 227)

with open(EC_IO_FILE,'r+b') as file:
	file.seek(0xef)
	lable_b6.config(text = (1, int(file.read(1).hex(),16)))"""


def on_closing():
    timer.cancel()
    window_m.destroy()
    return


canvas.pack(fill=BOTH, expand=1)
window_m.protocol("WM_DELETE_WINDOW", on_closing)
window_m.mainloop()
