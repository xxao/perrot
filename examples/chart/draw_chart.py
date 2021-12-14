#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero
import perrot

# init chart
chart = perrot.chart.Chart(
    frame_line_width = 1,
    frame_line_color = "k",
    frame_fill_color = "#fff",
    bgr_fill_color = "#eee"
    )

# init titles
title = perrot.chart.Title(
    position = pero.TOP,
    text = "Chart Title",
    font_size = 14)

sub_title = perrot.chart.Title(
    position = pero.TOP,
    text = "Sub Title",
    font_size = 10)

# init axes
x_axis = perrot.chart.LinAxis(
    title = "X-Axis",
    position = pero.BOTTOM,
    margin = 0,
    scale_in_range = (-10, 10))

y_axis = perrot.chart.LogAxis(
    title = "Y-Axis",
    position = pero.LEFT,
    margin = 0,
    scale_in_range = (1, 1e4))

# init grids
x_major_grid = perrot.chart.Grid(
    mode = perrot.chart.GRID_MAJOR,
    orientation = pero.VERTICAL,
    scale = x_axis.scale,
    ticker = x_axis.ticker)

y_major_grid = perrot.chart.Grid(
    mode = perrot.chart.GRID_MAJOR,
    orientation = pero.HORIZONTAL,
    scale = y_axis.scale,
    ticker = y_axis.ticker)

y_minor_grid = perrot.chart.Grid(
    mode = perrot.chart.GRID_MINOR,
    orientation = pero.HORIZONTAL,
    scale = y_axis.scale,
    ticker = y_axis.ticker,
    line_color = "#f5f5f5ff")

# init legend
legend = perrot.chart.InsideLegend(
    position = pero.NE,
    orientation = pero.VERTICAL,
    static = True,
    items = (
        pero.MarkerLegend(text="Legend 1", marker='o', marker_fill_color='r', marker_line_width=0),
        pero.MarkerLegend(text="Legend 2", marker='s', marker_fill_color='g', marker_line_width=0))
)

# add objects
chart.add(sub_title)
chart.add(title)

chart.add(x_axis)
chart.add(x_major_grid)

chart.add(y_axis)
chart.add(y_minor_grid)
chart.add(y_major_grid)

chart.add(legend)

# show chart
chart.show()

