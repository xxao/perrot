#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from pero.properties import *
from pero import Legend, LegendBox

from .. enums import *
from . graphics import InGraphics, OutGraphics


class OutLegend(OutGraphics):
    """
    OutLegend provides a wrapper for the pero.LegendBox glyph to draw the chart
    legend outside the main data frame.
    
    Properties:
        
        items: (pero.Legend,), None or UNDEF
            Specifies a collection of legend items to draw.
        
        static: bool
            Specifies whether the legend items are given by user directly (True)
            or whether they should be retrieved automatically from parent chart
            (False).
        
        position: pero.POSITION_LRTB
            Specifies the legend position within a chart as any item from the
            pero.POSITION_LRTB enum.
        
        orientation: pero.ORIENTATION
            Specifies the legend orientation as any item from the
            pero.ORIENTATION enum.
        
        margin: int, float, (int,), (float,) or UNDEF
            Specifies the space around the legend box as a single value or
            values for individual sides starting from top.
        
        padding: int, float, (int,), (float,) or UNDEF
            Specifies the inner space of the legend box as a single value or
            values for individual sides starting from top.
        
        spacing: int or float
            Specifies the additional space between legend items.
        
        radius: int, float, (int,), (float,) or UNDEF
            Specifies the corner radius of the legend box as a single value or
            values for individual corners starting from top-left.
        
        line properties:
            Includes pero.LineProperties to specify the legend box outline.
        
        fill properties:
            Includes pero.FillProperties to specify the legend box fill.
    """
    
    items = TupleProperty(UNDEF, types=(Legend,), dynamic=False, nullable=True)
    static = BoolProperty(False, dynamic=False)
    
    position = EnumProperty(POS_RIGHT, enum=POSITION_LRTB, dynamic=False)
    orientation = EnumProperty(ORI_VERTICAL, enum=ORIENTATION)
    
    radius = QuadProperty(3, dynamic=False)
    padding = QuadProperty(5, dynamic=False)
    spacing = NumProperty(5, dynamic=False)
    
    line = Include(LineProperties, line_color="#ddd")
    fill = Include(FillProperties, fill_color="#fffc")
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of the OutLegend."""
        
        # init legend glyph
        self._glyph = LegendBox()
        
        # init base
        super().__init__(**overrides)
    
    
    def get_extent(self, canvas, source=UNDEF, **overrides):
        """
        This method is automatically called by parent chart to get amount of
        logical space needed to draw the object.
        """
        
        # check if visible
        if not self.is_visible(source, overrides):
            return 0
        
        # update glyph properties
        self._glyph.set_properties_from(self, source=source, overrides=overrides)
        
        # get bbox
        bbox = self._glyph.get_bbox(canvas, source, **overrides)
        if bbox is None:
            return 0
        
        # get extent
        position = self.get_property('position', source, overrides)
        return bbox.height if position in POSITION_TB else bbox.width
    
    
    def prepare(self, chart, canvas, source=UNDEF, **overrides):
        """
        This method is automatically called by parent chart to prepare the
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
                items += obj.get_legends(canvas)
        
        # set new items
        self.items = items
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw the legend."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # update legend glyph
        self._update_glyph(canvas, source, **overrides)
        
        # draw legend
        self._glyph.draw(canvas)
    
    
    def _update_glyph(self, canvas=None, source=UNDEF, **overrides):
        """Updates legend glyph."""
        
        # get properties
        frame = self.get_property('frame', source, overrides)
        position = self.get_property('position', source, overrides)
        
        # check values
        position = position or POS_RIGHT
        
        # get anchor
        if position == POS_TOP:
            anchor = POS_N
            x = frame.cx
            y = frame.y1
        
        elif position == POS_RIGHT:
            anchor = POS_E
            x = frame.x2
            y = frame.cy
        
        elif position == POS_BOTTOM:
            anchor = POS_S
            x = frame.cx
            y = frame.y2
        
        elif position == POS_LEFT:
            anchor = POS_W
            x = frame.x1
            y = frame.cy
        
        else:
            anchor = POS_E
            x = frame.x2
            y = frame.cy
        
        # update glyph shared
        self._glyph.set_properties_from(self, source=source, overrides=overrides)
        
        # update glyph
        self._glyph.anchor = anchor
        self._glyph.x = x
        self._glyph.y = y


