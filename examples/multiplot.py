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

# init plots
p1 = perrot.Plot(tag="p1", **settings)
p1.profile(x=x_data, y=sin_data, title="sin(x)", color="b")
p1.profile(x=x_data, y=cos_data, title="cos(x)", color="g")
p1.zoom()

p2 = perrot.Plot(tag="p2", **settings)
p2.profile(x=x_data, y=sin_data, title="sin(x)", color="b")
p2.zoom()

p3 = perrot.Plot(tag="p3", **settings)
p3.profile(x=x_data, y=cos_data, title="cos(x)", color="g")
p3.zoom()

# make controls
c1 = perrot.PlotControl(graphics=p1)
c2 = perrot.PlotControl(graphics=p2)
c3 = perrot.PlotControl(graphics=p3)

# synchronize x-axes
syncer = perrot.Syncer()
syncer.sync_x(c1, c2)
syncer.sync_x(c1, c3)
syncer.sync_x(c2, c3)
syncer.sync_x(c3, c2)

# make layout
sizer = pero.Sizer()
sizer.add(c1, 0, 0, col_span=2)
sizer.add(c2, 1, 0)
sizer.add(c3, 1, 1)

sizer.show()
