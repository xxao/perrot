#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import numpy
import pero
import perrot

# prepare data
count = 50
x_data = numpy.linspace(-5, 5, count)
y_data_1 = numpy.random.normal(0, 1., count)
y_data_2 = numpy.random.normal(0, 5., count)

# init size scale
size_data = 10 + 30 * numpy.random.random(2 * count)
size_scale = pero.OrdinalScale(out_range=size_data, implicit=True)
size_fn = lambda d: size_scale.scale(d[0])

# init plot
plot = perrot.Plot(
    x_axis_title = "x-value",
    y_axis_title = "random",
    legend_position = perrot.NE,
    legend_orientation = perrot.VERTICAL)

# add series
series1 = plot.scatter(
    title = "Normal 1",
    x = x_data,
    y = y_data_1,
    marker = 'o',
    marker_size = size_fn,
    marker_fill_alpha = 150)

series2 = plot.scatter(
    title = "Normal 5",
    x = x_data,
    y = y_data_2,
    marker = 'd',
    marker_size = size_fn,
    marker_fill_alpha = 150)

# show plot
plot.zoom()
plot.view("Scatter Series")
