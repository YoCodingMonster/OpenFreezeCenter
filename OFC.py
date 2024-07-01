#! /usr/bin/python3

import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

EC_IO_FILE = '/sys/kernel/debug/ec/ec0/io'

# Universal EC Byte writing

def write(BYTE, VALUE):
    with open(EC_IO_FILE,'w+b') as file:
        file.seek(BYTE)
        file.write(bytes((VALUE,)))

# Universal EC Byte reading

def read(BYTE, SIZE, FORMAT):
    with open(EC_IO_FILE,'r+b') as file:
        file.seek(BYTE)
        if SIZE == 1 and FORMAT == 0:
            VALUE = int(file.read(1).hex(),16)
        elif SIZE == 1 and FORMAT == 1:
            VALUE = file.read(1).hex()
        elif SIZE == 2 and FORMAT == 0:
            VALUE = int(file.read(2).hex(),16)
        elif SIZE == 2 and FORMAT == 1:
            VALUE = file.read(2).hex()
    return VALUE

def fan_profile(PROFILE, ONOFF, ADDRESS = 0, SPEED = 0):
    # Setting up fan profiles
    if PROFILE != 4:
        write(ONOFF[0][0], ONOFF[0][1])      # Cooler Booster fan curve off
        write(ONOFF[1][0], ONOFF[1][1])      # Auto/Adv/Basic/ fan curve on
        for CPU_GPU_ROWS in range (0, 2):
            for FAN_SPEEDS in range (0, 7):
                write(ADDRESS[CPU_GPU_ROWS][FAN_SPEEDS], SPEED[CPU_GPU_ROWS][FAN_SPEEDS])
    else:
        write(ONOFF[0], ONOFF[1])      # Cooler Booster fan curve on/off

#   PROFILE                      = 1 or 2 or 3 or 4
#	AUTO_SPEED                   = [[CPU1, CPU2, CPU3, CPU4, CPU5, CPU6, CPU7], [GPU1, GPU2, GPU3, GPU4, GPU5, GPU6, GPU7]]
#	ADV_SPEED                    = [[CPU1, CPU2, CPU3, CPU4, CPU5, CPU6, CPU7], [GPU1, GPU2, GPU3, GPU4, GPU5, GPU6, GPU7]]
#   BASIC_OFFSET                 = Value between -30 to +30
#	CPU                          = 1 if CPU is 11th gen and above || 0 if CPU is 10th gen or below
#	AUTO_ADV_VALUES              = [FAN PROFILE ADDRESS, AUTO VALUE, ADVANCED VALUE]
#	COOLER_BOOSTER_OFF_ON_VALUES = [COOLER BOOSTER ADDRESS, COOLER BOOSTER OFF VALUE, COOLER BOOSTER ON VALUE]
#	CPU_GPU_FAN_SPEED_ADDRESS    = [[CPU1, CPU2, CPU3, CPU4, CPU5, CPU6, CPU7], [GPU1, GPU2, GPU3, GPU4, GPU5, GPU6, GPU7]]
#	CPU_GPU_TEMP_ADDRESS         = [CPU CURRENT TEMP ADDRESS, GPU CURRENT TEMP ADDRESS]
#	CPU_GPU_RPM_ADDRESS          = [CPU FAN RPM ADDRESS, GPU FAN RPM ADDRESS]
#   BATTERY_THRESHOLD_VALUE      = 50 to 100

MIN_MAX = [100, 0, 100, 0]
BASIC_SPEED = [[0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0]]

