#! /usr/bin/python3

from tkinter import *
import threading
import math

EC_IO_FILE = '/sys/kernel/debug/ec/ec0/io'

window_m = Tk()
window_m.title('EC Map')
dpi_base = 76
dpi = window_m.winfo_fpixels('1i')
dpi_scale = round(dpi/dpi_base)
dpi_scale_reducer = 0
if dpi_scale == 1:
    dpi_scale_reducer = 0
else:
    dpi_scale_reducer = dpi_scale
window_m.geometry(f'{dpi_scale * 390}x{dpi_scale * 380}')
canvas = Canvas(window_m)
canvas.configure(bg = 'black')
window_m.configure(bg = 'black')

def map(line):
    FILE = open(EC_IO_FILE,'r+b')
    lines = ""
    for i in range (0, 16):
        FILE.seek(i + (16 * line))
        char = int(FILE.read(1).hex(), 16)
        if char < 127 and char > 32:
            char = str(chr(char))
        else:
            char = " "
        lines = lines + "|" + char
    FILE.close()
    return lines

lable_1 = Label(window_m, padx = 0, pady = 0, text = "           0 1 2 3 4 5 6 7 8 9 A B C D E F  ", fg = 'white', bg = 'black', font=("monospace", 10))
lable_1.place(x = dpi_scale * 10, y = dpi_scale * 17)
canvas.create_line((dpi_scale * 97) - pow(2, dpi_scale_reducer), dpi_scale * 46, dpi_scale * 350, dpi_scale * 46, dash=(dpi_scale * 14, dpi_scale * 2), fill = "grey")

lable_2 = Label(window_m, padx = 0, pady = 0, text = "000000   >" + map(0) + "|< ", fg = 'white', bg = 'black', font=("monospace", 10))
lable_2.place(x = dpi_scale * 10, y = dpi_scale * 47)
canvas.create_line((dpi_scale * 97) - pow(2, dpi_scale_reducer), dpi_scale * 66, dpi_scale * 350, dpi_scale * 66, dash=(dpi_scale * 14, dpi_scale * 2), fill = "grey")

lable_3 = Label(window_m, padx = 0, pady = 0, text = "000010   >" + map(1) + "|< ", fg = 'white', bg = 'black', font=("monospace", 10))
lable_3.place(x = dpi_scale * 10, y = dpi_scale * 67)
canvas.create_line((dpi_scale * 97) - pow(2, dpi_scale_reducer), dpi_scale * 86, dpi_scale * 350, dpi_scale * 86, dash=(dpi_scale * 14, dpi_scale * 2), fill = "grey")

lable_4 = Label(window_m, padx = 0, pady = 0, text = "000020   >" + map(2) + "|< ", fg = 'white', bg = 'black', font=("monospace", 10))
lable_4.place(x = dpi_scale * 10, y = dpi_scale * 87)
canvas.create_line((dpi_scale * 97) - pow(2, dpi_scale_reducer), dpi_scale * 106, dpi_scale * 350, dpi_scale * 106, dash=(dpi_scale * 14, dpi_scale * 2), fill = "grey")

lable_5 = Label(window_m, padx = 0, pady = 0, text = "000030   >" + map(3) + "|< ", fg = 'white', bg = 'black', font=("monospace", 10))
lable_5.place(x = dpi_scale * 10, y = dpi_scale * 107)
canvas.create_line((dpi_scale * 97) - pow(2, dpi_scale_reducer), dpi_scale * 126, dpi_scale * 350, dpi_scale * 126, dash=(dpi_scale * 14, dpi_scale * 2), fill = "grey")

lable_6 = Label(window_m, padx = 0, pady = 0, text = "000040   >" + map(4) + "|< ", fg = 'white', bg = 'black', font=("monospace", 10))
lable_6.place(x = dpi_scale * 10, y = dpi_scale * 127)
canvas.create_line((dpi_scale * 97) - pow(2, dpi_scale_reducer), dpi_scale * 146, dpi_scale * 350, dpi_scale * 146, dash=(dpi_scale * 14, dpi_scale * 2), fill = "grey")

lable_7 = Label(window_m, padx = 0, pady = 0, text = "000050   >" + map(5) + "|< ", fg = 'white', bg = 'black', font=("monospace", 10))
lable_7.place(x = dpi_scale * 10, y = dpi_scale * 147)
canvas.create_line((dpi_scale * 97) - pow(2, dpi_scale_reducer), dpi_scale * 166, dpi_scale * 350, dpi_scale * 166, dash=(dpi_scale * 14, dpi_scale * 2), fill = "grey")

lable_8 = Label(window_m, padx = 0, pady = 0, text = "000060   >" + map(6) + "|< ", fg = 'white', bg = 'black', font=("monospace", 10))
lable_8.place(x = dpi_scale * 10, y = dpi_scale * 167)
canvas.create_line((dpi_scale * 97) - pow(2, dpi_scale_reducer), dpi_scale * 186, dpi_scale * 350, dpi_scale * 186, dash=(dpi_scale * 14, dpi_scale * 2), fill = "grey")

