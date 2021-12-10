#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero
import perrot

# init data
values_1 = [40, 17, 4]
titles_1 = ["I", "II", "III"]
explode_1 = [0, 0, 0]
palette_1 = pero.colors.Dark

values_2 = [10, 8, 22, 6, 8, 3, 4]
titles_2 = ["A", "B", "AB", "C", "AC", "BC", "ABC"]
explode_2 = [0, 0.2, 0, 0, 0, 0, 0]
palette_2 = [palette_1[i].lighter(f) for i in range(3) for f in (0.2, 0.4, 0.6)]

# init pie chart
pie = perrot.pie.Pie(
    title_text = "Pie Chart",
    legend_position = pero.RIGHT)

# add rings
pie.ring(values_1, titles_1, explode_1,
    inner_radius = 0.25,
    outer_radius = 0.5,
    palette = palette_1,
    label_text = lambda d: f"{d.value/sum(values_1):.0%}",
    label_font_weight = pero.BOLD,
    label_text_color = "w")

pie.ring(values_2, titles_2, explode_2,
    palette = palette_2,
    label_font_size = 14)

# show chart
pie.show("Pie Chart", width=450, height=400)
