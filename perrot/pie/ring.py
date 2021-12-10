#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import math

import pero
from pero.enums import *
from pero.properties import *
from pero import colors
from pero import Frame, OrdinalScale, TextLabel

from .. chart import InGraphics
from . wedge import Wedge


class Ring(InGraphics):
    """
    Defines a single ring of pie chart wedges.
    
    Properties:
        
        x: int
            Specifies the x-coordinate of the center.
        
        y: int
            Specifies the y-coordinate of the center.
        
        inner_radius: int
            Specifies the inner radius.
        
        outer_radius: int
            Specifies the outer radius including all the 'explode' shifts.
        
        angle properties:
            Includes pero.AngleProperties to specify the start angle.
        
        palette: pero.Palette, tuple, str
            Specifies the default color palette as a sequence of colors,
            pero.Palette or palette name. This is used to automatically
            provide new color for individual wedges.
        
        line properties:
            Includes pero.LineProperties to specify the wedges outline.
        
        label: pero.TextLabel
            Specifies the glyph to be used to draw labels.
    """
    
    x = NumProperty(UNDEF, dynamic=False)
    y = NumProperty(UNDEF, dynamic=False)
    inner_radius = NumProperty(UNDEF, dynamic=False)
    outer_radius = NumProperty(UNDEF, dynamic=False)
    angle = Include(AngleProperties, dynamic=False, angle=-0.5*math.pi)
    
    outline = Include(LineProperties, line_width=1, line_color="w")
    palette = PaletteProperty(colors.Dark, dynamic=False, nullable=False)
    
    label = Property(UNDEF, types=(TextLabel,), dynamic=False, nullable=True)
    
    
    def __init__(self, values, titles=None, explode=None, **overrides):
        """Initializes a new instance of wedges ring."""
        
        # init label
        if 'label' not in overrides:
            overrides['label'] = TextLabel(
                text = lambda d: d.value,
                x = lambda d: d.label_x,
                y = lambda d: d.label_y,
                font_size = 12,
                text_align = TEXT_ALIGN_CENTER,
                text_base = TEXT_BASE_MIDDLE)
        
        # init base
        super().__init__(**overrides)
        
        # get data
        self._values = tuple(values)
        self._titles = tuple(titles) if titles else tuple("" for _ in values)
        self._explode = tuple(explode) if explode else tuple(0 for _ in values)
        self._wedges = []
        
        # check data
        if len(self._values) != len(self._titles) or len(self._values) != len(self._explode):
            raise ValueError("Unequal length for values, titles and explode!")
        
        # init graphics
        self._init_graphics()
        
        # bind events
        self.bind(EVT_PROPERTY_CHANGED, self._on_ring_property_changed)
    
    
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
        
        # get properties
        label = self.get_property('label', source, overrides)
        
        # update wedges
        self._update_wedges(canvas, source, **overrides)
        
        # draw wedges
        for obj in self._wedges:
            obj.draw(canvas)
        
        # draw labels
        if label:
            for obj in self._wedges:
                if obj.is_visible(obj):
                    label.draw(canvas, obj)
    
    
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
        outer_radius = (outer_radius + (inner_radius * max(self._explode))) / (1 + max(self._explode))
        
        # init values
        start_angle = angle or 0
        total = float(sum(self._values))
        label_x = x + 0.5 * (outer_radius + inner_radius)
        label_y = y
        
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
            
            # update label
            angle = wedge.start_angle + 0.5 * (wedge.end_angle - wedge.start_angle)
            wedge.label_x, wedge.label_y = pero.rotate((label_x + wedge.offset, label_y), angle, (x, y))
            
            # keep last angle
            start_angle = wedge.end_angle
    
    
    def _init_graphics(self):
        """Initializes wedges glyphs."""
        
        # init container
        self._wedges = []
        
        # init wedges
        for i in range(len(self._values)):
            
            # init wedge
            wedge = Wedge(
                value = self._values[i],
                title = self._titles[i])
            
            # lock value
            wedge.lock_property('value')
            
            # store wedge
            self._wedges.append(wedge)
        
        # set wedges line and fill
        self._init_colors()
    
    
    def _init_colors(self):
        """Sets colors."""
        
        # init color scale
        color_scale = OrdinalScale(
            out_range = self.palette,
            implicit = True,
            recycle = True)
        
        # update wedges
        for obj in self._wedges:
            obj.fill_color = color_scale.scale(obj.tag)
            obj.set_properties_from(self, 'line_', 'line_')
    
    
    def _on_ring_property_changed(self, evt):
        """Called after any property has changed."""
        
        # color palette changed
        if evt.name == 'palette':
            self._init_colors()
        
        # outline changed
        if evt.name.startswith('line_'):
            self._init_colors()
