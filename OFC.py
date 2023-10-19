#! /usr/bin/python3

import os
import ECTweaker as ECT
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

# CPU_FAN_PROFILE_BYTE                  VALUES[0][0]   BYTE ADDRESS              FAN PROFILES BYTE AND VALUES
# CPU_FAN_PROFILE_VALUE_AUTO            VALUES[0][1]   VALUE
# CPU_FAN_PROFILE_VALUE_ADVANCED        VALUES[0][2]   VALUE
# CPU_COOLER_BOOSTER_BYTE               VALUES[1][0]   BYTE ADDRESS              COOLER BOOSTER BYTE AND VALUES
# CPU_COOLER_BOOSTER_VALUE              VALUES[1][1]   VALUE [off]
# CPU_COOLER_BOOSTER_VALUE              VALUES[1][2]   VALUE [on]

# CPU_FAN_SPEED_1_BYTE                  VALUES[2][0]   BYTE ADDRESS              CPU FAN SPEEDS ADDRESS
# CPU_FAN_SPEED_2_BYTE                  VALUES[2][1]   BYTE ADDRESS
# CPU_FAN_SPEED_3_BYTE                  VALUES[2][2]   BYTE ADDRESS
# CPU_FAN_SPEED_4_BYTE                  VALUES[2][3]   BYTE ADDRESS
# CPU_FAN_SPEED_5_BYTE                  VALUES[2][4]   BYTE ADDRESS
# CPU_FAN_SPEED_6_BYTE                  VALUES[2][5]   BYTE ADDRESS
# CPU_FAN_SPEED_7_BYTE                  VALUES[2][6]   BYTE ADDRESS
# GPU_FAN_SPEED_1_BYTE                  VALUES[3][0]   BYTE ADDRESS              GPU FAN SPEEDS ADDRESS
# GPU_FAN_SPEED_2_BYTE                  VALUES[3][1]   BYTE ADDRESS
# GPU_FAN_SPEED_3_BYTE                  VALUES[3][2]   BYTE ADDRESS
# GPU_FAN_SPEED_4_BYTE                  VALUES[3][3]   BYTE ADDRESS
# GPU_FAN_SPEED_5_BYTE                  VALUES[3][4]   BYTE ADDRESS
# GPU_FAN_SPEED_6_BYTE                  VALUES[3][5]   BYTE ADDRESS
# GPU_FAN_SPEED_7_BYTE                  VALUES[3][6]   BYTE ADDRESS

# AUTO_FAN_SPEEDS_VENDOR_VALUES         VALUES[4][]    BYTE ADDRESS              AUTO FAN SPEEDS
# ADVANCED_FAN_SPEEDS_VENDOR_VALUES     VALUES[5][]    BYTE ADDRESS              ADVANCED FAN SPEEDS

# CPU_TEMPERATURE_BYTE                  VALUES[6][0]   BYTE ADDRESS              CURRENT TEMPERATURE AND RPM ADDRESSES
# CPU_FAN_RPM_BYTE                      VALUES[6][1]   BYTE ADDRESS
# GPU_TEMPERATURE_BYTE                  VALUES[6][3]   BYTE ADDRESS
# GPU_FAN_RPM_BYTE                      VALUES[6][4]   BYTE ADDRESS

AUTO_SPEED = []
VALUES = []
LABELS = []
MIN_MAX = [100, 0, 100, 0]

LINE_UP = '\033[1A'
LINE_CLEAR = '\x1b[2K'

def create_dialog(TITLE, TEXT, LINE_YES, LINE_NO, x, y):
	dialog = Gtk.Dialog(title = TITLE)
	dialog.set_default_size(x, y)
	dialog.add_button("Yes", Gtk.ResponseType.YES)
	dialog.add_button("No", Gtk.ResponseType.NO)
	label = Gtk.Label(TEXT)
	dialog.vbox.add(label)
	label.show()

	response = dialog.run()
	if response == Gtk.ResponseType.YES: LINE = LINE_YES
	elif response == Gtk.ResponseType.NO: LINE = LINE_NO

	dialog.show_all()
	dialog.destroy()
	return LINE

################################################################
# Setting the config.py file where all the data will be stored #
################################################################

