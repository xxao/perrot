#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import math

from pero.properties import *
from pero import Text

from .. enums import *
from . graphics import OutGraphics


class Title(OutGraphics):
    """
    Title provides a wrapper for the pero.Text glyph to draw chart titles.
    
    Properties:
        
        text: str, None or UNDEF
            Specifies the text to show.
        
        text properties:
            Includes pero.TextProperties to specify the text properties.
    """
    
    position = EnumProperty(POS_TOP, enum=POSITION_LRTB, dynamic=False)
    
    text = StringProperty(UNDEF, dynamic=False)
    font = Include(TextProperties, dynamic=False, font_size=14, font_weight=FONT_WEIGHT_BOLD, text_align=TEXT_ALIGN_CENTER)
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of the Title."""
        
        super().__init__(**overrides)
        self._glyph = Text()
    
    
    def get_extent(self, canvas, source=UNDEF, **overrides):
        """
        This method is automatically called by parent chart to get amount of
        logical space needed to draw the object.
        """
        
        # check if visible
        if not self.is_visible(source, overrides):
            return 0
        
        # get properties
        text = self.get_property('text', source, overrides)
        
        # set text
        canvas.set_text_by(self)
        
        # get size
        return canvas.get_text_size(text)[1]
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw the title."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # update grid glyph
        self._update_glyph(canvas, source, **overrides)
        
        # draw grid
        self._glyph.draw(canvas)
    
    
    def _update_glyph(self, canvas=None, source=UNDEF, **overrides):
        """Updates text glyph."""
        
        # get properties
        frame = self.get_property('frame', source, overrides)
        position = self.get_property('position', source, overrides)
        align = self.get_property('text_align', source, overrides)
        text = self.get_property('text', source, overrides)
        
        # get angle and coords
        angle = 0
        x, y, width, height = frame.rect
        
        if position in (POS_TOP, POS_BOTTOM):
            angle = 0
            y += 0.5*height
            
            if align == TEXT_ALIGN_CENTER:
                x += 0.5*width
            elif align == TEXT_ALIGN_RIGHT:
                x += width
        
        elif position == POS_LEFT:
            angle = -0.5*math.pi
            x += 0.5*width
            
            if align == TEXT_ALIGN_CENTER:
                y += 0.5*height
            elif align == TEXT_ALIGN_LEFT:
                y += height
        
        elif position == POS_RIGHT:
            angle = 0.5*math.pi
            x += 0.5*width
            
            if align == TEXT_ALIGN_CENTER:
                y += 0.5*height
            elif align == TEXT_ALIGN_RIGHT:
                y += height
        
        # update glyph shared
        self._glyph.set_properties_from(self, source=source, overrides=overrides)
        
        # update text
        self._glyph.text = text
        self._glyph.x = x
        self._glyph.y = y
        self._glyph.angle = angle
        self._glyph.text_base = TEXT_BASE_MIDDLE
