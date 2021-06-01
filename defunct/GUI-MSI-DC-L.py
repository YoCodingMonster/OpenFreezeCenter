#! /usr/bin/python3

from tkinter import *
from tkinter import messagebox
import os
import sys
import subprocess
from subprocess import *
from crontab import CronTab
import getpass
import threading
import time
import webbrowser
import fileinput


"""############ Variables & Defaults"""

username = getpass.getuser()
EC_IO_FILE = '/sys/kernel/debug/ec/ec0/io'

path_to_script = os.path.dirname(os.path.abspath(__file__))
my_filename = os.path.join(path_to_script, "conf.txt")
check_1 = os.path.exists(my_filename)
if check_1 == False:
    """print("Enter your Sudo Password :-> ")
    pass_sudo = input()"""
    open(my_filename, "w").close()
    subprocess.call(['chmod', '0777', my_filename])
    conf_file = open(my_filename, "w")
    conf_file.writelines("0\n1\n0\n")
    temp_ = [140, 0, 20, 40, 45, 50, 60, 70, 0, 20, 40, 45, 50, 60, 70]
    for val in temp_:
        conf_file.write("%i," % val)
    """conf_file.writelines("\n" + pass_sudo)"""
    conf_file.close()
conf_file_a = open(my_filename, "r")
mode = int(conf_file_a.read(1))
all_lines = conf_file_a.readlines()
mode_f = all_lines[1]
"""sudo = str(all_lines[4])"""
conf_file_a.close()

my_filename_1 = os.path.join(path_to_script, "write_EC.py")
my_filename_2 = os.path.join(path_to_script, "monitor.py")

fm, offset, y = 12, 0, 100
monitoring = 0
temp_c = 0
temp_g = 0
temp_c_m = 100
temp_g_m = 100
ifu = 0
v = []
offset_official = 0
check = os.path.exists("/etc/modprobe.d/GUI-MSI-DC-L-ec_sys.conf")
window = Tk()
canvas = Canvas(window)
canvas.configure(bg='black' if mode == 1 else 'light grey')

str_1 = ''
for line in fileinput.FileInput(my_filename, inplace=1):
    if line.rstrip():
        str_1 = str_1 + line
conf_file = open(my_filename, "w")
conf_file.writelines(str_1)
conf_file.close()


def config_file_write(u, v, v_adv):
    conf_file_b = open(my_filename, "r")
    all_lines = conf_file_b.readlines()
    mode_f = all_lines[1]
    conf_file_b.close()
    global offset_official

    conf_file = open(my_filename, "w")
    if v == -1:
        lines = str(u) + "\n" + str(mode_f) + "\n" + \
            str(offset_official) + "\n"
    else:
        lines = str(u) + "\n" + str(v) + "\n" + str(offset_official) + "\n"
    conf_file.writelines(lines)
    count = 0

    if v == 3:
        if v_adv == -1:
            vr_1 = []
            vr_2 = []
            vr_1 = all_lines[3]
            vr_2 = vr_1.split(",")
            for i in vr_2:
                count = count + 1
                if count < 16:
                    conf_file.write("%i," % int(i))
        else:
            for val in v_adv:
                conf_file.write("%i," % val)

    else:
        vr_1 = []
        vr_2 = []
        vr_1 = all_lines[3]
        vr_2 = vr_1.split(",")
        for i in vr_2:
            count = count + 1
            if count < 16:
                conf_file.write("%i," % int(i))

    """conf_file.writelines("\n" + all_lines[4])"""
    conf_file.close()

    if v != -1:
        os.system(
            "x-terminal-emulator -e 'bash -c \"sudo nohup python3 ${pkgdir}write_EC.py; exec bash\"'")
        """command_w = "sudo nohup python3 ${pkgdir}write_EC.py"
		os.popen("sudo -S %s"%(command_w), 'w').write(sudo)"""
    return


def null():
    return