CHECK = ECT.check()
if CHECK != 1:
	PATH_TO_CONFIG = str(os.path.realpath(os.path.dirname(__file__))) + "/config.py"
	try:
		CONFIG_FILE = open(PATH_TO_CONFIG, "r")
	except FileNotFoundError:
		CONFIG = []
		CHOICE = "\nIf you want universal auto fan profile whihc is as below then [SELECT YES]\n\tAUTO SPEEDS = [0, 40, 48, 56, 64, 72, 80, 0, 48, 56, 64, 72, 79, 86]\n\nIf you want to fetch vendor specified auto fan profile which will require you to \n\t1 :- Close this(Before closing read all the steps)\n\t2 :- boot into windows\n\t3 :- set the fan profile to auto\n\t4 :- boot back to linux and then [SELECT NO]"
		LINE_YES = "AUTO_SPEED = [0, 40, 48, 56, 64, 72, 80, 0, 48, 56, 64, 72, 79, 86]"
		AUTO_SPEED_CPU = [ECT.read(0x72, 1), ECT.read(0x73, 1), ECT.read(0x74, 1), ECT.read(0x75, 1), ECT.read(0x76, 1), ECT.read(0x77, 1), ECT.read(0x78, 1)] # CPU FAN speed at LOWEST, LOWER, LOW, MEDIUM, HIGH, HIGHER, HIGHEST CPU TEMP
		AUTO_SPEED_GPU = [ECT.read(0x8a, 1), ECT.read(0x8b, 1), ECT.read(0x8c, 1), ECT.read(0x8d, 1), ECT.read(0x8e, 1), ECT.read(0x8f, 1), ECT.read(0x90, 1)] # GPU FAN speed at LOWEST, LOWER, LOW, MEDIUM, HIGH, HIGHER, HIGHEST GPU TEMP
		AUTO_SPEED = AUTO_SPEED_CPU + AUTO_SPEED_GPU
		LINE_NO = "AUTO_SPEED = ["+str(AUTO_SPEED[0])+", "+str(AUTO_SPEED[1])+", "+str(AUTO_SPEED[2])+", "+str(AUTO_SPEED[3])+", "+str(AUTO_SPEED[4])+", "+str(AUTO_SPEED[5])+", "+str(AUTO_SPEED[6])+", "+str(AUTO_SPEED[7])+", "+str(AUTO_SPEED[8])+", "+str(AUTO_SPEED[9])+", "+str(AUTO_SPEED[10])+", "+str(AUTO_SPEED[11])+", "+str(AUTO_SPEED[12])+", "+str(AUTO_SPEED[13])+"]"
		CONFIG.append(create_dialog("Auto Profile Selection", CHOICE, LINE_YES, LINE_NO, 300, 150))

		CHOICE = "\nIs your CPU intel 10th Gen and above\n"
		LINE_YES = "\nCPU = 1\nVALUES = [[0xd4, 13, 141],\n[0x98, 2, 130],\n[0x72, 0x73, 0x74, 0x75, 0x76, 0x77, 0x78],\n[0x8a, 0x8b, 0x8c, 0x8d, 0x8e, 0x8f, 0x90],\nAUTO_SPEED,\n[0, 50, 75, 100, 125, 150, 150, 0, 50, 75, 100, 125, 150, 150],\t\t# Edit this list for ADVANCED FAN SPEEDS with  refrence [CPU1, CPU2, CPU3, CPU4, CPU5, CPU6, CPU7, GPU1, GPU2, GPU3, GPU4, GPU5, GPU6, GPU7]\n[0x71, 0xc8, 0x80, 0xca]]"
		LINE_NO  = "\nCPU = 0\nVALUES = [[0xf4, 12, 140],\n[0x98, 0, 128],\n[0x72, 0x73, 0x74, 0x75, 0x76, 0x77, 0x78],\n[0x8a, 0x8b, 0x8c, 0x8d, 0x8e, 0x8f, 0x90],\nAUTO_SPEED,\n[0, 50, 75, 100, 125, 150, 150, 0, 50, 75, 100, 125, 150, 150],\t\t# Edit this list for ADVANCED FAN SPEEDS with  refrence [CPU1, CPU2, CPU3, CPU4, CPU5, CPU6, CPU7, GPU1, GPU2, GPU3, GPU4, GPU5, GPU6, GPU7]\n[0x71, 0xc8, 0x80, 0xca]]"
		CONFIG.append(create_dialog("CPU Gen Selection", CHOICE, LINE_YES, LINE_NO, 300, 50))

		CONFIG_FILE = open(PATH_TO_CONFIG, "w")
		CONFIG_FILE.writelines(CONFIG)
		CONFIG_FILE.close()
	finally:
		import config
		AUTO_SPEED = config.AUTO_SPEED
		VALUES = config.VALUES
else:
	os.system("shutdown -r +1")
	print("Rebooting system within 1 min!\nPlease save all work before it happens!")

#############################################
# Below functions are part of GUI designing #
#############################################

def profile_selection(combobox):
	model = combobox.get_model()
	active_iter = combobox.get_active_iter()
	profile = model[active_iter][0]
	if profile == "Auto": ECT.fan_profile("auto", VALUES)
	elif profile == "Advanced": ECT.fan_profile("advanced", VALUES)
	elif profile == "Cooler Booster": ECT.fan_profile("cooler booster", VALUES)

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
	LABEL.set_property("label", text)
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
	LABELS.append(LABEL)

