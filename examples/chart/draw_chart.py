#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero
import perrot

# init chart
chart = perrot.chart.Chart(
    bgr_fill_color = pero.colors.LightGrey,
)

# add titles
top_title = perrot.chart.Title(
    position = pero.TOP,
    text = "Top Title",
    font_size = 14)

bottom_title = perrot.chart.Title(
    position = pero.BOTTOM,
    text = "Bottom Title")

left_title = perrot.chart.Title(
    position = pero.LEFT,
    text = "Left Title")

right_title = perrot.chart.Title(
    position = pero.RIGHT,
    text = "Right Title")

chart.add(top_title)
chart.add(bottom_title)
chart.add(left_title)
chart.add(right_title)

# add legend
legend = perrot.chart.OutLegend(
    position = pero.TOP,
    orientation = pero.HORIZONTAL,
    z_index = top_title.z_index - 1,
    items = (
        pero.MarkerLegend(text="Legend 1", marker='o', marker_fill_color='r'),
        pero.MarkerLegend(text="Legend 2", marker='s', marker_fill_color='g'))
)

chart.add(legend)

# show chart
chart.show()

