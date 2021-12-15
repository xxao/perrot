#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from pero.properties import *
from pero import Wedge


class PieWedge(Wedge):
    """
    Defines a pie chart wedge glyph.
    
    Properties:
        
        value: int or float
            Specifies the wedge value.
        
        title: str or callable
            Specifies the wedge title.
        
        label_x: int
            Specifies the x-coordinate of the label.
        
        label_y: int
            Specifies the y-coordinate of the label.
    """
    
    value = NumProperty(0, dynamic=False)
    title = StringProperty(UNDEF)
    
    label_x = NumProperty(0, dynamic=False)
    label_y = NumProperty(0, dynamic=False)
