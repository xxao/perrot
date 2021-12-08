#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero
import perrot.venn

# init data [a, b, ab, c, ac, bc, abc]
data = [10, 8, 22, 6, 9, 4, 2]
# data = [10, 8, 22]

s = sum(data)

# create venn
venn = perrot.venn.Venn(
    *data,
    mode = perrot.venn.SEMI,
    palette = pero.colors.Dark.trans(0.6),
    title_text = "Venn Diagram",
    legend_position = pero.BOTTOM,
    A_title = "Series A",
    B_title = "Series B",
    C_title = "Series C",
    label_text = lambda d: f"{d.value}\n{d.value/s:.0%}")

# show diagram
venn.show("Venn Diagram", width=400, height=400)
