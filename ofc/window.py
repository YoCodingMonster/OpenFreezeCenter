"""The main window, the first-run assistant, and the EC error page."""

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gtk, GLib, Pango

from . import config as cfg
from . import profiles
from . import style
from .curve_editor import CurveEditorPage
from .ec import ECError
from .monitor import Monitor
from .power import PowerMeters
from .section import Section
from .widgets import METRIC_NAMES, LegendSwatch, SensorGraph

BATTERY_CHOICES = [str(value) for value in range(cfg.BATTERY_MIN, cfg.BATTERY_MAX + 1, 5)]


class ReadingsTable(Gtk.Grid):
    """The numeric view of what the graph plots.

    The chart carries the shape of the last minute; this carries the exact
    current value, and the running minimum and maximum, which a sixty-second
    window cannot show.

    It also carries every quantity, not just the two the chart is plotting.
    The chart can only show two at once without one of the scales becoming a
    lie; a column of numbers has no such limit, so nothing is ever hidden by
    the choice of axes — only drawn or not drawn.

    The unit lives in the column heading, not in each cell: five columns have
    to fit a 360px window, and "20.7" repeated is legible where "20.7 W" is
    not.
    """

    COLUMNS = ("Now", "Min", "Max", "Watts", "Fan")
    FIELDS = ("now", "min", "max", "watts", "rpm")

    def __init__(self):
        super().__init__(column_spacing=style.px(6), row_spacing=style.px(6))
        self.set_column_homogeneous(True)
        self.cells = {}

        for index, title in enumerate(self.COLUMNS):
            label = Gtk.Label(label=title, xalign=0.5)
            label.add_css_class("dim-label")
            label.add_css_class("caption")
            self.attach(label, index + 1, 0, 1, 1)

        for row, (key, name) in enumerate((("cpu", "CPU"), ("gpu", "GPU")), start=1):
            heading = Gtk.Box(spacing=style.px(8))
            heading.append(LegendSwatch(key))
            title = Gtk.Label(label=name, xalign=0.0)
            title.add_css_class("heading")
            heading.append(title)
            self.attach(heading, 0, row, 1, 1)

            for column, field in enumerate(self.FIELDS):
                value = Gtk.Label(label="—", xalign=0.5)
                value.add_css_class("ofc-reading")
                value.set_hexpand(True)
                self.attach(value, column + 1, row, 1, 1)
                self.cells[(key, field)] = value

    @staticmethod
    def watts(value):
        """Watts in four characters, which is all the column has room for."""
        if value is None:
            return "off"
        return f"{value:.0f}" if value >= 10 else f"{value:.1f}"

    def update(self, monitor, reading):
        pairs = (
            (
                "cpu",
                reading.cpu_temp,
                monitor.cpu_min,
                monitor.cpu_max,
                reading.cpu_watts,
                reading.cpu_rpm,
            ),
            (
                "gpu",
                reading.gpu_temp,
                monitor.gpu_min,
                monitor.gpu_max,
                reading.gpu_watts,
                reading.gpu_rpm,
            ),
        )
        for key, now, low, high, watts, rpm in pairs:
            # "off" rather than 0: a chip that is powered down has neither a
            # temperature nor a wattage, and the same word already stands for
            # a fan that is not turning.
            self.cells[(key, "now")].set_label(
                f"{now}°C" if now is not None else "off"
            )
            self.cells[(key, "min")].set_label(f"{low}°C" if low < 999 else "—")
            self.cells[(key, "max")].set_label(f"{high}°C" if high else "—")
            self.cells[(key, "watts")].set_label(self.watts(watts))
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
            # The assistant is a page of prose with two rows under it, and
            # prose did not shrink — only the gaps around it did. So the
            # width takes the 60% and the height is what the text needs at
            # that width, rather than 60% of what it needed at the old one.
            # It is asked once, and both choices have to be on screen.
            default_width=style.px(580),
            default_height=380,
        )
        self.add_css_class("ofc-compact")
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
    def __init__(self, application, controller, meters=None):
        super().__init__(
            application=application,
            title="Open Freeze Center",
            default_width=style.px(560),
            # No default height. The window takes the height of whatever it
            # is showing, which is the point of sections that fold away; see
            # _fit_to_content.
        )
        self.add_css_class("ofc-compact")
        self.controller = controller
        # Watts do not come from the EC, so they do not come from the
        # controller either; a simulated run wants simulated power for the
        # same reason it wants a simulated EC.
        self.meters = meters if meters is not None else PowerMeters.detect()
        self.config = None
        self.monitor = None
        self.graph = None
        self.curve_page = None
        self.first_run = None
        self.calibration = None
        self._loading = False
        self._fit_queued = False
        self._rpm_peak_saved = 0
        self._watt_peak_saved = 0.0

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

        # Not homogeneous: a stack sized to its tallest child would hold the
        # window open at the height of the error page nobody is looking at.
        self.status_stack = Gtk.Stack(hhomogeneous=False, vhomogeneous=False)
        self.status_stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
        self.status_stack.add_named(self._build_controls(), "controls")
        self.status_stack.add_named(Adw.StatusPage(), "error")

        toolbar = Adw.ToolbarView()
        toolbar.add_top_bar(header)
        toolbar.set_content(self.status_stack)

        page = Adw.NavigationPage(child=toolbar, title="Open Freeze Center")
        # ::shown, not the view's ::notify::visible-page, which fires as the
        # transition starts and would measure the page being navigated away
        # from.
        page.connect("shown", self._queue_fit)
        return page

    def _build_controls(self):
        # Adw.PreferencesPage takes preferences groups and nothing else, so the
        # page it would have built is assembled here instead: the same clamp,
        # the same margins, the same gap between groups, all at the compact
        # scale, with a collapsible Section in place of each group.
        page = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, spacing=style.SECTION_SPACING
        )
        page.set_margin_top(style.PAGE_MARGIN)
        page.set_margin_bottom(style.PAGE_MARGIN)
        page.set_margin_start(style.PAGE_MARGIN)
        page.set_margin_end(style.PAGE_MARGIN)

        # -- Cooling -----------------------------------------------------------
        cooling = Section("Cooling")
        self.cooling_section = cooling

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

        page.append(cooling)

        # -- Monitoring --------------------------------------------------------
        monitoring = Section("Monitoring")
        self.monitoring_section = monitoring

        reset = Gtk.Button(label="Reset")
        reset.set_tooltip_text("Forget the recorded minimum and maximum")
        reset.add_css_class("flat")
        reset.connect("clicked", self._on_reset_extremes)
        monitoring.set_header_suffix(reset)

        # Which two of the three measurements the chart plots. The forms are
        # not a choice: a line reads against the left axis and an area against
        # the right, and that pairing is what lets two scales share one plot.
        #
        # Side by side, one half of the width each, because the two are read
        # as a pair — left against right, exactly as they appear on the chart
        # — and stacked they read as two unrelated settings. A settings row
        # cannot be halved this far and keep a title, a subtitle and a value
        # legible, so each half is the caption over the control instead, which
        # is what the width can carry.
        axes = Gtk.Box(spacing=style.px(12), homogeneous=True)
        axes.set_margin_bottom(style.px(10))
        self.left_axis = self._axis_chooser(axes, "Left axis · line", "left")
        self.right_axis = self._axis_chooser(axes, "Right axis · area", "right")
        monitoring.add(axes)

        chart_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=style.px(14))
        chart_box.add_css_class("card")
        chart_box.add_css_class("ofc-chart")
        self.graph_placeholder = chart_box
        self.readings = ReadingsTable()
        chart_box.append(self.readings)
        monitoring.add(chart_box)
        page.append(monitoring)

        # -- Battery -----------------------------------------------------------
        battery = Section(
            "Battery",
            description="Stopping short of a full charge slows down long-term "
            "battery wear.",
        )
        self.battery_section = battery
        self.battery_row = Adw.ComboRow(
            title="Charge limit",
            subtitle="Percent",
            model=Gtk.StringList.new(BATTERY_CHOICES),
        )
        self.battery_row.connect("notify::selected", self._on_battery_changed)
        battery.add(self.battery_row)
        page.append(battery)

        for section in (cooling, monitoring, battery):
            section.connect("resized", self._queue_fit)

        self._update_summaries()

        clamp = Adw.Clamp(maximum_size=style.CLAMP_WIDTH, child=page)
        # propagate-natural-height is what carries the content's height out
        # to the window. Without it a scroller asks for almost nothing and
        # the window has no size to take.
        return Gtk.ScrolledWindow(
            hscrollbar_policy=Gtk.PolicyType.NEVER,
            propagate_natural_height=True,
            vexpand=True,
            child=clamp,
        )

    def _axis_chooser(self, box, caption, side):
        """One half of the axis pair: a caption over its dropdown."""
        label = Gtk.Label(label=caption, xalign=0.0)
        label.add_css_class("dim-label")
        label.add_css_class("caption")
        label.set_ellipsize(Pango.EllipsizeMode.END)

        chooser = Gtk.DropDown(
            model=Gtk.StringList.new(
                [METRIC_NAMES[name] for name in cfg.METRIC_ORDER]
            ),
        )
        chooser.set_tooltip_text(caption)
        # The caption is the control's name as far as anything reading the
        # window aloud is concerned; without this the dropdown announces only
        # whichever metric it happens to be showing.
        chooser.update_property([Gtk.AccessibleProperty.LABEL], [caption])
        chooser.connect("notify::selected", self._on_axis_changed, side)

        half = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=style.px(4))
        half.append(label)
        half.append(chooser)
        box.append(half)
        return chooser

    def _queue_fit(self, *_args):
        """Retake the window's height once the layout has settled.

        From an idle, and only once per round of changes, because the caller
        has usually just shown or hidden something and the natural height it
        would measure right now is the one it is on its way out of.
        """
        if self._fit_queued:
            return
        self._fit_queued = True
        GLib.idle_add(self._fit_to_content, priority=GLib.PRIORITY_LOW)

    def _fit_to_content(self):
        """Take the height of whatever is on screen, keeping the width.

        GTK sizes a window to its content once, when it is first mapped, and
        after that will grow it but never shrink it. Handing it a fresh
        default size with the height left open — the width pinned to what it
        already is, so this never fights a horizontal resize — makes it
        measure again and follow, which is what a window whose sections fold
        away has to do for the folding to be worth anything.

        A window the user has maximised or filled the screen with is theirs,
        and one that has not been mapped has no width worth keeping.
        """
        self._fit_queued = False
        if not self.get_mapped() or self.is_maximized() or self.is_fullscreen():
            return GLib.SOURCE_REMOVE
        self.set_default_size(self.get_width(), -1)
        return GLib.SOURCE_REMOVE

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

        self.monitor = Monitor(self.controller, config, meters=self.meters)
        self.monitor.connect("reading", self._on_reading)
        self.monitor.connect("failed", lambda _m, error: self._show_error(error))
        self.graph = SensorGraph(self.monitor, config)
        self.graph_placeholder.prepend(self.graph)
        self.note_rpm_peaks_saved()
        self.monitor.start()
        self.status_stack.set_visible_child_name("controls")
        self._queue_fit()

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
        self._queue_fit()

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
        self.left_axis.set_selected(cfg.METRIC_ORDER.index(config.graph_left))
        self.right_axis.set_selected(cfg.METRIC_ORDER.index(config.graph_right))
        try:
            self.battery_row.set_selected(
                BATTERY_CHOICES.index(str(config.battery_threshold))
            )
        except ValueError:
            self.battery_row.set_selected(len(BATTERY_CHOICES) - 1)
        self._loading = False
        self._update_summaries()
        self._queue_fit()

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
    # Section summaries
    ###########################################################################

    def _update_summaries(self, reading=None):
        """Restate each section as the one line its collapsed header shows.

        Everything a closed section holds has to be legible from this, or
        closing it would cost the user information rather than space. The
        monitoring line is the one that moves, so it is refreshed from the
        reading itself; the other two change only when a setting does.
        """
        config = self.config
        if config is None:
            for section in (
                self.cooling_section,
                self.monitoring_section,
                self.battery_section,
            ):
                section.set_summary("Starting up…")
            return

        profile = profiles.PROFILE_LABELS[config.profile]
        if config.profile == cfg.PROFILE_BASIC:
            profile += f" {config.basic_offset:+d}%"
        self.cooling_section.set_summary(
            f"{profile} · Booster {'on' if config.cooler_booster else 'off'}"
        )

        if reading is not None:
            # Each chip keeps its own three numbers together rather than the
            # two of them sharing a tail of fan speeds, which reads better and
            # is also the only arrangement that fits: with a unit on the fans
            # as well, the line runs past the width of the header and gets
            # ellipsised mid-number. A chip that is powered down says so once.
            def chip(temp, watts, rpm):
                parts = []
                if temp is not None:
                    parts.append(f"{temp}°")
                if watts is not None:
                    parts.append(f"{ReadingsTable.watts(watts)}W")
                if rpm:
                    parts.append(str(rpm))
                return " ".join(parts) if parts else "off"

            self.monitoring_section.set_summary(
                f"CPU {chip(reading.cpu_temp, reading.cpu_watts, reading.cpu_rpm)} · "
                f"GPU {chip(reading.gpu_temp, reading.gpu_watts, reading.gpu_rpm)}"
            )
        elif self.monitor is None or self.monitor.latest is None:
            self.monitoring_section.set_summary("Waiting for the first reading…")

        self.battery_section.set_summary(
            f"Charging stops at {config.battery_threshold}%"
        )

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
        self._update_summaries()
        self._persist_and_apply()

    def _on_booster_changed(self, row, _param):
        if self._loading or self.config is None:
            return
        self.config.cooler_booster = row.get_active()
        self._update_summaries()
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
        self._update_summaries()
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

    def _on_axis_changed(self, row, _param, side):
        """Move a metric onto an axis, pushing whatever was there aside.

        The two axes cannot show the same quantity — one of the scales would
        be a duplicate of the other and the area would sit exactly under the
        line. Rather than refuse the choice, the metric already on the other
        axis takes the place being vacated, so picking one thing always
        leaves a valid pair and never a rejected click.
        """
        if self._loading or self.config is None:
            return
        config = self.config
        chosen = cfg.METRIC_ORDER[row.get_selected()]
        other = config.graph_right if side == "left" else config.graph_left
        previous = config.graph_left if side == "left" else config.graph_right
        if chosen == other:
            other = previous
        if side == "left":
            config.graph_left, config.graph_right = chosen, other
        else:
            config.graph_right, config.graph_left = chosen, other

        self._sync_widgets()
        cfg.save(config)
        if self.graph is not None:
            self.graph.queue_draw()

    def _on_open_curves(self, _row):
        if self.config is None:
            return
        if self.curve_page is None:
            self.curve_page = CurveEditorPage(self.config, self._persist_and_apply)
            self.curve_page.connect("shown", self._queue_fit)
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
        self._watt_peak_saved = max(
            self.config.cpu_watt_peak, self.config.gpu_watt_peak
        )

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

    def _record_watt_peaks(self, reading):
        """The same for the power axis, which has no published ceiling.

        The CPU's RAPL package limit reads 200 W on this class of machine,
        which no laptop draws, and the GPU's varies with whatever power
        profile the firmware is in. What has actually been measured is the
        only honest scale, so the axis is grown from that.
        """
        config = self.config
        for attribute, watts in (
            ("cpu_watt_peak", reading.cpu_watts),
            ("gpu_watt_peak", reading.gpu_watts),
        ):
            if watts is None:
                continue
            current = getattr(config, attribute)
            setattr(config, attribute, min(max(current, watts), cfg.WATT_PEAK_MAX))

        peak = max(config.cpu_watt_peak, config.gpu_watt_peak)
        if peak >= self._watt_peak_saved + 5:
            cfg.save(config)
            self._watt_peak_saved = peak

    def _on_reading(self, monitor, reading):
        self.readings.update(monitor, reading)
        self._update_summaries(reading)
        self._record_rpm_peaks(reading)
        self._record_watt_peaks(reading)
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
