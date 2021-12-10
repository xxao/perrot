#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero
import perrot

# init chart
chart = perrot.chart.Chart()

# init title
title = perrot.chart.Title(
    position = pero.TOP,
    text = "Top Title",
    font_size = 14)

# init axes
top_axis = perrot.chart.OrdinalAxis(
    title = "Top Axis",
    position = pero.TOP,
    margin = 0,
    scale_in_range = (0, 10),
    labels = ("one", "two", "three", "four", "five"),
    major_tick_size = 0)

bottom_axis = perrot.chart.LinAxis(
    title = "Bottom Axis",
    position = pero.BOTTOM,
    margin = 0,
    scale_in_range = (-10, 10))

left_axis = perrot.chart.LogAxis(
    title = "Left Axis",
    position = pero.LEFT,
    margin = 0,
    scale_in_range = (1, 10000))

right_axis = perrot.chart.LinAxis(
    title = "Right Axis",
    position = pero.RIGHT,
    margin = 0)

# init legend
legend = perrot.chart.InLegend(
    position = pero.NE,
    orientation = pero.VERTICAL,
    items = (
        pero.MarkerLegend(text="Legend 1", marker='o', marker_fill_color='r', marker_line_width=0),
        pero.MarkerLegend(text="Legend 2", marker='s', marker_fill_color='g', marker_line_width=0))
)

# add objects
chart.add(top_axis)
chart.add(bottom_axis)
chart.add(left_axis)
chart.add(right_axis)
chart.add(title)
chart.add(legend)

# show chart
chart.show()