"""######################################################################################################################## Canvas layout"""

window.title('OpenFreezeCenter - MSI Fan Control')
window.geometry('370x270')
canvas.create_line(0, 210, 370, 210, dash=(10, 4), fill="grey")

lable1 = Label(window, text="Creator :-> Aditya Kumar Bajpai", fg='red',
               bg='black' if mode == 1 else 'light grey', font=("Helvetica", 12))
lable1.place(x=70, y=5)

lable2 = Label(window, text="Version 1.4", fg='black' if mode == 0 else 'white',
               bg='black' if mode == 1 else 'light grey', font=("Helvetica", 12))
lable2.place(x=140, y=25)


def credits():
    newWindow = Toplevel(window)
    canvas1 = Canvas(newWindow)
    canvas1.configure(bg='black' if mode == 1 else 'light grey')
    newWindow.title("Owner of Ideas")
    newWindow.geometry("400x200")
    lable = Label(newWindow, text="Rob Oudendijk", fg='red',
                  bg='black' if mode == 1 else 'light grey', font=("Helvetica", 16))
    lable.place(x=125, y=10)
    lable = Label(newWindow, text="-- Saperate Monitoring and Battery panels", fg='black' if mode ==
                  0 else 'white', bg='black' if mode == 1 else 'light grey', font=("Helvetica", 12))
    lable.place(x=10, y=40)
    lable = Label(newWindow, text="-- Dark Mode", fg='black' if mode == 0 else 'white',
                  bg='black' if mode == 1 else 'light grey', font=("Helvetica", 12))
    lable.place(x=10, y=60)
    lable = Label(newWindow, text="Thankyou so much for being a part of this project!", fg='grey' if mode ==
                  0 else 'white', bg='black' if mode == 1 else 'light grey', font=("Helvetica", 10))
    lable.place(x=50, y=180)
    canvas1.pack(fill=BOTH, expand=1)
    return


button_credits = Button(window, text="Credits", width=20, fg='black' if mode ==
                        0 else 'white', bg='black' if mode == 1 else 'light grey', command=credits)
button_credits.place(x=90, y=110)


def GitHub():
    url = 'https://github.com/YoCodingMonster/MSI-Dragon-Center-for-Linux'
    appcommand = ["firefox", url]
    run(appcommand)
    return


button_github = Button(window, text="Github Project", width=20, fg='black' if mode ==
                       0 else 'white', bg='black' if mode == 1 else 'light grey', command=GitHub)
button_github.place(x=90, y=170)

"""#################################################################################### Dark - Light modes"""


def dark():
    button_dark.config(text="Light Mode", fg='grey', command=light)
    config_file_write(1, -1, -1)
    os.popen("nohup python3 ${pkgdir}GUI-MSI-DC-L.py", 'w')
    """os.system("x-terminal-emulator -e 'bash -c \"nohup python3 ${pkgdir}GUI-MSI-DC-L.py; exec bash\"'")"""
    on_closing()
    return


def light():
    button_dark.config(text="Dark Mode", fg='black', command=dark)
    config_file_write(0, -1, -1)
    os.popen("nohup python3 ${pkgdir}GUI-MSI-DC-L.py", 'w')
    """os.system("x-terminal-emulator -e 'bash -c \"nohup python3 ${pkgdir}GUI-MSI-DC-L.py; exec bash\"'")"""
    on_closing()
    return


if mode == 1:
    button_dark = Button(window, text="Light Mode", width=20, fg='white',
                         bg='black' if mode == 1 else 'light grey', command=light)
else:
    button_dark = Button(window, text="Dark Mode", width=20, fg='black',
                         bg='black' if mode == 1 else 'light grey', command=dark)
button_dark.place(x=90, y=80)

"""#################################################################################### Install - Uninstall"""