def create_dialog(TITLE, TEXT, YES, NO, x, y, RESPONSE_TYPE):
	dialog = Gtk.Dialog(title = TITLE)
	dialog.set_default_size(x, y)
	if RESPONSE_TYPE == 1:
		dialog.add_button("Yes", Gtk.ResponseType.YES)
		dialog.add_button("No", Gtk.ResponseType.NO)
	elif RESPONSE_TYPE == 2:
		dialog.add_button("Yes", Gtk.ResponseType.OK)
		dialog.add_button("No", Gtk.ResponseType.CANCEL)
	else:
		dialog.add_button("Yes", Gtk.ResponseType.OK)
	label = Gtk.Label(TEXT)
	dialog.vbox.add(label)
	label.show()

	response = dialog.run()
	if RESPONSE_TYPE == 1:
		if response == Gtk.ResponseType.YES: LINE = YES
		elif response == Gtk.ResponseType.NO: LINE = NO
	elif RESPONSE_TYPE == 2:
		if response == Gtk.ResponseType.OK: os.system("shutdown -r +1")
		elif response == Gtk.ResponseType.CANCEL: create_dialog("Warning", "The Application will not be able to perform EC Read/Write for changing Fan profiles and Monitoring!", "", "", 200, 150, 3)

	dialog.show_all()
	dialog.destroy()
	return LINE

################################################################
# Setting the config.py file where all the data will be stored #
################################################################

PATH_TO_CONFIG = str(os.path.realpath(os.path.dirname(__file__))) + "/config.py"
try:
	open(PATH_TO_CONFIG, "r")
except FileNotFoundError:
	CONFIG = []
	CHOICE = "\nIf you want universal auto fan profile which is as below then [SELECT YES]\n\tAUTO SPEEDS = [[0, 40, 48, 56, 64, 72, 80], [0, 48, 56, 64, 72, 79, 86]]\n\nIf you want to fetch vendor specified auto fan profile which will require you to \n\t1 :- Close this(Before closing read all the steps)\n\t2 :- boot into windows\n\t3 :- set the fan profile to auto\n\t4 :- boot back to linux and then [SELECT NO]"
	LINE_YES = "PROFILE = 1\nAUTO_SPEED = [[0, 40, 48, 56, 64, 72, 80], [0, 48, 56, 64, 72, 79, 86]]"
	LINE_NO = "PROFILE = 1\nAUTO_SPEED = [["+str(read(0x72, 1, 0))+", "+str(read(0x73, 1, 0))+", "+str(read(0x74, 1, 0))+", "+str(read(0x75, 1, 0))+", "+str(read(0x76, 1, 0))+", "+str(read(0x77, 1, 0))+", "+str(read(0x78, 1, 0))+"], ["+str(read(0x8a, 1, 0))+", "+str(read(0x8b, 1, 0))+", "+str(read(0x8c, 1, 0))+", "+str(read(0x8d, 1, 0))+", "+str(read(0x8e, 1, 0))+", "+str(read(0x8f, 1, 0))+", "+str(read(0x90, 1, 0))+"]]"
	CONFIG.append(create_dialog("Auto Profile Selection", CHOICE, LINE_YES, LINE_NO, 300, 150, 1))

	CHOICE = "\nIs your CPU intel 10th Gen and above\n"
	LINE_YES = "\nADV_SPEED =  [[0, 40, 48, 56, 64, 72, 80], [0, 48, 56, 64, 72, 79, 86]] # Edit this list for ADVANCED FAN SPEEDS first the CPU speeds the GPU speeds\nBASIC_OFFSET = 0 # Edit this for a offset of fan speeds from AUTO SPEEDS from -30 to 30\nCPU = 1\nAUTO_ADV_VALUES = [0xd4, 13, 141]\nCOOLER_BOOSTER_OFF_ON_VALUES = [0x98, 2, 130]\nCPU_GPU_FAN_SPEED_ADDRESS = [[0x72, 0x73, 0x74, 0x75, 0x76, 0x77, 0x78], [0x8a, 0x8b, 0x8c, 0x8d, 0x8e, 0x8f, 0x90]]\nCPU_GPU_TEMP_ADDRESS = [0x68, 0x80]\nCPU_GPU_RPM_ADDRESS = [0xc8, 0xca]\nBATTERY_THRESHOLD_VALUE = 100 # Edit this value from between 50 to 100 for the percentage your battery will charge upto"
	LINE_NO =  "\nADV_SPEED =  [[0, 40, 48, 56, 64, 72, 80], [0, 48, 56, 64, 72, 79, 86]] # Edit this list for ADVANCED FAN SPEEDS first the CPU speeds the GPU speeds\nBASIC_OFFSET = 0 # Edit this for a offset of fan speeds from AUTO SPEEDS from -30 to 30\nCPU = 0\nAUTO_ADV_VALUES = [0xf4, 12, 140]\nCOOLER_BOOSTER_OFF_ON_VALUES = [0x98, 0, 128]\nCPU_GPU_FAN_SPEED_ADDRESS = [[0x72, 0x73, 0x74, 0x75, 0x76, 0x77, 0x78], [0x8a, 0x8b, 0x8c, 0x8d, 0x8e, 0x8f, 0x90]]\nCPU_GPU_TEMP_ADDRESS = [0x68, 0x80]\nCPU_GPU_RPM_ADDRESS = [0xc8, 0xca]\nBATTERY_THRESHOLD_VALUE = 100 # Edit this value from between 50 to 100 for the percentage your battery will charge upto"
	CONFIG.append(create_dialog("CPU Gen Selection", CHOICE, LINE_YES, LINE_NO, 300, 50, 1))

	CONFIG_FILE = open(PATH_TO_CONFIG, "w")
	CONFIG_FILE.writelines(CONFIG)
	CONFIG_FILE.close()
