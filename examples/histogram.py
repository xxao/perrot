#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import numpy
import perrot

# prepare data
data = numpy.random.normal(size=1000)
bins = 50

# init plot
plot = perrot.Plot(
    x_axis_title = 'random',
    y_axis_title = 'count',
    legend_position = perrot.NW)

# add additional axis
right_axis = perrot.LinAxis(
    title = '%',
    position = perrot.RIGHT,
    z_index = 1,
    margin = 0)

plot.add(right_axis)

# add bars
bars = plot.histogram(data, bins,
    title = "Histogram",
    margin = (0.05, 0, 0, 0))

# add cumulative
cumulative = plot.cumsum(data, bins,
    title = "Cumulative Sum",
    line_width = 2,
    margin = 0,
    color = "o",
    y_axis = right_axis)

# show plot
plot.zoom()
plot.view("Histogram")