lable_9 = Label(window_m, padx = 0, pady = 0, text = "000070   >" + map(7) + "|< ", fg = 'white', bg = 'black', font=("monospace", 10))
lable_9.place(x = dpi_scale * 10, y = dpi_scale * 187)
canvas.create_line((dpi_scale * 97) - pow(2, dpi_scale_reducer), dpi_scale * 206, dpi_scale * 350, dpi_scale * 206, dash=(dpi_scale * 14, dpi_scale * 2), fill = "grey")

lable_10 = Label(window_m, padx = 0, pady = 0, text = "000080   >" + map(8) + "|< ", fg = 'white', bg = 'black', font=("monospace", 10))
lable_10.place(x = dpi_scale * 10, y = dpi_scale * 207)
canvas.create_line((dpi_scale * 97) - pow(2, dpi_scale_reducer), dpi_scale * 226, dpi_scale * 350, dpi_scale * 226, dash=(dpi_scale * 14, dpi_scale * 2), fill = "grey")

lable_11 = Label(window_m, padx = 0, pady = 0, text = "000090   >" + map(9) + "|< ", fg = 'white', bg = 'black', font=("monospace", 10))
lable_11.place(x = dpi_scale * 10, y = dpi_scale * 227)
canvas.create_line((dpi_scale * 97) - pow(2, dpi_scale_reducer), dpi_scale * 246, dpi_scale * 350, dpi_scale * 246, dash=(dpi_scale * 14, dpi_scale * 2), fill = "grey")

lable_12 = Label(window_m, padx = 0, pady = 0, text = "0000A0   >" + map(10) + "|< ", fg = 'white', bg = 'black', font=("monospace", 10))
lable_12.place(x = dpi_scale * 10, y = dpi_scale * 247)
canvas.create_line((dpi_scale * 97) - pow(2, dpi_scale_reducer), dpi_scale * 266, dpi_scale * 350, dpi_scale * 266, dash=(dpi_scale * 14, dpi_scale * 2), fill = "grey")

lable_13 = Label(window_m, padx = 0, pady = 0, text = "0000B0   >" + map(11) + "|< ", fg = 'white', bg = 'black', font=("monospace", 10))
lable_13.place(x = dpi_scale * 10, y = dpi_scale * 267)
canvas.create_line((dpi_scale * 97) - pow(2, dpi_scale_reducer), dpi_scale * 286, dpi_scale * 350, dpi_scale * 286, dash=(dpi_scale * 14, dpi_scale * 2), fill = "grey")

lable_14 = Label(window_m, padx = 0, pady = 0, text = "0000C0   >" + map(12) + "|< ", fg = 'white', bg = 'black', font=("monospace", 10))
lable_14.place(x = dpi_scale * 10, y = dpi_scale * 287)
canvas.create_line((dpi_scale * 97) - pow(2, dpi_scale_reducer), dpi_scale * 306, dpi_scale * 350, dpi_scale * 306, dash=(dpi_scale * 14, dpi_scale * 2), fill = "grey")

lable_15 = Label(window_m, padx = 0, pady = 0, text ="0000D0   >" + map(13) + "|< ", fg = 'white', bg = 'black', font=("monospace", 10))
lable_15.place(x = dpi_scale * 10, y = dpi_scale * 307)
canvas.create_line((dpi_scale * 97) - pow(2, dpi_scale_reducer), dpi_scale * 326, dpi_scale * 350, dpi_scale * 326, dash=(dpi_scale * 14, dpi_scale * 2), fill = "grey")

lable_16 = Label(window_m, padx = 0, pady = 0, text = "0000E0   >" + map(14) + "|< ", fg = 'white', bg = 'black', font=("monospace", 10))
lable_16.place(x = dpi_scale * 10, y = dpi_scale * 327)
canvas.create_line((dpi_scale * 97) - pow(2, dpi_scale_reducer), dpi_scale * 346, dpi_scale * 350, dpi_scale * 346, dash=(dpi_scale * 14, dpi_scale * 2), fill = "grey")

lable_17 = Label(window_m, padx = 0, pady = 0, text = "0000F0   >" + map(15) + "|< ", fg = 'white', bg = 'black', font=("monospace", 10))
lable_17.place(x = dpi_scale * 10, y = dpi_scale * 347)
canvas.create_line((dpi_scale * 97) - pow(2, dpi_scale_reducer), dpi_scale * 366, dpi_scale * 350, dpi_scale * 366, dash=(dpi_scale * 14, dpi_scale * 2), fill = "grey")

def on_closing():
    window_m.destroy()
    return

canvas.pack(fill = BOTH, expand = 1)
window_m.protocol("WM_DELETE_WINDOW", on_closing)
window_m.mainloop()