finally:
	import config

##########################
# Writing config.py file #
##########################

def config_writer():
    CONFIG = ""
    CONFIG_FILE = open(PATH_TO_CONFIG, "r")
    CONFIG = CONFIG_FILE.read()
    CONFIG_FILE.close()

    CONFIG = ("PROFILE = " + str(config.PROFILE))
    CONFIG = CONFIG + ("\nAUTO_SPEED = " + str(config.AUTO_SPEED))
    CONFIG = CONFIG + ("\nADV_SPEED = " + str(config.ADV_SPEED))
    CONFIG = CONFIG + ("\nBASIC_OFFSET = " + str(config.BASIC_OFFSET))
    CONFIG = CONFIG + ("\nCPU = " + str(config.CPU))
    CONFIG = CONFIG + ("\nAUTO_ADV_VALUES = " + str(config.AUTO_ADV_VALUES))
    CONFIG = CONFIG + ("\nCOOLER_BOOSTER_OFF_ON_VALUES = " + str(config.COOLER_BOOSTER_OFF_ON_VALUES))
    CONFIG = CONFIG + ("\nCPU_GPU_FAN_SPEED_ADDRESS = " + str(config.CPU_GPU_FAN_SPEED_ADDRESS))
    CONFIG = CONFIG + ("\nCPU_GPU_TEMP_ADDRESS = " + str(config.CPU_GPU_TEMP_ADDRESS))
    CONFIG = CONFIG + ("\nCPU_GPU_RPM_ADDRESS = " + str(config.CPU_GPU_RPM_ADDRESS))
    CONFIG = CONFIG + ("\nBATTERY_THRESHOLD_VALUE = " + str(config.BATTERY_THRESHOLD_VALUE))

    CONFIG_FILE = open(PATH_TO_CONFIG, "w")
    CONFIG_FILE.writelines(CONFIG)
    CONFIG_FILE.close()

#########################################
# chekcing fan speeds are within limits #
#########################################

def speed_checker(SPEEDS, OFFSET):
	for ROW in range(0, 2):
		for COLUMN in range(0, 7):
			SPEEDS[ROW][COLUMN] = 0 if (SPEEDS[ROW][COLUMN] + OFFSET < 0) else 150 if (SPEEDS[ROW][COLUMN] + OFFSET > 150) else SPEEDS[ROW][COLUMN] + OFFSET
	return SPEEDS

#############################################
# Below functions are part of GUI designing #
#############################################

