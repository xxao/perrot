#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import numpy
import pero
import perrot

# prepare data
categories = ("Category A", 'Category B', "Category C", "Category D", "Category E")
y_data1 = numpy.array((5, 10, 7, 3, 4))
y_data2 = numpy.array((7, 5, 9, 1, 5))
y_data3 = numpy.array((2, 1, 3, 5, 4))

# init ordinal x-axis
x_axis = perrot.OrdinalAxis(
    position = perrot.BOTTOM,
    margin = 0,
    labels = categories,
    major_tick_size = 0,
    minor_tick_size = 6,
    level = 1)

# init plot
plot = perrot.Plot(
    x_axis = x_axis,
    y_axis_title = "count",
    y_axis_autoscale = True,
    x_major_grid = None)

# init labels
label = pero.TextLabel(
    text = lambda d: str(d),
    text_color = perrot.colors.White,
    text_base = perrot.MIDDLE,
    font_size = 13,
    font_weight = perrot.BOLD)

# add series
series1 = plot.vbars(
    title = "Series 1",
    data = y_data1,
    x = categories,
    top = y_data1,
    x_mapper = x_axis.mapper,
    anchor = perrot.CENTER,
    show_labels = True,
    label = label,
    x_axis = x_axis)

series2 = plot.vbars(
    title = "Series 2",
    data = y_data2,
    x = categories,
    top = y_data2,
    y_offset = y_data1,
    x_mapper = x_axis.mapper,
    anchor = perrot.CENTER,
    show_labels = True,
    label = label,
    x_axis = x_axis)

series3 = plot.vbars(
    title = "Series 3",
    data = y_data3,
    x = categories,
    top = y_data3,
    y_offset = y_data1 + y_data2,
    x_mapper = x_axis.mapper,
    anchor = perrot.CENTER,
    show_labels = True,
    label = label,
    x_axis = x_axis)

# show plot
plot.zoom()
plot.view("Stacked Series")
