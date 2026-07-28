"""The Advanced profile's fan curve editor.

This is the README's outstanding "Advanced & Basic GUI control" goal: the
seven CPU and seven GPU points used to be reachable only by hand-editing
config.py.
"""

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gtk

from . import config as cfg
from .widgets import CurvePreview

POINT_LABELS = (
    "Point 1 — idle",
    "Point 2",
    "Point 3",
    "Point 4",
    "Point 5",
    "Point 6",
    "Point 7 — hottest",
)


class CurveEditorPage(Adw.NavigationPage):
    """Edits config.advanced_cpu / advanced_gpu, live-previewed."""

    def __init__(self, config, on_changed):
        super().__init__(title="Fan Curves")
        self.config = config
        self.on_changed = on_changed
        self._loading = False

        header = Adw.HeaderBar()
        copy_button = Gtk.Button(label="Copy from Auto")
        copy_button.set_tooltip_text("Replace both curves with the Auto profile curve")
        copy_button.connect("clicked", self._on_copy_from_auto)
        header.pack_end(copy_button)

        page = Adw.PreferencesPage()

        preview_group = Adw.PreferencesGroup(
            title="Preview",
            description="Fan speed at each of the seven EC curve points, "
            "coolest on the left.",
        )
        self.preview = CurvePreview()
        preview_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        preview_box.add_css_class("card")
        preview_box.add_css_class("ofc-chart")
        preview_box.append(self.preview)
        preview_group.add(preview_box)
        page.add(preview_group)

        self.cpu_rows = self._build_group(page, "CPU Fan", "cpu")
        self.gpu_rows = self._build_group(page, "GPU Fan", "gpu")

        toolbar = Adw.ToolbarView()
        toolbar.add_top_bar(header)
        toolbar.set_content(page)
        self.set_child(toolbar)

        self.refresh()

    def _build_group(self, page, title, which):
        group = Adw.PreferencesGroup(
            title=title, description="Percent of maximum fan speed"
        )
        rows = []
        for index, label in enumerate(POINT_LABELS):
            row = Adw.SpinRow.new_with_range(cfg.SPEED_MIN, cfg.SPEED_MAX, 1)
            row.set_title(label)
            row.connect("notify::value", self._on_value_changed, which, index)
            group.add(row)
            rows.append(row)
        page.add(group)
        return rows

    def refresh(self):
        """Pull values out of the config into the spin rows and the preview."""
        self._loading = True
        for row, value in zip(self.cpu_rows, self.config.advanced_cpu):
            row.set_value(value)
        for row, value in zip(self.gpu_rows, self.config.advanced_gpu):
            row.set_value(value)
        self._loading = False
        self.preview.set_curves(self.config.advanced_cpu, self.config.advanced_gpu)

    def _on_value_changed(self, row, _param, which, index):
        if self._loading:
            return
        target = (
            self.config.advanced_cpu if which == "cpu" else self.config.advanced_gpu
        )
        target[index] = int(row.get_value())
        self.preview.set_curves(self.config.advanced_cpu, self.config.advanced_gpu)
        self.on_changed()

    def _on_copy_from_auto(self, _button):
        self.config.advanced_cpu = list(self.config.auto_cpu)
        self.config.advanced_gpu = list(self.config.auto_gpu)
        self.refresh()
        self.on_changed()
