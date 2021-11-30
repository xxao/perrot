#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from pero.enums import *
from pero.properties import *
from pero import colors
from pero import Glyph, Label, TextLabel, Shape

class Patch(Glyph):
    """
    """
    
    value = NumProperty(0, dynamic=False)
    label = Property(UNDEF, types=(TextLabel,))
    shape = Property(UNDEF, types=(Shape,))
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of Patch."""
        
        # init label
        if 'label' not in overrides:
            overrides['label'] = TextLabel(
                text = lambda d: str(d),
                text_align = TEXT_ALIGN_CENTER,
                text_base = TEXT_BASE_MIDDLE)
        
        # init shape
        if 'shape' not in overrides:
            overrides['shape'] = Shape()
        
        # init base
        super().__init__(**overrides)
