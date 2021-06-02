#!/usr/bin/env python3

# For controlling via the command line
# Example usage:
#       main.py --mode 0

import sys
import os
import argparse

import controller
import configurator

# May want cli only
try:
    import ui
except ImportError:
    pass

import driver


def main():
    # get values from command line if given
    argparser = argparse.ArgumentParser(
        description="MSI OpenFreezeCenter",
        epilog="Controls fan speed profiles",
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
        help="To launch the GUI.",
    )
    args = argparser.parse_args(sys.argv[1:])

    # If requesting to launch the gui, do nothing else
    if args.gui:
        ui.open_ui()
        return

    if args.stats:
        stats = controller.get_stats()
        print(stats)
        return

    # Get the settings from file. If not mode is specified whatever is in this file will be used.
    config = configurator.get_config()

    if args.mode == None:
        controller.enable_mode(
            mode=config["settings"]["mode"],
            vr=config["settings"]["vr_custom"],
            offset=config["settings"]["offset"],
        )
    else:
        controller.enable_mode(
            mode=args.mode,
            vr=config["settings"]["vr_custom"],
            offset=config["settings"]["offset"],
        )


if __name__ == "__main__":
    main()
