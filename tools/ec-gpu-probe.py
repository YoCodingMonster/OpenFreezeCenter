#!/usr/bin/env python3
"""Find out why the GPU temperature reads zero.

Run as root:

    sudo python3 tools/ec-gpu-probe.py

It reads the EC twice — once as the machine is now, and once while the
discrete GPU is held awake — and reports which bytes changed. There are only
two explanations for a zero, and the two readings tell them apart:

  * The dGPU is runtime-suspended. Then 0x80 reads 0 now and a real
    temperature in the second pass, and nothing needs fixing in the
    application beyond how it presents a GPU that is not running.

  * 0x80 is the wrong address on this model. Then it reads 0 in both passes,
    and the byte that tracks the temperature nvidia-smi reports is the
    address `gpu_temp_address` should be set to in
    ~/.config/openfreezecenter/config.json.
"""

import json
import os
import subprocess
import sys
import time

EC_IO_PATH = "/sys/kernel/debug/ec/ec0/io"
EC_SIZE = 256
CONFIG = os.path.expanduser("~/.config/openfreezecenter/config.json")

# Plausible temperatures for a chip that is powered on. A byte outside this
# is not a candidate however well it correlates.
SANE_RANGE = range(20, 105)


def read_ec():
    with open(EC_IO_PATH, "rb") as handle:
        return handle.read(EC_SIZE).ljust(EC_SIZE, b"\x00")


def nvidia_temp():
    """The temperature the driver reports, which also wakes the GPU."""
    try:
        out = subprocess.run(
            ["nvidia-smi", "--query-gpu=temperature.gpu", "--format=csv,noheader"],
            capture_output=True,
            text=True,
            timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    line = out.stdout.strip().splitlines()
    try:
        return int(line[0])
    except (IndexError, ValueError):
        return None


def runtime_status():
    for entry in sorted(os.listdir("/sys/bus/pci/devices")):
        path = f"/sys/bus/pci/devices/{entry}"
        try:
            with open(f"{path}/vendor") as handle:
                if handle.read().strip() != "0x10de":
                    continue
            with open(f"{path}/power/runtime_status") as handle:
                return entry, handle.read().strip()
        except OSError:
            continue
    return None, None


def configured_address():
    try:
        with open(CONFIG) as handle:
            return json.load(handle).get("hardware", {}).get("gpu_temp_address")
    except (OSError, ValueError):
        return None


def main():
    if os.geteuid() != 0:
        sys.exit("The EC is root-only. Re-run with sudo.")
    if not os.path.exists(EC_IO_PATH):
        sys.exit(f"{EC_IO_PATH} does not exist; load ec_sys write_support=1 first.")

    configured = configured_address()
    device, status = runtime_status()
    print(f"NVIDIA device {device or '?'} is currently: {status or 'unknown'}")
    if configured is not None:
        print(f"config gpu_temp_address: 0x{configured:02X}")

    asleep = read_ec()
    print(f"\nEC 0x80 with the GPU as-is: {asleep[0x80]}")

    print("Waking the GPU...")
    temp = nvidia_temp()
    if temp is None:
        sys.exit("nvidia-smi gave no temperature; cannot compare the two states.")
    # The driver lets the GPU fall back to D3cold quickly, so read straight
    # away and again a moment later, and keep whichever pass saw it awake.
    awake = read_ec()
    time.sleep(1.5)
    nvidia_temp()
    awake_again = read_ec()
    print(f"nvidia-smi reports: {temp} C")
    print(f"EC 0x80 with the GPU awake: {awake[0x80]} / {awake_again[0x80]}")

    print("\nBytes that changed, and how they compare to nvidia-smi:")
    for address in range(EC_SIZE):
        values = {asleep[address], awake[address], awake_again[address]}
        if len(values) == 1:
            continue
        best = max(awake[address], awake_again[address])
        note = ""
        if best in SANE_RANGE and abs(best - temp) <= 5:
            note = "  <-- tracks the driver's reading"
        print(
            f"  0x{address:02X}: asleep {asleep[address]:3d} -> "
            f"awake {awake[address]:3d}/{awake_again[address]:3d}{note}"
        )

    woke = max(awake[0x80], awake_again[0x80])
    print()
    if asleep[0x80] == 0 and woke in SANE_RANGE:
        print(
            "0x80 is the right address. It reads 0 only because the discrete\n"
            "GPU is powered down, which is what Optimus does whenever nothing\n"
            "is using it. There is no wrong address to fix."
        )
    elif woke == 0:
        print(
            "0x80 stayed 0 even with the GPU awake, so it is not where this\n"
            "model keeps the GPU temperature. Look above for a byte marked as\n"
            "tracking the driver's reading and set gpu_temp_address to it in\n"
            f"{CONFIG}."
        )
    else:
        print("Inconclusive — the GPU may have suspended again between reads.")


if __name__ == "__main__":
    main()
