"""Access to the MSI embedded controller through the ec_sys debugfs interface.

Everything the application knows about the hardware funnels through
`EmbeddedController`.  Reads go through `snapshot()`, which pulls the whole
256 byte EC address space in a single open/read; the old code opened the
device once per value, six times per refresh.
"""

import os
import random

EC_IO_PATH = "/sys/kernel/debug/ec/ec0/io"
EC_SIZE = 256

# The EC reports fan speed as a period; this is the constant the MSI firmware
# uses to turn that period into RPM.
RPM_CONSTANT = 478000


class ECError(Exception):
    """An EC access problem that the UI can present to the user."""

    def __init__(self, title, detail, hint=""):
        super().__init__(title)
        self.title = title
        self.detail = detail
        self.hint = hint


class ECUnavailable(ECError):
    """The debugfs EC interface is not there at all."""


class ECPermissionDenied(ECError):
    """We are not running with enough privilege to touch the EC."""


class ECWriteUnsupported(ECError):
    """The ec_sys module was loaded without write_support=1."""


def _describe_oserror(exc, path, writing):
    if isinstance(exc, FileNotFoundError):
        return ECUnavailable(
            "Embedded controller not available",
            f"{path} does not exist, so the fan controller cannot be reached.",
            "Load the ec_sys module with write support:\n"
            "    sudo modprobe ec_sys write_support=1\n"
            "Run install.sh once to make that setting persist across reboots.",
        )
    if isinstance(exc, PermissionError):
        return ECPermissionDenied(
            "Permission denied",
            f"{path} can only be read and written by root.",
            "Start the application with pkexec or sudo.",
        )
    if writing and exc.errno == 22:  # EINVAL, what ec_sys returns read-only
        return ECWriteUnsupported(
            "Embedded controller is read-only",
            "The ec_sys module was loaded without write support, so fan "
            "profiles cannot be changed.",
            "Add 'options ec_sys write_support=1' to "
            "/etc/modprobe.d/ec_sys.conf and reboot.",
        )
    return ECError("Embedded controller error", str(exc))


class EmbeddedController:
    """Reads and writes single EC bytes, plus whole-space snapshots."""

    def __init__(self, path=EC_IO_PATH):
        self.path = path

    def check(self):
        """Raise an ECError describing why the EC is unusable, or return None."""
        try:
            with open(self.path, "rb") as handle:
                handle.read(1)
        except OSError as exc:
            raise _describe_oserror(exc, self.path, writing=False) from exc
        if not os.access(self.path, os.W_OK):
            raise ECPermissionDenied(
                "Permission denied",
                f"{self.path} is not writable by this process.",
                "Start the application with pkexec or sudo.",
            )
        return None

    def snapshot(self):
        """Return the whole EC address space as `bytes`."""
        try:
            with open(self.path, "rb") as handle:
                data = handle.read(EC_SIZE)
        except OSError as exc:
            raise _describe_oserror(exc, self.path, writing=False) from exc
        if len(data) < EC_SIZE:
            data = data.ljust(EC_SIZE, b"\x00")
        return data

    def read_u8(self, address):
        return self.snapshot()[address]

    def write_u8(self, address, value):
        value = max(0, min(255, int(value)))
        try:
            with open(self.path, "r+b") as handle:
                handle.seek(address)
                handle.write(bytes((value,)))
        except OSError as exc:
            raise _describe_oserror(exc, self.path, writing=True) from exc

    def write_many(self, pairs):
        """Write several (address, value) pairs through one open file handle."""
        pairs = list(pairs)
        if not pairs:
            return
        try:
            with open(self.path, "r+b") as handle:
                for address, value in pairs:
                    handle.seek(address)
                    handle.write(bytes((max(0, min(255, int(value))),)))
        except OSError as exc:
            raise _describe_oserror(exc, self.path, writing=True) from exc


class SimulatedController(EmbeddedController):
    """An in-memory EC, so the interface can be developed without MSI hardware.

    Enabled with --simulate.  Temperatures wander around a baseline and fan
    RPM loosely follows them, which is enough to exercise the graphs.
    """

    def __init__(self):
        super().__init__(path="<simulated>")
        self._memory = bytearray(EC_SIZE)
        self._temps = [52.0, 46.0]

    def check(self):
        return None

    def snapshot(self):
        for index in range(2):
            self._temps[index] += random.uniform(-3.0, 3.2)
            self._temps[index] = max(35.0, min(94.0, self._temps[index]))
        cpu_temp, gpu_temp = (int(value) for value in self._temps)
        self._memory[0x68] = cpu_temp
        self._memory[0x80] = gpu_temp
        # Cooler Booster pins both fans near their ceiling whatever the
        # temperature is, which is what the fan speed measurement relies on.
        boosted = self._memory[0x98] in (128, 130)
        for address, temp, top in ((0xC8, cpu_temp, 5400), (0xCA, gpu_temp, 5150)):
            rpm = top - random.randint(0, 60) if boosted else 1200 + (temp - 35) * 55
            period = int(RPM_CONSTANT / max(rpm, 1))
            self._memory[address] = (period >> 8) & 0xFF
            self._memory[address + 1] = period & 0xFF
        return bytes(self._memory)

    def write_u8(self, address, value):
        self._memory[address] = max(0, min(255, int(value)))

    def write_many(self, pairs):
        for address, value in pairs:
            self.write_u8(address, value)


def u16(snapshot, address):
    """Read a big-endian 16 bit value out of a snapshot."""
    return (snapshot[address] << 8) | snapshot[address + 1]


def rpm_from_period(period):
    """Convert the EC's fan period reading into RPM (0 when the fan is idle)."""
    if period <= 0:
        return 0
    return RPM_CONSTANT // period
