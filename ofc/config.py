"""Persistent settings.

Settings used to live in a generated `config.py` that the application
imported and rewrote as source code.  They now live in a JSON file under the
invoking user's config directory, so a corrupt file cannot execute anything
and the settings survive reinstalls.
"""

import ast
import json
import os
import pwd
from dataclasses import dataclass, field, asdict, replace

FAN_POINTS = 7
SPEED_MIN = 0
SPEED_MAX = 150
OFFSET_MIN = -30
OFFSET_MAX = 30
BATTERY_MIN = 50
BATTERY_MAX = 100

# A ceiling on the recorded fan peaks. A misread EC period yields an absurd
# RPM - the divisor is a constant over a 16 bit value, so a period of 1 reads
# as 478000 - and a single bad sample must not be able to permanently wreck
# the scale of the chart it feeds.
RPM_PEAK_MAX = 12000

CONFIG_VERSION = 3

PROFILE_AUTO = "auto"
PROFILE_BASIC = "basic"
PROFILE_ADVANCED = "advanced"
PROFILE_ORDER = (PROFILE_AUTO, PROFILE_BASIC, PROFILE_ADVANCED)

DEFAULT_AUTO_CPU = [0, 40, 48, 56, 64, 72, 80]
DEFAULT_AUTO_GPU = [0, 48, 56, 64, 72, 79, 86]

# Register layouts differ between EC generations.  Index 0 is for 10th gen
# Intel CPUs and below, index 1 for 11th gen and above.
EC_LAYOUTS = {
    False: {
        "profile_address": 0xF4,
        "profile_auto_value": 12,
        "profile_manual_value": 140,
        "cooler_booster_address": 0x98,
        "cooler_booster_off": 0,
        "cooler_booster_on": 128,
    },
    True: {
        "profile_address": 0xD4,
        "profile_auto_value": 13,
        "profile_manual_value": 141,
        "cooler_booster_address": 0x98,
        "cooler_booster_off": 2,
        "cooler_booster_on": 130,
    },
}


def _clamp(value, low, high):
    return max(low, min(high, value))


def _rpm_peak(value):
    """Coerce a stored fan peak into a sane RPM, discarding rubbish as 0."""
    try:
        return _clamp(int(value), 0, RPM_PEAK_MAX)
    except (TypeError, ValueError):
        return 0


def _speed_list(values, fallback):
    """Coerce a stored fan curve into exactly FAN_POINTS clamped integers."""
    try:
        cleaned = [_clamp(int(value), SPEED_MIN, SPEED_MAX) for value in values]
    except (TypeError, ValueError):
        return list(fallback)
    if len(cleaned) < FAN_POINTS:
        cleaned += list(fallback[len(cleaned):])
    return cleaned[:FAN_POINTS]


@dataclass
class Hardware:
    """EC register addresses. Only touched by users porting a new model."""

    cpu_gen_11_plus: bool = True
    profile_address: int = 0xD4
    profile_auto_value: int = 13
    profile_manual_value: int = 141
    cooler_booster_address: int = 0x98
    cooler_booster_off: int = 2
    cooler_booster_on: int = 130
    cpu_fan_speed_address: list = field(
        default_factory=lambda: [0x72, 0x73, 0x74, 0x75, 0x76, 0x77, 0x78]
    )
    gpu_fan_speed_address: list = field(
        default_factory=lambda: [0x8A, 0x8B, 0x8C, 0x8D, 0x8E, 0x8F, 0x90]
    )
    cpu_temp_address: int = 0x68
    gpu_temp_address: int = 0x80
    cpu_rpm_address: int = 0xC8
    gpu_rpm_address: int = 0xCA
    battery_threshold_address: int = 0xE4

    @classmethod
    def for_cpu_generation(cls, gen_11_plus):
        layout = EC_LAYOUTS[bool(gen_11_plus)]
        return cls(cpu_gen_11_plus=bool(gen_11_plus), **layout)


