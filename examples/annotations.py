#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import numpy
import pero
import perrot

# prepare data
x_data = numpy.linspace(-2*numpy.pi, 2*numpy.pi, 100)
y_data = numpy.sin(x_data)
x_data /= numpy.pi

# init chart
plot = perrot.Plot(
    title_text = "Plot Annotations",
    x_axis_title = "pi",
    y_axis_title = "f(x)")

# add series
series = plot.scatter(
    title = "sin(x)",
    x = x_data,
    y = y_data,
    marker = 'o',
    marker_size = 5)

# zoom axes
plot.x_axis.zoom(-1.5, 1.5)
plot.y_axis.zoom(-1.5, 1.5)

# add zero lines annotations
x_zero = plot.vline(
    x = 0,
    line_color = pero.colors.Red,
    z_index = series.z_index-1)

y_zero = plot.hline(
    y = 0,
    line_color = pero.colors.Red,
    z_index = series.z_index-1)

# add zero bands annotations
x_band = plot.vband(
    left = -0.25,
    right = 0.25,
    fill_color = pero.colors.Grey.trans(0.9),
    z_index = series.z_index-2)

y_band = plot.hband(
    top = -0.25,
    bottom = 0.25,
    fill_color = pero.colors.Grey.trans(0.9),
    z_index = series.z_index-2)

# add unit rectangle annotation
rect = pero.Bar(
    fill_color = pero.colors.LightBlue.opaque(0.2),
    line_color = pero.colors.LightBlue,
    left = -1,
    right = 1,
    top = 1,
    bottom = -1,
    z_index = series.z_index-3)

plot.annotate(rect, x_props=('left', 'right'), y_props=('top', 'bottom'))

# add text annotations
left_text = plot.text(
    x = -.5,
    y = 1,
    text = "-pi/2",
    text_align = pero.RIGHT,
    text_base = pero.MIDDLE,
    line_color = pero.colors.Green,
    fill_color = pero.colors.LightGreen.lighter(0.5),
    x_offset = -5,
    y_offset = 0)

right_text = plot.text(
    x = .5,
    y = -1,
    text = "+pi/2",
    text_align = pero.LEFT,
    text_base = pero.MIDDLE,
    line_color = pero.colors.Red,
    fill_color = pero.colors.Red.lighter(0.5),
    x_offset = 5,
    y_offset = 0)

# add arrow annotation
arrow = pero.Arrow.create(
    '<|s|>',
    x1 = -.5,
    y1 = 1,
    x2 = .5,
    y2 = -1,
    line_color = pero.colors.Black,
    fill_color = pero.colors.Black,
    line_style = pero.DASHDOTTED)

plot.annotate(arrow, x_props=('x1', 'x2'), y_props=('y1', 'y2'))

# show chart
plot.view("Plot Annotations", width=600, height=400)
