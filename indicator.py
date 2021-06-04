#! /usr/bin/python3

import signal
import os
import subprocess
import webbrowser
import fileinput
from gi.repository  import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator

#################################################################################################### Indicator Making

APPINDICATOR_ID = 'myappindicator'
iconpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon_2.png")

path_to_script = os.path.dirname(os.path.abspath(__file__))
my_filename = os.path.join(path_to_script, "conf.txt")
check_1 = os.path.exists(my_filename)

if check_1 == False:
	open(my_filename, "w").close()
	subprocess.call(['chmod', '0777', my_filename])
	conf_file = open(my_filename, "w")
	conf_file.writelines("1\n0\n")
	temp_ = [140,0,20,40,45,50,60,70,0,20,40,45,50,60,70]
	for val in temp_:
		conf_file.write("%i," % val)
	conf_file.write("\n100")
	conf_file.close()

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
    os.system("x-terminal-emulator -e 'bash -c \"sudo nohup python3 ${pkgdir}write_EC.py >/dev/null 2>&1\"'")
    return

def main():
    indicator = appindicator.Indicator.new(APPINDICATOR_ID, iconpath, appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    gtk.main()

def build_menu():
    menu = gtk.Menu()
    basic_submenu = gtk.Menu()
    battery_charge_threshold_submenu = gtk.Menu()

    item_github = gtk.MenuItem.new_with_label('Visit Project')
    item_github.connect('activate', github)
    menu.append(item_github)

    Separator = gtk.SeparatorMenuItem()                                     ################################## Fan Mode
    menu.append(Separator)

    item_auto = gtk.MenuItem.new_with_label('Auto')                         ################# Auto
    item_auto.connect('activate', auto)
    menu.append(item_auto)

    item_basic = gtk.MenuItem.new_with_label('Basic')                       ################# Basic
    item_basic.set_submenu(basic_submenu)
    
    basic_slowest = gtk.MenuItem.new_with_label('Slowest')
    basic_slowest.connect('activate', slowest)
    basic_submenu.append(basic_slowest)

    basic_slower = gtk.MenuItem.new_with_label('Slower')
    basic_slower.connect('activate', slower)
    basic_submenu.append(basic_slower)
    
    basic_slow = gtk.MenuItem.new_with_label('Slow')
    basic_slow.connect('activate', slow)
    basic_submenu.append(basic_slow)
    
    basic_normal = gtk.MenuItem.new_with_label('Normal')
    basic_normal.connect('activate', normal)
    basic_submenu.append(basic_normal)
    
    basic_fast = gtk.MenuItem.new_with_label('Fast')
    basic_fast.connect('activate', fast)
    basic_submenu.append(basic_fast)
    
    basic_faster = gtk.MenuItem.new_with_label('Faster')
    basic_faster.connect('activate', faster)
    basic_submenu.append(basic_faster)

    basic_fastest = gtk.MenuItem.new_with_label('Fastest')
    basic_fastest.connect('activate', fastest)
    basic_submenu.append(basic_fastest)

    menu.append(item_basic)

    item_advanced = gtk.MenuItem.new_with_label('Advanced')                  ################# Advanced
    item_advanced.connect('activate', advanced)
    menu.append(item_advanced)

    item_cooler_booster = gtk.MenuItem.new_with_label('Cooler Booster')      ################# Cooler Booster
    item_cooler_booster.connect('activate', cooler_booster)
    menu.append(item_cooler_booster)

    Separator = gtk.SeparatorMenuItem()                                      ################################# Monitering & Battery Charging Threshold
    menu.append(Separator)

    item_monitor = gtk.MenuItem.new_with_label('Monitoring')
    item_monitor.connect('activate', monitoring)
    menu.append(item_monitor)

    item_battery_charge_threashold = gtk.MenuItem.new_with_label('Battery Charge Threashold')
    item_battery_charge_threashold.set_submenu(battery_charge_threshold_submenu)
    
    mx_90 = gtk.MenuItem.new_with_label('90%')
    mx_90.connect('activate', battery_charge_threashold_90)
    battery_charge_threshold_submenu.append(mx_90)

    mx_100 = gtk.MenuItem.new_with_label('100%')
    mx_100.connect('activate', battery_charge_threashold_100)
    battery_charge_threshold_submenu.append(mx_100)
    
    menu.append(item_battery_charge_threashold)

    Separator = gtk.SeparatorMenuItem()                                      ################################# Quit
    menu.append(Separator)

    item_quit = gtk.MenuItem.new_with_label('Quit')
    item_quit.connect('activate', quit)
    menu.append(item_quit)

    menu.show_all()
    return menu



def github(source):
    webbrowser.open("https://github.com/YoCodingMonster/MSI-Dragon-Center-for-Linux")

def auto(source):
    all_lines = reading()
    lines = str(1) + "\n" + all_lines[1] + "\n" + all_lines[2] + "\n" + all_lines[3]
    corrections(lines)

def slowest(source):
    all_lines = reading()
    lines = str(2) + "\n" + "-30" + "\n" + all_lines[2] + "\n" + all_lines[3]
    corrections(lines)

def slower(source):
    all_lines = reading()
    lines = str(2) + "\n" + "-20" + "\n" + all_lines[2] + "\n" + all_lines[3]
    corrections(lines)

def slow(source):
    all_lines = reading()
    lines = str(2) + "\n" + "-10" + "\n" + all_lines[2] + "\n" + all_lines[3]
    corrections(lines)

def normal(source):
    all_lines = reading()
    lines = str(2) + "\n" + "0" + "\n" + all_lines[2] + "\n" + all_lines[3]
    corrections(lines)

def fast(source):
    all_lines = reading()
    lines = str(2) + "\n" + "10" + "\n" + all_lines[2] + "\n" + all_lines[3]
    corrections(lines)

def faster(source):
    all_lines = reading()
    lines = str(2) + "\n" + "20" + "\n" + all_lines[2] + "\n" + all_lines[3]
    corrections(lines)

def fastest(source):
    all_lines = reading()
    lines = str(2) + "\n" + "30" + "\n" + all_lines[2] + "\n" + all_lines[3]
    corrections(lines)

def advanced(source):
    command_w = "nohup python3 ${pkgdir}advanced.py >/dev/null 2>&1"
    os.popen((command_w), 'w')

def cooler_booster(source):
    all_lines = reading()
    lines = str(4) + "\n" + all_lines[1] + "\n" + all_lines[2] + "\n" + all_lines[3]
    corrections(lines)

def monitoring(source):
    os.system("x-terminal-emulator -e 'bash -c \"sudo nohup python3 ${pkgdir}monitor.py >/dev/null 2>&1\"'")

def battery_charge_threashold_90(osurce):
    all_lines = reading()
    lines = all_lines[0] + "\n" + all_lines[1] + "\n" + all_lines[2] + "\n" + "90"
    corrections(lines)

def battery_charge_threashold_100(osurce):
    all_lines = reading()
    lines = all_lines[0] + "\n" + all_lines[1] + "\n" + all_lines[2] + "\n" + "100"
    corrections(lines)

def quit(source):
    gtk.main_quit()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()