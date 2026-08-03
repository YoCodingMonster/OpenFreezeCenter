"""Application object, CSS loading, and command line entry point."""

import argparse
import os
import pwd
import subprocess
import sys

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gio, Gtk, Gdk

from . import config as cfg
from .ec import EmbeddedController, SimulatedController
from .power import PowerMeters
from .style import STYLE
from .window import MainWindow

APP_ID = "io.github.yocodingmonster.OpenFreezeCenter"
VERSION = "7.0"

WEBSITE = "https://github.com/YoCodingMonster/OpenFreezeCenter"
ISSUE_URL = "https://github.com/YoCodingMonster/OpenFreezeCenter/issues"

# Adw.SwitchRow, Adw.SpinRow, Adw.NavigationView and Adw.ToolbarView arrived
# in libadwaita 1.4. GTK is the stricter of the two floors: ofc.widgets draws
# with Gsk.PathBuilder and Gtk.Snapshot.append_stroke/append_fill, which are
# GTK 4.14. A 1.4 + GTK 4.12 pairing (Ubuntu 23.10, Fedora 39) satisfies the
# libadwaita side and then dies on the first chart redraw, so both are checked.
REQUIRED_ADW = (1, 4)
REQUIRED_GTK = (4, 14)

# The stylesheet, and the 60% metric scale it is generated from, live in
# ofc.style.

# Handed through to the user's session so xdg-open can find the display.
SESSION_VARIABLES = ("DISPLAY", "WAYLAND_DISPLAY", "XAUTHORITY")


def invoking_user():
    """The account behind a sudo/pkexec launch, as (name, uid), else None.

    Returns None when we are not root, because then there is nobody to drop
    back to and the current environment is already the right one.
    """
    if os.geteuid() != 0:
        return None

    name = os.environ.get("SUDO_USER")
    uid = os.environ.get("SUDO_UID") or os.environ.get("PKEXEC_UID")
    try:
        if name is None:
            if uid is None:
                return None
            name = pwd.getpwuid(int(uid)).pw_name
        if uid is None:
            uid = pwd.getpwnam(name).pw_uid
        return name, int(uid)
    except (KeyError, ValueError):
        return None


def open_externally(target):
    """Open a URL or folder on the user's desktop. True if we got that far.

    The application itself has to be root - the EC is root-only - but nothing
    user-facing can stay root. GTK's own show_uri asks the desktop portal over
    the session bus, and root cannot authenticate to the user's bus, so links
    clicked inside the application appear to do nothing at all. Shelling out
    to the invoking user's xdg-open is the way around that, and it also stops
    a browser or file manager from starting up as root over the user's own
    profile.
    """
    user = invoking_user()
    if user is None:
        command = ["xdg-open", target]
    else:
        name, uid = user
        runtime_dir = f"/run/user/{uid}"
        # sudo scrubs the environment, so what xdg-open needs to reach the
        # session is re-applied on the far side with env(1).
        assignments = [
            f"XDG_RUNTIME_DIR={runtime_dir}",
            f"DBUS_SESSION_BUS_ADDRESS=unix:path={runtime_dir}/bus",
        ]
        assignments += [
            f"{key}={os.environ[key]}"
            for key in SESSION_VARIABLES
            if key in os.environ
        ]
        # Going from root to another account never prompts for a password.
        command = ["sudo", "-u", name, "--", "env", *assignments, "xdg-open", target]

    try:
        subprocess.Popen(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,  # outlives us, so quitting keeps the browser
        )
    except OSError:
        return False
    return True


