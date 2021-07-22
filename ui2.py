#!/usr/bin/env python3
import traceback
import sys
import os

import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk, THEMES
from tkinter import messagebox

from concurrent import futures
import time

import pandas as pd
import datetime
from pandas._config import config

import configurator
import controller
import driver

# Modes
# MODE_AUTO = 0
# MODE_BASIC = 1
# MODE_ADVANCED = 2
# MODE_COOLERBOOST = 3

list_fan_modes = {
    "Automatic Mode" : 0,
    "Basic Mode" : 1,
    "Advance Mode" : 2,
    "Cooler Boost Mode" : 3
}

thread_pool_executor = futures.ThreadPoolExecutor(max_workers=1)


class AppUI:
    def __init__(self, root):
        self.root = root

        # Get config
        self.config = configurator.get_config()

        # Log dataframe
        self.df_stats = pd.DataFrame()

        ## window property
        self.root.title("Open Freeze Center")
        self.root.set_theme(self.config["ui"]["theme"])
        self.root.resizable(width=False, height=False)
        self.root.geometry("665x400")

        # gives weight to the cells in the grid
        self.rows = 0
        while self.rows < 10:
            self.root.rowconfigure(self.rows, weight=1)
            self.rows += 1

        self.column = 0
        while self.column < 5:
            self.root.columnconfigure(self.column, weight=1)
            self.column += 1

        # Defines and places the notebook widget
        self.nb = ttk.Notebook(self.root)
        self.nb.grid(row=0, column=0, columnspan=5, rowspan=10, sticky='NESW')

        # Adds tabs
        self.tab_overview = ttk.Frame(self.nb)
        self.nb.add(self.tab_overview, text='Overview')

        # Adds tabs
        self.tab_moniter = ttk.Frame(self.nb)
        self.nb.add(self.tab_moniter, text='Moniter')

        # Adds tabs
        self.tab_settings = ttk.Frame(self.nb)
        self.nb.add(self.tab_settings, text='Settings')

        # Adds tabs
        self.tab_about = ttk.Frame(self.nb)
        self.nb.add(self.tab_about, text='About')

        # tab overview widgets

        ## fan mode widgets
        self.label_fan_mode = ttk.Label(
            self.tab_overview,
            text="Current Fan Mode",
            font=("Arial", 15, "bold")
        )
        self.label_fan_mode.grid(
            column=0,
            row=0,
            padx=50,
            pady=(50, 3),
            columnspan=2,
            sticky='NESW'
        )

        self.opt_fan_mode_var = tk.StringVar()
        self.current_fan_mode = self.get_key(self.config["settings"]["mode"])
        self.opt_fan_mode_var.set(self.current_fan_mode)
        self.opt_fan_mode_list = list(list_fan_modes.keys())

        self.opt_fan_mode = ttk.OptionMenu(
            self.tab_overview,
            self.opt_fan_mode_var,
            self.current_fan_mode,
            *self.opt_fan_mode_list
        )
        self.opt_fan_mode.grid(
            column=1,
            row=0,
            padx=5,
            pady=(50, 3),
            columnspan=2,
            sticky='NESW'
        )

        ## battery charging threshold widget
        self.label_charging_threshold = ttk.Label(
            self.tab_overview,
            text="Charging Threshold",
            font=("Arial", 15, "bold")
        )
        self.label_charging_threshold.grid(
            column=0,
            row=1,
            padx=50,
            pady=(15, 30),
            sticky = tk.W
        )

        self.sp_charging_threshold_var = tk.IntVar()
        self.config_charging_threshold = self.config["settings"]["battery_threshold"]
        self.sp_charging_threshold_var.set(self.config_charging_threshold)

        self.sp_charging_threshold = ttk.Spinbox(
            self.tab_overview,
            from_=20,
            to=100,
            increment=1,
            textvariable=self.sp_charging_threshold_var,
            validate='all',
            validatecommand=self.validate_input
        )
        self.sp_charging_threshold.grid(
            column=1,
            row=1,
            columnspan=2,
            padx=20,
            pady=(15, 30)
        )

        self.btn_set = ttk.Button(
            self.tab_overview,
            text="Save Setting and Apply",
            command = self.save_setting_and_apply
        )
        self.btn_set.grid(
            column=0,
            row=4,
            columnspan=5,
            padx=50,
            pady=(15, 30)
        )


        # tab moniter

        self.label_current = ttk.Label(
            self.tab_moniter,
            text="Current",
            font=("Arial", 13, "bold")
        )
        self.label_current.grid(
            column=1,
            row=0,
            padx=50,
            pady=(15, 30)
        )

        self.label_min = ttk.Label(
            self.tab_moniter,
            text="Min",
            font=("Arial", 13, "bold")
        )
        self.label_min.grid(
            column=2,
            row=0,
            padx=50,
            pady=(15, 30)
        )

        self.label_max = ttk.Label(
            self.tab_moniter,
            text="Max",
            font=("Arial", 13, "bold")
        )
        self.label_max.grid(
            column=3,
            row=0,
            padx=50,
            pady=(15, 30)
        )

        self.label_cpu_temp = ttk.Label(
            self.tab_moniter,
            text="CPU Temp",
            font=("Arial", 13, "bold")
        )
        self.label_cpu_temp.grid(
            column=0,
            row=1,
            padx=20,
            pady=(15, 30)
        )

        self.label_gpu_temp = ttk.Label(
            self.tab_moniter,
            text="GPU Temp",
            font=("Arial", 13, "bold")
        )
        self.label_gpu_temp.grid(
            column=0,
            row=2,
            padx=20,
            pady=(15, 30)
        )

        self.label_cpu_fan_rpm = ttk.Label(
            self.tab_moniter,
            text="CPU Fan RPM",
            font=("Arial", 13, "bold")
        )
        self.label_cpu_fan_rpm.grid(
            column=0,
            row=3,
            padx=20,
            pady=(15, 30)
        )

        self.label_gpu_fan_rpm = ttk.Label(
            self.tab_moniter,
            text="GPU Fan RPM",
            font=("Arial", 13, "bold")
        )
        self.label_gpu_fan_rpm.grid(
            column=0,
            row=4,
            padx=20,
            pady=(15, 30)
        )

        ## monitering labels

        ### CPU temp
        self.label_cpu_temp_cur_var = tk.IntVar()
        self.label_cpu_temp_cur_var.set(0)
        self.label_cpu_temp_cur = ttk.Label(
            self.tab_moniter,
            font=("Arial", 13, "bold"),
            textvariable=self.label_cpu_temp_cur_var
        )
        self.label_cpu_temp_cur.grid(
            column=1,
            row=1,
            padx=50,
            pady=(15, 30)
        )

        self.label_cpu_temp_min_var = tk.IntVar()
        self.label_cpu_temp_min_var.set(0)
        self.label_cpu_temp_min = ttk.Label(
            self.tab_moniter,
            font=("Arial", 13, "bold"),
            textvariable=self.label_cpu_temp_min_var
        )
        self.label_cpu_temp_min.grid(
            column=2,
            row=1,
            padx=50,
            pady=(15, 30)
        )

        self.label_cpu_temp_max_var = tk.IntVar()
        self.label_cpu_temp_max_var.set(0)
        self.label_cpu_temp_max = ttk.Label(
            self.tab_moniter,
            font=("Arial", 13, "bold"),
            textvariable=self.label_cpu_temp_max_var
        )
        self.label_cpu_temp_max.grid(
            column=3,
            row=1,
            padx=50,
            pady=(15, 30)
        )

        ### GPU temp
        self.label_gpu_temp_cur_var = tk.IntVar()
        self.label_gpu_temp_cur_var.set(0)
        self.label_gpu_temp_cur = ttk.Label(
            self.tab_moniter,
            font=("Arial", 13, "bold"),
            textvariable=self.label_gpu_temp_cur_var
        )
        self.label_gpu_temp_cur.grid(
            column=1,
            row=2,
            padx=50,
            pady=(15, 30)
        )

        self.label_gpu_temp_min_var = tk.IntVar()
        self.label_gpu_temp_min_var.set(0)
        self.label_gpu_temp_min = ttk.Label(
            self.tab_moniter,
            font=("Arial", 13, "bold"),
            textvariable=self.label_gpu_temp_min_var
        )
        self.label_gpu_temp_min.grid(
            column=2,
            row=2,
            padx=50,
            pady=(15, 30)
        )

        self.label_gpu_temp_max_var = tk.IntVar()
        self.label_gpu_temp_max_var.set(0)
        self.label_gpu_temp_max = ttk.Label(
            self.tab_moniter,
            font=("Arial", 13, "bold"),
            textvariable=self.label_gpu_temp_max_var
        )
        self.label_gpu_temp_max.grid(
            column=3,
            row=2,
            padx=50,
            pady=(15, 30)
        )


        ### CPU Fan
        self.label_cpu_fan_rpm_cur_var = tk.IntVar()
        self.label_cpu_fan_rpm_cur_var.set(0)
        self.label_cpu_fan_rpm_cur = ttk.Label(
            self.tab_moniter,
            font=("Arial", 13, "bold"),
            textvariable=self.label_cpu_fan_rpm_cur_var
        )
        self.label_cpu_fan_rpm_cur.grid(
            column=1,
            row=3,
            padx=50,
            pady=(15, 30)
        )

        self.label_cpu_fan_rpm_min_var = tk.IntVar()
        self.label_cpu_fan_rpm_min_var.set(0)
        self.label_cpu_fan_rpm_min = ttk.Label(
            self.tab_moniter,
            font=("Arial", 13, "bold"),
            textvariable=self.label_cpu_fan_rpm_min_var
        )
        self.label_cpu_fan_rpm_min.grid(
            column=2,
            row=3,
            padx=50,
            pady=(15, 30)
        )

        self.label_cpu_fan_rpm_max_var = tk.IntVar()
        self.label_cpu_fan_rpm_max_var.set(0)
        self.label_cpu_fan_rpm_max = ttk.Label(
            self.tab_moniter,
            font=("Arial", 13, "bold"),
            textvariable=self.label_cpu_fan_rpm_max_var
        )
        self.label_cpu_fan_rpm_max.grid(
            column=3,
            row=3,
            padx=50,
            pady=(15, 30)
        )

        ### GPU Fan
        self.label_gpu_fan_rpm_cur_var = tk.IntVar()
        self.label_gpu_fan_rpm_cur_var.set(0)
        self.label_gpu_fan_rpm_cur = ttk.Label(
            self.tab_moniter,
            font=("Arial", 13, "bold"),
            textvariable=self.label_gpu_fan_rpm_cur_var
        )
        self.label_gpu_fan_rpm_cur.grid(
            column=1,
            row=4,
            padx=50,
            pady=(15, 30)
        )

        self.label_gpu_fan_rpm_min_var = tk.IntVar()
        self.label_gpu_fan_rpm_min_var.set(0)
        self.label_gpu_fan_rpm_min = ttk.Label(
            self.tab_moniter,
            font=("Arial", 13, "bold"),
            textvariable=self.label_gpu_fan_rpm_min_var
        )
        self.label_gpu_fan_rpm_min.grid(
            column=2,
            row=4,
            padx=50,
            pady=(15, 30)
        )

        self.label_gpu_fan_rpm_max_var = tk.IntVar()
        self.label_gpu_fan_rpm_max_var.set(0)
        self.label_gpu_fan_rpm_max = ttk.Label(
            self.tab_moniter,
            font=("Arial", 13, "bold"),
            textvariable=self.label_gpu_fan_rpm_max_var
        )
        self.label_gpu_fan_rpm_max.grid(
            column=3,
            row=4,
            padx=50,
            pady=(15, 30)
        )

        # tab Settings widgets

        ## themes
        self.label_theme = ttk.Label(
            self.tab_settings,
            text="Current theme",
            font=("Arial", 15, "bold")
        )
        self.label_theme.grid(
            column=0,
            row=0,
            pady=(50, 30),
            columnspan=2,
        )

        self.opt_themes_var = tk.StringVar()
        self.opt_themes_var.set(self.config["ui"]["theme"])
        self.themes = THEMES

        self.opt_themes = ttk.OptionMenu(
            self.tab_settings,
            self.opt_themes_var,
            self.config["ui"]["theme"],
            *self.themes,
            command = self.theme_change
        )
        self.opt_themes.grid(
            column=2,
            row=0,
            padx=5,
            pady=(50, 30),
            columnspan=2,
            sticky='NESW'
        )

        ## module installation
        self.btn_instal_var = tk.StringVar()

        # if driver.is_installed():
        if True:
            self.btn_instal_var.set("Uninstall Modules")
        else:
            self.btn_instal_var.set("Install Modules")

        self.btn_install = ttk.Button(
            self.tab_settings,
            text="Save Setting and Apply",
            textvariable=self.btn_instal_var,
            command=self.button_install_command
        )
        self.btn_install.grid(
            column=0,
            row=1,
            columnspan=5,
            padx=270,
            pady=(50, 30),
            sticky=tk.NSEW

        )

        # tab about
        self.credit = "Creator(s): -> Aditya Kumar Bajpai\nRob Oudendijk\nLiam Lalonde\nSangram Singha"
        self.label_about = tk.Label(
            self.tab_about,
            text=self.credit
        )
        self.label_about.grid(
            pady=100
        )

        self.label_about.pack(fill=tk.BOTH, expand=True)


        self.updater()

        ## window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def is_root(self):
        return (os.geteuid() == 0)

    def updater(self):
        thread_pool_executor.submit(self.update_stats)

    # blocking code
    def update_stats(self):

        if not self.is_root():
            return

        stats = controller.get_stats()

        # Log stats to pandas
        stats["DATE"] = pd.to_datetime("now")
        self.df_stats = self.df_stats.append(stats, ignore_index=True)

        self.label_cpu_temp_cur_var.set(stats["CPU_TEMP"])
        self.label_cpu_temp_min_var.set(self.df_stats["CPU_TEMP"].min())
        self.label_cpu_temp_max_var.set(self.df_stats["CPU_TEMP"].max())

        self.label_gpu_temp_cur_var.set(stats["GPU_TEMP"])
        self.label_gpu_temp_min_var.set(self.df_stats["GPU_TEMP"].min())
        self.label_gpu_temp_max_var.set(self.df_stats["GPU_TEMP"].max())

        self.label_cpu_fan_rpm_cur_var.set(stats["CPU_RPM"])
        self.label_cpu_fan_rpm_min_var.set(self.df_stats["CPU_RPM"].min())
        self.label_cpu_fan_rpm_max_var.set(self.df_stats["CPU_RPM"].max())

        self.label_gpu_fan_rpm_cur_var.set(stats["GPU_RPM"])
        self.label_gpu_fan_rpm_min_var.set(self.df_stats["GPU_RPM"].min())
        self.label_gpu_fan_rpm_max_var.set(self.df_stats["GPU_RPM"].max())

        self.updater()



    def theme_change(self, value):
        self.root.set_theme(value)
        if self.config["ui"]["theme"] != value:
            self.config["ui"]["theme"] = value
            configurator.write_config(self.config)

    def button_install_command(self):

        if not self.is_root():
            messagebox.showinfo(
                "Operation Failed",
                "Sudo privilege needed for this operation",
            )

            return

        else:

            if driver.is_installed():
                res = driver.install()
                if res == True:
                    messagebox.showinfo(
                        "Installation Complete!",
                        "Please Reboot your system to enable EC module write capablities of script",
                    )
                    self.btn_instal_var.set("Uninstall Modules")
                else:
                    messagebox.showinfo(
                        "Installation Failure!",
                        "Please check the logs for more information",
                    )
            else:
                res = driver.uninstall()
                if res == True:
                    messagebox.showinfo(
                        "Uninstallation Complete!",
                        "Please Reboot your system to disable EC module write capablities of script",
                    )
                    self.btn_instal_var.set("Install Modules")
                else:
                    messagebox.showinfo(
                        "Uninstallation Failure!",
                        "Please check the logs for more information",
                    )

    def validate_input(self):
        self.battery_threshold = self.sp_charging_threshold_var.get()
        return (self.battery_threshold >= 20 and self.battery_threshold <= 100)


    def save_setting_and_apply(self):

        if not self.is_root():
            messagebox.showinfo(
                "Operation Failed",
                "Sudo privilege needed for this operation",
            )
            return

        self.fan_mode = list_fan_modes[self.opt_fan_mode_var.get()]
        self.fan_mode_changed = (self.config["settings"]["mode"] != self.fan_mode)

        self.battery_threshold = self.sp_charging_threshold_var.get()
        self.battery_threshold_changed = (
            self.config["settings"]["battery_threshold"] != self.battery_threshold
        )
        self.battery_threshold_changed = self.battery_threshold_changed and (
            self.battery_threshold >= 20 and self.battery_threshold <= 100
        )

        if self.fan_mode_changed:
            self.config["settings"]["mode"] = self.fan_mode

        if self.battery_threshold_changed:
            self.config["settings"]["battery_threshold"] = self.battery_threshold


        if self.fan_mode_changed or self.battery_threshold_changed:

            if self.fan_mode_changed:

                mode = self.config["settings"]["mode"]
                vr = self.config["settings"]["vr_custom"]
                offset = self.config["settings"]["offset"]

                controller.enable_mode(mode, vr, offset)

            if self.battery_threshold_changed:
                battery_threshold = self.config["settings"]["battery_threshold"]

                controller.change_battery_threshold(battery_threshold)

            configurator.write_config(self.config)




    def get_key(self, val):
        for key, value in list_fan_modes.items():
            if val == value:
                return key

        return 0

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()


def format_stacktrace():
    parts = ["Traceback (most recent call last):\n"]
    parts.extend(traceback.format_stack(limit=25)[:-2])
    parts.extend(traceback.format_exception(*sys.exc_info())[1:])
    return "".join(parts)


def open_ui():
    try:
        root = ThemedTk(themebg=True)
        app = AppUI(root)
        root.mainloop()
    except Exception as e:
        stacktrace = format_stacktrace()
        print(stacktrace)

if __name__ == "__main__":
    open_ui()
