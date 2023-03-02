import subprocess

def install_lib(option, option_1, option_2 = " "):
    if option == 1: subprocess.check_call(["pip", "install", option_1])
    else: subprocess.check_call(["pip", "install", option_1, option_2])

subprocess.check_call(["sudo", "apt", "install", "python3-pip", "-y"])

try:
   import psutil
except (ImportError, ModuleNotFoundError):
   print ("Error, Module psutil is required")
   install_lib(1, "psutil")
   import psutil

try:
   import gi.repository
except (ImportError, ModuleNotFoundError):
   print ("Error, Module gir1.2-appindicator3-0.1 is required")
   install_lib(2, "gir1.2-appindicator3-0.1", "-y")
   import gi.repository

try:
   import signal
except (ImportError, ModuleNotFoundError):
   print ("Error, Module signal is required")
   install_lib(2, "signal", "-y")
   import signal

try:
   import webbrowser
except (ImportError, ModuleNotFoundError):
   print ("Error, Module webbrowser is required")
   install_lib(2, "webbrowser", "-y")
   import webbrowser

try:
   import fileinput
except (ImportError, ModuleNotFoundError):
   print ("Error, Module fileinput is required")
   install_lib(2, "fileinput", "-y")
   import fileinput

try:
   import threading
except (ImportError, ModuleNotFoundError):
   print ("Error, Module threading is required")
   install_lib(2, "threading", "-y")
   import threading

try:
   import os
except (ImportError, ModuleNotFoundError):
   print ("Error, Module os is required")
   install_lib(2, "os", "-y")
   import os