@dataclass
class Config:
    profile: str = PROFILE_AUTO
    cooler_booster: bool = False
    auto_cpu: list = field(default_factory=lambda: list(DEFAULT_AUTO_CPU))
    auto_gpu: list = field(default_factory=lambda: list(DEFAULT_AUTO_GPU))
    advanced_cpu: list = field(default_factory=lambda: list(DEFAULT_AUTO_CPU))
    advanced_gpu: list = field(default_factory=lambda: list(DEFAULT_AUTO_GPU))
    basic_offset: int = 0
    battery_threshold: int = 100

    # The fastest each fan has ever been recorded at, which is what the RPM
    # axis of the sensor chart is scaled from. Kept here rather than in the
    # chart so that a fresh session starts at the scale the last one ended
    # at, instead of growing under the plot while the fans spin up.
    cpu_rpm_peak: int = 0
    gpu_rpm_peak: int = 0
    # True once the peaks came from a deliberate full-speed measurement
    # rather than from whatever happened to be observed. `fan_rpm_asked`
    # records that the offer to measure has been made, so declining it once
    # is not re-asked at every launch; the main menu still offers it.
    fan_rpm_calibrated: bool = False
    fan_rpm_asked: bool = False

    hardware: Hardware = field(default_factory=Hardware)

    def normalised(self):
        """Return a copy with every field forced into its valid range."""
        return replace(
            self,
            profile=self.profile if self.profile in PROFILE_ORDER else PROFILE_AUTO,
            cooler_booster=bool(self.cooler_booster),
            auto_cpu=_speed_list(self.auto_cpu, DEFAULT_AUTO_CPU),
            auto_gpu=_speed_list(self.auto_gpu, DEFAULT_AUTO_GPU),
            advanced_cpu=_speed_list(self.advanced_cpu, DEFAULT_AUTO_CPU),
            advanced_gpu=_speed_list(self.advanced_gpu, DEFAULT_AUTO_GPU),
            basic_offset=_clamp(int(self.basic_offset), OFFSET_MIN, OFFSET_MAX),
            battery_threshold=_clamp(
                int(self.battery_threshold), BATTERY_MIN, BATTERY_MAX
            ),
            cpu_rpm_peak=_rpm_peak(self.cpu_rpm_peak),
            gpu_rpm_peak=_rpm_peak(self.gpu_rpm_peak),
            fan_rpm_calibrated=bool(self.fan_rpm_calibrated),
            fan_rpm_asked=bool(self.fan_rpm_asked),
        )


###############################################################################
# Where the file lives
###############################################################################


def _invoking_user():
    """The human behind the session, even when we were started through sudo."""
    name = os.environ.get("SUDO_USER") or os.environ.get("PKEXEC_UID")
    if name and name.isdigit():
        try:
            return pwd.getpwuid(int(name))
        except KeyError:
            return None
    if name:
        try:
            return pwd.getpwnam(name)
        except KeyError:
            return None
    return None


def config_path():
    """Path of the settings file, in the invoking user's config directory."""
    user = _invoking_user()
    if user is not None:
        base = os.path.join(user.pw_dir, ".config")
    else:
        base = os.environ.get("XDG_CONFIG_HOME") or os.path.expanduser("~/.config")
    return os.path.join(base, "openfreezecenter", "config.json")


def _restore_ownership(path):
    """Keep the file owned by the user, not by root, after a sudo run."""
    user = _invoking_user()
    if user is None:
        return
    try:
        os.chown(path, user.pw_uid, user.pw_gid)
        os.chown(os.path.dirname(path), user.pw_uid, user.pw_gid)
    except OSError:
        pass


###############################################################################
# Load and save
###############################################################################


def _from_dict(data):
    hardware_data = data.get("hardware") or {}
    known = {f for f in Hardware.__dataclass_fields__}
    hardware = Hardware(**{k: v for k, v in hardware_data.items() if k in known})
    known = {f for f in Config.__dataclass_fields__} - {"hardware"}
    config = Config(
        hardware=hardware, **{k: v for k, v in data.items() if k in known}
    )
    return config.normalised()


def load():
    """Read the settings file, migrating a legacy config.py if one is found.

    Never raises: a missing or damaged file falls back to defaults so the
    application always starts.
    """
    path = config_path()
    if not os.path.exists(path):
        legacy = migrate_legacy()
        if legacy is not None:
            save(legacy)
            return legacy
        return None
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return _from_dict(json.load(handle))
    except (OSError, ValueError, TypeError) as exc:
        print(f"OFC: ignoring unreadable config at {path}: {exc}")
        return Config()


