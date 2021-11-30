#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from pero.enums import *
from pero.properties import *
from pero import colors
from pero import Graphics, Frame, Path, Shape
from pero import OrdinalScale

from . enums import *
from . import utils
from . patch import Patch

# define constants
_REGIONS = ('a', 'b', 'ab', 'c', 'ac', 'bc', 'abc')
_CIRCLES = ('A', 'B', 'C')


class Venn(Graphics):
    """
    
    Properties:
        
        mode: pero.VENN or callable
            Specifies whether circles and overlaps should be proportional to
            their area as any item from the pero.venn.VENN enum.
                perrot.venn.VENN.NONE - non-proportional
                perrot.venn.VENN.SEMI - circles are proportional but overlaps not
                perrot.venn.VENN.FULL - circles and overlaps try to be proportional
        
        x: int or float
            Specifies the x-coordinate of the top-left corner
        
        y: int or float
            Specifies the y-coordinate of the top-left corner
        
        width: int, float or UNDEF
            Specifies the full diagram width. If set to UNDEF the full area of
            given canvas is used.
        
        height: int, float or UNDEF
            Specifies the full diagram height. If set to UNDEF the full area of
            given canvas is used.
        
        padding: int, float or tuple
            Specifies the inner space of the diagram as a single value or values
            for individual sides starting from top.
        
        bgr_line properties:
            Includes pero.LineProperties to specify the diagram outline.
        
        bgr_fill properties:
            Includes pero.FillProperties to specify the diagram fill.
        
        palette: pero.Palette, tuple, str
            Specifies the default color palette as a sequence of colors,
            pero.Palette or palette name. This is used to automatically
            provide new color for main diagram circles.
        
        outline properties:
            Includes pero.LineProperties to specify the main circles outline.
    """
    
    x = NumProperty(0, dynamic=False)
    y = NumProperty(0, dynamic=False)
    width = NumProperty(UNDEF, dynamic=False)
    height = NumProperty(UNDEF, dynamic=False)
    padding = QuadProperty(10, dynamic=False)
    
    bgr_line = Include(LineProperties, prefix="bgr", dynamic=False, line_width=0)
    bgr_fill = Include(FillProperties, prefix="bgr", dynamic=False, fill_color="#fff")
    
    mode = EnumProperty(VENN_MODE_SEMI, enum=VENN_MODE, dynamic=False, nullable=True)
    palette = PaletteProperty(colors.Set2, dynamic=False, nullable=True)
    outline = Include(LineProperties, prefix="outline", line_width=2, line_color="#fff")
    labels = Include(TextProperties, prefix="labels", font_size=16, text_align=TEXT_ALIGN_CENTER, text_base=TEXT_BASE_MIDDLE)
    
    a = Property(UNDEF, types=(Patch,), dynamic=False, nullable=False)
    b = Property(UNDEF, types=(Patch,), dynamic=False, nullable=False)
    ab = Property(UNDEF, types=(Patch,), dynamic=False, nullable=False)
    c = Property(UNDEF, types=(Patch,), dynamic=False, nullable=False)
    ac = Property(UNDEF, types=(Patch,), dynamic=False, nullable=False)
    bc = Property(UNDEF, types=(Patch,), dynamic=False, nullable=False)
    abc = Property(UNDEF, types=(Patch,), dynamic=False, nullable=False)
    
    A = Property(UNDEF, types=(Patch,), dynamic=False, nullable=False)
    B = Property(UNDEF, types=(Patch,), dynamic=False, nullable=False)
    C = Property(UNDEF, types=(Patch,), dynamic=False, nullable=False)
    
    
    def __init__(self, a, b, ab, c=0, ac=0, bc=0, abc=0, **overrides):
        """Initializes a new instance of Venn diagram."""
        
        # init main graphics
        for key in _REGIONS:
            if key not in overrides:
                overrides[key] = Patch(
                    tag = key,
                    z_index = REGION_Z,
                    shape_line_width = 0,
                    shape_fill_color = colors.Transparent,
                    label_font_size = UNDEF,
                    label_font_name = UNDEF,
                    label_font_family = UNDEF,
                    label_font_style = UNDEF,
                    label_font_weight = UNDEF,
                    label_text_align = UNDEF,
                    label_text_base = UNDEF)
        
        for key in _CIRCLES:
            if key not in overrides:
                overrides[key] = Patch(
                    tag = key,
                    z_index = CIRCLE_Z,
                    shape_line_width = UNDEF,
                    shape_line_dash = UNDEF,
                    shape_line_style = UNDEF,
                    shape_line_cap = UNDEF,
                    shape_line_join = UNDEF,
                    shape_fill_alpha = 128)
        
        # init base
        super().__init__(**overrides)
        
        # set values
        self.get_property(_REGIONS[0]).value = a
        self.get_property(_REGIONS[1]).value = b
        self.get_property(_REGIONS[2]).value = ab
        self.get_property(_REGIONS[3]).value = c
        self.get_property(_REGIONS[4]).value = ac
        self.get_property(_REGIONS[5]).value = bc
        self.get_property(_REGIONS[6]).value = abc
        self.get_property(_CIRCLES[0]).value = a + ab + ac + abc
        self.get_property(_CIRCLES[1]).value = b + ab + bc + abc
        self.get_property(_CIRCLES[2]).value = c + ac + bc + abc
        
        # init buffs
        self._regions = tuple(self.get_property(k) for k in _REGIONS)
        self._circles = tuple(self.get_property(k) for k in _CIRCLES)
        self._frame = Frame(0, 0, 1, 1)
        
        # bind events
        self.bind(EVT_PROPERTY_CHANGED, self._on_venn_property_changed)
    
    
    @property
    def regions(self):
        """
        Gets regions in following order (a, b, ab, c, ac, bc, abc).
        
        Returns:
            (perrot.venn.Patch,)
                Regions patches.
        """
        
        return self._regions
    
    
    @property
    def circles(self):
        """
        Gets main circles in following order (a, b, c).
        
        Returns:
            (perrot.venn.Patch,)
                Circles patches.
        """
        
        return self._circles
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw the diagram."""
        
        # get properties
        x = self.get_property('x', source, overrides)
        y = self.get_property('y', source, overrides)
        width = self.get_property('width', source, overrides)
        height = self.get_property('height', source, overrides)
        padding = self.get_property('padding', source, overrides)
        mode = self.get_property('mode', source, overrides)
        
        # get size from canvas
        if width is UNDEF:
            width = canvas.viewport.width
        if height is UNDEF:
            height = canvas.viewport.height
        
        # init frame
        self._frame = Frame(padding[3], padding[0], width - (padding[1]+padding[3]), height - (padding[0]+padding[2]))
        
        # draw main bgr
        canvas.set_pen_by(self, prefix="bgr", source=source, overrides=overrides)
        canvas.set_brush_by(self, prefix="bgr", source=source, overrides=overrides)
        canvas.draw_rect(x, y, width, height)
        
        # refuse to draw if "negative" size
        if self._frame.reversed:
            return
        
        # init patches
        self._init_patches(mode, self._frame)
        
        # draw
        self._draw_circles(canvas, source, overrides)
        self._draw_regions(canvas, source, overrides)
        self._draw_labels(canvas, source, overrides)
    
    
    def _draw_circles(self, canvas, source, overrides):
        """Draws circles."""
        
        # get properties
        palette = self.get_property('palette', source, overrides)
        
        # init colors
        color_scale = OrdinalScale(in_range=_CIRCLES, out_range=palette)
        
        # sort objects by z-index
        objects = sorted(self._circles, key=lambda o: o.z_index)
        
        # draw fill
        for obj in objects:
            
            # get overrides
            obj_overrides = self.get_child_overrides(obj.tag, overrides)
            
            # check if visible
            if not obj.is_visible(obj.value, obj_overrides):
                continue
            
            # set fill color
            if obj.shape.fill_color is UNDEF:
                obj_overrides['fill_color'] = color_scale.scale(obj.tag) or colors.Transparent
            
            # set pen and brush
            canvas.line_width = 0
            canvas.set_brush_by(obj.shape, source=obj.value, overrides=obj_overrides)
            
            # draw path
            canvas.draw_path(obj.shape.path)
        
        # draw outline
        for obj in objects:
            
            # get overrides
            obj_overrides = self.get_child_overrides(obj.tag, overrides)
            
            # check if visible
            if not obj.is_visible(obj.value, obj_overrides):
                continue
            
            # set pen and brush
            canvas.fill_style = FILL_STYLE_TRANS
            canvas.set_pen_by(self, 'outline', source=obj.value, overrides=overrides)
            canvas.set_pen_by(obj.shape, source=obj.value, overrides=obj_overrides)
            
            # draw path
            canvas.draw_path(obj.shape.path)
    
    
    def _draw_regions(self, canvas, source, overrides):
        """Draws regions."""
        
        # sort objects by z-index
        objects = sorted(self._regions, key=lambda o: o.z_index)
        
        # draw regions
        for obj in objects:
            
            # get overrides
            obj_overrides = self.get_child_overrides(obj.tag, overrides)
            
            # check if visible
            if not obj.is_visible(obj.value, obj_overrides):
                continue
            
            # draw shape
            obj.shape.draw(canvas, obj.value, **obj_overrides)
    
    
    def _draw_labels(self, canvas, source, overrides):
        """Draws labels."""
        
        # sort objects by z-index
        objects = sorted(self._regions, key=lambda o: o.z_index)
        
        # draw labels
        for obj in objects:
            
            # get overrides
            obj_overrides = self.get_child_overrides(obj.tag, overrides)
            
            # check if visible
            if not obj.is_visible(obj.value, obj_overrides):
                continue
            
            # set font
            canvas.set_text_by(self, 'labels', source=obj.value, overrides=overrides)
            
            # draw label
            obj.label.draw(canvas, obj.value, **obj_overrides)
    
    
    def _init_patches(self, mode, frame):
        """Initializes all patches."""
        
        # get values from regions
        values = [self.get_property(key).value for key in _REGIONS]
        
        # calculate venn
        coords, radii = utils.calc_venn(*values, mode=mode)
        coords, radii = utils.fit_into(coords, radii, *frame.rect)
        
        # create regions
        regions = utils.make_regions(coords, radii)
        
        # update regions
        for obj in self._regions:
            obj.shape.path = regions[obj.tag].path()
            obj.label.x, obj.label.y = regions[obj.tag].label()
        
        # update circles
        for i, obj in enumerate(self._circles):
            obj.shape.path = Path().circle(coords[i][0], coords[i][1], radii[i])
            obj.label.x, obj.label.y = coords[i]
    
    
    def _on_venn_property_changed(self, evt):
        """Called after any property has changed."""
        
        pass
