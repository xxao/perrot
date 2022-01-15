#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import numpy
import perrot

# prepare data
data = numpy.random.normal(size=1000)
bins, hist, cumsum = perrot.calc_histogram(data, 50)
cumsum = cumsum / len(data) * 100

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
bars = plot.bars(
    title = "Histogram",
    top = hist,
    left = bins[:-1],
    right = bins[1:],
    bottom = 0,
    anchor = perrot.TOP,
    margin = (0.05, 0, 0, 0))

# add cumulative
cumulative = plot.profile(
    title = "Cumulative Sum",
    x = 0.5*(bins[:-1] + bins[1:]),
    y = cumsum,
    line_width = 2,
    steps = perrot.MIDDLE,
    margin = 0,
    color = "o",
    y_axis = right_axis)

# show plot
plot.zoom()
plot.view("Histogram")
