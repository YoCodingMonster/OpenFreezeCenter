"""A settings group that folds away behind its own title.

libadwaita's preferences group is a heading with a list under it and no way
to put the list away. Three of them stacked is more than a compact window
shows at once, and two of the three — the fan profile and the charge limit —
are set once and then only ever read.

A section is the same heading and the same boxed list, with the heading
turned into a button that reveals or hides the list. What is lost when the
list goes away is what it was showing, so a collapsed section says its own
state in a line of text beside the title: the profile that is selected, the
temperatures being read, the charge limit that is set. Collapsed is then a
smaller way of seeing the same thing, not a way of hiding it, and nothing
has to be opened to be checked.

The list itself is a real Adw.PreferencesGroup, so the rows keep exactly the
boxed-list styling, spacing and activation behaviour they had before.
"""

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, GLib, GObject, Gtk, Pango

from .style import px


class Section(Gtk.Box):
    """A titled group of rows, with a summary that shows when it is closed."""

    __gtype_name__ = "OfcSection"

    # Emitted once the section has finished changing size, for a window that
    # follows the height of what it is showing. A section cannot resize a
    # window itself without knowing what it is inside of.
    __gsignals__ = {"resized": (GObject.SignalFlags.RUN_FIRST, None, ())}

    expanded = GObject.Property(type=bool, default=True)

    def __init__(self, title, description=None, expanded=True):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=px(8))
        self.title = title

        self._arrow = Gtk.Image.new_from_icon_name("go-next-symbolic")
        self._arrow.add_css_class("ofc-section-arrow")

        heading = Gtk.Label(label=title, xalign=0.0)
        heading.add_css_class("heading")

        # Ellipsised rather than wrapped: the summary is a second reading of
        # the section, and it must not be able to grow the header out of the
        # one line the title occupies.
        self._summary = Gtk.Label(xalign=0.0, hexpand=True)
        self._summary.add_css_class("dim-label")
        self._summary.add_css_class("caption")
        self._summary.set_ellipsize(Pango.EllipsizeMode.END)

        labels = Gtk.Box(spacing=px(10))
        labels.append(self._arrow)
        labels.append(heading)
        labels.append(self._summary)

        self._toggle = Gtk.Button(child=labels, hexpand=True)
        self._toggle.add_css_class("flat")
        self._toggle.add_css_class("ofc-section-header")
        self._toggle.connect("clicked", lambda _b: self.set_expanded(not self.expanded))

        # The suffix sits outside the button: a control in the header is its
        # own action, and nesting it would make pressing it also toggle the
        # section.
        self._header = Gtk.Box(spacing=px(6))
        self._header.append(self._toggle)
        self.append(self._header)

        # No slide. The window this lives in takes the height of what it is
        # showing, so revealing is already a resize; animating the content
        # into a window that is itself jumping reads as two things going
        # wrong rather than one thing happening.
        self.group = Adw.PreferencesGroup(description=description)
        self._revealer = Gtk.Revealer(child=self.group, transition_duration=0)
        self.append(self._revealer)

        self.connect("notify::expanded", lambda *_: self._apply())
        self.expanded = expanded
        self._apply(announce=False)

    ###########################################################################
    # Contents
    ###########################################################################

    def add(self, child):
        """Add a row, or any widget, exactly as a preferences group would."""
        self.group.add(child)

    def set_header_suffix(self, widget):
        """Put a control on the title line, to the right of the summary.

        Hidden while the section is closed: the summary has the width in that
        state, and a button acting on a list nobody can see is noise.
        """
        self._header.append(widget)
        self.bind_property(
            "expanded", widget, "visible", GObject.BindingFlags.SYNC_CREATE
        )

    def set_summary(self, text):
        """The one-line reading of this section, shown while it is closed."""
        self._summary.set_label(text)
        self._summary.set_tooltip_text(text)

    ###########################################################################
    # Open and closed
    ###########################################################################

    def get_expanded(self):
        return self.expanded

    def set_expanded(self, expanded):
        self.expanded = bool(expanded)

    def _apply(self, announce=True):
        expanded = self.expanded
        self._revealer.set_reveal_child(expanded)
        self._summary.set_visible(not expanded)
        self._toggle.set_tooltip_text(
            f"Hide {self.title}" if expanded else f"Show {self.title}"
        )
        # So a screen reader announces the header as the disclosure control
        # it is, rather than as a plain button. The tristate goes in as a
        # plain int: handed the enum, PyGObject builds a GValue of the enum's
        # own type and GTK, which reads an int back out, warns on every call.
        self._toggle.update_state(
            [Gtk.AccessibleState.EXPANDED],
            [
                int(
                    Gtk.AccessibleTristate.TRUE
                    if expanded
                    else Gtk.AccessibleTristate.FALSE
                )
            ],
        )
        if expanded:
            self._arrow.add_css_class("expanded")
        else:
            self._arrow.remove_css_class("expanded")

        # From an idle, so the revealer has been through a layout pass and
        # anyone measuring us gets the height we have actually settled on.
        if announce:
            GLib.idle_add(self._announce_resize, priority=GLib.PRIORITY_LOW)

    def _announce_resize(self):
        self.emit("resized")
        return GLib.SOURCE_REMOVE
