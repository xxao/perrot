#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from pero.properties import *
from pero import colors
from pero import Path

from .. enums import *
from .. chart import InGraphics


class VennPatch(InGraphics):
    """
    Abstract base class for various types of Venn diagram patches.
    
    Properties:
        
        value: int or float
            Specifies the region value.
        
        total: int or float
            Specifies the total diagram value.
        
        title: str or callable
            Specifies the region title.
        
        path: pero.Path
            Specifies the patch shape.
        
        line properties:
            Includes pero.LineProperties to specify the patch outline.
        
        fill properties:
            Includes pero.FillProperties to specify the patch fill.
        
        label_x: int
            Specifies the x-coordinate of the label.
        
        label_y: int
            Specifies the y-coordinate of the label.
    """
    
    value = NumProperty(0, dynamic=False)
    total = NumProperty(0, dynamic=False)
    
    path = Property(UNDEF, types=(Path,))
    line = Include(LineProperties)
    fill = Include(FillProperties)
    
    label_x = NumProperty(0, dynamic=False)
    label_y = NumProperty(0, dynamic=False)
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw the full patch."""
        
        # get properties
        path = self.get_property('path', source, overrides)
        
        # check data
        if not path:
            return
        
        # set pen and brush
        canvas.set_pen_by(self, source=source, overrides=overrides)
        canvas.set_brush_by(self, source=source, overrides=overrides)
        
        # draw
        canvas.draw_path(path)
    
    
    def draw_fill(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw the path fill only."""
        
        # get properties
        path = self.get_property('path', source, overrides)
        
        # check data
        if not path:
            return
        
        # set pen and brush
        canvas.line_width = 0
        canvas.set_brush_by(self, source=source, overrides=overrides)
        
        # draw
        canvas.draw_path(path)
    
    
    def draw_outline(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw the patch outline only."""
        
        # get properties
        path = self.get_property('path', source, overrides)
        
        # check data
        if not path:
            return
        
        # set pen and brush
        canvas.set_pen_by(self, source=source, overrides=overrides)
        canvas.fill_style = FILL_STYLE_TRANS
        
        # draw
        canvas.draw_path(path)


class VennRegion(VennPatch):
    """Defines a Venn diagram region glyph."""
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of the VennRegion."""
        
        # init outline
        if 'line_width' not in overrides:
            overrides['line_width'] = 2
        
        if 'line_color' not in overrides:
            overrides['line_color'] = colors.Transparent
        
        # init fill
        if 'fill_color' not in overrides:
            overrides['fill_color'] = colors.Transparent
        
        # init base
        super().__init__(**overrides)


class VennCircle(VennPatch):
    """
    Defines a Venn diagram circle glyph.
    
    Properties:
        
        title: str or callable
            Specifies the region title.
    """
    
    title = StringProperty(UNDEF)
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of the VennCircle."""
        
        # init outline
        if 'line_width' not in overrides:
            overrides['line_width'] = 2
        
        if 'line_color' not in overrides:
            overrides['line_color'] = colors.White
        
        # unset fill
        if "fill_color" not in overrides:
            overrides["fill_color"] = UNDEF
        
        # init base
        super().__init__(**overrides)