def install():
    os.system(
        "x-terminal-emulator -e 'bash -c \"sudo install -Dm 644 etc/modprobe.d/GUI-MSI-DC-L-ec_sys.conf \"${pkgdir}/etc/modprobe.d/GUI-MSI-DC-L-ec_sys.conf\" && sudo install -Dm 644 etc/modules-load.d/GUI-MSI-DC-L-ec_sys.conf \"${pkgdir}/etc/modules-load.d/GUI-MSI-DC-L-ec_sys.conf\"; exec bash\"'")
    button1.config(text="Uninstall", fg='grey', command=uninstall)
    messagebox.showinfo("Installation Complete!",
                        "Please Reboot your system to enable EC module write capablities of script")
    return


def uninstall():
    os.system("x-terminal-emulator -e 'bash -c \"sudo rm /etc/modprobe.d/GUI-MSI-DC-L-ec_sys.conf /etc/modules-load.d/GUI-MSI-DC-L-ec_sys.conf /usr/share/GUI-MSI-DC-L.py; exec bash\"'")
    if os.path.exist("/usr/share/GUI-MSI-DC-L.py") == True:
        os.system(
            "x-terminal-emulator -e 'bash -c \"sudo rm /usr/share/GUI-MSI-DC-L.py; exec bash\"'")
    my_cron = CronTab(user=username)
    for job in my_cron:
        if job.comment == '@reboot python3 /usr/share/GUI-MSI-DC-L.py':
            my_cron.remove(job)
            my_cron.write()
    button1.config(text="Install", fg='black', command=install)
    return


if check == True:
    button1 = Button(window, text="Uninstall", width=20, fg='grey' if mode ==
                     0 else 'white', bg='black' if mode == 1 else 'light grey', command=uninstall)
else:
    button1 = Button(window, text="Install", width=20, fg='black' if mode ==
                     0 else 'white', bg='black' if mode == 1 else 'light grey', command=install)
button1.place(x=90, y=50)

"""#################################################################################### Startup - Unstartup
    
def startup():
	button2.config(fg = 'grey', text = 'Dont run at Startup', command = unstartup)
	os.system("x-terminal-emulator -e 'bash -c \"sudo install -Dm 644 GUI-MSI-DC-L.py \"${pkgdir}/usr/share/GUI-MSI-DC-L.py\"; exec bash\"'")
	my_cron = CronTab(user = username)
	job = my_cron.new(command = '@reboot python3 /usr/share/GUI-MSI-DC-L.py')
	my_cron.write()
	return
	
def unstartup():
	button2.config(fg = 'black', text = 'Run at Startup', command = startup)
	os.system("x-terminal-emulator -e 'bash -c \"sudo rm /usr/share/GUI-MSI-DC-L.py; exec bash\"'")
	my_cron = CronTab(user = username)
	for job in my_cron:
		if job.comment == '@reboot python3 /usr/share/GUI-MSI-DC-L.py':
			my_cron.remove(job)
			my_cron.write()
	return
	
button2 = Button(window, text = "Run at Startup", width = 20, fg = 'black', command = startup)
button2.place(x = 90, y = 80)

my_cron = CronTab(user = username)
for job in my_cron:
	if job.comment == '@reboot python3 /usr/share/GUI-MSI-DC-L.py':
		button2.config(fg = 'grey', text = 'Dont run at Startup', command = unstartup)
	else:
		button2.config(fg = 'black', text = 'Run at Startup', command = startup)"""

"""#################################################################################### Monitering Fan speeds and temperatures"""


def monitering():
    """command_m = "sudo nohup python3 ${pkgdir}monitor.py"
    os.popen("sudo -S %s"%(command_m), 'w').write(sudo)"""
    os.system(
        "x-terminal-emulator -e 'bash -c \"sudo nohup python3 ${pkgdir}monitor.py; exec bash\"'")
    return


button_GitHub = Button(window, text="Monitering", width=20, fg='black' if mode ==
                       0 else 'white', bg='black' if mode == 1 else 'light grey', command=monitering)
