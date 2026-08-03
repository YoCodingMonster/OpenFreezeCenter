"""Where the watts come from.

Neither figure is in the embedded controller, so neither arrives with the
rest of a reading. The CPU's comes from Intel's RAPL counter, which is not a
power reading at all but a running total of energy spent, in microjoules;
watts are the difference between two samples divided by the time between
them. The GPU's comes from NVML, the library the NVIDIA driver already
ships, reached through ctypes so that nothing new has to be installed —
which is the same reason the charts are drawn with GSK rather than Cairo.

Nothing here may wake a sleeping GPU. Optimus powers the discrete GPU right
down whenever nothing is using it, and merely asking NVML for a number is
enough to bring it back; done twice a second forever, that would cost far
more battery than the reading is worth. The PCI runtime status says whether
the GPU is up, costs nothing to read and does not disturb it, so it is
consulted first and NVML is only reached for when there is something running
to ask about. When the GPU goes back to sleep the NVML handle is dropped
again, so nothing of ours is left holding it open.

Every reader returns None rather than raising when it has nothing to give: a
missing counter, a permission it does not have, or a chip that is powered
down are all ordinary, and none of them is a reason to take down a window
whose real job is fan control.
"""

import ctypes
import os
import random
import time

RAPL_ROOT = "/sys/class/powercap"
PCI_DEVICES = "/sys/bus/pci/devices"

NVIDIA_VENDOR = "0x10de"
DISPLAY_CLASS = "0x0300"
NVML_LIBRARY = "libnvidia-ml.so.1"
NVML_SUCCESS = 0

# A reading above this is a misread rather than a measurement, and one bad
# sample must not be able to wreck the scale of the chart it feeds. Mirrors
# what cfg.RPM_PEAK_MAX does for the fans.
WATTS_MAX = 400.0


def _read_text(path):
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return handle.read().strip()
    except OSError:
        return None


def _sane(watts):
    if watts is None or watts < 0 or watts > WATTS_MAX:
        return None
    return watts


class CpuPower:
    """Package power, from the energy counter RAPL keeps running.

    The counter is root-only on current kernels — it leaks enough about what
    the machine is doing to have been a side channel — which is no obstacle
    here, since the EC is root-only too and the application already runs
    that way. Unreadable simply means no CPU watts, not an error.
    """

    def __init__(self, path):
        self.path = path
        self._energy_path = os.path.join(path, "energy_uj")
        self._wrap = None
        self._previous = None
        self._when = None

        limit = _read_text(os.path.join(path, "max_energy_range_uj"))
        if limit is not None:
            try:
                self._wrap = int(limit)
            except ValueError:
                self._wrap = None

    @classmethod
    def detect(cls):
        """The package domain, or None if this machine has no RAPL."""
        try:
            entries = sorted(os.listdir(RAPL_ROOT))
        except OSError:
            return None
        for entry in entries:
            # intel-rapl:0 is a package; intel-rapl:0:0 is a domain inside
            # it, which measures only part of what the package draws.
            if not entry.startswith("intel-rapl:") or entry.count(":") != 1:
                continue
            path = os.path.join(RAPL_ROOT, entry)
            name = _read_text(os.path.join(path, "name")) or ""
            if name.startswith("package"):
                return cls(path)
        return None

    def read(self):
        now = time.monotonic()
        raw = _read_text(self._energy_path)
        if raw is None:
            return None
        try:
            energy = int(raw)
        except ValueError:
            return None

        previous, when = self._previous, self._when
        self._previous, self._when = energy, now
        if previous is None or when is None:
            return None  # the first sample only establishes a baseline

        elapsed = now - when
        if elapsed <= 0:
            return None
        spent = energy - previous
        if spent < 0:
            if self._wrap is None:
                return None
            spent += self._wrap  # the counter went round
        return _sane(spent / elapsed / 1_000_000)

    def close(self):
        # Drop the baseline. Monitoring can stop and start again — the error
        # page does exactly that — and energy spent across the pause averaged
        # over the pause is not the power draw of the moment it resumes.
        self._previous = None
        self._when = None


