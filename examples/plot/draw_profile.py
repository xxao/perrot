#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import numpy
import pero
import perrot

# prepare data
x_data = numpy.linspace(-2*numpy.pi, 2*numpy.pi, 100)
y_data = numpy.sin(x_data)
x_data /= numpy.pi

# init plot
plot = perrot.plot.Plot(
    x_axis_title = "pi",
    y_axis_title = "f(x)")

# add series
series = perrot.plot.Profile(
    x = x_data,
    y = y_data,
    base = 0,
    title = "sin(x)",
    steps = pero.LINE_STEP.NONE,
    marker_line_color = "white",
    show_area = True)

plot.plot(series)

# show plot
plot.zoom()
plot.view("Profile Series")
