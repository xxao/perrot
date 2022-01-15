#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import numpy
import perrot

# prepare data
x_data = numpy.linspace(-1.5*numpy.pi, 1.5*numpy.pi, 50)
y1_data = numpy.sin(x_data)
y2_data = 0.75*y1_data - 1
x_data /= numpy.pi

# init plot
plot = perrot.Plot(
    x_axis_title = "pi",
    y_axis_title = "f(x)")

# add series
series = plot.band(
    x = x_data,
    y1 = y1_data,
    y2 = y2_data,
    title = "Band",
    show_points = perrot.UNDEF,
    marker_line_color = "white")

# show plot
plot.zoom()
plot.view("Band Series")