button_GitHub.place(x=90, y=140)

"""#################################################################################### Fan modes"""
"""########################################## Auto Mode"""


def auto_on():
    window.geometry('370x270')
    global mode_f
    mode_f = 1
    config_file_write(mode, 1, -1)

    a_on.config(fg='red', bg='black' if mode ==
                1 else 'light grey', command=null)
    b_on.config(fg='black' if mode == 0 else 'white',
                bg='black' if mode == 1 else 'light grey', command=basic_build)
    ad_on.config(fg='black' if mode == 0 else 'white',
                 bg='black' if mode == 1 else 'light grey', command=advanced_on)
    cb_on.config(fg='black' if mode == 0 else 'white', bg='black' if mode ==
                 1 else 'light grey', command=cooler_booster_on)
    return


"""########################################## Baisc Mode"""

basic_slider = Scale(window, from_=-30, to=30, orient=HORIZONTAL, length=200, showvalue=1, tickinterval=10,
                     resolution=10, fg='black' if mode == 0 else 'white', bg='black' if mode == 1 else 'light grey')
basic_slider.place(x=10, y=265)


def basic_on(offset):
    global offset_official
    offset_official = offset
    global mode_f
    mode_f = 2
    config_file_write(mode, 2, -1)
    return


def basic_build():
    window.geometry('370x330')

    a_on.config(fg='black' if mode == 0 else 'white',
                bg='black' if mode == 1 else 'light grey', command=auto_on)
    b_on.config(fg='red', bg='black' if mode ==
                1 else 'light grey', command=null)
    ad_on.config(fg='black' if mode == 0 else 'white',
                 bg='black' if mode == 1 else 'light grey', command=advanced_on)
    cb_on.config(fg='black' if mode == 0 else 'white', bg='black' if mode ==
                 1 else 'light grey', command=cooler_booster_on)
    return


button_basic = Button(window, text="Apply", width=10, fg='black' if mode == 0 else 'white',
                      bg='black' if mode == 1 else 'light grey', command=lambda: basic_on(basic_slider.get()))
button_basic.place(x=235, y=280)

"""########################################## Advanced Mode"""


