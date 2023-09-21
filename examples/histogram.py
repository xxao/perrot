#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import numpy
import perrot

# prepare data
data = numpy.random.normal(size=1000)
bins = 50

# init plot
plot = perrot.Plot(
    title_text = "Histogram for numpy.random.normal()",
    x_axis_title = 'random',
    y_axis_title = 'count',
    legend_position = perrot.NW,
    y_minor_grid = None)

# add additional axis
right_axis = perrot.LinAxis(
    title = '%',
    position = perrot.RIGHT,
    margin = 0,
    label_text_color = "r")

plot.add(right_axis)

# add additional grid
right_grid = perrot.Grid(
    mode = perrot.GRID_MAJOR,
    orientation = perrot.HORIZONTAL,
    z_index = perrot.GRID_MAJOR_Z,
    line_color = "r",
    line_alpha = 75)

plot.add(right_grid)
plot.map(right_grid, 'scale', right_axis, 'scale')
plot.map(right_grid, 'ticker', right_axis, 'ticker')

# add bars
bars = plot.histogram(data, bins,
    minimum = -5,
    maximum = 5,
    title = "Histogram",
    spacing = (0, 2),
    margin = (0.05, 0, 0, 0),
    color = "b")

# add cumulative
cumulative = plot.cumsum(data, bins,
    minimum = -5,
    maximum = 5,
    title = "Cumulative Sum",
    line_width = 2,
    margin = 0,
    color = "r",
    y_axis = right_axis)

# show plot
plot.zoom()
plot.view("Histogram")
