#!/usr/bin/env bash
#
# Open Freeze Center installer.
#
#   ./install.sh              install (or update) and set up EC access
#   ./install.sh --uninstall  remove everything this script installed
#
# Run it from the directory you unpacked, as your normal user; it asks for
# sudo only for the steps that need it.

set -euo pipefail

PREFIX=/opt/openfreezecenter
BIN=/usr/local/bin/openfreezecenter
DESKTOP=/usr/share/applications/io.github.yocodingmonster.OpenFreezeCenter.desktop
POLICY=/usr/share/polkit-1/actions/io.github.yocodingmonster.OpenFreezeCenter.policy
MODPROBE_CONF=/etc/modprobe.d/ec_sys.conf
MODULES_CONF=/etc/modules-load.d/ec_sys.conf

SOURCE_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

say()  { printf '\033[1;36m==>\033[0m %s\n' "$*"; }
warn() { printf '\033[1;33m==>\033[0m %s\n' "$*" >&2; }
die()  { printf '\033[1;31m==>\033[0m %s\n' "$*" >&2; exit 1; }

if [[ $(id -u) -eq 0 ]]; then
    die "Run this as your normal user, not with sudo. It asks for sudo when it needs it."
fi

###############################################################################
# Uninstall
###############################################################################

if [[ "${1:-}" == "--uninstall" ]]; then
    say "Removing Open Freeze Center"
    sudo rm -rf "$PREFIX" "$BIN" "$DESKTOP" "$POLICY"
    sudo rm -f "$MODPROBE_CONF" "$MODULES_CONF"
    say "Removed. Settings in ~/.config/openfreezecenter were left alone."
    exit 0
fi

###############################################################################
# Dependencies
###############################################################################

install_dependencies() {
    if command -v apt-get >/dev/null; then
        say "Installing dependencies with apt"
        sudo apt-get update || warn "  apt update failed; continuing with the current package lists"
        local packages=(python3 python3-gi gir1.2-gtk-4.0 gir1.2-adw-1)
        # pkexec moved out of policykit-1 into its own package; Ubuntu 26.04 and
        # newer have no policykit-1 at all, so pick whichever the release has.
        local candidate
        for candidate in pkexec policykit-1; do
            if apt-cache show "$candidate" >/dev/null 2>&1; then
                packages+=("$candidate")
                break
            fi
        done
        sudo apt-get install -y "${packages[@]}"
    elif command -v dnf >/dev/null; then
        say "Installing dependencies with dnf"
        sudo dnf install -y python3 python3-gobject gtk4 libadwaita polkit
    elif command -v pacman >/dev/null; then
        say "Installing dependencies with pacman"
        sudo pacman -S --needed --noconfirm python python-gobject gtk4 libadwaita polkit
    elif command -v zypper >/dev/null; then
        say "Installing dependencies with zypper"
        sudo zypper install -y python3 python3-gobject gtk4 libadwaita-1-0 polkit
    else
        warn "Unrecognised package manager. Install these yourself, then re-run:"
        warn "  python3, PyGObject, GTK 4, libadwaita 1.4+, polkit"
    fi
}

check_versions() {
    python3 - <<'PY' || die "Missing or too-old GTK/libadwaita. See the message above."
import sys
try:
    import gi
    gi.require_version("Gtk", "4.0")
    gi.require_version("Adw", "1")
    from gi.repository import Adw, Gtk
except Exception as exc:
    sys.exit(f"PyGObject with GTK 4 and libadwaita is not usable: {exc}")

gtk = (Gtk.get_major_version(), Gtk.get_minor_version())
adw = (Adw.get_major_version(), Adw.get_minor_version())
problems = []
# GTK is the stricter floor: the charts use the GSK path API from 4.14.
if gtk < (4, 14):
    problems.append(f"GTK {gtk[0]}.{gtk[1]} is too old; 4.14 or newer is required")
if adw < (1, 4):
    problems.append(f"libadwaita {adw[0]}.{adw[1]} is too old; 1.4 or newer is required")
if problems:
    sys.exit(
        "\n".join("  " + p for p in problems)
        + "\n  Ubuntu 24.04+, Debian 13+, Fedora 40+ and current Arch are new enough."
        + "\n  On an older system use OpenFreezeCenter-Lite instead:"
        + "\n  https://github.com/YoCodingMonster/OpenFreezeCenter-Lite"
    )
print(f"  GTK {gtk[0]}.{gtk[1]} / libadwaita {adw[0]}.{adw[1]} OK")
PY
}

###############################################################################
# EC access
#
# The previous installer drove `nano` through `expect` to append these two
# lines, which broke whenever nano's keybindings changed. `tee` does the same
# job with no terminal emulator in the loop.
###############################################################################

