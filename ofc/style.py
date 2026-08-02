"""The compact metric scale, and the stylesheet that applies it.

The space between things is drawn at 60% of the stock Adwaita size. That is
one number, `UI_SCALE`, and every gap in the application — row padding,
margins, border spacing, the distance between groups — is derived from its
full-size value through `px()`. Scaling from a single constant is what keeps
the proportions between them intact: nothing is compressed by hand, so
nothing drifts out of relation to anything else.

What is *in* the space is left alone. Type is exactly the size it has always
been, and so is everything sized to hold it — the chart's axis gutters, its
legends, its labels. The window gets smaller by giving up its air, not by
becoming harder to read.

Colour is untouched too. The palette, the Adwaita widget styling and the
chart series colours are exactly what they were.
"""

UI_SCALE = 0.60


def px(size):
    """A stock Adwaita gap, in compact pixels."""
    return max(1, round(size * UI_SCALE))


def chart_height(full_height, gutters):
    """A chart's compact height: full-size gutters, plot area at 60%.

    The margins a chart reserves for its axis labels and legend are text,
    and text does not shrink here; only the plot between them does.
    """
    return px(full_height - gutters) + gutters


# Page furniture, from what Adw.PreferencesPage uses. The margins and the
# gap between sections are space, so they take the 60%. The clamp is not —
# it is the width a line of text is allowed to reach before it becomes hard
# to track back to the next one — so it stays where Adwaita put it.
CLAMP_WIDTH = 600
PAGE_MARGIN = px(24)
SECTION_SPACING = px(24)


STYLE = f"""
.ofc-chart {{
    padding: {px(14)}px;
}}
.ofc-reading {{
    font-family: monospace;
    font-size: 1.05em;
}}

/* -- Collapsible sections ------------------------------------------------
   The header is a button that has to read as a group heading, so it carries
   no chrome of its own until it is hovered. */
.ofc-section-header {{
    min-height: 0;
    padding: {px(6)}px {px(8)}px;
    border-radius: {px(9)}px;
}}
.ofc-section-arrow {{
    transition: -gtk-icon-transform 200ms ease;
}}
.ofc-section-arrow.expanded {{
    -gtk-icon-transform: rotate(90deg);
}}

/* -- The 60% scale -------------------------------------------------------
   Adwaita is sized for touch. Every declaration below restates one that the
   libadwaita stylesheet already makes, with its length taken through px() —
   same selectors, same properties, same relationships, 60% of the space.
   Nothing here invents a metric, and nothing here touches font-size, which
   is why the result still reads as Adwaita rather than as Adwaita with the
   air let out unevenly. */

/* Rows. The height of a list row is the min-height of its header box, not
   anything on the row itself, and the gaps inside it are border-spacing. */
.ofc-compact row > box.header {{
    margin-left: {px(12)}px;
    margin-right: {px(12)}px;
    border-spacing: {px(6)}px;
    min-height: {px(50)}px;
}}
.ofc-compact row > box.header > box.title {{
    margin-top: {px(6)}px;
    margin-bottom: {px(6)}px;
    border-spacing: {px(3)}px;
}}
.ofc-compact row > box.header > .prefixes,
.ofc-compact row > box.header > .suffixes {{
    border-spacing: {px(6)}px;
}}
.ofc-compact row.button > box {{
    margin-left: {px(12)}px;
    margin-right: {px(12)}px;
    border-spacing: {px(6)}px;
    min-height: {px(40)}px;
}}

.ofc-compact preferencesgroup > box,
.ofc-compact preferencesgroup > box box.labels {{
    border-spacing: {px(6)}px;
}}
.ofc-compact preferencesgroup > box > box.header:not(.single-line) {{
    margin-bottom: {px(6)}px;
}}
.ofc-compact preferencesgroup > box > box.single-line {{
    min-height: {px(34)}px;
}}
.ofc-compact preferencespage > scrolledwindow > viewport > clamp > box {{
    margin: {px(24)}px {px(12)}px;
    border-spacing: {px(24)}px;
}}

.ofc-compact switch {{
    border-radius: {px(14)}px;
    padding: {px(3)}px;
}}
.ofc-compact switch > slider {{
    min-width: {px(20)}px;
    min-height: {px(20)}px;
}}
.ofc-compact row.spin spinbutton > button.image-button {{
    min-width: {px(30)}px;
    min-height: {px(30)}px;
    margin: {px(10)}px {px(2)}px;
}}

.ofc-compact button {{
    min-height: {px(24)}px;
    min-width: {px(16)}px;
    padding: {px(5)}px {px(10)}px;
    border-radius: {px(9)}px;
}}
.ofc-compact button.pill {{
    padding: {px(10)}px {px(32)}px;
}}
.ofc-compact .card {{
    border-radius: {px(12)}px;
}}

/* The header bar. Adw.ToolbarView's own rule is the one that lands, so it
   is the one restated; windowcontrols would otherwise keep full-size
   buttons in a half-size bar. */
.ofc-compact headerbar,
.ofc-compact toolbarview > .top-bar headerbar {{
    min-height: {px(46)}px;
}}
.ofc-compact headerbar > windowhandle > box {{
    padding: {px(6)}px {px(7)}px {px(7)}px {px(7)}px;
}}
.ofc-compact headerbar > windowhandle > box > box.start,
.ofc-compact headerbar > windowhandle > box > box.end {{
    border-spacing: {px(6)}px;
}}
.ofc-compact windowtitle {{
    margin-top: -{px(6)}px;
    margin-bottom: -{px(6)}px;
    min-height: {px(12)}px;
}}
.ofc-compact windowcontrols {{
    border-spacing: {px(3)}px;
}}
.ofc-compact windowcontrols > button {{
    min-width: {px(24)}px;
    padding: {px(5)}px;
}}

/* The EC error page. */
.ofc-compact statuspage > scrolledwindow > viewport > box {{
    margin: {px(36)}px {px(12)}px;
    border-spacing: {px(36)}px;
}}
.ofc-compact statuspage > scrolledwindow > viewport > box > clamp > box {{
    border-spacing: {px(12)}px;
}}
.ofc-compact statuspage > scrolledwindow > viewport > box > clamp > box > .icon {{
    -gtk-icon-size: {px(128)}px;
}}
"""