def profile_selection(combobox):
	model = combobox.get_model()
	active_iter = combobox.get_active_iter()
	profile = model[active_iter][0]
	if profile == "Auto":
		config.PROFILE = 1
		config_writer()
		fan_profile(1, [[config.AUTO_ADV_VALUES[0], config.AUTO_ADV_VALUES[1]], [config.COOLER_BOOSTER_OFF_ON_VALUES[0], config.COOLER_BOOSTER_OFF_ON_VALUES[1]]], config.CPU_GPU_FAN_SPEED_ADDRESS, speed_checker(config.AUTO_SPEED, 0))
	elif profile == "Basic":
		config.PROFILE = 2
		config_writer()
		fan_profile(2, [[config.AUTO_ADV_VALUES[0], config.AUTO_ADV_VALUES[2]], [config.COOLER_BOOSTER_OFF_ON_VALUES[0], config.COOLER_BOOSTER_OFF_ON_VALUES[1]]], config.CPU_GPU_FAN_SPEED_ADDRESS, speed_checker(BASIC_SPEED, 30 if (config.BASIC_OFFSET > 30) else -30 if (config.BASIC_OFFSET < -30) else config.BASIC_OFFSET))
	elif profile == "Advanced":
		config.PROFILE = 3
		config_writer()
		fan_profile(3, [[config.AUTO_ADV_VALUES[0], config.AUTO_ADV_VALUES[2]], [config.COOLER_BOOSTER_OFF_ON_VALUES[0], config.COOLER_BOOSTER_OFF_ON_VALUES[1]]], config.CPU_GPU_FAN_SPEED_ADDRESS, speed_checker(config.ADV_SPEED, 0))
	elif profile == "Cooler Booster":
		config.PROFILE = 4
		config_writer()
		fan_profile(4, [config.COOLER_BOOSTER_OFF_ON_VALUES[0], config.COOLER_BOOSTER_OFF_ON_VALUES[2]])

def bct_selection(combobox):
	model = combobox.get_model()
	active_iter = combobox.get_active_iter()
	config.BATTERY_THRESHOLD_VALUE = int(model[active_iter][0])
	write(0xe4, config.BATTERY_THRESHOLD_VALUE + 128)
	config_writer()

def label_maker(text, x, y, offset, fixed):
	LABEL = Gtk.Label()
	LABEL.set_property("width-request", 80)
	LABEL.set_property("height-request", 35)
	LABEL.set_property("visible", True)
	LABEL.set_property("can-focus", False)
	LABEL.set_property("halign", Gtk.Align.CENTER)
	LABEL.set_property("valign", Gtk.Align.CENTER)
	LABEL.set_xalign(offset)
	LABEL.set_property("margin-left", 0)
	LABEL.set_property("margin-right", 10)
	LABEL.set_label(text)
	css_provider = Gtk.CssProvider()
	css_provider.load_from_data(f"""
	label {{
		text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.3);
	}}
	""".encode())
	context = LABEL.get_style_context()
	context.add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
	fixed.put(LABEL, x, y)
	fixed.add(LABEL)

def update_label():
	CPU_TEMP = read(config.CPU_GPU_TEMP_ADDRESS[0], 1, 0)
	GPU_TEMP = read(config.CPU_GPU_TEMP_ADDRESS[1], 1, 0)
	try:
		CPU_FAN_RPM = 478000//read(config.CPU_GPU_RPM_ADDRESS[0], 2, 0)
	except ZeroDivisionError:
		CPU_FAN_RPM = 0
	try:
		GPU_FAN_RPM = 478000//read(config.CPU_GPU_RPM_ADDRESS[1], 2, 0)
	except ZeroDivisionError:
		GPU_FAN_RPM = 0

	parent_window.CPU_CURR_TEMP.set_text(str(CPU_TEMP))
	if MIN_MAX[0] > CPU_TEMP:
		MIN_MAX[0] = CPU_TEMP
	if MIN_MAX[1] < CPU_TEMP:
		MIN_MAX[1] = CPU_TEMP
	parent_window.CPU_MIN_TEMP.set_text(str(MIN_MAX[0]))
	parent_window.CPU_MAX_TEMP.set_text(str(MIN_MAX[1]))

	parent_window.GPU_CURR_TEMP.set_text(str(GPU_TEMP))
	if MIN_MAX[2] > GPU_TEMP:
		MIN_MAX[2] = GPU_TEMP
	if MIN_MAX[3] < GPU_TEMP:
		MIN_MAX[3] = GPU_TEMP
	parent_window.GPU_MIN_TEMP.set_text(str(MIN_MAX[2]))
	parent_window.GPU_MAX_TEMP.set_text(str(MIN_MAX[3]))

	parent_window.CPU_FAN_RPM.set_text(str(CPU_FAN_RPM))
	parent_window.GPU_FAN_RPM.set_text(str(GPU_FAN_RPM))
	return True

