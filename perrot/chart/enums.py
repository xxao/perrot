#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from pero import Enum

# constants
DATA_FRAME = 'data_frame'

GRID_MAJOR = 'major'
GRID_MINOR = 'minor'

# define grid mode
GRID_MODE = Enum(
    MAJOR = GRID_MAJOR,
    MINOR = GRID_MINOR)
