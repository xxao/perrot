#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from pero.properties import *
from pero import StraitGauge
from pero import ContinuousScale, LinScale

from .. enums import *
from . graphics import OutGraphics


class PositionBar(OutGraphics):
    """
    PositionBar provides a wrapper for the pero.Gauge glyph to get an overview
    of current zoom in the context of the chart full data range.
    
    Properties:
        
        scale: pero.ContinuousScale
            Specifies the scale providing actual data range to display and to
            re-calculate the range into final coordinates.
        
        full_range: (float, float)
            Specifies the minimum and maximum values of the full range in real
            data units. This property is automatically set by parent plot.
        
        thickness: int or float
            Specifies the gauge thickness.
        
        radius: int, float, tuple or UNDEF
            Specifies the corner radius as a single value or values for
            individual corners starting from top-left.
        
        limit: int, float or callable
            Specifies the minimum display length of the foreground.
        
        bgr_line properties:
            Includes pero.LineProperties to specify the background outline.
        
        bgr_fill properties:
            Includes pero.FillProperties to specify the background fill.
        
        for_line properties:
            Includes pero.LineProperties to specify the foreground outline.
        
        for_fill properties:
            Includes pero.FillProperties to specify the foreground fill.
    """
    
    scale = Property(UNDEF, types=(ContinuousScale,), dynamic=False)
    full_range = TupleProperty((0., 1.), types=(float,), dynamic=False)
    
    x = NumProperty(0, dynamic=False)
    y = NumProperty(0, dynamic=False)
    thickness = NumProperty(7, dynamic=False)
    radius = QuadProperty(0, dynamic=False)
    limit = NumProperty(5)
    
    bgr_pen = Include(LineProperties, prefix="bgr_", dynamic=False, line_color="#555")
    bgr_fill = Include(FillProperties, prefix="bgr_", dynamic=False, fill_color="#ccc")
    for_pen = Include(LineProperties, prefix="for_", dynamic=False, line_color="#000a")
    for_fill = Include(FillProperties, prefix="for_", dynamic=False, fill_color="#000a")
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of the PositionBar."""
        
        # init scale
        if 'scale' not in overrides:
            overrides['scale'] = LinScale()
        
        # init base
        super().__init__(**overrides)
        
        # init glyph
        self._glyph = StraitGauge()
    
    
    def get_extent(self, canvas, source=UNDEF, **overrides):
        """
        This method is automatically called by parent chart to get amount of
        logical space needed to draw the object.
        """
        
        return self.get_property('thickness', source, overrides)
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw position bar."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # update gauge glyph
        self._update_glyph(canvas, source, **overrides)
        
        # draw gauge
        self._glyph.draw(canvas)
    
    
    def _update_glyph(self, canvas=None, source=UNDEF, **overrides):
        """Updates gauge glyph."""
        
        # get properties
        frame = self.get_property('frame', source, overrides)
        position = self.get_property('position', source, overrides)
        scale = self.get_property('scale', source, overrides)
        full_range = self.get_property('full_range', source, overrides)
        
        # get orientation
        orientation = ORI_HORIZONTAL
        if position in (POS_LEFT, POS_RIGHT):
            orientation = ORI_VERTICAL
        
        # get length
        length = abs(scale.out_range[1] - scale.out_range[0])
        
        # get range
        start = 0
        end = 1
        
        if full_range and full_range[0] is not None and full_range[1] is not None:
            
            bar_min = scale.out_range[0]
            bar_max = scale.out_range[1]
            full_min = scale.scale(full_range[0])
            full_max = scale.scale(full_range[1])
            full_length = abs(full_max - full_min)
            
            if full_min > full_max:
                full_min, full_max = full_max, full_min
            
            if bar_min > bar_max:
                bar_min, bar_max = bar_max, bar_min
            
            if full_length:
                start = (bar_min - full_min) / full_length
                end = (bar_max - full_min) / full_length
            
            elif full_min < bar_min:
                start = 1
                end = 1
            
            elif full_max > bar_max:
                start = 0
                end = 0
        
        # update glyph shared
        self._glyph.set_properties_from(self, source=source, overrides=overrides)
        
        # update glyph
        self._glyph.x = frame.x
        self._glyph.y = frame.y
        self._glyph.orientation = orientation
        self._glyph.start = start
        self._glyph.end = end
        self._glyph.length = length
