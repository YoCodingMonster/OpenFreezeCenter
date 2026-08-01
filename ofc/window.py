"""The main window, the first-run assistant, and the EC error page."""

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gtk, GLib

from . import config as cfg
from . import profiles
from .curve_editor import CurveEditorPage
from .ec import ECError
from .monitor import Monitor
from .widgets import LegendSwatch, SensorGraph

BATTERY_CHOICES = [str(value) for value in range(cfg.BATTERY_MIN, cfg.BATTERY_MAX + 1, 5)]


class ReadingsTable(Gtk.Grid):
    """The numeric view of what the graph plots.

    The chart carries the shape of the last minute; this carries the exact
    current value, and the running minimum and maximum, which a sixty-second
    window cannot show.
    """

    COLUMNS = ("Now", "Min", "Max", "Fan")

    def __init__(self):
        super().__init__(column_spacing=6, row_spacing=6)
        self.set_column_homogeneous(True)
        self.cells = {}

        for index, title in enumerate(self.COLUMNS):
            label = Gtk.Label(label=title, xalign=0.5)
            label.add_css_class("dim-label")
            label.add_css_class("caption")
            self.attach(label, index + 1, 0, 1, 1)

        for row, (key, name) in enumerate((("cpu", "CPU"), ("gpu", "GPU")), start=1):
            heading = Gtk.Box(spacing=8)
            heading.append(LegendSwatch(key))
            title = Gtk.Label(label=name, xalign=0.0)
            title.add_css_class("heading")
            heading.append(title)
            self.attach(heading, 0, row, 1, 1)

            for column, field in enumerate(("now", "min", "max", "rpm")):
                value = Gtk.Label(label="—", xalign=0.5)
                value.add_css_class("ofc-reading")
                value.set_hexpand(True)
                self.attach(value, column + 1, row, 1, 1)
                self.cells[(key, field)] = value

    def update(self, monitor, reading):
        pairs = (
            ("cpu", reading.cpu_temp, monitor.cpu_min, monitor.cpu_max, reading.cpu_rpm),
            ("gpu", reading.gpu_temp, monitor.gpu_min, monitor.gpu_max, reading.gpu_rpm),
        )
        for key, now, low, high, rpm in pairs:
            self.cells[(key, "now")].set_label(f"{now}°C")
            self.cells[(key, "min")].set_label(f"{low}°C" if low < 999 else "—")
            self.cells[(key, "max")].set_label(f"{high}°C")
            self.cells[(key, "rpm")].set_label(f"{rpm}" if rpm else "off")


