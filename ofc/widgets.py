"""The live temperature chart and the fan curve preview.

Drawn with GSK paths rather than Cairo, so the application needs nothing
beyond PyGObject itself — the Cairo bridge (gi._gi_cairo) is a separate
distro package that is easy to end up without.

Both charts use the same two-colour categorical assignment, fixed per
entity: slot 1 blue for the CPU, slot 2 orange for the GPU, never cycled.
The pair is validated against the Adwaita card surface in both modes —
worst adjacent CVD ΔE 24.7 light / 26.8 dark, normal-vision 33.6 / 31.8,
both series at or above 3:1 contrast.

Fan speed shares the sensor chart with temperature but not its axis: it is
a filled area read against a second scale on the right. Encoding it as a
tint of the same series colour keeps one colour per entity, and the change
of form — fill against line — is what separates the two quantities.
"""

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Gsk", "4.0")
gi.require_version("Graphene", "1.0")
from gi.repository import Adw, Gdk, Graphene, Gsk, Gtk, Pango

from .style import chart_height

# (light, dark) steps per series.
SERIES_COLORS = {
    "cpu": ("#2a78d6", "#3987e5"),
    "gpu": ("#eb6834", "#d95926"),
}

# Ink and rules stay neutral: colour identifies a series, never the text.
INK = {
    "primary": ("#0b0b0b", "#ffffff"),
    "secondary": ("#52514e", "#c3c2b7"),
    "grid": ("#e6e6e3", "#454542"),
    "surface": ("#ffffff", "#353535"),
}

# The fan areas are the same colours held well back. The fill is faint on
# purpose: two of them overlap for most of the plot, and anything stronger
# blends into one mass that reads as a third colour and buries the
# temperature lines. What carries a fan series is its stroked top edge, so
# that is where the weight goes; the fill only says which side is under it.
FILL_ALPHA = (0.11, 0.15)
EDGE_ALPHA = (0.70, 0.75)
SWATCH_ALPHA = 0.45

TEMP_MAX = 100.0
GRID_STEPS = (0, 25, 50, 75, 100)

# The RPM axis is quantised up to a multiple of this, which keeps both the
# ceiling and the quarter-way gridline labels round whatever the peak is.
RPM_STEP = 1000


def _rgba(hex_colour, alpha=1.0):
    colour = Gdk.RGBA()
    colour.parse(hex_colour)
    colour.alpha = alpha
    return colour


def _is_dark():
    return Adw.StyleManager.get_default().get_dark()


def ink(role):
    return INK[role][_is_dark()]


def series_colour(name):
    return SERIES_COLORS[name][_is_dark()]


def _stroke(width):
    stroke = Gsk.Stroke.new(width)
    stroke.set_line_cap(Gsk.LineCap.ROUND)
    stroke.set_line_join(Gsk.LineJoin.ROUND)
    return stroke


def _polyline(snapshot, points, colour, width=2.0):
    if len(points) < 2:
        if points:
            _dot(snapshot, points[0][0], points[0][1], width / 2, colour)
        return
    builder = Gsk.PathBuilder.new()
    builder.move_to(*points[0])
    for point in points[1:]:
        builder.line_to(*point)
    snapshot.append_stroke(builder.to_path(), _stroke(width), _rgba(colour))


def _area(snapshot, points, baseline, colour, fill_alpha, edge_alpha):
    """Fill a series down to `baseline`, then stroke its top edge."""
    if len(points) < 2:
        return
    builder = Gsk.PathBuilder.new()
    builder.move_to(points[0][0], baseline)
    for point in points:
        builder.line_to(*point)
    builder.line_to(points[-1][0], baseline)
    builder.close()
    snapshot.append_fill(
        builder.to_path(), Gsk.FillRule.WINDING, _rgba(colour, fill_alpha)
    )

    edge = Gsk.PathBuilder.new()
    edge.move_to(*points[0])
    for point in points[1:]:
        edge.line_to(*point)
    snapshot.append_stroke(edge.to_path(), _stroke(1.25), _rgba(colour, edge_alpha))


def _rect(snapshot, x, y, width, height, colour, alpha=1.0):
    builder = Gsk.PathBuilder.new()
    builder.add_rect(Graphene.Rect().init(x, y, width, height))
    snapshot.append_fill(builder.to_path(), Gsk.FillRule.WINDING, _rgba(colour, alpha))


def _hline(snapshot, x1, x2, y, colour):
    builder = Gsk.PathBuilder.new()
    builder.move_to(x1, y)
    builder.line_to(x2, y)
    snapshot.append_stroke(builder.to_path(), Gsk.Stroke.new(1.0), _rgba(colour))


def _dot(snapshot, x, y, radius, colour):
    builder = Gsk.PathBuilder.new()
    builder.add_circle(Graphene.Point().init(x, y), radius)
    snapshot.append_fill(builder.to_path(), Gsk.FillRule.WINDING, _rgba(colour))


