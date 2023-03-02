#! /usr/bin/python3

import imports_manager

#################################################################################################### Indicator Making

APPINDICATOR_ID = 'myappindicator'
iconpath = imports_manager.os.path.join(imports_manager.os.path.dirname(imports_manager.os.path.abspath(__file__)), "icon_22.png")

path_to_script = imports_manager.os.path.dirname(imports_manager.os.path.abspath(__file__))
my_filename = imports_manager.os.path.join(path_to_script, "conf.txt")
check_1 = imports_manager.os.path.exists(my_filename)

if check_1 == False:
    # os.system("x-terminal-emulator -e 'bash -c \"./root_permissions.sh\"'")
    imports_manager.os.system("x-terminal-emulator -e 'bash -c \"sudo ./install_deps.sh\"'")
    open(my_filename, "w").close()
    imports_manager.subprocess.call(['chmod', '0777', my_filename])
    conf_file = open(my_filename, "w")
    conf_file.writelines("1\n0\n")
    temp_ = [140,0,20,40,45,50,60,70,0,20,40,45,50,60,70]
    for val in temp_:
        conf_file.write("%i," % val)
    conf_file.write("\n100\n")
    temp_ = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for val in temp_:
        conf_file.write("%i," % val)
    conf_file.write("\n")
    temp_ = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    conf_file.write("12,")
    for val in temp_:
        conf_file.write("%i," % val)
    conf_file.write("\n0")
    conf_file.close()
    imports_manager.os.system("sudo python3 read_temp_set.py")
    
import gi.repository
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository  import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator

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
    for line in imports_manager.fileinput.FileInput(my_filename, inplace = True):
        if line.rstrip():
            str_1 = str_1 + line
    conf_file = open(my_filename, "w")
    conf_file.writelines(str_1)
    conf_file.close()
    imports_manager.os.system("sudo python3 write_EC.py")
    return

all_lines = reading()
lines = all_lines[0] + "\n" + all_lines[1] + "\n" + all_lines[2] + "\n" + all_lines[3] + "\n" + all_lines[4] + "\n" + all_lines[5] + "\n" + all_lines[6]
corrections(lines)