class InLegend(InGraphics):
    """
    InLegend provides a wrapper for the pero.LegendBox glyph to draw the
    chart legend inside the main data frame.
    
    Properties:
        
        items: (pero.Legend,), None or UNDEF
            Specifies a collection of legend items to draw.
        
        static: bool
            Specifies whether the legend items are given by user directly (True)
            or whether they should be retrieved automatically from parent chart
            (False).
        
        position: pero.POSITION_COMPASS
            Specifies the legend position within a chart as any item from the
            pero.POSITION_COMPASS enum.
        
        orientation: pero.ORIENTATION
            Specifies the legend orientation as any item from the
            pero.ORIENTATION enum.
        
        margin: int, float, (int,), (float,) or UNDEF
            Specifies the space around the legend box as a single value or
            values for individual sides starting from top.
        
        padding: int, float, (int,), (float,) or UNDEF
            Specifies the inner space of the legend box as a single value or
            values for individual sides starting from top.
        
        spacing: int or float
            Specifies the additional space between legend items.
        
        radius: int, float, (int,), (float,) or UNDEF
            Specifies the corner radius of the legend box as a single value or
            values for individual corners starting from top-left.
        
        line properties:
            Includes pero.LineProperties to specify the legend box outline.
        
        fill properties:
            Includes pero.FillProperties to specify the legend box fill.
    """
    
    items = TupleProperty(UNDEF, types=(Legend,), dynamic=False, nullable=True)
    static = BoolProperty(False, dynamic=False)
    
    position = EnumProperty(POS_NE, enum=POSITION_COMPASS, dynamic=False)
    orientation = EnumProperty(ORI_VERTICAL, enum=ORIENTATION)
    
    margin = QuadProperty(10, dynamic=False)
    radius = QuadProperty(3, dynamic=False)
    padding = QuadProperty(5, dynamic=False)
    spacing = NumProperty(5, dynamic=False)
    
    line = Include(LineProperties, line_color="#ddd")
    fill = Include(FillProperties, fill_color="#fffc")
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of the InLegend."""
        
        # init legend glyph
        self._glyph = LegendBox()
        
        # init base
        super().__init__(**overrides)
    
    
    def prepare(self, chart, canvas, source=UNDEF, **overrides):
        """
        This method is automatically called by parent chart to prepare the
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
                items += obj.get_legends(canvas)
        
        # set new items
        self.items = items
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw the legend."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # update legend glyph
        self._update_glyph(canvas, source, **overrides)
        
        # draw legend
        self._glyph.draw(canvas)
    
    
    def _update_glyph(self, canvas=None, source=UNDEF, **overrides):
        """Updates legend glyph."""
        
        # get properties
        frame = self.get_property('frame', source, overrides)
        position = self.get_property('position', source, overrides)
        margin = self.get_property('margin', source, overrides)
        
        # check values
        position = position or POS_RIGHT
        margin = margin or (10, 10, 10, 10)
        
        # set anchor
        self._glyph.anchor = position
        
        if position == POS_N:
            x = frame.cx
            y = frame.y1 + margin[0]
        
        elif position == POS_NE:
            x = frame.x2 - margin[1]
            y = frame.y1 + margin[0]
        
        elif position == POS_E:
            x = frame.x2 - margin[1]
            y = frame.cy
        
        elif position == POS_SE:
            x = frame.x2 - margin[1]
            y = frame.y2 - margin[2]
        
        elif position == POS_S:
            x = frame.cx
            y = frame.y2 - margin[2]
        
        elif position == POS_SW:
            x = frame.x1 + margin[3]
            y = frame.y2 - margin[2]
        
        elif position == POS_W:
            x = frame.x1 + margin[3]
            y = frame.cy
        
        elif position == POS_NW:
            x = frame.x1 + margin[3]
            y = frame.y1 + margin[0]
        
        elif position == POS_C:
            x = frame.cx
            y = frame.cy
        
        else:
            x = frame.x2 - margin[1]
            y = frame.y1 + margin[0]
        
        # update glyph shared
        self._glyph.set_properties_from(self, source=source, overrides=overrides)
        
        # update glyph
        self._glyph.anchor = position
        self._glyph.x = x
        self._glyph.y = y
