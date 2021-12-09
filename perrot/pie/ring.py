#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import math

from pero.enums import *
from pero.properties import *
from pero import colors
from pero import Frame, OrdinalScale

from .. chart import InGraphics
from . wedge import Wedge


class Ring(InGraphics):
    """
    Abstract base class for various types of Venn diagram patches.
    
    Properties:
        
        x: int
            Specifies the x-coordinate of the center.
        
        y: int
            Specifies the y-coordinate of the center.
        
        inner_radius: int
            Specifies the inner radius.
        
        outer_radius: int
            Specifies the outer radius.
        
        angle properties:
            Includes pero.AngleProperties to specify the start angle.
        
        palette: pero.Palette, tuple, str
            Specifies the default color palette as a sequence of colors,
            pero.Palette or palette name. This is used to automatically
            provide new color for individual wedges.
        
        line properties:
            Includes pero.LineProperties to specify the wedges outline.
    """
    
    x = NumProperty(UNDEF, dynamic=False)
    y = NumProperty(UNDEF, dynamic=False)
    inner_radius = NumProperty(UNDEF, dynamic=False)
    outer_radius = NumProperty(UNDEF, dynamic=False)
    angle = Include(AngleProperties, dynamic=False, angle=-0.5*math.pi)
    
    outline = Include(LineProperties, line_width=1, line_color="w")
    palette = PaletteProperty(colors.Dark, dynamic=False, nullable=False)
    
    
    def __init__(self, values, titles=None, explode=None, **overrides):
        """Initializes a new instance of wedges ring."""
        
        # init base
        super().__init__(**overrides)
        
        # get data
        self._values = tuple(values)
        self._titles = tuple(titles) if titles else tuple("" for v in values)
        self._explode = tuple(explode) if explode else tuple(0 for v in values)
        self._wedges = []
        
        # init graphics
        self._init_graphics()
    
    
    @property
    def wedges(self):
        """
        Gets individual wedges.
        
        Returns:
            (perrot.pie.Wedge,)
                Pie wedges.
        """
        
        return tuple(self._wedges)
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw the ring."""
        
        # update wedges
        self._update_wedges(canvas, source, **overrides)
        
        # draw wedges
        for wedge in self._wedges:
            wedge.draw(canvas)
    
    
    def _update_wedges(self, canvas, source=UNDEF, **overrides):
        """Updates wedges shape."""
        
        # get properties
        frame = self.get_property('frame', source, overrides)
        x = self.get_property('x', source, overrides)
        y = self.get_property('y', source, overrides)
        inner_radius = self.get_property('inner_radius', source, overrides)
        outer_radius = self.get_property('outer_radius', source, overrides)
        angle = AngleProperties.get_angle(self, '', ANGLE_RAD, source, overrides)
        
        # get frame
        if not frame:
            frame = Frame(0, 0, canvas.viewport.width, canvas.viewport.height)
        
        # get center
        if x is UNDEF:
            x = frame.cx
        if y is UNDEF:
            y = frame.cy
        
        # get radii
        inner_radius = inner_radius or 0
        outer_radius = outer_radius or (0.5 * min(frame.width, frame.height))
        outer_radius /=  1 + max(self._explode)
        
        # get start
        start_angle = angle or 0
        total = float(sum(self._values))
        
        # update wedges
        for i, wedge in enumerate(self._wedges):
            
            # update shape
            wedge.x = x
            wedge.y = y
            wedge.inner_radius = inner_radius
            wedge.outer_radius = outer_radius
            wedge.offset = self._explode[i] * (outer_radius - inner_radius)
            wedge.start_angle = start_angle
            wedge.end_angle = start_angle + 2 * math.pi * self._values[i] / total
            
            # keep last angle
            start_angle = wedge.end_angle
    
    
    def _init_graphics(self):
        """Initializes wedges glyphs."""
        
        # init container
        self._wedges = []
        
        # init color scale
        color_scale = OrdinalScale(
            in_range = self._wedges,
            out_range = self.palette,
            implicit = True,
            recycle = True)
        
        # init wedges
        for i in range(len(self._values)):
            
            # init wedge
            wedge = Wedge(
                value = self._values[i],
                title = self._titles[i])
            
            # set line and fill
            wedge.fill_color = color_scale.scale(wedge.tag)
            wedge.set_properties_from(self, 'line_', 'line_')
            
            # store wedge
            self._wedges.append(wedge)