class FanCalibration:
    """Find the fans' real top speed by running them flat out for a minute.

    The chart scales its RPM axis from the highest speed ever recorded. Left
    to discover that on its own, a fresh install spends its first minutes
    with the axis growing under the plot, because an idle fan is nowhere near
    the machine's ceiling. Measuring it once directly, and storing the result,
    means every later session opens at the right scale.

    Cooler Booster is the only way to ask for maximum speed regardless of
    profile, so it is what the measurement uses. The fans are loud for the
    duration, which is why nothing here starts without the user agreeing to
    it, and why the run can be stopped at any point.
    """

    DURATION_SECONDS = 60

    def __init__(self, window):
        self.window = window
        self.dialog = None
        self.remaining = self.DURATION_SECONDS
        self.peaks = {"cpu": 0, "gpu": 0}
        self.restore_booster = False
        self.timer_id = None
        self.reading_id = None
        self.close_id = None
        self.finished = False

    ###########################################################################
    # The offer
    ###########################################################################

    def offer(self):
        """Ask permission. Recorded either way, so it is asked only once."""
        config = self.window.config
        config.fan_rpm_asked = True
        cfg.save(config)

        dialog = Adw.MessageDialog(
            transient_for=self.window,
            heading="Measure maximum fan speed?",
            body="The monitor scales its fan axis to the fastest speed it has "
            "seen. Measuring that now means the axis is right from the first "
            "reading, instead of growing under the chart as the fans spin up.\n\n"
            "Both fans will run flat out for one minute, which is loud. You "
            "can stop it at any time, and run it later from the main menu.",
        )
        dialog.add_response("later", "Not Now")
        dialog.add_response("measure", "Measure")
        dialog.set_response_appearance("measure", Adw.ResponseAppearance.SUGGESTED)
        dialog.set_default_response("measure")
        dialog.set_close_response("later")
        dialog.connect("response", self._on_offer_response)
        dialog.present()

    def _on_offer_response(self, _dialog, response):
        if response == "measure":
            self.start()
        else:
            # Released, or the menu item would have nothing to hand out next
            # time it is chosen.
            self.window.calibration = None

    ###########################################################################
    # The run
    ###########################################################################

    def start(self):
        window = self.window
        config = window.config
        if window.monitor is None:
            window.calibration = None
            return

        self.restore_booster = config.cooler_booster
        try:
            profiles.apply_cooler_booster(window.controller, config, True)
        except ECError as error:
            window.calibration = None
            window._show_error(error)
            return

        self.reading_id = window.monitor.connect("reading", self._on_reading)
        self.timer_id = GLib.timeout_add_seconds(1, self._on_tick)
        # A run left going when the window closes would leave the fans pinned
        # at full speed with nothing left to turn them down.
        self.close_id = window.connect("close-request", self._on_window_close)

        self.dialog = Adw.MessageDialog(
            transient_for=window,
            heading="Measuring maximum fan speed",
            body=self._progress_text(),
        )
        self.dialog.add_response("stop", "Stop")
        self.dialog.set_close_response("stop")
        self.dialog.connect("response", lambda *_: self.finish(False))
        self.dialog.present()

    def _progress_text(self):
        seen = " · ".join(
            f"{label} {self.peaks[key] or '—'}"
            for key, label in (("cpu", "CPU"), ("gpu", "GPU"))
        )
        return (
            "Both fans are running at full speed.\n\n"
            f"{self.remaining} seconds remaining\n"
            f"Fastest so far: {seen} RPM"
        )

    def _on_reading(self, _monitor, reading):
        for key, rpm in (("cpu", reading.cpu_rpm), ("gpu", reading.gpu_rpm)):
            self.peaks[key] = min(max(self.peaks[key], rpm), cfg.RPM_PEAK_MAX)

    def _on_tick(self):
        self.remaining -= 1
        if self.remaining <= 0:
            self.finish(True)
            return GLib.SOURCE_REMOVE
        self.dialog.set_body(self._progress_text())
        return GLib.SOURCE_CONTINUE

    def _on_window_close(self, _window):
        self.finish(False)
        return False  # let the close proceed

    ###########################################################################
    # Teardown
    ###########################################################################

    def finish(self, completed):
        if self.finished:
            return
        self.finished = True
        window = self.window

        if self.timer_id is not None:
            GLib.source_remove(self.timer_id)
            self.timer_id = None
        if self.reading_id is not None and window.monitor is not None:
            window.monitor.disconnect(self.reading_id)
            self.reading_id = None
        if self.close_id is not None:
            window.disconnect(self.close_id)
            self.close_id = None
        if self.dialog is not None:
            self.dialog.close()
            self.dialog = None
        window.calibration = None

        # Restoring the fans matters more than reporting the result, so it
        # happens first and unconditionally.
        try:
            profiles.apply_cooler_booster(
                window.controller, window.config, self.restore_booster
            )
        except ECError as error:
            window._show_error(error)
            return

        if not completed:
            window.toasts.add_toast(Adw.Toast.new("Fan measurement stopped"))
            return

        config = window.config
        config.cpu_rpm_peak = max(config.cpu_rpm_peak, self.peaks["cpu"])
        config.gpu_rpm_peak = max(config.gpu_rpm_peak, self.peaks["gpu"])
        config.fan_rpm_calibrated = True
        cfg.save(config)
        window.note_rpm_peaks_saved()
        if window.graph is not None:
            window.graph.queue_draw()
        window.toasts.add_toast(
            Adw.Toast.new(
                f"Maximum fan speed: {config.cpu_rpm_peak} CPU, "
                f"{config.gpu_rpm_peak} GPU RPM"
            )
        )