def advanced_on():
    v = []
    vr_2 = []
    vr_1 = []
    conf_file_x = open(my_filename, "r")
    all_lines = conf_file_x.readlines()
    vr_1 = all_lines[3]
    vr_2 = vr_1.split(",")
    count = 0
    for i in vr_2:
        count = count + 1
        if count < 16:
            v.append(int(i))
    conf_file_x.close()
    window.geometry('370x920')

    offset = 50
    lable_ct8 = Label(window, text="CPU fan Speeds", fg='blue',
                      bg='black' if mode == 1 else 'light grey', font=("Helvetica", 10))
    lable_ct8.place(x=135, y=offset + 280)

    lable_gt7 = Label(window, text="GPU fan Speeds", fg='blue',
                      bg='black' if mode == 1 else 'light grey', font=("Helvetica", 10))
    lable_gt7.place(x=135, y=offset + 560)

    canvas.create_line(0, offset + 550, 370, offset +
                       550, dash=(10, 4), fill="grey")

    lable_ct1 = Label(window, text=str(v[1]) + "%", fg='black' if mode == 0 else 'white',
                      bg='black' if mode == 1 else 'light grey', font=("Helvetica", 10))
    lable_ct1.place(x=35, y=offset + 300)
    lable_ct2 = Label(window, text=str(v[2]) + "%", fg='black' if mode == 0 else 'white',
                      bg='black' if mode == 1 else 'light grey', font=("Helvetica", 10))
    lable_ct2.place(x=85, y=offset + 300)
    lable_ct3 = Label(window, text=str(v[3]) + "%", fg='black' if mode == 0 else 'white',
                      bg='black' if mode == 1 else 'light grey', font=("Helvetica", 10))
    lable_ct3.place(x=135, y=offset + 300)
    lable_ct4 = Label(window, text=str(v[4]) + "%", fg='black' if mode == 0 else 'white',
                      bg='black' if mode == 1 else 'light grey', font=("Helvetica", 10))
    lable_ct4.place(x=185, y=offset + 300)
    lable_ct5 = Label(window, text=str(v[5]) + "%", fg='black' if mode == 0 else 'white',
                      bg='black' if mode == 1 else 'light grey', font=("Helvetica", 10))
    lable_ct5.place(x=235, y=offset + 300)
    lable_ct6 = Label(window, text=str(v[6]) + "%", fg='black' if mode == 0 else 'white',
                      bg='black' if mode == 1 else 'light grey', font=("Helvetica", 10))
    lable_ct6.place(x=285, y=offset + 300)
    lable_ct7 = Label(window, text=str(v[7]) + "%", fg='black' if mode == 0 else 'white',
                      bg='black' if mode == 1 else 'light grey', font=("Helvetica", 10))
    lable_ct7.place(x=335, y=offset + 300)
    lable_gt1 = Label(window, text=str(v[8]) + "%", fg='black' if mode == 0 else 'white',
                      bg='black' if mode == 1 else 'light grey', font=("Helvetica", 10))
    lable_gt1.place(x=35, y=offset + 580)
    lable_gt2 = Label(window, text=str(v[9]) + "%", fg='black' if mode == 0 else 'white',
                      bg='black' if mode == 1 else 'light grey', font=("Helvetica", 10))
    lable_gt2.place(x=85, y=offset + 580)
    lable_gt3 = Label(window, text=str(v[10]) + "%", fg='black' if mode == 0 else 'white',
                      bg='black' if mode == 1 else 'light grey', font=("Helvetica", 10))
    lable_gt3.place(x=135, y=offset + 580)
    lable_gt4 = Label(window, text=str(v[11]) + "%", fg='black' if mode == 0 else 'white',
                      bg='black' if mode == 1 else 'light grey', font=("Helvetica", 10))
    lable_gt4.place(x=185, y=offset + 580)
    lable_gt5 = Label(window, text=str(v[12]) + "%", fg='black' if mode == 0 else 'white',
                      bg='black' if mode == 1 else 'light grey', font=("Helvetica", 10))
    lable_gt5.place(x=235, y=offset + 580)
    lable_gt6 = Label(window, text=str(v[13]) + "%", fg='black' if mode == 0 else 'white',
                      bg='black' if mode == 1 else 'light grey', font=("Helvetica", 10))
    lable_gt6.place(x=285, y=offset + 580)
    lable_gt7 = Label(window, text=str(v[14]) + "%", fg='black' if mode == 0 else 'white',
                      bg='black' if mode == 1 else 'light grey', font=("Helvetica", 10))
    lable_gt7.place(x=335, y=offset + 580)

    lable_ct1_t = Label(window, text="<40°C", fg='Green',
                        bg='black' if mode == 1 else 'light grey', font=("Helvetica", 10))
    lable_ct1_t.place(x=30, y=offset + 527)
    lable_ct2_t = Label(window, text="40°C", fg='Green',
                        bg='black' if mode == 1 else 'light grey', font=("Helvetica", 10))
    lable_ct2_t.place(x=80, y=offset + 527)
    lable_ct3_t = Label(window, text="50°C", fg='Yellow',
                        bg='black' if mode == 1 else 'light grey', font=("Helvetica", 10))
    lable_ct3_t.place(x=130, y=offset + 527)
    lable_ct4_t = Label(window, text="60°C", fg='Yellow',
                        bg='black' if mode == 1 else 'light grey', font=("Helvetica", 10))
    lable_ct4_t.place(x=180, y=offset + 527)
    lable_ct5_t = Label(window, text="70°C", fg='orange',
                        bg='black' if mode == 1 else 'light grey', font=("Helvetica", 10))
    lable_ct5_t.place(x=230, y=offset + 527)
    lable_ct6_t = Label(window, text="80°C", fg='Red', bg='black' if mode ==
                        1 else 'light grey', font=("Helvetica", 10))
    lable_ct6_t.place(x=280, y=offset + 527)
    lable_ct7_t = Label(window, text="90°C", fg='Red', bg='black' if mode ==
                        1 else 'light grey', font=("Helvetica", 10))
    lable_ct7_t.place(x=330, y=offset + 527)
    lable_gt1_t = Label(window, text="<40°C", fg='Green',
                        bg='black' if mode == 1 else 'light grey', font=("Helvetica", 10))
    lable_gt1_t.place(x=30, y=offset + 810)
    lable_gt2_t = Label(window, text="40°C", fg='Green',
                        bg='black' if mode == 1 else 'light grey', font=("Helvetica", 10))
    lable_gt2_t.place(x=80, y=offset + 810)
    lable_gt3_t = Label(window, text="50°C", fg='Yellow',
                        bg='black' if mode == 1 else 'light grey', font=("Helvetica", 10))
    lable_gt3_t.place(x=130, y=offset + 810)
    lable_gt4_t = Label(window, text="60°C", fg='Yellow',
                        bg='black' if mode == 1 else 'light grey', font=("Helvetica", 10))
    lable_gt4_t.place(x=180, y=offset + 810)
    lable_gt5_t = Label(window, text="70°C", fg='orange',
                        bg='black' if mode == 1 else 'light grey', font=("Helvetica", 10))
    lable_gt5_t.place(x=230, y=offset + 810)
    lable_gt6_t = Label(window, text="80°C", fg='red', bg='black' if mode ==
                        1 else 'light grey', font=("Helvetica", 10))
    lable_gt6_t.place(x=280, y=offset + 810)
    lable_gt7_t = Label(window, text="90°C", fg='red', bg='black' if mode ==
                        1 else 'light grey', font=("Helvetica", 10))
    lable_gt7_t.place(x=330, y=offset + 810)

    def sct_val(val):
        lable_ct1.config(text=str(sct1.get()) + "%")
        lable_ct2.config(text=str(sct2.get()) + "%")
        lable_ct3.config(text=str(sct3.get()) + "%")
        lable_ct4.config(text=str(sct4.get()) + "%")
        lable_ct5.config(text=str(sct5.get()) + "%")
        lable_ct6.config(text=str(sct6.get()) + "%")
        lable_ct7.config(text=str(sct7.get()) + "%")
        lable_gt1.config(text=str(sgt1.get()) + "%")
        lable_gt2.config(text=str(sgt2.get()) + "%")
        lable_gt3.config(text=str(sgt3.get()) + "%")
        lable_gt4.config(text=str(sgt4.get()) + "%")
        lable_gt5.config(text=str(sgt5.get()) + "%")
        lable_gt6.config(text=str(sgt6.get()) + "%")
        lable_gt7.config(text=str(sgt7.get()) + "%")
        return

    sct1 = Scale(window, from_=150, to=0, orient=VERTICAL, length=200, showvalue=0, tickinterval=5, resolution=5,
                 fg='black' if mode == 0 else 'white', bg='black' if mode == 1 else 'light grey', command=sct_val)
    sct1.place(x=10, y=offset + 320)
    sct1.set(v[1])
    sct2 = Scale(window, from_=150, to=0, orient=VERTICAL, length=200, showvalue=0, tickinterval=5, resolution=5,
                 fg='black' if mode == 0 else 'white', bg='black' if mode == 1 else 'light grey', command=sct_val)
    sct2.place(x=60, y=offset + 320)
    sct2.set(v[2])
    sct3 = Scale(window, from_=150, to=0, orient=VERTICAL, length=200, showvalue=0, tickinterval=5, resolution=5,
                 fg='black' if mode == 0 else 'white', bg='black' if mode == 1 else 'light grey', command=sct_val)
    sct3.place(x=110, y=offset + 320)
    sct3.set(v[3])
    sct4 = Scale(window, from_=150, to=0, orient=VERTICAL, length=200, showvalue=0, tickinterval=5, resolution=5,
                 fg='black' if mode == 0 else 'white', bg='black' if mode == 1 else 'light grey', command=sct_val)
    sct4.place(x=160, y=offset + 320)
    sct4.set(v[4])
    sct5 = Scale(window, from_=150, to=0, orient=VERTICAL, length=200, showvalue=0, tickinterval=5, resolution=5,
                 fg='black' if mode == 0 else 'white', bg='black' if mode == 1 else 'light grey', command=sct_val)
    sct5.place(x=210, y=offset + 320)
    sct5.set(v[5])
    sct6 = Scale(window, from_=150, to=0, orient=VERTICAL, length=200, showvalue=0, tickinterval=5, resolution=5,
                 fg='black' if mode == 0 else 'white', bg='black' if mode == 1 else 'light grey', command=sct_val)
    sct6.place(x=260, y=offset + 320)
    sct6.set(v[6])
    sct7 = Scale(window, from_=150, to=0, orient=VERTICAL, length=200, showvalue=0, tickinterval=5, resolution=5,
                 fg='black' if mode == 0 else 'white', bg='black' if mode == 1 else 'light grey', command=sct_val)
    sct7.place(x=310, y=offset + 320)
    sct7.set(v[7])
    sgt1 = Scale(window, from_=150, to=0, orient=VERTICAL, length=200, showvalue=0, tickinterval=5, resolution=5,
                 fg='black' if mode == 0 else 'white', bg='black' if mode == 1 else 'light grey', command=sct_val)
    sgt1.place(x=10, y=offset + 600)
    sgt1.set(v[8])
    sgt2 = Scale(window, from_=150, to=0, orient=VERTICAL, length=200, showvalue=0, tickinterval=5, resolution=5,
                 fg='black' if mode == 0 else 'white', bg='black' if mode == 1 else 'light grey', command=sct_val)
    sgt2.place(x=60, y=offset + 600)
    sgt2.set(v[9])
    sgt3 = Scale(window, from_=150, to=0, orient=VERTICAL, length=200, showvalue=0, tickinterval=5, resolution=5,
                 fg='black' if mode == 0 else 'white', bg='black' if mode == 1 else 'light grey', command=sct_val)
    sgt3.place(x=110, y=offset + 600)
    sgt3.set(v[10])
    sgt4 = Scale(window, from_=150, to=0, orient=VERTICAL, length=200, showvalue=0, tickinterval=5, resolution=5,
                 fg='black' if mode == 0 else 'white', bg='black' if mode == 1 else 'light grey', command=sct_val)
    sgt4.place(x=160, y=offset + 600)
    sgt4.set(v[11])
    sgt5 = Scale(window, from_=150, to=0, orient=VERTICAL, length=200, showvalue=0, tickinterval=5, resolution=5,
                 fg='black' if mode == 0 else 'white', bg='black' if mode == 1 else 'light grey', command=sct_val)
    sgt5.place(x=210, y=offset + 600)
    sgt5.set(v[12])
    sgt6 = Scale(window, from_=150, to=0, orient=VERTICAL, length=200, showvalue=0, tickinterval=5, resolution=5,
                 fg='black' if mode == 0 else 'white', bg='black' if mode == 1 else 'light grey', command=sct_val)
    sgt6.place(x=260, y=offset + 600)
    sgt6.set(v[13])
    sgt7 = Scale(window, from_=150, to=0, orient=VERTICAL, length=200, showvalue=0, tickinterval=5, resolution=5,
                 fg='black' if mode == 0 else 'white', bg='black' if mode == 1 else 'light grey', command=sct_val)
    sgt7.place(x=310, y=offset + 600)
    sgt7.set(v[14])

    def adv_apply():
        vr = [140, sct1.get(), sct2.get(), sct3.get(), sct4.get(), sct5.get(), sct6.get(), sct7.get(
        ), sgt1.get(), sgt2.get(), sgt3.get(), sgt4.get(), sgt5.get(), sgt6.get(), sgt7.get()]
        global mode_f
        mode_f = 3
        config_file_write(mode, 3, vr)
        return

    adv = Button(window, text="Apply", width=20, fg='black' if mode ==
                 0 else 'white', bg='black' if mode == 1 else 'light grey', command=adv_apply)
    adv.place(x=90, y=offset + 830)

    a_on.config(fg='black' if mode == 0 else 'white',
                bg='black' if mode == 1 else 'light grey', command=auto_on)
    b_on.config(fg='black' if mode == 0 else 'white',
                bg='black' if mode == 1 else 'light grey', command=basic_build)
    ad_on.config(fg='red', bg='black' if mode ==
                 1 else 'light grey', command=null)
    cb_on.config(fg='black' if mode == 0 else 'white', bg='black' if mode ==
                 1 else 'light grey', command=cooler_booster_on)
    return


