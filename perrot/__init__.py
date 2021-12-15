#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# set version
version = (0, 15, 2)

# import enums
from . enums import *

# import modules
from . import chart
from . import pie
from . import plot
from . import venn

# import main objects
from . chart import *

# import pie chart
from . pie import Pie

# import Venn diagram
from . venn import Venn

# import pre-build charts
from . prebuilds import Chart