def main():
    indicator = appindicator.Indicator.new(APPINDICATOR_ID, iconpath, appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    gtk.main()

def build_menu():
    menu = gtk.Menu()
    basic_submenu = gtk.Menu()
    cpu_submenu = gtk.Menu()
    battery_charge_threshold_submenu = gtk.Menu()
    flip_board_submenu = gtk.Menu()
    backlight_submenu = gtk.Menu()

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

    item_monitor = gtk.MenuItem.new_with_label('Monitoring')                 ################# Monitering
    item_monitor.connect('activate', monitoring)
    menu.append(item_monitor)
    
    item_cpu = gtk.MenuItem.new_with_label('CPU Profiles')                   ################# CPU profiles
    item_cpu.set_submenu(cpu_submenu)
    
    cpu_powersaver = gtk.MenuItem.new_with_label('PowerSaver')
    cpu_powersaver.connect('activate', powersaver)
    cpu_submenu.append(cpu_powersaver)
    
    cpu_balanced = gtk.MenuItem.new_with_label('Balanced')
    cpu_balanced.connect('activate', balanced)
    cpu_submenu.append(cpu_balanced)
    
    cpu_performance = gtk.MenuItem.new_with_label('Performance')
    cpu_performance.connect('activate', performance)
    cpu_submenu.append(cpu_performance)
    
    cpu_manual = gtk.MenuItem.new_with_label('Manual')
    cpu_manual.connect('activate', manual)
    cpu_submenu.append(cpu_manual)
    
    menu.append(item_cpu)

    item_battery_charge_threashold = gtk.MenuItem.new_with_label('Battery Charge Threashold')          ################# Battery Profiles
    item_battery_charge_threashold.set_submenu(battery_charge_threshold_submenu)
    
    mx_50 = gtk.MenuItem.new_with_label('50%')
    mx_50.connect('activate', battery_charge_threashold_50)
    battery_charge_threshold_submenu.append(mx_50)
    
    mx_60 = gtk.MenuItem.new_with_label('60%')
    mx_60.connect('activate', battery_charge_threashold_60)
    battery_charge_threshold_submenu.append(mx_60)
    
    mx_70 = gtk.MenuItem.new_with_label('70%')
    mx_70.connect('activate', battery_charge_threashold_70)
    battery_charge_threshold_submenu.append(mx_70)
    
    mx_80 = gtk.MenuItem.new_with_label('80%')
    mx_80.connect('activate', battery_charge_threashold_80)
    battery_charge_threshold_submenu.append(mx_80)
    
    mx_90 = gtk.MenuItem.new_with_label('90%')
    mx_90.connect('activate', battery_charge_threashold_90)
    battery_charge_threshold_submenu.append(mx_90)

    mx_100 = gtk.MenuItem.new_with_label('100%')
    mx_100.connect('activate', battery_charge_threashold_100)
    battery_charge_threshold_submenu.append(mx_100)
    
    menu.append(item_battery_charge_threashold)
    
    Separator = gtk.SeparatorMenuItem()                                      ################################# EC Dump
    menu.append(Separator)

    item_ec = gtk.MenuItem.new_with_label('EC Mapping')
    item_ec.connect('activate', ec_map)
    menu.append(item_ec)

    item_flip_board = gtk.MenuItem.new_with_label('Intel 10th Gen or above')                       ################# CPU fan monitor choose "ca" and "c8"
    item_flip_board.set_submenu(flip_board_submenu)
    
    item_flip_board_1 = gtk.MenuItem.new_with_label('Yes')
    item_flip_board_1.connect('activate', flip_board_1)
    flip_board_submenu.append(item_flip_board_1)

    item_flip_board_2 = gtk.MenuItem.new_with_label('No')
    item_flip_board_2.connect('activate', flip_board_2)
    flip_board_submenu.append(item_flip_board_2)

    menu.append(item_flip_board)

    Separator = gtk.SeparatorMenuItem()                                      ################################# Quit
    menu.append(Separator)

    item_quit = gtk.MenuItem.new_with_label('Quit')
    item_quit.connect('activate', quit)
    menu.append(item_quit)

    menu.show_all()
    return menu

def github(source):
    imports_manager.webbrowser.open("https://github.com/YoCodingMonster/MSI-Dragon-Center-for-Linux")

def auto(source):
    all_lines = reading()
    lines = str(1) + "\n" + all_lines[1] + "\n" + all_lines[2] + "\n" + all_lines[3] + "\n" + all_lines[4] + "\n" + all_lines[5] + "\n" + all_lines[6]
    corrections(lines)

def slowest(source):
    all_lines = reading()
    lines = str(2) + "\n" + "-30" + "\n" + all_lines[2] + "\n" + all_lines[3] + "\n" + all_lines[4] + "\n" + all_lines[5] + "\n" + all_lines[6]
    corrections(lines)

def slower(source):
    all_lines = reading()
    lines = str(2) + "\n" + "-20" + "\n" + all_lines[2] + "\n" + all_lines[3] + "\n" + all_lines[4] + "\n" + all_lines[5] + "\n" + all_lines[6]
    corrections(lines)

def slow(source):
    all_lines = reading()
    lines = str(2) + "\n" + "-10" + "\n" + all_lines[2] + "\n" + all_lines[3] + "\n" + all_lines[4] + "\n" + all_lines[5] + "\n" + all_lines[6]
    corrections(lines)

def normal(source):
    all_lines = reading()
    lines = str(2) + "\n" + "0" + "\n" + all_lines[2] + "\n" + all_lines[3] + "\n" + all_lines[4] + "\n" + all_lines[5] + "\n" + all_lines[6]
    corrections(lines)

def fast(source):
    all_lines = reading()
    lines = str(2) + "\n" + "10" + "\n" + all_lines[2] + "\n" + all_lines[3] + "\n" + all_lines[4] + "\n" + all_lines[5] + "\n" + all_lines[6]
    corrections(lines)

def faster(source):
    all_lines = reading()
    lines = str(2) + "\n" + "20" + "\n" + all_lines[2] + "\n" + all_lines[3] + "\n" + all_lines[4] + "\n" + all_lines[5] + "\n" + all_lines[6]
    corrections(lines)

def fastest(source):
    all_lines = reading()
    lines = str(2) + "\n" + "30" + "\n" + all_lines[2] + "\n" + all_lines[3] + "\n" + all_lines[4] + "\n" + all_lines[5] + "\n" + all_lines[6]
    corrections(lines)

def advanced(source):
    imports_manager.os.system("sudo python3 advanced.py")

def cooler_booster(source):
    all_lines = reading()
    lines = str(4) + "\n" + all_lines[1] + "\n" + all_lines[2] + "\n" + all_lines[3] + "\n" + all_lines[4] + "\n" + all_lines[5] + "\n" + all_lines[6]
    corrections(lines)

def monitoring(source):
    imports_manager.os.system("sudo python3 monitor.py")
    
def powersaver(source):
    f = 0

def balanced(source):
    f = 0

def performance(source):
    f = 0
    
def manual(source):
    f = 0
    
def cpu(source):
    f = 0
    
def battery_charge_threashold_50(source):
    all_lines = reading()
    lines = all_lines[0] + "\n" + all_lines[1] + "\n" + all_lines[2] + "\n" + "50" + "\n" + all_lines[4] + "\n" + all_lines[5] + "\n" + all_lines[6]
    corrections(lines)

def battery_charge_threashold_60(source):
    all_lines = reading()
    lines = all_lines[0] + "\n" + all_lines[1] + "\n" + all_lines[2] + "\n" + "60" + "\n" + all_lines[4] + "\n" + all_lines[5] + "\n" + all_lines[6]
    corrections(lines)

def battery_charge_threashold_70(source):
    all_lines = reading()
    lines = all_lines[0] + "\n" + all_lines[1] + "\n" + all_lines[2] + "\n" + "70" + "\n" + all_lines[4] + "\n" + all_lines[5] + "\n" + all_lines[6]
    corrections(lines)

def battery_charge_threashold_80(source):
    all_lines = reading()
    lines = all_lines[0] + "\n" + all_lines[1] + "\n" + all_lines[2] + "\n" + "80" + "\n" + all_lines[4] + "\n" + all_lines[5] + "\n" + all_lines[6]
    corrections(lines)

def battery_charge_threashold_90(source):
    all_lines = reading()
    lines = all_lines[0] + "\n" + all_lines[1] + "\n" + all_lines[2] + "\n" + "90" + "\n" + all_lines[4] + "\n" + all_lines[5] + "\n" + all_lines[6]
    corrections(lines)

def battery_charge_threashold_100(source):
    all_lines = reading()
    lines = all_lines[0] + "\n" + all_lines[1] + "\n" + all_lines[2] + "\n" + "100" + "\n" + all_lines[4] + "\n" + all_lines[5] + "\n" + all_lines[6]
    corrections(lines)
    
def ec_map(source):
    imports_manager.os.system("sudo python3 ec_dump.py")
    
def flip_board_1(source):
    all_lines = reading()
    lines = all_lines[0] + "\n" + all_lines[1] + "\n" + all_lines[2] + "\n" + all_lines[3] + "\n" + all_lines[4] + "\n" + all_lines[5] + "\n" + str(1)
    corrections(lines)
    
def flip_board_2(source):
    all_lines = reading()
    lines = all_lines[0] + "\n" + all_lines[1] + "\n" + all_lines[2] + "\n" + all_lines[3] + "\n" + all_lines[4] + "\n" + all_lines[5] + "\n" + str(0)
    corrections(lines)

def quit(source):
    gtk.main_quit()

if __name__ == "__main__":
    imports_manager.signal.signal(imports_manager.signal.SIGINT, imports_manager.signal.SIG_DFL)
    main()