class _ChartBase(Gtk.Widget):
    """Shared text helper and dark-mode invalidation."""

    def __init__(self):
        super().__init__()
        Adw.StyleManager.get_default().connect(
            "notify::dark", lambda *_: self.queue_draw()
        )

    def _label(self, text, size):
        layout = self.create_pango_layout(text)
        description = layout.get_context().get_font_description()
        description = description.copy() if description else Pango.FontDescription()
        description.set_size(int(size * Pango.SCALE))
        layout.set_font_description(description)
        return layout, layout.get_pixel_size()

    def _text(self, snapshot, x, y, text, colour, size=8, align="left"):
        """Draw text with (x, y) as the left/right/centre of its vertical middle."""
        layout, (width, height) = self._label(text, size)
        if align == "right":
            x -= width
        elif align == "center":
            x -= width / 2
        snapshot.save()
        snapshot.translate(Graphene.Point().init(x, y - height / 2))
        snapshot.append_layout(layout, _rgba(colour))
        snapshot.restore()
        return width, height


class SensorGraph(_ChartBase):
    """Sixty seconds of CPU and GPU temperature and fan speed.

    Temperature is a line on the left 0–100 °C axis: both series measure the
    same quantity in the same unit, so they share it. Fan speed is a
    different quantity on a different scale, so it gets the right-hand RPM
    axis and a different form — a filled area, held back far enough that the
    temperature lines stay the foreground of the chart.
    """

    def __init__(self, monitor, config):
        super().__init__()
        self.monitor = monitor
        self.config = config
        # 26 above for the legend, 18 below for the unit labels; see do_snapshot.
        self.set_size_request(-1, chart_height(168, 26 + 18))
        self.set_hexpand(True)

    def _fan_ceiling(self):
        """The RPM axis top: the stored peak, rounded up to a round number.

        Scaling from the peak the fans have ever reached rather than from the
        peak in the visible sixty seconds is what keeps the axis still. The
        stored value only ever grows, so the axis cannot rescale downwards
        under a plot the user is in the middle of reading.
        """
        peak = max(self.config.cpu_rpm_peak, self.config.gpu_rpm_peak)
        return max(RPM_STEP, -(-peak // RPM_STEP) * RPM_STEP)

    def do_snapshot(self, snapshot):
        width = self.get_width()
        height = self.get_height()
        if width < 2 or height < 2:
            return

        ink_secondary = ink("secondary")
        ink_primary = ink("primary")
        dark = _is_dark()

        # The right margin carries two things side by side: the temperature
        # value at the end of each line, then the RPM axis beyond it.
        left, right, top, bottom = 36, 78, 26, 18
        plot_width = max(1, width - left - right)
        plot_height = max(1, height - top - bottom)
        baseline = top + plot_height
        fan_ceiling = self._fan_ceiling()

        # Grid: hairline, recessive, labelled in muted ink. One set of rules
        # for both axes, so neither scale implies gridlines the other lacks.
        for step in GRID_STEPS:
            y = top + plot_height * (1 - step / TEMP_MAX)
            _hline(snapshot, left, left + plot_width, y, ink("grid"))
            self._text(snapshot, left - 8, y, f"{step}", ink_secondary, 8, "right")
            self._text(
                snapshot,
                width - 4,
                y,
                f"{int(fan_ceiling * step / 100)}",
                ink_secondary,
                8,
                "right",
            )

        # Which number belongs to which axis, said once at the foot of each.
        unit_y = baseline + 11
        self._text(snapshot, left - 8, unit_y, "°C", ink_secondary, 8, "right")
        self._text(snapshot, width - 4, unit_y, "RPM", ink_secondary, 8, "right")

        series = (
            ("cpu", "CPU", self.monitor.cpu_history),
            ("gpu", "GPU", self.monitor.gpu_history),
        )

        # Legend: always present for two series, so identity is never colour alone.
        legend_x = left
        for key, label, _history in series:
            _dot(snapshot, legend_x + 4, top - 14, 4, series_colour(key))
            text_width, _ = self._text(
                snapshot, legend_x + 14, top - 14, label, ink_secondary, 8
            )
            legend_x += 14 + text_width + 18

        # ... and one more entry for the form, since the areas repeat the
        # series colours rather than introducing any of their own.
        fan_width, _ = self._text(
            snapshot, width - 4, top - 14, "fan", ink_secondary, 8, "right"
        )
        fan_x = width - 4 - fan_width
        for index, key in enumerate(("cpu", "gpu")):
            _rect(
                snapshot,
                fan_x - 22 + index * 9,
                top - 18,
                9,
                9,
                series_colour(key),
                SWATCH_ALPHA,
            )

        capacity = self.monitor.cpu_history.maxlen or 1

        # Areas first: the lines cross them and have to stay legible.
        for key, history in (
            ("cpu", self.monitor.cpu_rpm_history),
            ("gpu", self.monitor.gpu_rpm_history),
        ):
            if not history:
                continue
            points = [
                (
                    left + plot_width * (index / max(1, capacity - 1)),
                    baseline - plot_height * min(value / fan_ceiling, 1.0),
                )
                for index, value in enumerate(history)
            ]
            _area(
                snapshot,
                points,
                baseline,
                series_colour(key),
                FILL_ALPHA[dark],
                EDGE_ALPHA[dark],
            )

        endpoints = []
        for key, _label, history in series:
            if not history:
                continue
            colour = series_colour(key)
            # A history can have holes in it: a discrete GPU that powers down
            # reports no temperature at all, and that is not the same as
            # reporting a low one. Each unbroken run is drawn as its own line
            # so the gap stays a gap, rather than a segment joining the
            # temperature before the GPU slept to the one after it woke.
            runs = []
            run = []
            for index, value in enumerate(history):
                if value is None:
                    if run:
                        runs.append(run)
                        run = []
                    continue
                run.append(
                    (
                        left + plot_width * (index / max(1, capacity - 1)),
                        top + plot_height * (1 - min(value, TEMP_MAX) / TEMP_MAX),
                    )
                )
            if run:
                runs.append(run)

            for run in runs:
                _polyline(snapshot, run, colour, 2.0)

            # The head of the line is only a current reading if the series is
            # still reporting; a run that ended when the GPU slept gets no
            # marker and no direct label.
            if runs and history[-1] is not None:
                head = runs[-1][-1]
                _dot(snapshot, head[0], head[1], 4, colour)
                endpoints.append([head[0], head[1], int(history[-1])])

        # Direct labels: a colour-carrying dot on the line, the number in plain
        # ink beside it. When the two series finish at similar temperatures the
        # labels would otherwise sit on top of each other, so nudge them apart.
        endpoints.sort(key=lambda item: item[1])
        minimum_gap = 14
        if len(endpoints) == 2 and endpoints[1][1] - endpoints[0][1] < minimum_gap:
            middle = (endpoints[0][1] + endpoints[1][1]) / 2
            endpoints[0][1] = middle - minimum_gap / 2
            endpoints[1][1] = middle + minimum_gap / 2
        for x, y, value in endpoints:
            y = min(max(y, 8), height - 8)
            self._text(snapshot, x + 9, y, f"{value}°", ink_primary, 9)


class CurvePreview(_ChartBase):
    """The seven-point CPU and GPU fan curve currently being edited."""

    def __init__(self):
        super().__init__()
        self.cpu = []
        self.gpu = []
        # 26 above for the legend, 26 below for the point numbers.
        self.set_size_request(-1, chart_height(156, 26 + 26))
        self.set_hexpand(True)

    def set_curves(self, cpu, gpu):
        self.cpu = list(cpu)
        self.gpu = list(gpu)
        self.queue_draw()

    def do_snapshot(self, snapshot):
        width = self.get_width()
        height = self.get_height()
        if width < 2 or height < 2 or not (self.cpu or self.gpu):
            return

        ink_secondary = ink("secondary")
        surface = ink("surface")
        ceiling = max(100, max(self.cpu + self.gpu, default=0))

        left, right, top, bottom = 40, 18, 26, 26
        plot_width = max(1, width - left - right)
        plot_height = max(1, height - top - bottom)

        for fraction in (0.0, 0.5, 1.0):
            y = top + plot_height * (1 - fraction)
            _hline(snapshot, left, left + plot_width, y, ink("grid"))
            self._text(
                snapshot,
                left - 8,
                y,
                f"{int(ceiling * fraction)}%",
                ink_secondary,
                8,
                "right",
            )

        count = max(len(self.cpu), len(self.gpu), 2)
        for index in range(count):
            x = left + plot_width * (index / (count - 1))
            self._text(
                snapshot,
                x,
                top + plot_height + 12,
                str(index + 1),
                ink_secondary,
                8,
                "center",
            )

        legend_x = left
        for key, label in (("cpu", "CPU"), ("gpu", "GPU")):
            _dot(snapshot, legend_x + 4, top - 14, 4, series_colour(key))
            text_width, _ = self._text(
                snapshot, legend_x + 14, top - 14, label, ink_secondary, 8
            )
            legend_x += 14 + text_width + 18

        for key, values in (("cpu", self.cpu), ("gpu", self.gpu)):
            if not values:
                continue
            colour = series_colour(key)
            points = [
                (
                    left + plot_width * (index / max(1, len(values) - 1)),
                    top + plot_height * (1 - value / ceiling),
                )
                for index, value in enumerate(values)
            ]
            _polyline(snapshot, points, colour, 2.0)
            # A surface ring keeps the markers readable where the curves cross.
            for x, y in points:
                _dot(snapshot, x, y, 5.5, surface)
                _dot(snapshot, x, y, 4, colour)


class LegendSwatch(_ChartBase):
    """The colour dot beside the CPU/GPU labels in the readings table."""

    def __init__(self, series):
        super().__init__()
        self.series = series
        self.set_size_request(10, 10)
        self.set_valign(Gtk.Align.CENTER)
        self.set_halign(Gtk.Align.CENTER)

    def do_snapshot(self, snapshot):
        width = self.get_width()
        height = self.get_height()
        if width < 2 or height < 2:
            return
        _dot(
            snapshot,
            width / 2,
            height / 2,
            min(width, height) / 2,
            series_colour(self.series),
        )