class GpuPower:
    """Discrete GPU power through NVML, and only while the GPU is awake."""

    def __init__(self, device_path):
        self.device_path = device_path
        self.bus_id = os.path.basename(device_path)
        self._status_path = os.path.join(device_path, "power", "runtime_status")
        self._nvml = None
        self._handle = None
        self._unavailable = False

    @classmethod
    def detect(cls):
        """The first NVIDIA display device, or None if there is not one."""
        try:
            entries = sorted(os.listdir(PCI_DEVICES))
        except OSError:
            return None
        for entry in entries:
            path = os.path.join(PCI_DEVICES, entry)
            if _read_text(os.path.join(path, "vendor")) != NVIDIA_VENDOR:
                continue
            # The card also presents an audio function; it is not the GPU.
            if not (_read_text(os.path.join(path, "class")) or "").startswith(
                DISPLAY_CLASS
            ):
                continue
            return cls(path)
        return None

    def _awake(self):
        """Whether the GPU is powered up. Reading this does not wake it."""
        status = _read_text(self._status_path)
        if status is None:
            return True  # no runtime power management: it is always on
        return status == "active"

    def _open(self):
        try:
            nvml = ctypes.CDLL(NVML_LIBRARY)
        except OSError:
            self._unavailable = True
            return False

        nvml.nvmlDeviceGetHandleByPciBusId_v2.argtypes = [
            ctypes.c_char_p,
            ctypes.POINTER(ctypes.c_void_p),
        ]
        nvml.nvmlDeviceGetPowerUsage.argtypes = [
            ctypes.c_void_p,
            ctypes.POINTER(ctypes.c_uint),
        ]

        if nvml.nvmlInit_v2() != NVML_SUCCESS:
            self._unavailable = True
            return False
        handle = ctypes.c_void_p()
        if (
            nvml.nvmlDeviceGetHandleByPciBusId_v2(self.bus_id.encode(), handle)
            != NVML_SUCCESS
        ):
            nvml.nvmlShutdown()
            self._unavailable = True
            return False

        self._nvml, self._handle = nvml, handle
        return True

    def read(self):
        if self._unavailable:
            return None
        if not self._awake():
            # Let go of it while it sleeps, so nothing of ours is a reason
            # for it to stay up.
            self.close()
            return None
        if self._handle is None and not self._open():
            return None

        milliwatts = ctypes.c_uint()
        if self._nvml.nvmlDeviceGetPowerUsage(self._handle, milliwatts) != NVML_SUCCESS:
            return None
        return _sane(milliwatts.value / 1000.0)

    def close(self):
        if self._nvml is not None:
            try:
                self._nvml.nvmlShutdown()
            except OSError:
                pass
        self._nvml = None
        self._handle = None


class SimulatedPower:
    """Wandering watts, so the interface can be worked on without hardware."""

    def __init__(self, baseline, spread):
        self._watts = float(baseline)
        self._baseline = float(baseline)
        self._spread = float(spread)

    def read(self):
        self._watts += random.uniform(-self._spread, self._spread)
        low, high = self._baseline * 0.3, self._baseline * 2.4
        self._watts = max(low, min(high, self._watts))
        return round(self._watts, 1)

    def close(self):
        pass


class PowerMeters:
    """Both readings together, so the monitor has one thing to poll."""

    def __init__(self, cpu=None, gpu=None):
        self.cpu = cpu
        self.gpu = gpu

    @classmethod
    def detect(cls):
        return cls(CpuPower.detect(), GpuPower.detect())

    @classmethod
    def simulated(cls):
        return cls(SimulatedPower(22, 2.5), SimulatedPower(45, 6.0))

    def read(self):
        """(cpu watts, gpu watts), either of which may be None."""
        return (
            self.cpu.read() if self.cpu is not None else None,
            self.gpu.read() if self.gpu is not None else None,
        )

    def close(self):
        for meter in (self.cpu, self.gpu):
            if meter is not None:
                meter.close()
