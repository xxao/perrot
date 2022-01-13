#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import math

import pero
from pero.properties import *
from pero import colors
from pero import OrdinalScale
from pero import MarkerLegend
from pero import Label, TextLabel
from pero import Tooltip, TextTooltip

from .. enums import *
from .. chart import InGraphics
from . wedge import PieWedge


class Pie(InGraphics):
    """
    Pie provides a mechanism to construct and draw pie chart wedges rings.
    
    Properties:
        
        x: int
            Specifies the x-coordinate of the center.
        
        y: int
            Specifies the y-coordinate of the center.
        
        inner_radius: int
            Specifies the inner radius. If the value is equal or les than 1, the
            radius is handled as relative to available space. Otherwise the
            exact radius is used.
        
        outer_radius: int
            Specifies the outer radius. If the value is equal or les than 1, the
            radius is handled as relative to available space. Otherwise the
            exact radius is used. The radius includes all the 'explode' shifts.
        
        angle properties:
            Includes pero.AngleProperties to specify the start angle.
        
        palette: pero.Palette, tuple, str
            Specifies the default color palette as a sequence of colors,
            pero.Palette or palette name. This is used to automatically
            provide new color for individual wedges.
        
        line properties:
            Includes pero.LineProperties to specify the wedges outline.
        
        legend: perrot.MarkerLegend, None or UNDEF
            Specifies the explicit value for the legend or a template to create
            it. When the actual legend is initialized, current wedge is
            provided as a source, therefore properties can be dynamic to
            retrieve the final value from the wedge.
        
        label: pero.TextLabel
            Specifies a template to create wedges labels. When the actual label
            is initialized, current wedge is provided as a source, therefore
            properties can be dynamic to retrieve the final value from the wedge.
        
        tooltip: pero.Tooltip, None or UNDEF
            Specifies a template to create wedges tooltips. When the actual
            tooltip is initialized, current wedge is provided as a source,
            therefore properties can be dynamic to retrieve the final value from
            the wedge.
        
        show_legend: bool
            Specifies whether the legend should be shown.
        
        show_labels: bool
            Specifies whether the labels should be shown.
        
        show_tooltip: bool
            Specifies whether the wedges tooltip should be shown.
    """
    
    x = NumProperty(UNDEF, dynamic=False)
    y = NumProperty(UNDEF, dynamic=False)
    inner_radius = NumProperty(UNDEF, dynamic=False)
    outer_radius = NumProperty(UNDEF, dynamic=False)
    angle = Include(AngleProperties, dynamic=False, angle=-0.5*math.pi)
    
    outline = Include(LineProperties, line_width=1, line_color="w")
    palette = PaletteProperty(colors.Dark, dynamic=False, nullable=False)
    
    legend = Property(UNDEF, types=(MarkerLegend,), dynamic=False, nullable=True)
    label = Property(UNDEF, types=(Label,), dynamic=False, nullable=True)
    tooltip = Property(UNDEF, types=(Tooltip,), dynamic=False, nullable=True)
    
    show_legend = BoolProperty(True, dynamic=False)
    show_labels = BoolProperty(True, dynamic=False)
    show_tooltip = BoolProperty(True, dynamic=False)
    
    
    def __init__(self, values, titles=None, explode=None, **overrides):
        """
        Initializes a new instance of the Pie.
        
        Args:
            values: (float,)
                Values for individual wedges.
            
            titles: (str,) or None
                Titles for individual wedges.
            
            explode: (float,) or None
                Relative offsets for individual wedges.
        """
        
        # init legend
        if 'legend' not in overrides:
            overrides['legend'] = MarkerLegend(
                text = lambda d: d.title,
                marker = MARKER_CIRCLE,
                marker_size = 12)
        
        # init label
        if 'label' not in overrides:
            overrides['label'] = TextLabel(
                text = lambda d: str(d.value),
                font_size = 12,
                text_align = TEXT_ALIGN_CENTER,
                text_base = TEXT_BASE_MIDDLE)
        
        # init tooltip
        if 'tooltip' not in overrides:
            overrides['tooltip'] = TextTooltip(
                text = lambda d: str(d.value))
        
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
        self.bind(EVT_PROPERTY_CHANGED, self._on_pie_property_changed)
    
    
    def get_legends(self, canvas=None, source=UNDEF, **overrides):
        """Gets wedges legend items."""
        
        # get properties
        show_legend = self.get_property('show_legend', source, overrides)
        legend = self.get_property('legend', source, overrides)
        
        # check legend
        if not show_legend or not legend:
            return ()
        
        # get items
        items = []
        for obj in self._wedges:
            
            # skip empty
            if not obj.visible or not obj.value or not obj.title:
                continue
            
            # init item
            item = legend.clone(obj, deep=True)
            item.marker.set_properties_from(obj, 'line_', 'line_')
            item.marker.set_properties_from(obj, 'fill_', 'fill_')
            
            # add item
            items.append(item)
        
        return items
    
    
    def get_labels(self, canvas=None, source=UNDEF, **overrides):
        """Gets wedges labels."""
        
        # get properties
        show_labels = self.get_property('show_labels', source, overrides)
        label = self.get_property('label', source, overrides)
        
        # check labels
        if not show_labels or not label:
            return ()
        
        # update wedges
        self._update_wedges(canvas, source, **overrides)
        
        # get items
        items = []
        for obj in self._wedges:
            
            # skip empty
            if not obj.visible or not obj.value:
                continue
            
            # init item
            item = label.clone(obj, deep=True)
            item.x = obj.label_x
            item.y = obj.label_y
            
            # add item
            items.append(item)
        
        return items
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw the ring."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # update wedges
        self._update_wedges(canvas, source, **overrides)
        
        # draw wedges
        for obj in self._wedges:
            obj.draw(canvas)
    
    
    def _update_wedges(self, canvas=None, source=UNDEF, **overrides):
        """Updates wedges shape."""
        
        # get properties
        frame = self.get_property('frame', source, overrides)
        x = self.get_property('x', source, overrides)
        y = self.get_property('y', source, overrides)
        inner_radius = self.get_property('inner_radius', source, overrides)
        outer_radius = self.get_property('outer_radius', source, overrides)
        angle = AngleProperties.get_angle(self, '', ANGLE_RAD, source, overrides)
        
        # get center
        if x is UNDEF:
            x = frame.cx
        if y is UNDEF:
            y = frame.cy
        
        # get max radius
        max_radius = 0.5 * min(frame.wh)
        
        # get inner radius
        inner_radius = inner_radius or 0
        if inner_radius and inner_radius <= 1:
            inner_radius = inner_radius * max_radius
        
        # get outer radius
        outer_radius = outer_radius or 1
        if outer_radius and outer_radius <= 1:
            outer_radius = outer_radius * max_radius
        
        # include explode
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
            wedge = PieWedge(
                value = self._values[i],
                title = self._titles[i])
            
            # lock value
            wedge.lock_property('value')
            
            # store wedge
            self._wedges.append(wedge)
        
        # set wedges line and fill
        self._init_colors()
    
    
    def _init_colors(self):
        """Sets colors to wedges."""
        
        # init color scale
        color_scale = OrdinalScale(
            out_range = self.palette,
            implicit = True,
            recycle = True)
        
        # update wedges
        for obj in self._wedges:
            obj.fill_color = color_scale.scale(obj.tag)
            obj.set_properties_from(self, 'line_', 'line_')
    
    
    def _on_pie_property_changed(self, evt):
        """Called after any property has changed."""
        
        # color palette changed
        if evt.name == 'palette':
            self._init_colors()
        
        # outline changed
        if evt.name.startswith('line_'):
            self._init_colors()
