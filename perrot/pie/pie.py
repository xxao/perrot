#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from pero.enums import *
from pero.properties import *
from pero import colors
from pero import Path, TextLabel, MarkerLegend
from pero import OrdinalScale

from .. chart import Chart, Title, OutLegend
from . ring import Ring


class Pie(Chart):
    """
    This class provides main functionality to construct and draw pie charts.
    
    Properties:
        
        title: perrot.chart.Title, None or UNDEF
            Specifies the title display graphics.
        
        legend: perrot.chart.OutLegend, None or UNDEF
            Specifies the legend display graphics.
    """
    
    title = Property(UNDEF, types=(Title,), dynamic=False, nullable=True)
    legend = Property(UNDEF, types=(OutLegend,), dynamic=False, nullable=True)
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of pie chart."""
        
        # init title
        if 'title' not in overrides:
            overrides['title'] = Title(
                tag = 'title',
                position = POS_TOP)
        
        # init legend
        if 'legend' not in overrides:
            overrides['legend'] = OutLegend(
                tag = 'legend',
                position = POS_RIGHT,
                orientation = ORI_VERTICAL)
        
        # init base
        super().__init__(**overrides)
        
        # init containers
        self._rings = []
        
        # init graphics
        self._init_graphics()
        
        # bind events
        self.bind(EVT_PROPERTY_CHANGED, self._on_pie_property_changed)
    
    
    @property
    def rings(self):
        """
        Gets individual rings.
        
        Returns:
            (perrot.pie.Ring,)
                Pie rings.
        """
        
        return tuple(self._rings)
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw the diagram."""
        
        # update legend
        self._update_legend(canvas, source, overrides)
        
        # init frames
        self.init_frames(canvas, source, **overrides)
        
        # draw main bgr
        self.draw_bgr(canvas, source, **overrides)
        
        # refuse to draw if "negative" size
        if self.get_frame().reversed:
            return
        
        # get objects
        objects = list(self.graphics)
        objects.sort(key=lambda o: o.z_index)
        rings = [o for o in objects if isinstance(o, Ring)]
        others = [o for o in objects if not isinstance(o, Ring)]
        
        # get max radius
        data_frame = self.get_frame()
        max_radius = 0.5 * min(data_frame.wh)
        
        # draw rings
        last_radius = 0
        for i, obj in enumerate(rings):
            
            # get inner radius
            inner_radius = obj.inner_radius
            if inner_radius is UNDEF:
                inner_radius = last_radius
            else:
                inner_radius *= max_radius
            
            # get outer radius
            outer_radius = max_radius * (obj.outer_radius or (i + 1) / len(rings))
            
            # check radii
            inner_radius = min(inner_radius, max_radius)
            outer_radius = min(outer_radius, max_radius)
            
            # remember last
            last_radius = outer_radius
            
            # draw ring
            obj.draw(canvas,
                x = data_frame.cx,
                y = data_frame.cy,
                inner_radius = inner_radius,
                outer_radius = outer_radius)
        
        # draw remaining objects
        for obj in others:
            obj.draw(canvas)
        
        # draw debug frames
        # self.draw_frames(canvas)
    
    
    def add(self, obj):
        """
        Adds additional graphics to the chart.
        
        Args:
            obj: perrot.plot.InGraphics or perrot.plot.OutGraphics
                Object to be added.
        """
        
        # register object
        super().add(obj)
        
        # add to rings
        if isinstance(obj, Ring):
            self._rings.append(obj)
    
    
    def remove(self, obj):
        """
        Removes object corresponding to given tag.
        
        Args:
            obj: str or pero.Graphics
                Object's unique tag or the object itself.
        """
        
        # get object
        obj = self.get_obj(obj)
        
        # remove object
        super().remove(obj)
        
        # remove ring
        if obj in self._rings:
            self._rings.remove(obj)
    
    
    def ring(self, values, titles=None, explode=None, **overrides):
        """
        Creates and adds a new pie chart ring based on given values.
        
        Args:
            values: (float,)
                Values for individual wedges.
            
            titles: (str,) or None
                Titles for individual wedges.
            
            explode: (float,) or None
                Shifts from center for individual wedges.
        """
        
        # create and add ring
        self.add(Ring(values, titles, explode, **overrides))
    
    
    def _update_legend(self, canvas, source, overrides):
        """Updates legend items."""
        
        # check if visible
        if not self.legend or not self.legend.is_visible():
            return
        
        # check if static
        if self.legend.static:
            return
        
        # get items
        items = []
        for ring in self._rings:
            for obj in ring.wedges:
                
                # skip empty
                if obj.value == 0:
                    continue
                
                # get title
                title = obj.get_property('title', obj)
                if not title:
                    continue
                
                # init item
                item = MarkerLegend(
                    text = title,
                    marker = 'o',
                    marker_size = 12)
                
                # set line and fill
                item.marker.set_properties_from(obj, 'line_', 'line_')
                item.marker.set_properties_from(obj, 'fill_', 'fill_')
                
                # add item
                items.append(item)
        
        # set items
        self.legend.items = items
    
    
    def _init_graphics(self):
        """Initializes and registers required graphics."""
        
        # register additional objects
        if self.legend:
            self.add(self.legend)
        
        if self.title:
            self.add(self.title)
    
    
    def _on_pie_property_changed(self, evt):
        """Called after any property has changed."""
        
        # main objects
        if evt.name in ('title', 'legend'):
            
            # remove old
            if evt.old_value:
                self.remove(evt.old_value.tag)
            
            # register new
            if evt.new_value:
                self.add(evt.new_value)