def update_label():
	CPU_TEMP = ECT.read(VALUES[6][0], 1)
	GPU_TEMP = ECT.read(VALUES[6][2], 1)
	try:
		CPU_FAN_RPM = 478000//ECT.read(VALUES[6][1], 2)
	except ZeroDivisionError:
		CPU_FAN_RPM = 0
	try:
		GPU_FAN_RPM = 478000//ECT.read(VALUES[6][3], 2)
	except ZeroDivisionError:
		GPU_FAN_RPM = 0

	LABELS[7].set_text(str(CPU_TEMP))
	if MIN_MAX[0] > CPU_TEMP:
		MIN_MAX[0] = CPU_TEMP
	if MIN_MAX[1] < CPU_TEMP:
		MIN_MAX[1] = CPU_TEMP
	LABELS[8].set_text(str(MIN_MAX[0]))
	LABELS[9].set_text(str(MIN_MAX[1]))

	LABELS[10].set_text(str(GPU_TEMP))
	if MIN_MAX[2] > GPU_TEMP:
		MIN_MAX[2] = GPU_TEMP
	if MIN_MAX[3] < GPU_TEMP:
		MIN_MAX[3] = GPU_TEMP
	LABELS[11].set_text(str(MIN_MAX[2]))
	LABELS[12].set_text(str(MIN_MAX[3]))

	LABELS[13].set_text(str(CPU_FAN_RPM))
	LABELS[14].set_text(str(GPU_FAN_RPM))
	return True

class ParentWindow(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self, title = "Open Freeze Center (OFC)")
		self.set_default_size(300, 150)
		fixed = Gtk.Fixed()
		self.add(fixed)

		if ECT.read(VALUES[1][0], 1) == VALUES[1][1]:
			if ECT.read(VALUES[0][0], 1) == VALUES[0][1]: row = 0
			if ECT.read(VALUES[0][0], 1) == VALUES[0][2]: row = 1
		else: row = 2

		profile_selector = Gtk.ComboBox()
		profile_list = Gtk.ListStore(str)
		profile_list.append(["Auto"])
		profile_list.append(["Advanced"])
		profile_list.append(["Cooler Booster"])
		profile_selector.set_model(profile_list)
		cell_renderer = Gtk.CellRendererText()
		profile_selector.pack_start(cell_renderer, True)
		profile_selector.add_attribute(cell_renderer, "text", 0)
		profile_selector.set_active(row)
		profile_selector.connect("changed", profile_selection)
		profile_selector.set_property("width-request", 80)
		profile_selector.set_property("height-request", 35)
		fixed.put(profile_selector, 160, 10)
		fixed.add(profile_selector)

		label_maker("Select a fan profile", 10, 10, 0.0, fixed)                                                                 # Fan Profile
		label_maker("CURRENT", 60, 50, 0.0, fixed)                                                                              # Current
		label_maker("MIN", 140, 50, 0.0, fixed)                                                                                 # Minimum
		label_maker("MAX", 190, 50, 0.0, fixed)                                                                                 # Maximum
		label_maker("FAN RPM", 240, 50, 0.0, fixed)                                                                             # Fan RPM
		label_maker("CPU", 10, 80, 0.0, fixed)                                                                                  # CPU
		label_maker("GPU", 10, 110, 0.0, fixed)                                                                                 # GPU
		label_maker(str(ECT.read(VALUES[6][0], 1)), 60, 80, 0.35, fixed)                                                        # CPU Temperature (Current)
		label_maker("", 140, 80, 0.05, fixed)                                                                                   # CPU Temperature (Min)
		label_maker("", 190, 80, 0.05, fixed)                                                                                   # CPU Temperature (Max)
		label_maker(str(ECT.read(VALUES[6][2], 1)), 60, 110, 0.35, fixed)                                                       # GPU Temperature (Current)
		label_maker("", 140, 110, 0.05, fixed)                                                                                  # GPU Temperature (Min)
		label_maker("", 190, 110, 0.05, fixed)                                                                                  # GPU Temperature (Max)
		label_maker("" if ECT.read(VALUES[6][1], 2) == 0 else str(478000//ECT.read(VALUES[6][1], 2)), 240, 80, 0.3, fixed)      # CPU Fan RPM
		label_maker("" if ECT.read(VALUES[6][3], 2) == 0 else str(478000//ECT.read(VALUES[6][3], 2)), 240, 110, 0.3, fixed)     # GPU Fan RPM

		timer_id = GLib.timeout_add(500, update_label)

parent_window = ParentWindow()
parent_window.connect("destroy", Gtk.main_quit)
parent_window.show_all()
Gtk.main()