class ParentWindow(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self, title = "Open Freeze Center (OFC)")
		self.set_default_size(300, 190)
		fixed = Gtk.Fixed()
		self.add(fixed)

		profile_selector = Gtk.ComboBox()
		profile_list = Gtk.ListStore(str)
		profile_list.append(["Auto"])
		profile_list.append(["Basic"])
		profile_list.append(["Advanced"])
		profile_list.append(["Cooler Booster"])
		profile_selector.set_model(profile_list)
		cell_renderer = Gtk.CellRendererText()
		profile_selector.pack_start(cell_renderer, True)
		profile_selector.add_attribute(cell_renderer, "text", 0)
		profile_selector.set_active(config.PROFILE - 1)
		profile_selector.connect("changed", profile_selection)
		profile_selector.set_property("width-request", 80)
		profile_selector.set_property("height-request", 35)
		fixed.put(profile_selector, 160, 10)
		fixed.add(profile_selector)

		css_provider = Gtk.CssProvider()
		css_provider.load_from_data(f"""
		label {{
			text-shadow: 0px 0px 10px rgba(0, 0, 0, 0.3);
		}}
		""".encode())

		label_maker("Select a fan profile", 10, 10, 0.0, fixed)                                                                 # Fan Profile
		label_maker("CURRENT", 60, 50, 0.0, fixed)                                                                              # Current
		label_maker("MIN", 140, 50, 0.0, fixed)                                                                                 # Minimum
		label_maker("MAX", 190, 50, 0.0, fixed)                                                                                 # Maximum
		label_maker("FAN RPM", 240, 50, 0.0, fixed)                                                                             # Fan RPM
		label_maker("CPU", 10, 80, 0.0, fixed)                                                                                  # CPU
		label_maker("GPU", 10, 110, 0.0, fixed)                                                                                 # GPU

		self.CPU_CURR_TEMP = Gtk.Label()
		self.CPU_CURR_TEMP.set_property("width-request", 80)
		self.CPU_CURR_TEMP.set_property("height-request", 35)
		self.CPU_CURR_TEMP.set_property("visible", True)
		self.CPU_CURR_TEMP.set_property("can-focus", False)
		self.CPU_CURR_TEMP.set_property("halign", Gtk.Align.CENTER)
		self.CPU_CURR_TEMP.set_property("valign", Gtk.Align.CENTER)
		self.CPU_CURR_TEMP.set_xalign(0.35)
		self.CPU_CURR_TEMP.set_property("margin-left", 0)
		self.CPU_CURR_TEMP.set_property("margin-right", 10)
		self.CPU_CURR_TEMP.set_label(str(read(config.CPU_GPU_TEMP_ADDRESS[0], 1, 0)))
		CPU_CURR_TEMP_STYLE = self.CPU_CURR_TEMP.get_style_context()
		CPU_CURR_TEMP_STYLE.add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
		fixed.put(self.CPU_CURR_TEMP, 60, 80)
		fixed.add(self.CPU_CURR_TEMP)

		self.CPU_MIN_TEMP = Gtk.Label()
		self.CPU_MIN_TEMP.set_property("width-request", 80)
		self.CPU_MIN_TEMP.set_property("height-request", 35)
		self.CPU_MIN_TEMP.set_property("visible", True)
		self.CPU_MIN_TEMP.set_property("can-focus", False)
		self.CPU_MIN_TEMP.set_property("halign", Gtk.Align.CENTER)
		self.CPU_MIN_TEMP.set_property("valign", Gtk.Align.CENTER)
		self.CPU_MIN_TEMP.set_xalign(0.05)
		self.CPU_MIN_TEMP.set_property("margin-left", 0)
		self.CPU_MIN_TEMP.set_property("margin-right", 10)
		CPU_MIN_TEMP_STYLE = self.CPU_MIN_TEMP.get_style_context()
		CPU_MIN_TEMP_STYLE.add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
		fixed.put(self.CPU_MIN_TEMP, 140, 80)
		fixed.add(self.CPU_MIN_TEMP)

		self.CPU_MAX_TEMP = Gtk.Label()
		self.CPU_MAX_TEMP.set_property("width-request", 80)
		self.CPU_MAX_TEMP.set_property("height-request", 35)
		self.CPU_MAX_TEMP.set_property("visible", True)
		self.CPU_MAX_TEMP.set_property("can-focus", False)
		self.CPU_MAX_TEMP.set_property("halign", Gtk.Align.CENTER)
		self.CPU_MAX_TEMP.set_property("valign", Gtk.Align.CENTER)
		self.CPU_MAX_TEMP.set_xalign(0.05)
		self.CPU_MAX_TEMP.set_property("margin-left", 0)
		self.CPU_MAX_TEMP.set_property("margin-right", 10)
		CPU_MAX_TEMP_STYLE = self.CPU_MAX_TEMP.get_style_context()
		CPU_MAX_TEMP_STYLE.add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
		fixed.put(self.CPU_MAX_TEMP, 190, 80)
		fixed.add(self.CPU_MAX_TEMP)

		self.CPU_FAN_RPM = Gtk.Label()
		self.CPU_FAN_RPM.set_property("width-request", 80)
		self.CPU_FAN_RPM.set_property("height-request", 35)
		self.CPU_FAN_RPM.set_property("visible", True)
		self.CPU_FAN_RPM.set_property("can-focus", False)
		self.CPU_FAN_RPM.set_property("halign", Gtk.Align.CENTER)
		self.CPU_FAN_RPM.set_property("valign", Gtk.Align.CENTER)
		self.CPU_FAN_RPM.set_xalign(0.3)
		self.CPU_FAN_RPM.set_property("margin-left", 0)
		self.CPU_FAN_RPM.set_property("margin-right", 10)
		self.CPU_FAN_RPM.set_label("0" if read(config.CPU_GPU_RPM_ADDRESS[0], 2, 0) == 0 else str(478000//read(config.CPU_GPU_RPM_ADDRESS[0], 2, 0)))
		CPU_FAN_RPM_STYLE = self.CPU_FAN_RPM.get_style_context()
		CPU_FAN_RPM_STYLE.add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
		fixed.put(self.CPU_FAN_RPM, 240, 80)
		fixed.add(self.CPU_FAN_RPM)

		self.GPU_CURR_TEMP = Gtk.Label()
		self.GPU_CURR_TEMP.set_property("width-request", 80)
		self.GPU_CURR_TEMP.set_property("height-request", 35)
		self.GPU_CURR_TEMP.set_property("visible", True)
		self.GPU_CURR_TEMP.set_property("can-focus", False)
		self.GPU_CURR_TEMP.set_property("halign", Gtk.Align.CENTER)
		self.GPU_CURR_TEMP.set_property("valign", Gtk.Align.CENTER)
		self.GPU_CURR_TEMP.set_xalign(0.35)
		self.GPU_CURR_TEMP.set_property("margin-left", 0)
		self.GPU_CURR_TEMP.set_property("margin-right", 10)
		self.GPU_CURR_TEMP.set_label(str(read(config.CPU_GPU_TEMP_ADDRESS[1], 1, 0)))
		GPU_CURR_TEMP_STYLE = self.GPU_CURR_TEMP.get_style_context()
		GPU_CURR_TEMP_STYLE.add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
		fixed.put(self.GPU_CURR_TEMP, 60, 110)
		fixed.add(self.GPU_CURR_TEMP)

		self.GPU_MIN_TEMP = Gtk.Label()
		self.GPU_MIN_TEMP.set_property("width-request", 80)
		self.GPU_MIN_TEMP.set_property("height-request", 35)
		self.GPU_MIN_TEMP.set_property("visible", True)
		self.GPU_MIN_TEMP.set_property("can-focus", False)
		self.GPU_MIN_TEMP.set_property("halign", Gtk.Align.CENTER)
		self.GPU_MIN_TEMP.set_property("valign", Gtk.Align.CENTER)
		self.GPU_MIN_TEMP.set_xalign(0.05)
		self.GPU_MIN_TEMP.set_property("margin-left", 0)
		self.GPU_MIN_TEMP.set_property("margin-right", 10)
		GPU_MIN_TEMP_STYLE = self.GPU_MIN_TEMP.get_style_context()
		GPU_MIN_TEMP_STYLE.add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
		fixed.put(self.GPU_MIN_TEMP, 140, 110)
		fixed.add(self.GPU_MIN_TEMP)

		self.GPU_MAX_TEMP = Gtk.Label()
		self.GPU_MAX_TEMP.set_property("width-request", 80)
		self.GPU_MAX_TEMP.set_property("height-request", 35)
		self.GPU_MAX_TEMP.set_property("visible", True)
		self.GPU_MAX_TEMP.set_property("can-focus", False)
		self.GPU_MAX_TEMP.set_property("halign", Gtk.Align.CENTER)
		self.GPU_MAX_TEMP.set_property("valign", Gtk.Align.CENTER)
		self.GPU_MAX_TEMP.set_xalign(0.05)
		self.GPU_MAX_TEMP.set_property("margin-left", 0)
		self.GPU_MAX_TEMP.set_property("margin-right", 10)
		GPU_MAX_TEMP_STYLE = self.GPU_MAX_TEMP.get_style_context()
		GPU_MAX_TEMP_STYLE.add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
		fixed.put(self.GPU_MAX_TEMP, 190, 110)
		fixed.add(self.GPU_MAX_TEMP)

		self.GPU_FAN_RPM = Gtk.Label()
		self.GPU_FAN_RPM.set_property("width-request", 80)
		self.GPU_FAN_RPM.set_property("height-request", 35)
		self.GPU_FAN_RPM.set_property("visible", True)
		self.GPU_FAN_RPM.set_property("can-focus", False)
		self.GPU_FAN_RPM.set_property("halign", Gtk.Align.CENTER)
		self.GPU_FAN_RPM.set_property("valign", Gtk.Align.CENTER)
		self.GPU_FAN_RPM.set_xalign(0.3)
		self.GPU_FAN_RPM.set_property("margin-left", 0)
		self.GPU_FAN_RPM.set_property("margin-right", 10)
		self.GPU_FAN_RPM.set_label("0" if read(config.CPU_GPU_RPM_ADDRESS[1], 2, 0) == 0 else str(478000//read(config.CPU_GPU_RPM_ADDRESS[1], 2, 0)))
		GPU_FAN_RPM_STYLE = self.GPU_FAN_RPM.get_style_context()
		GPU_FAN_RPM_STYLE.add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
		fixed.put(self.GPU_FAN_RPM, 240, 110)
		fixed.add(self.GPU_FAN_RPM)

		timer_id = GLib.timeout_add(500, update_label)

		label_maker("Battery charge threshold", 10, 150, 0.0, fixed)                                                                 # Fan Profile

		bct_selector = Gtk.ComboBox()
		bct_list = Gtk.ListStore(str)
		for bct_values in range (50, 101, 5):
			bct_list.append([str(bct_values)])
		bct_selector.set_model(bct_list)
		bct_renderer = Gtk.CellRendererText()
		bct_selector.pack_start(bct_renderer, True)
		bct_selector.add_attribute(bct_renderer, "text", 0)
		model = bct_selector.get_model()
		for index, row in enumerate(model):
			if row[0] == str(config.BATTERY_THRESHOLD_VALUE):
				bct_selector.set_active(index)
				break
		bct_selector.connect("changed", bct_selection)
		bct_selector.set_property("width-request", 80)
		bct_selector.set_property("height-request", 35)
		fixed.put(bct_selector, 200, 150)
		fixed.add(bct_selector)

parent_window = ParentWindow()
parent_window.connect("destroy", Gtk.main_quit)
parent_window.show_all()
Gtk.main()

