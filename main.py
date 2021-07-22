#!/usr/bin/env python3

# For controlling via the command line
# Example usage:
#       main.py --mode 0

import sys
import os
import argparse

import subprocess
import controller
import configurator
from getpass import getpass

# May want cli only
try:
    import ui2
except ImportError:
    pass

import driver


def main():
    # get values from command line if given
    argparser = argparse.ArgumentParser(
        description="MSI Open Freeze Center",
        epilog="Controls fan speed and battery threshold profiles",
    )
    argparser.add_argument(
        "-m",
        "--mode",
        action="store",
        default=None,
        type=int,
        help="The fan profile mode to use. 0 for Auto, 1 for Basic, 2 for Advanced, and 3 for COOLER BOOST.",
    )
    argparser.add_argument(
        "-g",
        "--gui",
        action="store_true",
        default=False,
        help="To launch the GUI.",
    )
    argparser.add_argument(
        "-s",
        "--stats",
        action="store_true",
        default=False,
        help="Standard outs the stats",
    )
    argparser.add_argument(
        "-b",
        "--battery",
        action="store",
        default=None,
        type=int,
        help="Set charging threshold between 20 and 100",
    )
    args = argparser.parse_args(sys.argv[1:])

    # If requesting to launch the gui, do nothing else
    if args.gui:
        ui2.open_ui()
        return

    if args.stats:
        stats = controller.get_stats()
        print(stats)
        return

    # Get the settings from file. If not mode is specified whatever is in this file will be used.
    config = configurator.get_config()

    if args.battery == None:
        controller.change_battery_threshold(
            config["settings"]["battery_threshold"]
        )
    else:
        if args.battery < 20 or args.battery > 100:
            print("Set battery threshold between 20 and 100")
        else:
            controller.change_battery_threshold(
                args.battery
            )
            config["settings"]["battery_threshold"] = args.battery
            configurator.write_config(config)

    if args.mode == None:
        controller.enable_mode(
            mode=config["settings"]["mode"],
            vr=config["settings"]["vr_custom"],
            offset=config["settings"]["offset"],
        )
        configurator.write_config(config)
    else:
        if args.mode < 0 or args.mode > 3:
            print("The fan profile mode to use. 0 for Auto, 1 for Basic, 2 for Advanced, and 3 for COOLER BOOST.")
        else:
            controller.enable_mode(
                mode=args.mode,
                vr=config["settings"]["vr_custom"],
                offset=config["settings"]["offset"],
            )
            config["settings"]["mode"] = args.mode
            configurator.write_config(config)


def is_root():
    return os.geteuid() == 0

def test_sudo(pwd=""):
    args = "sudo -S echo OK".split()
    kwargs = dict(stdout=subprocess.PIPE,
                  encoding="ascii")
    if pwd:
        kwargs.update(input=pwd)
    cmd = subprocess.run(args, **kwargs)
    return ("OK" in cmd.stdout)


def run_with_sudo(pwd="", args=[]):

    python_path = subprocess.check_output("which python", shell=True).strip()
    python_path = python_path.decode('utf-8')

    file_path = os.path.dirname(os.path.abspath(__file__))
    file_path = file_path + os.sep + "main.py"

    command = []
    command.append("sudo")
    command.append("-S")
    command.append(python_path)
    command.append(file_path)

    command = command + args

    p = subprocess.Popen(command, stdin=subprocess.PIPE, stderr=subprocess.PIPE,
              universal_newlines=True)
    sudo_prompt = p.communicate(pwd + '\n')[1]
    code = p.wait()

if __name__ == "__main__":
    args = sys.argv[1:]
    if is_root():
        main()
    elif test_sudo():
        run_with_sudo(args=args)
    else:
        pwd = getpass("root password: ")
        run_with_sudo(pwd=pwd, args=args)
