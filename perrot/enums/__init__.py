#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

# import pero enums
from pero.enums import *

# define constants
CHART_FRAME = 'chart_frame'
DATA_FRAME = 'data_frame'

GRID_MAJOR_Z = 20
GRID_MINOR_Z = 10

AXIS_Z = 10
COLOR_BAR_Z = 1000
TITLE_Z = 5000

SERIES_Z = 1000
PIE_Z = 1000
VENN_Z = 1000

LABELS_Z = 2000
ANNOTS_Z = 3000
LEGEND_Z = 4000

VENN_CIRCLE_Z = 1000
VENN_REGION_Z = 1100

# define values
MAJOR = 'major'
MINOR = 'minor'

FULL = 'full'
SEMI = 'semi'

ZOOM_X = 'x'
ZOOM_Y = 'y'
ZOOM_XY = 'xy'
ZOOM_AUTO = 'auto'

MEASURE_X = 'x'
MEASURE_Y = 'y'
MEASURE_AUTO = 'auto'

# define gridlines modes
GRID_MAJOR = MAJOR
GRID_MINOR = MINOR

GRID_MODE = Enum(
    MAJOR = GRID_MAJOR,
    MINOR = GRID_MINOR)

# define venn diagram modes
VENN_NONE = NONE
VENN_SEMI = SEMI
VENN_FULL = FULL

VENN_MODE = Enum(
    NONE = VENN_NONE,
    SEMI = VENN_SEMI,
    FULL = VENN_FULL)

# define zoom tool modes
ZOOM_MODE = Enum(
    X = ZOOM_X,
    Y = ZOOM_Y,
    XY = ZOOM_XY,
    AUTO = ZOOM_AUTO)

# define measurement tool mode
MEASURE_MODE = Enum(
    X = MEASURE_X,
    Y = MEASURE_Y,
    AUTO = MEASURE_AUTO)
