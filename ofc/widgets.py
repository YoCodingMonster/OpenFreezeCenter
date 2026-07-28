"""The live temperature chart and the fan curve preview.

Drawn with GSK paths rather than Cairo, so the application needs nothing
beyond PyGObject itself — the Cairo bridge (gi._gi_cairo) is a separate
distro package that is easy to end up without.

Both charts use the same two-colour categorical assignment, fixed per
entity: slot 1 blue for the CPU, slot 2 orange for the GPU, never cycled.
The pair is validated against the Adwaita card surface in both modes —
worst adjacent CVD ΔE 24.7 light / 26.8 dark, normal-vision 33.6 / 31.8,
both series at or above 3:1 contrast.
"""

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Gsk", "4.0")
gi.require_version("Graphene", "1.0")
from gi.repository import Adw, Gdk, Graphene, Gsk, Gtk, Pango

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

TEMP_MAX = 100.0
GRID_STEPS = (0, 25, 50, 75, 100)


def _rgba(hex_colour):
    colour = Gdk.RGBA()
    colour.parse(hex_colour)
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
    """Sixty seconds of CPU and GPU temperature on one shared 0–100 °C axis.

    Both series measure the same quantity in the same unit, so they share a
    single axis. Fan RPM is a different quantity on a different scale and
    stays in the table below rather than becoming a second y-axis here.
    """

    def __init__(self, monitor):
        super().__init__()
        self.monitor = monitor
        self.set_size_request(-1, 168)
        self.set_hexpand(True)

    def do_snapshot(self, snapshot):
        width = self.get_width()
        height = self.get_height()
        if width < 2 or height < 2:
            return

        ink_secondary = ink("secondary")
        ink_primary = ink("primary")

        left, right, top, bottom = 36, 56, 26, 16
        plot_width = max(1, width - left - right)
        plot_height = max(1, height - top - bottom)

        # Grid: hairline, recessive, labelled in muted ink.
        for step in GRID_STEPS:
            y = top + plot_height * (1 - step / TEMP_MAX)
            _hline(snapshot, left, left + plot_width, y, ink("grid"))
            self._text(snapshot, left - 8, y, f"{step}", ink_secondary, 8, "right")

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

        capacity = self.monitor.cpu_history.maxlen or 1
        endpoints = []
        for key, _label, history in series:
            if not history:
                continue
            colour = series_colour(key)
            points = [
                (
                    left + plot_width * (index / max(1, capacity - 1)),
                    top + plot_height * (1 - min(value, TEMP_MAX) / TEMP_MAX),
                )
                for index, value in enumerate(history)
            ]
            _polyline(snapshot, points, colour, 2.0)
            _dot(snapshot, points[-1][0], points[-1][1], 4, colour)
            endpoints.append([points[-1][0], points[-1][1], int(history[-1])])

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
        self.set_size_request(-1, 156)
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
