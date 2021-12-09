#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import math

from pero.enums import *
from pero.properties import *
from pero import Wedge as WedgeGlyph


class Wedge(WedgeGlyph):
    """
    Defines a wedge glyph.
    
    Properties:
        
        value: int or float
            Specifies the wedge value.
        
        title: str or callable
            Specifies the wedge title.
    """
    
    value = NumProperty(0, dynamic=False)
    title = StringProperty(UNDEF)
