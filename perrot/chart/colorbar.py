#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from pero.properties import *
from pero import colors
from pero import ColorBar as ColorBarGlyph
from pero import ContinuousScale, LinScale

from .. enums import *
from .graphics import OutGraphics


class ColorBar(OutGraphics):
    """
    ColorBar provides a wrapper for the pero.ColorBar glyph to visualize a color
    gradient range used to colorize data within a chart.
    
    Properties:
        
        scale: pero.ContinuousScale
            Specifies the scale providing actual data range and to normalize
            input values for gradient.
        
        gradient: pero.Gradient, pero.Palette, tuple, str or callable
            Specifies the color gradient as a sequence of colors,
            pero.Palette, palette name. Note that the gradient is expected to be
            normalized to range 0-1.
        
        thickness: int or float
            Specifies the bar thickness.
        
        steps: int
            Specifies the number of color steps to use for gradient drawing.
        
        line properties:
            Includes pero.LineProperties to specify the bar outline.
        
        fill properties:
            Includes pero.FillProperties to specify the bar fill.
    """
    
    position = EnumProperty(POS_RIGHT, enum=POSITION_LRTB, dynamic=False)
    
    scale = Property(UNDEF, types=(ContinuousScale,), dynamic=False)
    gradient = GradientProperty(UNDEF, dynamic=False)
    
    thickness = NumProperty(20, dynamic=False)
    steps = NumProperty(128, dynamic=False)
    line = Include(LineProperties, line_color="#000")
    fill = Include(FillProperties, fill_color="#fff")
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of the ColorBar."""
        
        # init scale
        if 'scale' not in overrides:
            overrides['scale'] = LinScale()
        
        # init gradient
        if 'gradient' not in overrides:
            overrides['gradient'] = colors.YlOrBr
        
        # init base
        super().__init__(**overrides)
        
        # init glyph
        self._glyph = ColorBarGlyph()
    
    
    def get_extent(self, canvas, source=UNDEF, **overrides):
        """
        This method is automatically called by parent plot to get amount of
        logical space needed to draw the object.
        """
        
        return self.get_property('thickness', source, overrides)
    
    
    def get_color(self, value):
        """
        Converts given value into color according to current gradient and scale.
        
        Args:
            value: float
                Value to convert in real data units.
        
        Returns:
            pero.Color
                Corresponding color.
        """
        
        # normalize value by current scale
        norm = self.scale.normalize(value)
        
        # convert normalized value into color
        return self.gradient.color_at(norm)
    
    
    def draw(self, canvas, source=None, **overrides):
        """Uses given canvas to draw color bar."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # update gauge glyph
        self._update_glyph(canvas, source, **overrides)
        
        # draw colorbar
        self._glyph.draw(canvas)
    
    
    def _update_glyph(self, canvas=None, source=UNDEF, **overrides):
        """Updates colorbar glyph."""
        
        # get properties
        frame = self.get_property('frame', source, overrides)
        position = self.get_property('position', source, overrides)
        
        # get orientation
        orientation = ORI_VERTICAL
        if position in (POS_TOP, POS_BOTTOM):
            orientation = ORI_HORIZONTAL
        
        # get length
        length = frame.height if orientation == ORI_VERTICAL else frame.height
        
        # update glyph shared
        self._glyph.set_properties_from(self, source=source, overrides=overrides)
        
        # update colorbar
        self._glyph.x = frame.x
        self._glyph.y = frame.y
        self._glyph.orientation = orientation
        self._glyph.reverse = orientation == ORI_VERTICAL
        self._glyph.length = length