class OFCApplication(Adw.Application):
    def __init__(self, controller, meters=None):
        super().__init__(application_id=APP_ID, flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.controller = controller
        self.meters = meters
        self.window = None

    def do_startup(self):
        Adw.Application.do_startup(self)

        provider = Gtk.CssProvider()
        provider.load_from_data(STYLE.encode())
        display = Gdk.Display.get_default()
        if display is not None:
            Gtk.StyleContext.add_provider_for_display(
                display, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
            )

        for name, callback, accels in (
            ("quit", self._on_quit, ["<primary>q"]),
            ("about", self._on_about, []),
            ("open-config", self._on_open_config, []),
            ("calibrate-fans", self._on_calibrate_fans, []),
            ("website", self._on_website, []),
            ("report-issue", self._on_report_issue, []),
        ):
            action = Gio.SimpleAction.new(name, None)
            action.connect("activate", callback)
            self.add_action(action)
            if accels:
                self.set_accels_for_action(f"app.{name}", accels)

    def do_activate(self):
        if self.window is None:
            self.window = MainWindow(self, self.controller, self.meters)
        self.window.present()

    def _on_quit(self, *_args):
        self.quit()

    def _on_about(self, *_args):
        # The window's own "website" and "issue-url" properties are left
        # unset on purpose. libadwaita opens those rows itself rather than
        # emitting ::activate-link, so there is no way to send them through
        # open_externally, and as root they silently do nothing. The same two
        # links are in the main menu instead, as actions we control.
        about = Adw.AboutWindow(
            transient_for=self.window,
            application_name="Open Freeze Center",
            application_icon="computer-symbolic",
            version=VERSION,
            developer_name="YoCodingMonster",
            comments="Fan profiles, temperature monitoring and battery charge "
            "limiting for MSI laptops on Linux.",
            license_type=Gtk.License.GPL_3_0,
        )
        about.add_credit_section("Settings file", [cfg.config_path()])
        # Still worth handling for links inside the comments and credits,
        # which do go through this signal.
        about.connect("activate-link", lambda _w, uri: open_externally(uri))
        about.present()

    def _on_website(self, *_args):
        open_externally(WEBSITE)

    def _on_report_issue(self, *_args):
        open_externally(ISSUE_URL)

    def _on_calibrate_fans(self, *_args):
        if self.window is not None:
            self.window.calibrate_fans()

    def _on_open_config(self, *_args):
        folder = os.path.dirname(cfg.config_path())
        os.makedirs(folder, exist_ok=True)
        open_externally(folder)


def _check_versions():
    """Refuse to start rather than fail later on a missing symbol.

    The binding versions are checked at run time, not against whatever the
    typelib was built with, because those can differ on a mixed system.
    """
    problems = []

    gtk_have = (Gtk.get_major_version(), Gtk.get_minor_version())
    if gtk_have < REQUIRED_GTK:
        problems.append(
            f"GTK {REQUIRED_GTK[0]}.{REQUIRED_GTK[1]} or newer is required "
            f"(this system has {gtk_have[0]}.{gtk_have[1]}); the charts are "
            "drawn with the GSK path API, which arrived in GTK 4.14."
        )

    adw_have = (Adw.get_major_version(), Adw.get_minor_version())
    if adw_have < REQUIRED_ADW:
        problems.append(
            f"libadwaita {REQUIRED_ADW[0]}.{REQUIRED_ADW[1]} or newer is "
            f"required (this system has {adw_have[0]}.{adw_have[1]}); the "
            "settings rows and the navigation view arrived in libadwaita 1.4."
        )

    if problems:
        sys.stderr.write("Open Freeze Center cannot run on this system:\n")
        for problem in problems:
            sys.stderr.write(f"  - {problem}\n")
        sys.stderr.write(
            "\nUbuntu 24.04+, Debian 13+, Fedora 40+ and current Arch are new\n"
            "enough. On an older system use OpenFreezeCenter-Lite instead:\n"
            "  https://github.com/YoCodingMonster/OpenFreezeCenter-Lite\n"
        )
        return False
    return True


def _prefer_cairo_renderer():
    """Draw on the CPU unless the user has asked for something else.

    GTK's GPU renderers map in the whole Mesa stack, which for this
    application measured ~200 MB resident against ~80 MB with the cairo
    renderer - a lot for a background utility that is a form plus one chart
    redrawn twice a second, and which no GPU path makes faster. This is GSK's
    own C renderer, so it adds no dependency; in particular it does not need
    the gi._gi_cairo bridge that ofc.widgets avoids.

    Set GSK_RENDERER (to "ngl", "vulkan", ...) to override.
    """
    os.environ.setdefault("GSK_RENDERER", "cairo")


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="OFC", description="Fan and battery control for MSI laptops."
    )
    parser.add_argument(
        "--simulate",
        action="store_true",
        help="run against a fake embedded controller, for UI work on any machine",
    )
    args = parser.parse_args(argv if argv is not None else sys.argv[1:])

    # Before any surface is realised, which is when GSK picks its renderer.
    _prefer_cairo_renderer()

    if not _check_versions():
        return 1

    if args.simulate:
        controller = SimulatedController()
        meters = PowerMeters.simulated()
    else:
        meters = None
        controller = EmbeddedController()
        if os.geteuid() != 0:
            sys.stderr.write(
                "Note: not running as root. The embedded controller will most "
                "likely be unreadable; start with pkexec or sudo.\n"
            )

    Adw.init()
    return OFCApplication(controller, meters).run([])
