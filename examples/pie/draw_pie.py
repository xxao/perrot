#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero
import perrot

# init data
values1 = [10, 8, 22, 6, 9, 4, 2]
titles1 = ["A", "B", "AB", "C", "AC", "BC", "ABC"]

values2 = [40, 19, 2]
titles2 = ["I", "II", "III"]

# init pie chart
pie = perrot.pie.Pie(
    title_text = "Pie Chart",
    legend_position = pero.RIGHT)

# add rings
pie.ring(values1, titles1, inner_radius=0.33, outer_radius=0.66, palette=pero.colors.Dark)
pie.ring(values2, titles2, palette=pero.colors.Set2)

# show chart
pie.show("Pie Chart", width=500, height=400)
