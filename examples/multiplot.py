#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import numpy
import pero
import perrot

# prepare data
x_data = numpy.linspace(-2*numpy.pi, 2*numpy.pi, 100)
sin_data = numpy.sin(x_data)
cos_data = numpy.cos(x_data)
x_data /= numpy.pi

# init plots
settings = {
    "x_axis_title": "pi",
    "y_axis_title": "f(x)"}

plot1 = perrot.Plot(**settings)
plot2 = perrot.Plot(**settings)
plot3 = perrot.Plot(**settings)

# add series
plot1.profile(x=x_data, y=sin_data, title="sin(x)", color="b")
plot1.profile(x=x_data, y=cos_data, title="cos(x)", color="g")
plot1.zoom()

plot2.profile(x=x_data, y=sin_data, title="sin(x)", color="b")
plot2.zoom()

plot3.profile(x=x_data, y=cos_data, title="cos(x)", color="g")
plot3.zoom()

# make layout
layout = pero.Layout()
layout.add(plot1, 0, 0, col_span=2)
layout.add(plot2, 1, 0)
layout.add(plot3, 1, 1)

layout.show()
