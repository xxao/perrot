#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import perrot

# init axes
left_axis = perrot.LogAxis(
    title = "Left Axis (log10)",
    tag = "left_axis",
    position = perrot.LEFT,
    margin = 0,
    z_index = perrot.AXIS_Z,
    scale_in_range = (1, 1.e5),
    level = 2)

bottom_axis = perrot.LinAxis(
    title = "Bottom Axis (lin)",
    tag = "bottom_axis",
    position = perrot.BOTTOM,
    margin = 0,
    z_index = perrot.AXIS_Z,
    scale_in_range = (-200, 555),
    ticker_minor_count = 5,
    level = 1)

right_axis = perrot.LinAxis(
    title = "Right Axis",
    tag = "right_axis",
    position = perrot.RIGHT,
    margin = 0,
    z_index = perrot.AXIS_Z,
    ticker_formatter_hide_suffix = True,
    scale_in_range = (1, 1.e5),
    level = 2)

top_axis = perrot.LinAxis(
    title = "Top Axis",
    tag = "top_axis",
    position = perrot.TOP,
    margin = 0,
    z_index = perrot.AXIS_Z,
    scale_in_range = (0.1, 1500),
    label_angle = -45,
    label_text_align = perrot.LEFT,
    level = 1)

ordinal_axis = perrot.OrdinalAxis(
    title = "Ordinal Axis",
    tag = "ordinal_axis",
    position = perrot.BOTTOM,
    margin = (20, 0, 0, 0),
    z_index = perrot.AXIS_Z+1,
    labels = ("one", 'two', "three", "four", "five"),
    major_tick_size = 0,
    static = False,
    level = 3)

color_axis = perrot.LinAxis(
    title = "Color Axis",
    tag = "color_axis",
    position = perrot.RIGHT,
    margin = 0,
    z_index = perrot.AXIS_Z+2,
    scale_in_range = (0, 1),
    static = False,
    level = 3)

color_bar = perrot.ColorBar(
    tag = "color_bar",
    position = perrot.RIGHT,
    margin = (0, 0, 0, 20),
    z_index = perrot.AXIS_Z+1,
    gradient = perrot.colors.YlOrRd)

# init grids
h_major_grid = perrot.Grid(
    mode = perrot.MAJOR,
    orientation = perrot.HORIZONTAL,
    scale = left_axis.scale,
    ticker = left_axis.ticker,
    line_color = perrot.colors.LightGrey,
    z_index = perrot.GRID_MAJOR_Z)

h_minor_grid = perrot.Grid(
    mode = perrot.MINOR,
    orientation = perrot.HORIZONTAL,
    scale = left_axis.scale,
    ticker = left_axis.ticker,
    line_color = perrot.colors.LightGrey.lighter(0.7),
    z_index = perrot.GRID_MINOR_Z)

v_major_grid = perrot.Grid(
    mode = perrot.MAJOR,
    orientation = perrot.VERTICAL,
    scale = bottom_axis.scale,
    ticker = bottom_axis.ticker,
    line_color = perrot.colors.LightGrey,
    z_index = perrot.GRID_MAJOR_Z)

v_minor_grid = perrot.Grid(
    mode = perrot.MINOR,
    orientation = perrot.VERTICAL,
    scale = bottom_axis.scale,
    ticker = bottom_axis.ticker,
    line_color = perrot.colors.LightGrey.lighter(0.7),
    z_index = perrot.GRID_MINOR_Z)

# init plot
plot = perrot.Plot(
    x_axis = bottom_axis,
    y_axis = left_axis,
    x_major_grid = v_major_grid,
    x_minor_grid = v_minor_grid,
    y_major_grid = h_major_grid,
    y_minor_grid = h_minor_grid)

# add additional axes
plot.add(right_axis)
plot.add(top_axis)
plot.add(ordinal_axis)
plot.add(color_axis)
plot.add(color_bar)

# show plot
plot.view("Multiple Axes")
