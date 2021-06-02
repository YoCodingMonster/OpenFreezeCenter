#!/usr/bin/env python3

# Handles loading, and creating configuarion files

import toml
import os
import sys

CONFIG_PATH = os.path.expanduser("~") + "/.config/OpenFreezeCenter"
CONFIG_FILE = "config.toml"


def write_default_config():

    user_config_dir = CONFIG_PATH
    user_config = user_config_dir + "/" + CONFIG_FILE

    # Settings is just a nested dict - like a json
    config = {"settings": dict(), "ui": dict()}

    os.makedirs(user_config_dir, exist_ok=True)

    config["settings"]["mode"] = 0
    config["settings"]["offset"] = 0
    config["settings"]["vr_custom"] = [
        13,
        45,
        50,
        60,
        72,
        80,
        85,
        100,
        0,
        50,
        60,
        72,
        80,
        85,
        100,
    ]

    config["ui"]["dark_mode_enabled"] = False
    config["ui"]["update_freq"] = 10

    # Not sure what this is but it was in the first config file on line 2
    config["settings"]["four"] = 4

    write_config(config)


def get_config():

    user_config_dir = CONFIG_PATH
    user_config = user_config_dir + "/" + CONFIG_FILE

    if not os.path.isfile(user_config):
        write_default_config()

    config = toml.load(user_config)

    return config


def write_config(config):
    user_config_dir = CONFIG_PATH
    user_config = user_config_dir + "/" + CONFIG_FILE

    with open(user_config, "w") as f:
        toml.dump(config, f)
    f.close()
