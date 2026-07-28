"""Sensor polling and history.

One EC snapshot per tick feeds every reading, and a bounded history buffer
backs the graphs.
"""

from collections import deque

from gi.repository import GLib, GObject

from .ec import u16, rpm_from_period

HISTORY_SECONDS = 60


class Reading:
    """One poll: temperatures in °C, fan speeds in RPM."""

    __slots__ = ("cpu_temp", "gpu_temp", "cpu_rpm", "gpu_rpm")

    def __init__(self, cpu_temp, gpu_temp, cpu_rpm, gpu_rpm):
        self.cpu_temp = cpu_temp
        self.gpu_temp = gpu_temp
        self.cpu_rpm = cpu_rpm
        self.gpu_rpm = gpu_rpm


class Monitor(GObject.Object):
    """Polls the EC on a timer and emits `reading` / `failed`."""

    __gsignals__ = {
        "reading": (GObject.SignalFlags.RUN_FIRST, None, (object,)),
        "failed": (GObject.SignalFlags.RUN_FIRST, None, (object,)),
    }

    def __init__(self, controller, config, interval_ms=500):
        super().__init__()
        self.controller = controller
        self.config = config
        self.interval_ms = interval_ms
        self._source_id = None

        points = max(1, (HISTORY_SECONDS * 1000) // interval_ms)
        self.cpu_history = deque(maxlen=points)
        self.gpu_history = deque(maxlen=points)

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

    def reset_extremes(self):
        self.cpu_min = self.gpu_min = 999
        self.cpu_max = self.gpu_max = 0
        if self.latest is not None:
            self._record_extremes(self.latest)

    def _record_extremes(self, reading):
        self.cpu_min = min(self.cpu_min, reading.cpu_temp)
        self.cpu_max = max(self.cpu_max, reading.cpu_temp)
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

        reading = Reading(
            cpu_temp=snapshot[hardware.cpu_temp_address],
            gpu_temp=snapshot[hardware.gpu_temp_address],
            cpu_rpm=rpm_from_period(u16(snapshot, hardware.cpu_rpm_address)),
            gpu_rpm=rpm_from_period(u16(snapshot, hardware.gpu_rpm_address)),
        )

        self.latest = reading
        self._record_extremes(reading)
        self.cpu_history.append(reading.cpu_temp)
        self.gpu_history.append(reading.gpu_temp)
        self.emit("reading", reading)
        return GLib.SOURCE_CONTINUE