class FirstRunWindow(Adw.Window):
    """Replaces the two chained Gtk.Dialogs the old build used at first start.

    Those dialogs called dialog.run() and then show_all() on an already
    destroyed widget, and left the return value unbound on the cancel path.
    """

    def __init__(self, parent, controller, on_finished):
        super().__init__(
            transient_for=parent,
            modal=True,
            title="Set up Open Freeze Center",
            default_width=580,
            default_height=520,
        )
        self.controller = controller
        self.on_finished = on_finished

        page = Adw.PreferencesPage()

        cpu_group = Adw.PreferencesGroup(
            title="Processor generation",
            description="The EC uses different registers on either side of "
            "Intel's 11th generation. Pick the wrong one and fan control will "
            "not take effect.",
        )
        self.cpu_row = Adw.ComboRow(
            title="CPU generation",
            model=Gtk.StringList.new(["11th gen or newer", "10th gen or older"]),
        )
        cpu_group.add(self.cpu_row)
        page.add(cpu_group)

        curve_group = Adw.PreferencesGroup(
            title="Auto fan curve",
            description="Read the curve the firmware is using right now, or "
            "start from a known-good generic curve. To capture MSI's own "
            "curve, boot Windows, set the fan profile to Auto there, then "
            "come back and read it from the EC.",
        )
        self.curve_row = Adw.ComboRow(
            title="Source",
            model=Gtk.StringList.new(["Read from the EC", "Generic curve"]),
        )
        curve_group.add(self.curve_row)
        page.add(curve_group)

        continue_button = Gtk.Button(label="Continue")
        continue_button.add_css_class("suggested-action")
        continue_button.connect("clicked", self._on_continue)

        header = Adw.HeaderBar()
        header.set_show_end_title_buttons(False)
        header.pack_end(continue_button)

        toolbar = Adw.ToolbarView()
        toolbar.add_top_bar(header)
        toolbar.set_content(page)
        self.set_content(toolbar)

    def _on_continue(self, _button):
        gen_11_plus = self.cpu_row.get_selected() == 0
        config = cfg.Config(hardware=cfg.Hardware.for_cpu_generation(gen_11_plus))

        if self.curve_row.get_selected() == 0:
            try:
                cpu, gpu = profiles.read_auto_curve(self.controller, config)
                if any(cpu) or any(gpu):
                    config.auto_cpu, config.auto_gpu = cpu, gpu
            except ECError:
                pass  # fall back to the generic curve baked into Config

        config.advanced_cpu = list(config.auto_cpu)
        config.advanced_gpu = list(config.auto_gpu)
        config = config.normalised()
        cfg.save(config)
        self.close()
        self.on_finished(config)


