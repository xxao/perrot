#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from pero.properties import *

from .. enums import *
from .. chart import ChartBase, Title, OutLegend, Labels
from .. pie import Pie
from .. venn import Venn


class Chart(ChartBase):
    """
    Chart provides a pre-build simple chart with included title, legend and
    labels container. In addition, convenient methods to create pie chart or
    venn diagram are available.
    
    Properties:
        
        title: perrot.Title, None or UNDEF
            Specifies the title display graphics.
        
        legend: perrot.Legend, None or UNDEF
            Specifies the legend display graphics.
        
        label: pero.TextLabel
            Specifies the glyph to be used to draw labels.
    """
    
    title = Property(UNDEF, types=(Title,), dynamic=False, nullable=True)
    legend = Property(UNDEF, types=(OutLegend,), dynamic=False, nullable=True)
    labels = Property(UNDEF, types=(Labels,), dynamic=False, nullable=True)
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of the Chart."""
        
        # init title
        if 'title' not in overrides:
            overrides['title'] = Title(
                tag = 'title',
                z_index = TITLE_Z,
                position = POS_TOP)
        
        # init legend
        if 'legend' not in overrides:
            overrides['legend'] = OutLegend(
                tag = 'legend',
                z_index = LEGEND_Z,
                position = POS_RIGHT,
                orientation = ORI_VERTICAL)
        
        # init labels
        if 'labels' not in overrides:
            overrides['labels'] = Labels(
                tag = 'labels',
                z_index = LABELS_Z)
        
        # init base
        super().__init__(**overrides)
        
        # init graphics
        self._init_graphics()
        
        # bind events
        self.bind(EVT_PROPERTY_CHANGED, self._on_chart_property_changed)
    
    
    def pie(self, values, titles=None, explode=None, **overrides):
        """
        Creates and adds a new pie ring based on given values.
        
        Args:
            values: (float,)
                Values for individual wedges.
            
            titles: (str,) or None
                Titles for individual wedges.
            
            explode: (float,) or None
                Relative offsets for individual wedges.
            
            overrides: key:value pairs
                Specific properties to be set additionally to the pie ring.
        
        Returns:
            perrot.pie.Pie
                Pie ring.
        """
        
        # init z-index
        if 'z_index' not in overrides:
            overrides['z_index'] = PIE_Z
        
        # init pie
        obj = Pie(values, titles, explode, **overrides)
        
        # add object
        self.add(obj)
        
        return obj
    
    
    def venn(self, a, b, ab, c=0, ac=0, bc=0, abc=0, **overrides):
        """
        Creates and adds a new Venn diagram based on given values.
        
        Args:
            a: int
                Number of items unique to A.
            
            b: int
                Number of items unique to B.
            
            ab: int
                Number of items unique to AB overlap.
            
            c: int
                Number of items unique to C.
            
            ac: int
                Number of items unique to AC overlap.
            
            bc: int
                Number of items unique to BC overlap.
            
            abc: int
                Number of items unique to ABC overlap.
            
            overrides: key:value pairs
                Specific properties to be set additionally to the venn diagram.
        
        Returns:
            perrot.venn.Venn
                Venn diagram.
        """
        
        # init z-index
        if 'z_index' not in overrides:
            overrides['z_index'] = VENN_Z
        
        # init venn
        obj = Venn(a, b, ab, c, ac, bc, abc, **overrides)
        
        # add object
        self.add(obj)
        
        return obj
    
    
    def _init_graphics(self):
        """Initializes and registers required graphics."""
        
        # register objects
        if self.title:
            self.add(self.title)
        
        if self.legend:
            self.add(self.legend)
        
        if self.labels:
            self.add(self.labels)
    
    
    def _on_chart_property_changed(self, evt):
        """Called after any property has changed."""
        
        # main objects
        if evt.name in ('title', 'legend', 'labels'):
            
            # remove old
            if evt.old_value:
                self.remove(evt.old_value.tag)
            
            # register new
            if evt.new_value:
                self.add(evt.new_value)
