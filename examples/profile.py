#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import numpy
import perrot

# prepare data
x_data = numpy.linspace(-2*numpy.pi, 2*numpy.pi, 50)
y_data = numpy.sin(x_data)
x_data /= numpy.pi

# init plot
plot = perrot.Plot(
    x_axis_title = "pi",
    y_axis_title = "f(x)")

# add series
series = plot.profile(
    x = x_data,
    y = y_data,
    base = 0,
    title = "sin(x)",
    steps = perrot.LINE_STEP.NONE,
    show_area = True,
    show_points = perrot.UNDEF,
    marker_line_color = "white")

# show plot
plot.zoom()
plot.view("Profile Series")
