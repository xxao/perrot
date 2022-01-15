#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import numpy
import perrot

# prepare data
count = 25
data = []

for x in numpy.linspace(-numpy.pi, numpy.pi, count):
    for y in numpy.linspace(-numpy.pi, numpy.pi, count):
        z = (numpy.sin(x) + numpy.sin(y))/2
        data.append((x/numpy.pi, y/numpy.pi, z))

data = numpy.array(data)
z_min = numpy.min(data[:, 2])
z_max = numpy.max(data[:, 2])

# init plot
plot = perrot.Plot(
    x_axis_title = "pi",
    x_axis_ticker_major_step = 0.5,
    y_axis_title = "pi",
    y_axis_ticker_major_step = 0.5,)

# init color bar
color_bar = perrot.ColorBar(
    position = perrot.RIGHT,
    gradient = perrot.colors.YlOrBr,
    margin = (0, 0, 0, 15))

# init z-axis
z_axis = perrot.LinAxis(
    title = "sin(x) + sin(y)",
    position = perrot.RIGHT,
    scale_in_range = (z_min, z_max),
    level = 3,
    margin = 0,
    show_line = False)

# add bar and axis
plot.add(color_bar)
plot.add(z_axis)

# map bar scale to z-axis
plot.map(color_bar, 'scale', z_axis, 'scale')

# add series
series = plot.rects(
    data = data,
    x = lambda d: d[0],
    y = lambda d: d[1],
    width = 2/(count-1),
    height = 2/(count-1),
    margin = 0,
    line_width = 0,
    fill_color = lambda d: color_bar.get_color(d[2]))

# show plot
plot.zoom()
plot.view("Heatmap Plot", 660, 500)
