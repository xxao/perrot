#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import perrot

# init chart
chart = perrot.Chart(
    title_text = "Venn Diagram",
    legend_position = perrot.TOP,
    legend_orientation = perrot.HORIZONTAL)

# add venn diagram
data = [10, 8, 22, 6, 9, 4, 2]

venn = chart.venn(*data,
    mode = perrot.SEMI,
    palette = perrot.colors.Dark.trans(0.6),
    A_title = "Series A",
    B_title = "Series B",
    C_title = "Series C",
    label_text = lambda d: f"{d.value}\n{d.value/sum(data):.0%}")

# show chart
chart.show("Venn Diagram", width=450, height=400)