"""########################################## Cooler Booster Mode"""


def cooler_booster_on():
    window.geometry('370x270')
    global mode_f
    mode_f = 4
    config_file_write(mode, 4, -1)

    a_on.config(fg='black' if mode == 0 else 'white',
                bg='black' if mode == 1 else 'light grey', command=auto_on)
    b_on.config(fg='black' if mode == 0 else 'white',
                bg='black' if mode == 1 else 'light grey', command=basic_build)
    ad_on.config(fg='black' if mode == 0 else 'white',
                 bg='black' if mode == 1 else 'light grey', command=advanced_on)
    cb_on.config(fg='red', bg='black' if mode ==
                 1 else 'light grey', command=null)
    return


cb = Label(window, text="Fan Mode", fg='red', bg='black' if mode ==
           1 else 'light grey', font=("Helvetica", 12))
cb.place(x=150, y=215)

a_on = Button(window, text="Auto", width=6, fg='black' if mode ==
              0 else 'white', bg='black' if mode == 1 else 'light grey', command=auto_on)
a_on.place(x=10, y=235)

b_on = Button(window, text="Basic", width=6, fg='black' if mode == 0 else 'white',
              bg='black' if mode == 1 else 'light grey', command=basic_build)
b_on.place(x=90, y=235)

ad_on = Button(window, text="Advanced", width=6, fg='black' if mode ==
               0 else 'white', bg='black' if mode == 1 else 'light grey', command=advanced_on)
ad_on.place(x=170, y=235)

cb_on = Button(window, text="Cooler Booster", width=10, fg='black' if mode ==
               0 else 'white', bg='black' if mode == 1 else 'light grey', command=cooler_booster_on)
cb_on.place(x=250, y=235)

if int(mode_f) == 1:
    a_on.config(fg='red')
elif int(mode_f) == 2:
    b_on.config(fg='red')
    conf_file_x = open(my_filename, "r")
    all_lines = conf_file_x.readlines()
    offset_official = int(all_lines[2])
    basic_slider.set(offset_official)
elif int(mode_f) == 3:
    ad_on.config(fg='red')
    vr_3 = []
    vr_2 = []
    vr_1 = []
    conf_file_x = open(my_filename, "r")
    all_lines = conf_file_x.readlines()
    vr_1 = all_lines[3]
    vr_2 = vr_1.split(",")
    count = 0
    for i in vr_2:
        count = count + 1
        if count < 16:
            vr_3.append(int(i))
    conf_file_x.close()
    advanced_on()
else:
    cb_on.config(fg='red')


def on_closing():
    window.destroy()
    return


canvas.pack(fill=BOTH, expand=1)
window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()
