#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero
import perrot


# init sizer
sizer = pero.Sizer(graphics_padding=(30, 0, 0, 0))
rows = -1
margin = 1, 30

# add linear axis
lin_axis = perrot.LinAxis(
    title = "LinAxis",
    tag = "lin_axis",
    scale_in_range = (-100, 100),
    margin = margin)

rows += 1
sizer.add(perrot.AxisControl(graphics=lin_axis), row=rows, col=0)

# add log10 axis
log10_axis = perrot.LogAxis(
    title = "LogAxis (10)",
    tag = "log10_axis",
    scale_in_range = (1, 1000),
    margin = margin)

rows += 1
sizer.add(perrot.AxisControl(graphics=log10_axis), row=rows, col=0)

# add log2 axis
log2_axis = perrot.LogAxis(
    title = "LogAxis (2)",
    tag = "log2_axis",
    base = 2,
    scale_in_range = (1, 512),
    margin = margin)

rows += 1
sizer.add(perrot.AxisControl(graphics=log2_axis), row=rows, col=0)

# add symlog10 axis
symlog10_axis = perrot.SymlogAxis(
    title = "SymlogAxis (10, 0.01)",
    tag = "symlog_axis",
    threshold = .01,
    scale_in_range = (-100, 100),
    margin = margin)

rows += 1
sizer.add(perrot.AxisControl(graphics=symlog10_axis), row=rows, col=0)

# add symlog2 axis
symlog2_axis = perrot.SymlogAxis(
    title = "SymlogAxis (2, 1)",
    tag = "symlog_axis",
    base = 2,
    threshold = 1,
    scale_in_range = (-512, 512),
    margin = margin)

rows += 1
sizer.add(perrot.AxisControl(graphics=symlog2_axis), row=rows, col=0)

# add time axis
time_axis = perrot.TimeAxis(
    title = "TimeAxis",
    tag = "time_axis",
    scale_in_range = (0, 1000),
    margin = margin)

rows += 1
sizer.add(perrot.AxisControl(graphics=time_axis), row=rows, col=0)

# add ordinal axis
ordinal_axis = perrot.OrdinalAxis(
    title = "OrdinalAxis",
    tag = "ordinal_axis",
    labels = ("one", 'two', "three", "four", "five"),
    major_tick_size = 0,
    static = False,
    margin = margin)

rows += 1
sizer.add(perrot.AxisControl(graphics=ordinal_axis), row=rows, col=0)

# show sizer
sizer.show("Axes", width=700, height=500)