setup_ec() {
    say "Configuring embedded controller access"

    if ! grep -qs '^options ec_sys write_support=1' "$MODPROBE_CONF"; then
        echo 'options ec_sys write_support=1' | sudo tee "$MODPROBE_CONF" >/dev/null
        say "  wrote $MODPROBE_CONF"
    fi

    if ! grep -qs '^ec_sys$' "$MODULES_CONF"; then
        echo 'ec_sys' | sudo tee "$MODULES_CONF" >/dev/null
        say "  wrote $MODULES_CONF"
    fi

    # Load it now, so there is no reboot between installing and using it. If it
    # is already loaded read-only, reload it with write support.
    if sudo test -e /sys/kernel/debug/ec/ec0/io && ! sudo test -w /sys/kernel/debug/ec/ec0/io; then
        sudo modprobe -r ec_sys 2>/dev/null || true
    fi
    if sudo modprobe ec_sys write_support=1 2>/dev/null; then
        say "  ec_sys loaded with write support"
    else
        warn "  could not load ec_sys now; it will load on the next boot"
    fi

    if sudo test -w /sys/kernel/debug/ec/ec0/io; then
        say "  EC read/write confirmed"
    else
        warn "  EC not writable yet — reboot, then start the application"
    fi
}

###############################################################################
# Install
###############################################################################

install_files() {
    say "Installing to $PREFIX"
    if [[ ! -f "$SOURCE_DIR/OFC.py" || ! -d "$SOURCE_DIR/ofc" ]]; then
        die "Run this script from the folder containing OFC.py and ofc/"
    fi

    sudo rm -rf "$PREFIX"
    sudo install -d "$PREFIX"
    sudo cp -r "$SOURCE_DIR/OFC.py" "$SOURCE_DIR/ofc" "$PREFIX/"
    sudo find "$PREFIX" -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null || true
    sudo chmod +x "$PREFIX/OFC.py"

    # The launcher re-runs itself through pkexec, forwarding just enough of the
    # session environment for the window to land on the user's display.
    sudo tee "$BIN" >/dev/null <<'LAUNCHER'
#!/bin/sh
# Open Freeze Center launcher: elevates only when it has to.
APP=/opt/openfreezecenter/OFC.py

if [ "$(id -u)" -eq 0 ]; then
    exec python3 "$APP" "$@"
fi

for arg in "$@"; do
    # The simulator never touches the EC, so it does not need root.
    if [ "$arg" = "--simulate" ]; then
        exec python3 "$APP" "$@"
    fi
done

exec pkexec env \
    DISPLAY="${DISPLAY}" \
    WAYLAND_DISPLAY="${WAYLAND_DISPLAY}" \
    XDG_RUNTIME_DIR="${XDG_RUNTIME_DIR}" \
    XDG_SESSION_TYPE="${XDG_SESSION_TYPE}" \
    XAUTHORITY="${XAUTHORITY}" \
    SUDO_USER="$(id -un)" \
    python3 "$APP" "$@"
LAUNCHER
    sudo chmod +x "$BIN"

    sudo tee "$DESKTOP" >/dev/null <<DESKTOP_FILE
[Desktop Entry]
Type=Application
Name=Open Freeze Center
GenericName=Fan Control
Comment=Fan profiles, temperature monitoring and battery charge limiting for MSI laptops
Exec=$BIN
Icon=computer-symbolic
Terminal=false
Categories=Settings;HardwareSettings;
Keywords=fan;cooling;temperature;msi;battery;
StartupNotify=true
DESKTOP_FILE

    sudo tee "$POLICY" >/dev/null <<'POLICY_FILE'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE policyconfig PUBLIC
 "-//freedesktop//DTD PolicyKit Policy Configuration 1.0//EN"
 "http://www.freedesktop.org/software/polkit/policyconfig-1.dtd">
<policyconfig>
  <vendor>Open Freeze Center</vendor>
  <vendor_url>https://github.com/YoCodingMonster/OpenFreezeCenter</vendor_url>
  <action id="io.github.yocodingmonster.OpenFreezeCenter.run">
    <description>Control laptop fans and battery charge limit</description>
    <message>Authentication is required to control the embedded controller</message>
    <defaults>
      <allow_any>auth_admin</allow_any>
      <allow_inactive>auth_admin</allow_inactive>
      <allow_active>auth_admin_keep</allow_active>
    </defaults>
    <annotate key="org.freedesktop.policykit.exec.path">/usr/bin/env</annotate>
    <annotate key="org.freedesktop.policykit.exec.allow_gui">true</annotate>
  </action>
</policyconfig>
POLICY_FILE

    if command -v update-desktop-database >/dev/null; then
        sudo update-desktop-database /usr/share/applications 2>/dev/null || true
    fi
}

###############################################################################

install_dependencies
say "Checking versions"
check_versions
setup_ec
install_files

say "Done."
cat <<'NEXT'

  Launch it from your applications menu, or run:
      openfreezecenter

  To try the interface without touching the hardware:
      openfreezecenter --simulate

  Settings live in ~/.config/openfreezecenter/config.json
NEXT
