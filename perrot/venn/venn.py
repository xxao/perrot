#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from pero.enums import *
from pero.properties import *
from pero import colors
from pero import Path, TextLabel, MarkerLegend
from pero import OrdinalScale

from .. chart import Chart, Title, OutLegend
from . enums import *
from . import utils
from . regions import EmptyRegion
from . patches import Patch, RegionPatch, CirclePatch

# define constants
_REGIONS = ('a', 'b', 'ab', 'c', 'ac', 'bc', 'abc')
_CIRCLES = ('A', 'B', 'C')


class Venn(Chart):
    """
    This class provides main functionality to construct and draw Venn diagrams
    with two or three circles.
    
    Properties:
        
        mode: pero.VENN or callable
            Specifies whether circles and overlaps should be proportional to
            their area as any item from the pero.venn.VENN enum.
                perrot.venn.VENN.NONE - non-proportional
                perrot.venn.VENN.SEMI - circles are proportional but overlaps not
                perrot.venn.VENN.FULL - circles and overlaps try to be proportional
        
        palette: pero.Palette, tuple, str
            Specifies the default color palette as a sequence of colors,
            pero.Palette or palette name. This is used to automatically
            provide new color for main diagram circles.
        
        title: perrot.chart.Title, None or UNDEF
            Specifies the title display graphics.
        
        legend: perrot.chart.OutLegend, None or UNDEF
            Specifies the legend display graphics.
        
        label: pero.TextLabel
            Specifies the glyph to be used to draw labels.
    """
    
    mode = EnumProperty(VENN_MODE_SEMI, enum=VENN_MODE, dynamic=False, nullable=False)
    palette = PaletteProperty(colors.Dark.trans(0.6), dynamic=False, nullable=False)
    
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
    
    title = Property(UNDEF, types=(Title,), dynamic=False, nullable=True)
    legend = Property(UNDEF, types=(OutLegend,), dynamic=False, nullable=True)
    label = Property(UNDEF, types=(TextLabel,), dynamic=False, nullable=True)
    
    
    def __init__(self, a, b, ab, c=0, ac=0, bc=0, abc=0, **overrides):
        """Initializes a new instance of Venn diagram."""
        
        # init regions
        for i, key in enumerate(_REGIONS):
            overrides[key] = RegionPatch(
                tag = key,
                z_index = REGION_Z+i)
        
        # init circles
        for i, key in enumerate(_CIRCLES):
            overrides[key] = CirclePatch(
                tag = key,
                z_index = CIRCLE_Z+i,
                title = key)
        
        # init title
        if 'title' not in overrides:
            overrides['title'] = Title(
                tag = 'title',
                position = POS_TOP)
        
        # init legend
        if 'legend' not in overrides:
            overrides['legend'] = OutLegend(
                tag = 'legend',
                position = POS_BOTTOM,
                orientation = ORI_HORIZONTAL)
        
        # init label
        if 'label' not in overrides:
            overrides['label'] = TextLabel(
                text = lambda d: d.value,
                x = lambda d: d.label_x,
                y = lambda d: d.label_y,
                font_size = 14,
                text_align = TEXT_ALIGN_CENTER,
                text_base = TEXT_BASE_MIDDLE)
        
        # init base
        super().__init__(**overrides)
        
        # init containers
        self._data = {'a': a, 'b': b, 'ab': ab, 'c': c, 'ac': ac, 'bc': bc, 'abc': abc}
        self._regions = tuple(self.get_property(k) for k in _REGIONS)
        self._circles = tuple(self.get_property(k) for k in _CIRCLES)
        
        # init graphics
        self._init_graphics()
        
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
        Gets main circles in following order (A, B, C).
        
        Returns:
            (perrot.venn.CirclePatch,)
                Circles patches.
        """
        
        return self._circles
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw the diagram."""
        
        # get properties
        label = self.get_property('label', source, overrides)
        
        # update legend
        self._update_legend(canvas, source, **overrides)
        
        # init frames
        self.init_frames(canvas, source, **overrides)
        
        # update patches
        self._update_patches(canvas, source, **overrides)
        
        # draw main bgr
        self.draw_bgr(canvas, source, **overrides)
        
        # refuse to draw if "negative" size
        if self.get_frame().reversed:
            return
        
        # get objects
        objects = list(self.graphics)
        objects.sort(key=lambda o: o.z_index)
        regions = [o for o in objects if isinstance(o, RegionPatch)]
        circles = [o for o in objects if isinstance(o, CirclePatch)]
        others = [o for o in objects if not isinstance(o, Patch)]
        
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
        if label:
            for obj in regions:
                if obj.is_visible(obj):
                    label.draw(canvas, obj)
        
        # draw remaining objects
        for obj in others:
            obj.draw(canvas)
        
        # draw debug frames
        # self.draw_frames(canvas)
    
    
    def _update_legend(self, canvas, source=UNDEF, **overrides):
        """Updates legend items."""
        
        # check if visible
        if not self.legend or not self.legend.is_visible():
            return
        
        # check if static
        if self.legend.static:
            return
        
        # get items
        items = []
        for obj in self._circles:
            
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
        self.legend.items = tuple(items)
    
    
    def _update_patches(self, canvas, source=UNDEF, **overrides):
        """Updates circles and regions patches."""
        
        # get properties
        mode = self.get_property('mode', source, overrides)
        
        # calculate venn
        frame = self.get_frame()
        data = [self.get_property(key).value for key in _REGIONS]
        coords, radii = utils.calc_venn(*data, mode=mode)
        coords, radii = utils.fit_into(coords, radii, *frame.rect)
        
        # create regions
        regions = utils.make_regions(coords, radii)
        
        # update regions
        for obj in self._regions:
            obj.path = regions[obj.tag].path()
            obj.label_x, obj.label_y = regions[obj.tag].anchor() or (0, 0)
            obj.visible = not isinstance(regions[obj.tag], EmptyRegion)
        
        # update circles
        for i, obj in enumerate(self._circles):
            obj.path = Path().circle(coords[i][0], coords[i][1], radii[i])
            obj.label_x, obj.label_y = coords[i]
    
    
    def _init_graphics(self):
        """Initializes and registers required graphics."""
        
        # set regions values
        for key in _REGIONS:
            self.get_property(key).value = self._data[key]
        
        # set circles values
        a, b, ab, c, ac, bc, abc = [self._data[k] for k in _REGIONS]
        self.get_property(_CIRCLES[0]).value = a + ab + ac + abc
        self.get_property(_CIRCLES[1]).value = b + ab + bc + abc
        self.get_property(_CIRCLES[2]).value = c + ac + bc + abc
        
        # set circles fill
        self._init_colors()
        
        # lock properties
        for key in _REGIONS + _CIRCLES:
            self.lock_property(key)
            self.get_property(key).lock_property('value')
        
        # register circles
        for key in _CIRCLES:
            self.add(self.get_property(key))
        
        # register regions
        for key in _REGIONS:
            self.add(self.get_property(key))
        
        # register additional objects
        if self.legend:
            self.add(self.legend)
        
        if self.title:
            self.add(self.title)
    
    
    def _init_colors(self):
        """Sets colors."""
        
        # init color scale
        color_scale = OrdinalScale(
            out_range = self.palette,
            implicit = True,
            recycle = True)
        
        # update circles
        for obj in self._circles:
            obj.fill_color = color_scale.scale(obj.tag)
    
    
    def _on_venn_property_changed(self, evt):
        """Called after any property has changed."""
        
        # color palette changed
        if evt.name == 'palette':
            self._init_colors()
        
        # main objects
        if evt.name in ('title', 'legend'):
            
            # remove old
            if evt.old_value:
                self.remove(evt.old_value.tag)
            
            # register new
            if evt.new_value:
                self.add(evt.new_value)
