#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from pero.properties import *
from pero import ParallelGrid
from pero import ContinuousScale, LinScale
from pero import Ticker, LinTicker

from .. enums import *
from . graphics import InGraphics


class Grid(InGraphics):
    """
    Grid provides a wrapper for the pero.ParallelGrid glyph to draw major or
    minor grid lines according to specified orientation, scale and ticker.
    
    Properties:
        
        mode: str
            Specifies the grid ticks type to use as as any item from the
            perrot.GRID_MODE enum.
        
        scale: pero.ContinuousScale
            Specifies the scale providing actual range to use and to
            re-calculate the ticks values into final coordinates.
        
        ticker: pero.Ticker
            Specifies the ticks generator to provide lines positions.
        
        orientation: str
            Specifies the lines orientation as any item from the
            pero.ORIENTATION enum.
        
        line properties:
            Includes pero.LineProperties to specify the lines.
    """
    
    mode = EnumProperty(GRID_MAJOR, enum=GRID_MODE, dynamic=False)
    scale = Property(UNDEF, types=(ContinuousScale,), dynamic=False)
    ticker = Property(UNDEF, types=(Ticker,), dynamic=False)
    
    orientation = EnumProperty(ORI_HORIZONTAL, enum=ORIENTATION, dynamic=False)
    line = Include(LineProperties, dynamic=False, line_color="#e6e6e6ff")
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of the Grid."""
        
        # init base
        super().__init__(**overrides)
        
        # init glyph
        self._glyph = ParallelGrid(relative=False)
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw the grid."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # update grid glyph
        self._update_glyph(canvas, source, **overrides)
        
        # draw grid
        self._glyph.draw(canvas)
    
    
    def _update_glyph(self, canvas=None, source=UNDEF, **overrides):
        """Updates grid glyph."""
        
        # get properties
        frame = self.get_property('frame', source, overrides)
        orientation = self.get_property('orientation', source, overrides)
        scale = self.get_property('scale', source, overrides)
        ticker = self.get_property('ticker', source, overrides)
        mode = self.get_property('mode', source, overrides)
        
        # check scale
        if not scale or not ticker:
            self._glyph.ticks = ()
            return
        
        # get ticks
        ticker.start = scale.in_range[0]
        ticker.end = scale.in_range[1]
        ticks = ticker.minor_ticks() if mode == GRID_MINOR else ticker.major_ticks()
        
        # scale ticks
        ticks = tuple(map(scale.scale, ticks))
        
        # get length
        length = frame.width
        if orientation == ORI_VERTICAL:
            length = frame.height
        
        # update glyph shared
        self._glyph.set_properties_from(self, source=source, overrides=overrides)
        
        # update grid
        self._glyph.x = frame.x
        self._glyph.y = frame.y
        self._glyph.ticks = ticks
        self._glyph.length = length
        self._glyph.orientation = orientation