class MainWindow(Adw.ApplicationWindow):
    def __init__(self, application, controller):
        super().__init__(
            application=application,
            title="Open Freeze Center",
            default_width=560,
            default_height=800,
        )
        self.controller = controller
        self.config = None
        self.monitor = None
        self.graph = None
        self.curve_page = None
        self.first_run = None
        self.calibration = None
        self._loading = False
        self._rpm_peak_saved = 0

        self.toasts = Adw.ToastOverlay()
        self.navigation = Adw.NavigationView()
        self.toasts.set_child(self.navigation)
        self.set_content(self.toasts)

        self.navigation.push(self._build_main_page())
        GLib.idle_add(self._start)

    ###########################################################################
    # Page construction
    ###########################################################################

    def _build_main_page(self):
        header = Adw.HeaderBar()

        menu = Gtk.MenuButton(icon_name="open-menu-symbolic", tooltip_text="Main Menu")
        model = Gtk.Builder.new_from_string(MENU_XML, -1).get_object("primary-menu")
        menu.set_menu_model(model)
        header.pack_end(menu)

        self.status_stack = Gtk.Stack()
        self.status_stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
        self.status_stack.add_named(self._build_controls(), "controls")
        self.status_stack.add_named(Adw.StatusPage(), "error")

        toolbar = Adw.ToolbarView()
        toolbar.add_top_bar(header)
        toolbar.set_content(self.status_stack)
        return Adw.NavigationPage(child=toolbar, title="Open Freeze Center")

    def _build_controls(self):
        page = Adw.PreferencesPage()

        # -- Cooling -----------------------------------------------------------
        cooling = Adw.PreferencesGroup(title="Cooling")

        self.profile_row = Adw.ComboRow(
            title="Fan profile",
            model=Gtk.StringList.new(
                [profiles.PROFILE_LABELS[name] for name in cfg.PROFILE_ORDER]
            ),
        )
        self.profile_row.connect("notify::selected", self._on_profile_changed)
        cooling.add(self.profile_row)

        self.offset_row = Adw.SpinRow.new_with_range(cfg.OFFSET_MIN, cfg.OFFSET_MAX, 1)
        self.offset_row.set_title("Speed offset")
        self.offset_row.set_subtitle("Percentage points added to the auto curve")
        self.offset_row.connect("notify::value", self._on_offset_changed)
        cooling.add(self.offset_row)

        self.curve_row = Adw.ActionRow(
            title="Fan curves",
            subtitle="Set the CPU and GPU curve point by point",
            activatable=True,
        )
        self.curve_row.add_suffix(Gtk.Image.new_from_icon_name("go-next-symbolic"))
        self.curve_row.connect("activated", self._on_open_curves)
        cooling.add(self.curve_row)

        self.booster_row = Adw.SwitchRow(
            title="Cooler Booster",
            subtitle="Run both fans flat out, whatever the profile says",
        )
        self.booster_row.connect("notify::active", self._on_booster_changed)
        cooling.add(self.booster_row)

        page.add(cooling)

        # -- Monitoring --------------------------------------------------------
        monitoring = Adw.PreferencesGroup(title="Monitoring")

        reset = Gtk.Button(label="Reset")
        reset.set_tooltip_text("Forget the recorded minimum and maximum")
        reset.add_css_class("flat")
        reset.connect("clicked", self._on_reset_extremes)
        monitoring.set_header_suffix(reset)

        chart_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=14)
        chart_box.add_css_class("card")
        chart_box.add_css_class("ofc-chart")
        self.graph_placeholder = chart_box
        self.readings = ReadingsTable()
        chart_box.append(self.readings)
        monitoring.add(chart_box)
        page.add(monitoring)

        # -- Battery -----------------------------------------------------------
        battery = Adw.PreferencesGroup(
            title="Battery",
            description="Stopping short of a full charge slows down long-term "
            "battery wear.",
        )
        self.battery_row = Adw.ComboRow(
            title="Charge limit",
            subtitle="Percent",
            model=Gtk.StringList.new(BATTERY_CHOICES),
        )
        self.battery_row.connect("notify::selected", self._on_battery_changed)
        battery.add(self.battery_row)
        page.add(battery)

        return page

    ###########################################################################
    # Start-up
    ###########################################################################

    def _start(self):
        try:
            self.controller.check()
        except ECError as error:
            self._show_error(error)
            return GLib.SOURCE_REMOVE

        config = cfg.load()
        if config is None:
            # Held on the window so it is not collected while it is on screen.
            self.first_run = FirstRunWindow(self, self.controller, self._activate_config)
            self.first_run.present()
        else:
            self._activate_config(config)
        return GLib.SOURCE_REMOVE

    def _activate_config(self, config):
        self.config = config
        self._sync_widgets()

        # Re-assert the saved profile, so a reboot does not silently drop the
        # user back onto the firmware curve.
        try:
            profiles.apply_profile(self.controller, config)
            profiles.apply_battery_threshold(
                self.controller, config, config.battery_threshold
            )
        except ECError as error:
            self._show_error(error)
            return

        self.monitor = Monitor(self.controller, config)
        self.monitor.connect("reading", self._on_reading)
        self.monitor.connect("failed", lambda _m, error: self._show_error(error))
        self.graph = SensorGraph(self.monitor, config)
        self.graph_placeholder.prepend(self.graph)
        self.note_rpm_peaks_saved()
        self.monitor.start()
        self.status_stack.set_visible_child_name("controls")

        # Once, on a config that has never been asked - which includes every
        # fresh install, since the peaks start at zero and the axis would
        # otherwise have to learn them from an idle fan.
        if not config.fan_rpm_calibrated and not config.fan_rpm_asked:
            GLib.timeout_add(700, lambda: (self.calibrate_fans(), GLib.SOURCE_REMOVE)[1])

    def _show_error(self, error):
        if self.calibration is not None:
            # Whatever else is wrong, do not leave the fans pinned on.
            self.calibration.finish(False)
        if self.monitor is not None:
            self.monitor.stop()
        title = getattr(error, "title", "Something went wrong")
        detail = getattr(error, "detail", str(error))
        hint = getattr(error, "hint", "")

        status = Adw.StatusPage(
            icon_name="dialog-warning-symbolic",
            title=title,
            description=detail + (f"\n\n{hint}" if hint else ""),
        )
        retry = Gtk.Button(label="Try Again")
        retry.add_css_class("pill")
        retry.add_css_class("suggested-action")
        retry.set_halign(Gtk.Align.CENTER)
        retry.connect("clicked", lambda _b: self._retry())
        status.set_child(retry)

        old = self.status_stack.get_child_by_name("error")
        if old is not None:
            self.status_stack.remove(old)
        self.status_stack.add_named(status, "error")
        self.status_stack.set_visible_child_name("error")

    def _retry(self):
        if self.monitor is not None:
            self.monitor.stop()
            self.monitor = None
        if self.config is not None and self.graph is not None:
            self.graph_placeholder.remove(self.graph)
            self.graph = None
        self._start()

    ###########################################################################
    # Widget <-> config
    ###########################################################################

    def _sync_widgets(self):
        self._loading = True
        config = self.config
        self.profile_row.set_selected(cfg.PROFILE_ORDER.index(config.profile))
        self.profile_row.set_subtitle(profiles.PROFILE_DESCRIPTIONS[config.profile])
        self.offset_row.set_value(config.basic_offset)
        self.offset_row.set_visible(config.profile == cfg.PROFILE_BASIC)
        self.curve_row.set_visible(config.profile == cfg.PROFILE_ADVANCED)
        self.booster_row.set_active(config.cooler_booster)
        try:
            self.battery_row.set_selected(
                BATTERY_CHOICES.index(str(config.battery_threshold))
            )
        except ValueError:
            self.battery_row.set_selected(len(BATTERY_CHOICES) - 1)
        self._loading = False

    def _persist_and_apply(self, message=None):
        cfg.save(self.config)
        try:
            profiles.apply_profile(self.controller, self.config)
        except ECError as error:
            self._show_error(error)
            return
        if message:
            self.toasts.add_toast(Adw.Toast.new(message))

    ###########################################################################
    # Handlers
    ###########################################################################

    def _on_profile_changed(self, row, _param):
        if self._loading or self.config is None:
            return
        self.config.profile = cfg.PROFILE_ORDER[row.get_selected()]
        self._sync_widgets()
        self._persist_and_apply(
            f"{profiles.PROFILE_LABELS[self.config.profile]} profile applied"
        )

    def _on_offset_changed(self, row, _param):
        if self._loading or self.config is None:
            return
        self.config.basic_offset = int(row.get_value())
        self._persist_and_apply()

    def _on_booster_changed(self, row, _param):
        if self._loading or self.config is None:
            return
        self.config.cooler_booster = row.get_active()
        cfg.save(self.config)
        try:
            profiles.apply_cooler_booster(
                self.controller, self.config, self.config.cooler_booster
            )
        except ECError as error:
            self._show_error(error)
            return
        self.toasts.add_toast(
            Adw.Toast.new(
                "Cooler Booster on" if self.config.cooler_booster else "Cooler Booster off"
            )
        )

    def _on_battery_changed(self, row, _param):
        if self._loading or self.config is None:
            return
        self.config.battery_threshold = int(BATTERY_CHOICES[row.get_selected()])
        cfg.save(self.config)
        try:
            profiles.apply_battery_threshold(
                self.controller, self.config, self.config.battery_threshold
            )
        except ECError as error:
            self._show_error(error)
            return
        self.toasts.add_toast(
            Adw.Toast.new(f"Charging stops at {self.config.battery_threshold}%")
        )

    def _on_open_curves(self, _row):
        if self.config is None:
            return
        if self.curve_page is None:
            self.curve_page = CurveEditorPage(self.config, self._persist_and_apply)
        else:
            self.curve_page.refresh()
        self.navigation.push(self.curve_page)

    def _on_reset_extremes(self, _button):
        if self.monitor is not None:
            self.monitor.reset_extremes()

    def calibrate_fans(self):
        """Offer to measure the fans' top speed. Also the main menu item."""
        if self.config is None or self.monitor is None or self.calibration is not None:
            return
        self.calibration = FanCalibration(self)
        self.calibration.offer()

    def note_rpm_peaks_saved(self):
        """Mark the stored peaks as being what is on disk."""
        self._rpm_peak_saved = max(self.config.cpu_rpm_peak, self.config.gpu_rpm_peak)

    def _record_rpm_peaks(self, reading):
        """Raise the stored peaks to match anything faster we just saw.

        A measured ceiling is the good case, but it is not the only one: a
        machine that was never measured, or one whose fans turn out to go
        faster than they did during the measurement, still ends up with an
        axis that fits. Writing only once the peak has moved meaningfully
        keeps this off the disk twice a second.
        """
        config = self.config
        config.cpu_rpm_peak = min(
            max(config.cpu_rpm_peak, reading.cpu_rpm), cfg.RPM_PEAK_MAX
        )
        config.gpu_rpm_peak = min(
            max(config.gpu_rpm_peak, reading.gpu_rpm), cfg.RPM_PEAK_MAX
        )
        peak = max(config.cpu_rpm_peak, config.gpu_rpm_peak)
        if peak >= self._rpm_peak_saved + 100:
            cfg.save(config)
            self._rpm_peak_saved = peak

    def _on_reading(self, monitor, reading):
        self.readings.update(monitor, reading)
        self._record_rpm_peaks(reading)
        self.graph.queue_draw()


MENU_XML = """
<?xml version="1.0" encoding="UTF-8"?>
<interface>
  <menu id="primary-menu">
    <section>
      <item>
        <attribute name="label">Measure Maximum Fan Speed</attribute>
        <attribute name="action">app.calibrate-fans</attribute>
      </item>
      <item>
        <attribute name="label">Open Config Folder</attribute>
        <attribute name="action">app.open-config</attribute>
      </item>
    </section>
    <section>
      <item>
        <attribute name="label">Project Website</attribute>
        <attribute name="action">app.website</attribute>
      </item>
      <item>
        <attribute name="label">Report an Issue</attribute>
        <attribute name="action">app.report-issue</attribute>
      </item>
    </section>
    <section>
      <item>
        <attribute name="label">About Open Freeze Center</attribute>
        <attribute name="action">app.about</attribute>
      </item>
      <item>
        <attribute name="label">Quit</attribute>
        <attribute name="action">app.quit</attribute>
      </item>
    </section>
  </menu>
</interface>
"""
