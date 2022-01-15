#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import perrot

# init chart
chart = perrot.Chart(
    title_text = "Pie Chart")

# add 1st pie
values_1 = [40, 17, 4]
titles_1 = ["I", "II", "III"]
explode_1 = [0, 0, 0]
palette_1 = perrot.colors.Dark

pie_1 = chart.pie(values_1, titles_1, explode_1,
    inner_radius = 0.25,
    outer_radius = 0.5,
    palette = palette_1,
    label_text = lambda d: f"{d.value/sum(values_1):.0%}",
    label_font_weight = perrot.BOLD,
    label_text_color = "w")

# add 2nd pie
values_2 = [10, 8, 22, 6, 8, 3, 4]
titles_2 = ["A", "B", "AB", "C", "AC", "BC", "ABC"]
explode_2 = [0, 0.1, 0, 0, 0, 0, 0]
palette_2 = [palette_1[i].lighter(f) for i in range(3) for f in (0.2, 0.4, 0.6)]

pie_2 = chart.pie(values_2, titles_2, explode_2,
    palette = palette_2,
    inner_radius = 0.5,
    label_font_size = 14)

# show chart
chart.show("Pie Chart", width=450, height=400)