def save(config):
    path = config_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    payload = asdict(config.normalised())
    payload["version"] = CONFIG_VERSION
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")
    os.replace(tmp, path)
    _restore_ownership(path)


###############################################################################
# Legacy config.py migration
###############################################################################

LEGACY_PATHS = (
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.py"),
    os.path.expanduser("~/Desktop/OFC/config.py"),
)


def _parse_legacy(path):
    """Pull literals out of the old config.py without executing it."""
    with open(path, "r", encoding="utf-8") as handle:
        tree = ast.parse(handle.read(), filename=path)
    values = {}
    for node in tree.body:
        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue
        target = node.targets[0]
        if not isinstance(target, ast.Name):
            continue
        try:
            values[target.id] = ast.literal_eval(node.value)
        except ValueError:
            continue
    return values


def migrate_legacy():
    """Convert an old config.py into a Config, or return None if there is none."""
    for path in LEGACY_PATHS:
        if not os.path.exists(path):
            continue
        try:
            values = _parse_legacy(path)
        except (OSError, SyntaxError) as exc:
            print(f"OFC: could not read legacy config {path}: {exc}")
            continue

        hardware = Hardware.for_cpu_generation(bool(values.get("CPU", 1)))
        profile_values = values.get("AUTO_ADV_VALUES")
        if isinstance(profile_values, (list, tuple)) and len(profile_values) == 3:
            hardware.profile_address = int(profile_values[0])
            hardware.profile_auto_value = int(profile_values[1])
            hardware.profile_manual_value = int(profile_values[2])
        booster = values.get("COOLER_BOOSTER_OFF_ON_VALUES")
        if isinstance(booster, (list, tuple)) and len(booster) == 3:
            hardware.cooler_booster_address = int(booster[0])
            hardware.cooler_booster_off = int(booster[1])
            hardware.cooler_booster_on = int(booster[2])
        speeds = values.get("CPU_GPU_FAN_SPEED_ADDRESS")
        if isinstance(speeds, (list, tuple)) and len(speeds) == 2:
            hardware.cpu_fan_speed_address = [int(v) for v in speeds[0]]
            hardware.gpu_fan_speed_address = [int(v) for v in speeds[1]]
        temps = values.get("CPU_GPU_TEMP_ADDRESS")
        if isinstance(temps, (list, tuple)) and len(temps) == 2:
            hardware.cpu_temp_address, hardware.gpu_temp_address = (int(v) for v in temps)
        rpms = values.get("CPU_GPU_RPM_ADDRESS")
        if isinstance(rpms, (list, tuple)) and len(rpms) == 2:
            hardware.cpu_rpm_address, hardware.gpu_rpm_address = (int(v) for v in rpms)

        auto = values.get("AUTO_SPEED") or [DEFAULT_AUTO_CPU, DEFAULT_AUTO_GPU]
        advanced = values.get("ADV_SPEED") or auto
        # Legacy profile 4 was "Cooler Booster" as a fourth profile; it is now
        # an independent toggle layered on top of a real profile.
        legacy_profile = int(values.get("PROFILE", 1) or 1)
        profile = {1: PROFILE_AUTO, 2: PROFILE_BASIC, 3: PROFILE_ADVANCED}.get(
            legacy_profile, PROFILE_AUTO
        )

        config = Config(
            profile=profile,
            cooler_booster=legacy_profile == 4,
            auto_cpu=list(auto[0]),
            auto_gpu=list(auto[1]),
            advanced_cpu=list(advanced[0]),
            advanced_gpu=list(advanced[1]),
            basic_offset=int(values.get("BASIC_OFFSET", 0) or 0),
            battery_threshold=int(values.get("BATTERY_THRESHOLD_VALUE", 100) or 100),
            hardware=hardware,
        )
        try:
            os.rename(path, path + ".migrated")
        except OSError:
            pass
        print(f"OFC: migrated legacy settings from {path}")
        return config.normalised()
    return None
