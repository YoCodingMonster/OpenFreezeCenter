"""Sensor polling and history.

One EC snapshot per tick feeds the temperatures and fan speeds, and the
power meters are read on the same tick, so everything in a reading describes
the same instant. A bounded history buffer per quantity backs the graph.
"""

from collections import deque

from gi.repository import GLib, GObject

from .ec import u16, rpm_from_period
from .power import PowerMeters

HISTORY_SECONDS = 60


class Reading:
    """One poll: temperatures in °C, fan speeds in RPM, power in watts.

    Anything the machine cannot answer for is None rather than zero. On a
    laptop with switchable graphics the discrete GPU spends most of its life
    powered down: the EC reads a chip that is not running back as zero, and
    NVML is not asked at all. Zero is not a temperature and not a wattage, so
    carrying it as one would drag the chart line to the floor and hold the
    recorded minimum at 0 °C forever. CPU watts are None too until the second
    sample, because a counter of energy spent says nothing about rate until
    there is a previous total to subtract.

    A fan speed of zero is left as zero: a fan that is not turning is a
    measurement, not a gap.
    """

    __slots__ = (
        "cpu_temp",
        "gpu_temp",
        "cpu_rpm",
        "gpu_rpm",
        "cpu_watts",
        "gpu_watts",
    )

    def __init__(self, cpu_temp, gpu_temp, cpu_rpm, gpu_rpm, cpu_watts, gpu_watts):
        self.cpu_temp = cpu_temp
        self.gpu_temp = gpu_temp
        self.cpu_rpm = cpu_rpm
        self.gpu_rpm = gpu_rpm
        self.cpu_watts = cpu_watts
        self.gpu_watts = gpu_watts


class Monitor(GObject.Object):
    """Polls the EC and the power meters on a timer, emits `reading`/`failed`."""

    __gsignals__ = {
        "reading": (GObject.SignalFlags.RUN_FIRST, None, (object,)),
        "failed": (GObject.SignalFlags.RUN_FIRST, None, (object,)),
    }

    def __init__(self, controller, config, interval_ms=500, meters=None):
        super().__init__()
        self.controller = controller
        self.config = config
        self.interval_ms = interval_ms
        self.meters = meters if meters is not None else PowerMeters()
        self._source_id = None

        points = max(1, (HISTORY_SECONDS * 1000) // interval_ms)
        self.cpu_history = deque(maxlen=points)
        self.gpu_history = deque(maxlen=points)
        self.cpu_rpm_history = deque(maxlen=points)
        self.gpu_rpm_history = deque(maxlen=points)
        self.cpu_watt_history = deque(maxlen=points)
        self.gpu_watt_history = deque(maxlen=points)

        # Seeded past any real temperature so the first reading replaces them.
        self.cpu_min = self.gpu_min = 999
        self.cpu_max = self.gpu_max = 0
        self.latest = None

    def start(self):
        if self._source_id is None:
            self._source_id = GLib.timeout_add(self.interval_ms, self._tick)
            self._tick()

    def stop(self):
        if self._source_id is not None:
            GLib.source_remove(self._source_id)
            self._source_id = None
        self.meters.close()

    def reset_extremes(self):
        self.cpu_min = self.gpu_min = 999
        self.cpu_max = self.gpu_max = 0
        if self.latest is not None:
            self._record_extremes(self.latest)

    def _record_extremes(self, reading):
        self.cpu_min = min(self.cpu_min, reading.cpu_temp)
        self.cpu_max = max(self.cpu_max, reading.cpu_temp)
        if reading.gpu_temp is not None:
            self.gpu_min = min(self.gpu_min, reading.gpu_temp)
            self.gpu_max = max(self.gpu_max, reading.gpu_temp)

    def _tick(self):
        hardware = self.config.hardware
        try:
            snapshot = self.controller.snapshot()
        except Exception as error:  # noqa: BLE001 - surfaced to the UI as-is
            self._source_id = None
            self.emit("failed", error)
            return GLib.SOURCE_REMOVE

        gpu_temp = snapshot[hardware.gpu_temp_address]
        cpu_watts, gpu_watts = self.meters.read()
        reading = Reading(
            cpu_temp=snapshot[hardware.cpu_temp_address],
            gpu_temp=gpu_temp if gpu_temp else None,
            cpu_rpm=rpm_from_period(u16(snapshot, hardware.cpu_rpm_address)),
            gpu_rpm=rpm_from_period(u16(snapshot, hardware.gpu_rpm_address)),
            cpu_watts=cpu_watts,
            gpu_watts=gpu_watts,
        )

        self.latest = reading
        self._record_extremes(reading)
        self.cpu_history.append(reading.cpu_temp)
        self.gpu_history.append(reading.gpu_temp)
        self.cpu_rpm_history.append(reading.cpu_rpm)
        self.gpu_rpm_history.append(reading.gpu_rpm)
        self.cpu_watt_history.append(reading.cpu_watts)
        self.gpu_watt_history.append(reading.gpu_watts)
        self.emit("reading", reading)
        return GLib.SOURCE_CONTINUE
