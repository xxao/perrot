#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from pero.properties import *
from pero import colors
from pero import OrdinalScale
from pero import Path
from pero import MarkerLegend
from pero import Label, TextLabel
from pero import Tooltip, TextTooltip

from .. enums import *
from .. chart import InGraphics
from . import utils
from . regions import EmptyRegion
from . patches import VennRegion, VennCircle

# define constants
_REGIONS = ('a', 'b', 'ab', 'c', 'ac', 'bc', 'abc')
_CIRCLES = ('A', 'B', 'C')


class Venn(InGraphics):
    """
    Venn provides a mechanism to construct and draw Venn diagrams with two or
    three circles.
    
    Properties:
        
        mode: pero.VENN or callable
            Specifies whether circles and overlaps should be proportional to
            their area as any item from the pero.venn.VENN_MODE enum.
                perrot.venn.VENN_MODE.NONE - non-proportional
                perrot.venn.VENN_MODE.SEMI - circles are proportional but overlaps not
                perrot.venn.VENN_MODE.FULL - circles and overlaps try to be proportional
        
        palette: pero.Palette, tuple, str
            Specifies the default color palette as a sequence of colors,
            pero.Palette or palette name. This is used to automatically
            provide new color for main diagram circles.
        
        legend: perrot.MarkerLegend, None or UNDEF
            Specifies the explicit value for the legend or a template to create
            it. When the actual legend is initialized, current region is
            provided as a source, therefore properties can be dynamic to
            retrieve the final value from the region.
        
        label: pero.TextLabel
            Specifies a template to create regions labels. When the actual label
            is initialized, current region is provided as a source, therefore
            properties can be dynamic to retrieve the final value from the point.
        
        tooltip: pero.Tooltip, None or UNDEF
            Specifies a template to create regions tooltips. When the actual
            tooltip is initialized, current region is provided as a source,
            therefore properties can be dynamic to retrieve the final value from
            the region.
        
        show_legend: bool
            Specifies whether the legend should be shown.
        
        show_labels: bool
            Specifies whether the labels should be shown.
        
        show_tooltip: bool
            Specifies whether the wedges tooltip should be shown.
    """
    
    mode = EnumProperty(VENN_SEMI, enum=VENN_MODE, dynamic=False, nullable=False)
    palette = PaletteProperty(colors.Dark.trans(0.6), dynamic=False, nullable=False)
    
    a = Property(UNDEF, types=(VennRegion,), dynamic=False, nullable=False)
    b = Property(UNDEF, types=(VennRegion,), dynamic=False, nullable=False)
    ab = Property(UNDEF, types=(VennRegion,), dynamic=False, nullable=False)
    c = Property(UNDEF, types=(VennRegion,), dynamic=False, nullable=False)
    ac = Property(UNDEF, types=(VennRegion,), dynamic=False, nullable=False)
    bc = Property(UNDEF, types=(VennRegion,), dynamic=False, nullable=False)
    abc = Property(UNDEF, types=(VennRegion,), dynamic=False, nullable=False)
    
    A = Property(UNDEF, types=(VennCircle,), dynamic=False, nullable=False)
    B = Property(UNDEF, types=(VennCircle,), dynamic=False, nullable=False)
    C = Property(UNDEF, types=(VennCircle,), dynamic=False, nullable=False)
    
    legend = Property(UNDEF, types=(MarkerLegend,), dynamic=False, nullable=True)
    label = Property(UNDEF, types=(Label,), dynamic=False, nullable=True)
    tooltip = Property(UNDEF, types=(Tooltip,), dynamic=False, nullable=True)
    
    show_legend = BoolProperty(True, dynamic=False)
    show_labels = BoolProperty(True, dynamic=False)
    show_tooltip = BoolProperty(True, dynamic=False)
    
    
    def __init__(self, a, b, ab, c=0, ac=0, bc=0, abc=0, **overrides):
        """
        Initializes a new instance of the Venn.
        
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
        """
        
        # init regions
        for i, key in enumerate(_REGIONS):
            overrides[key] = VennRegion(
                tag = key,
                z_index = VENN_REGION_Z+i)
        
        # init circles
        for i, key in enumerate(_CIRCLES):
            overrides[key] = VennCircle(
                tag = key,
                z_index = VENN_CIRCLE_Z+i,
                title = key)
        
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
                font_size = 14,
                text_align = TEXT_ALIGN_CENTER,
                text_base = TEXT_BASE_MIDDLE)
        
        # init tooltip
        if 'tooltip' not in overrides:
            overrides['tooltip'] = TextTooltip(
                text = lambda d: str(d.value))
        
        # init base
        super().__init__(**overrides)
        
        # init containers
        self._values = {'a': a, 'b': b, 'ab': ab, 'c': c, 'ac': ac, 'bc': bc, 'abc': abc}
        self._regions = tuple(self.get_property(k) for k in _REGIONS)
        self._circles = tuple(self.get_property(k) for k in _CIRCLES)
        
        # init graphics
        self._init_graphics()
        
        # bind events
        self.bind(EVT_PROPERTY_CHANGED, self._on_venn_property_changed)
    
    
    def get_legends(self, canvas=None, source=UNDEF, **overrides):
        """Gets circles legend items."""
        
        # get properties
        show_legend = self.get_property('show_legend', source, overrides)
        legend = self.get_property('legend', source, overrides)
        
        # check legend
        if not show_legend or not legend:
            return ()
        
        # get items
        items = []
        for obj in self._circles:
            
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
        """Gets segments labels."""
        
        # get properties
        show_labels = self.get_property('show_labels', source, overrides)
        label = self.get_property('label', source, overrides)
        
        # check labels
        if not show_labels or not label:
            return ()
        
        # update patches
        self._update_patches(canvas, source, **overrides)
        
        # get items
        items = []
        for obj in self._regions:
            
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
        """Uses given canvas to draw the diagram."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # update patches
        self._update_patches(canvas, source, **overrides)
        
        # get objects
        circles = [o for o in self._circles]
        circles.sort(key=lambda o: o.z_index)
        
        regions = [o for o in self._regions]
        regions.sort(key=lambda o: o.z_index)
        
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
    
    
    def _update_patches(self, canvas=None, source=UNDEF, **overrides):
        """Updates circles and regions patches."""
        
        # get properties
        mode = self.get_property('mode', source, overrides)
        frame = self.get_property('frame', source, overrides)
        
        # calculate venn
        values = [self._values[key] for key in _REGIONS]
        coords, radii = utils.calc_venn(*values, mode=mode)
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
            self.get_property(key).value = self._values[key]
        
        # set circles values
        a, b, ab, c, ac, bc, abc = [self._values[k] for k in _REGIONS]
        self.get_property(_CIRCLES[0]).value = a + ab + ac + abc
        self.get_property(_CIRCLES[1]).value = b + ab + bc + abc
        self.get_property(_CIRCLES[2]).value = c + ac + bc + abc
        
        # set circles fill
        self._init_colors()
        
        # lock properties
        for key in _REGIONS + _CIRCLES:
            self.lock_property(key)
            self.get_property(key).lock_property('value')
    
    
    def _init_colors(self):
        """Sets colors to circles."""
        
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
