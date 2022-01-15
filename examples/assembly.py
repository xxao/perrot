#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero
import perrot

# init chart
chart = perrot.ChartBase(
    frame_line_width = 1,
    frame_line_color = "k",
    frame_fill_color = "#fff",
    bgr_fill_color = "#eee")

# init titles
title = perrot.Title(
    text = "Chart Title",
    position = perrot.TOP,
    z_index = perrot.TITLE_Z,
    font_size = 14)

sub_title = perrot.Title(
    text = "Sub Title",
    position = perrot.TOP,
    z_index = perrot.TITLE_Z-1,
    font_size = 10)

chart.add(title)
chart.add(sub_title)

# init main axes
x_axis = perrot.LinAxis(
    title = "X-Axis",
    position = perrot.BOTTOM,
    z_index = perrot.AXIS_Z,
    margin = 0,
    scale_in_range = (-10, 10))

y_axis = perrot.LogAxis(
    title = "Y-Axis",
    position = perrot.LEFT,
    z_index = perrot.AXIS_Z,
    margin = 0,
    scale_in_range = (1, 1e4))

chart.add(x_axis)
chart.add(y_axis)

# init grids
x_major_grid = perrot.Grid(
    mode = perrot.GRID_MAJOR,
    orientation = perrot.VERTICAL,
    z_index = perrot.GRID_MAJOR_Z,
    scale = x_axis.scale,
    ticker = x_axis.ticker)

y_major_grid = perrot.Grid(
    mode = perrot.GRID_MAJOR,
    orientation = perrot.HORIZONTAL,
    z_index = perrot.GRID_MAJOR_Z,
    scale = y_axis.scale,
    ticker = y_axis.ticker)

y_minor_grid = perrot.Grid(
    mode = perrot.GRID_MINOR,
    orientation = perrot.HORIZONTAL,
    z_index = perrot.GRID_MINOR_Z,
    scale = y_axis.scale,
    ticker = y_axis.ticker,
    line_color = "#f5f5f5ff")

chart.add(x_major_grid)
chart.add(y_major_grid)
chart.add(y_minor_grid)

# init color bar and axis
c_bar = perrot.ColorBar(
    position = perrot.RIGHT,
    z_index = perrot.COLOR_BAR_Z,
    gradient = perrot.colors.YlOrBr,
    margin = (0, 0, 0, 10))

c_axis = perrot.LinAxis(
    title = "Z-Axis",
    position = perrot.RIGHT,
    z_index = perrot.COLOR_BAR_Z+1,
    margin = 0,
    scale_in_range = (0, 100))

chart.add(c_bar)
chart.add(c_axis)

# init legend
legends = (
    pero.MarkerLegend(text="Legend 1", marker='o', marker_fill_color='r', marker_line_width=0),
    pero.MarkerLegend(text="Legend 2", marker='s', marker_fill_color='g', marker_line_width=0))

legend = perrot.InLegend(
    position = perrot.NE,
    orientation = perrot.VERTICAL,
    z_index = perrot.LEGEND_Z,
    static = True,
    items = legends)

chart.add(legend)

# show chart
chart.show("Perrot Chart", width=600, height=450)
