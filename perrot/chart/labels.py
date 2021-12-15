#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from pero.properties import *
from pero import Label, LabelBox

from .. enums import *
from . graphics import InGraphics


class Labels(InGraphics):
    """
    Labels provides a wrapper for the pero.LabelBox glyph to draw all specified
    chart labels at once.
    
    Properties:
        
        items: (pero.Label,), None or UNDEF
            Specifies labels to draw.
        
        static: bool
            Specifies whether the label items are given by user directly (True)
            or whether they should be retrieved automatically from parent chart
            (False).
        
        overlap: bool
            Specifies whether the labels can overlap each other (True) or should
            be skipped automatically if there is not enough space available
            (False).
        
        spacing: int
            Specifies the minimum additional space between adjacent labels.
        
        padding: int, (int,) or UNDEF
            Specifies the inner space as a single value or values for individual
            sides starting from top. This is used in addition to the 'clip' to
            shift partially visible labels.
    """
    
    items = ListProperty(UNDEF, types=(Label,), dynamic=False)
    static = BoolProperty(False, dynamic=False)
    
    overlap = BoolProperty(False, dynamic=False)
    spacing = NumProperty(4, dynamic=False)
    padding = QuadProperty(5, dynamic=False)
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of the Labels."""
        
        super().__init__(**overrides)
        self._glyph = LabelBox()
    
    
    def finalize(self, chart, canvas, source=UNDEF, **overrides):
        """
        This method is automatically called by parent chart to finalize the
        object.
        """
        
        # check if static
        static = self.get_property('static', source, overrides)
        if static:
            return
        
        # clean items
        self.items = []
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # get items from objects
        items = []
        for obj in chart.graphics:
            if isinstance(obj, InGraphics) and obj.visible:
                items += obj.get_labels(canvas)
        
        # set new items
        self.items = items
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw the legend."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # get properties
        frame = self.get_property('frame', source, overrides)
        
        # update glyph
        self._glyph.set_properties_from(self, source=source, overrides=overrides)
        self._glyph.clip = frame
        
        # draw labels
        self._glyph.draw(canvas)
