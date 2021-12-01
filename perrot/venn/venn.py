#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from pero.enums import *
from pero.properties import *
from pero import colors
from pero import Graphics, Frame, Path, TextLabel
from pero import OrdinalScale

from . enums import *
from . import utils
from . patches import RegionPatch, CirclePatch

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
        
        label: pero.TextLabel
            Specifies the glyph to be used to draw labels.
    """
    
    x = NumProperty(0, dynamic=False)
    y = NumProperty(0, dynamic=False)
    width = NumProperty(UNDEF, dynamic=False)
    height = NumProperty(UNDEF, dynamic=False)
    padding = QuadProperty(10, dynamic=False)
    
    bgr_line = Include(LineProperties, prefix="bgr_", dynamic=False, line_width=0)
    bgr_fill = Include(FillProperties, prefix="bgr_", dynamic=False, fill_color="#fff")
    
    mode = EnumProperty(VENN_MODE_SEMI, enum=VENN_MODE, dynamic=False, nullable=False)
    palette = PaletteProperty(colors.Dark.trans(0.6), dynamic=False, nullable=False)
    label = Property(UNDEF, types=(TextLabel,), dynamic=False, nullable=True)
    
    a = Property(UNDEF, types=(RegionPatch,), dynamic=False, nullable=False)
    b = Property(UNDEF, types=(RegionPatch,), dynamic=False, nullable=False)
    ab = Property(UNDEF, types=(RegionPatch,), dynamic=False, nullable=False)
    c = Property(UNDEF, types=(RegionPatch,), dynamic=False, nullable=False)
    ac = Property(UNDEF, types=(RegionPatch,), dynamic=False, nullable=False)
    bc = Property(UNDEF, types=(RegionPatch,), dynamic=False, nullable=False)
    abc = Property(UNDEF, types=(RegionPatch,), dynamic=False, nullable=False)
    
    A = Property(UNDEF, types=(CirclePatch,), dynamic=False, nullable=False)
    B = Property(UNDEF, types=(CirclePatch,), dynamic=False, nullable=False)
    C = Property(UNDEF, types=(CirclePatch,), dynamic=False, nullable=False)
    
    
    def __init__(self, a, b, ab, c=0, ac=0, bc=0, abc=0, **overrides):
        """Initializes a new instance of Venn diagram."""
        
        # init regions
        for i, key in enumerate(_REGIONS):
            overrides[key] = RegionPatch(tag=key, z_index=REGION_Z+i, title=lambda d: str(d))
        
        # init circles
        for i, key in enumerate(_CIRCLES):
            overrides[key] = CirclePatch(tag=key, z_index=CIRCLE_Z+i, title=key)
        
        # init label
        if 'label' not in overrides:
            overrides['label'] = TextLabel(font_size=16, text_align=TEXT_ALIGN_CENTER, text_base=TEXT_BASE_MIDDLE)
        
        # init base
        super().__init__(**overrides)
        
        # init containers
        self._regions = tuple(self.get_property(k) for k in _REGIONS)
        self._circles = tuple(self.get_property(k) for k in _CIRCLES)
        self._frame = Frame(0, 0, 1, 1)
        
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
        
        # lock properties
        for key in _REGIONS + _CIRCLES:
            self.lock_property(key)
            self.get_property(key).lock_property('value')
        
        # init colors
        self._init_colors(force=False)
        
        # bind events
        self.bind(EVT_PROPERTY_CHANGED, self._on_venn_property_changed)
    
    
    @property
    def regions(self):
        """
        Gets regions in following order (a, b, ab, c, ac, bc, abc).
        
        Returns:
            (perrot.venn.RegionPatch,)
                Regions patches.
        """
        
        return self._regions
    
    
    @property
    def circles(self):
        """
        Gets main circles in following order (a, b, c).
        
        Returns:
            (perrot.venn.CirclePatch,)
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
        label = self.get_property('label', source, overrides)
        
        # get size from canvas
        if width is UNDEF:
            width = canvas.viewport.width
        if height is UNDEF:
            height = canvas.viewport.height
        
        # init frame
        self._frame = Frame(padding[3], padding[0], width - (padding[1]+padding[3]), height - (padding[0]+padding[2]))
        
        # draw main bgr
        canvas.set_pen_by(self, prefix="bgr_", source=source, overrides=overrides)
        canvas.set_brush_by(self, prefix="bgr_", source=source, overrides=overrides)
        canvas.draw_rect(x, y, width, height)
        
        # refuse to draw if "negative" size
        if self._frame.reversed:
            return
        
        # init patches
        self._init_patches(source, overrides)
        
        # sort objects by z-index
        regions = sorted(self._regions, key=lambda o: o.z_index)
        circles = sorted(self._circles, key=lambda o: o.z_index)
        
        # draw circles fill
        for obj in circles:
            obj.draw_fill(canvas)
        
        # draw regions fill
        for obj in regions:
            obj.draw_fill(canvas)
        
        # draw circles outline
        for obj in circles:
            obj.draw_outline(canvas)
        
        # draw regions outline
        for obj in regions:
            obj.draw_outline(canvas)
        
        # draw labels
        for obj in regions:
            title = obj.get_property('title', obj.value)
            obj_overrides = {'x': obj.x, 'y': obj.y, 'text': title}
            label.draw(canvas, obj, **obj_overrides)
    
    
    def _init_patches(self, source, overrides):
        """Initializes all patches."""
        
        # get properties
        mode = self.get_property('mode', source, overrides)
        
        # calculate venn
        data = [self.get_property(key).value for key in _REGIONS]
        coords, radii = utils.calc_venn(*data, mode=mode)
        coords, radii = utils.fit_into(coords, radii, *self._frame.rect)
        
        # create regions
        regions = utils.make_regions(coords, radii)
        
        # update regions path
        for obj in self._regions:
            obj.path = regions[obj.tag].path()
            obj.x, obj.y = regions[obj.tag].anchor()
        
        # update circles path
        for i, obj in enumerate(self._circles):
            obj.path = Path().circle(coords[i][0], coords[i][1], radii[i])
            obj.x, obj.y = coords[i]
    
    
    def _init_colors(self, force=True):
        """Sets colors."""
        
        # init color scale
        scale = OrdinalScale(
            in_range = _CIRCLES,
            out_range = self.palette,
            implicit = True,
            recycle = True)
        
        # set to circles
        for obj in self._circles:
            color = obj.get_property('fill_color')
            if force or color is UNDEF:
                obj.fill_color = scale.scale(obj.tag)
    
    
    def _on_venn_property_changed(self, evt):
        """Called after any property has changed."""
        
        # color palette changed
        if evt.name == 'palette':
            self._init_colors()
