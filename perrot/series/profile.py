#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import numpy

from pero.enums import *
from pero.properties import *
from pero import Profile as ProfileGlyph
from pero import Path, Marker, MarkerLegend

from . series import Series
from . import utils


class Profile(Series):
    """
    This type of series plots raw x-sorted data as continuous line. Data can be
    provided either directly by specifying the 'x' and 'y' properties or as a
    sequence of raw 'data' points together with 'x' and 'y' coordinates
    selectors. All the coordinates as well as the 'base' are expected to be in
    real data units.
    
    To plot data as a line the 'show_line' property must be set to True.
    Similarly, to display individual points, the 'show_points' property must be
    set to True. If set to UNDEF, and line is enabled, the points are
    automatically visible if they are separated enough, as defined by the
    'spacing' property.
    
    Any property of the 'marker' can be dynamic (including the 'marker' property
    itself), expecting the raw data point as a 'source'. By this, its color,
    fill and other properties, as well as the marker itself can be set
    independently for each data point. However, be sure that all dynamic
    properties return reasonable value for UNDEF to be used for legend. If raw
    'data' property is not specified a sequence of internal raw data is created
    as ((x,y),) coordinates.
    
    Optionally the area under the curve can also be displayed if the 'show_area'
    property is set to True. In such case the line is additionally drawn as a
    filled polygon either by connecting first and last points directly or using
    strait line defined by the 'base' property.
    
    Properties:
        
        show_line: bool
            Specifies whether the profile line should be displayed.
        
        show_points: bool or UNDEF
            Specifies whether individual points should be displayed. If set to
            UNDEF, the points are displayed automatically as long as their
            distance is big enough.
        
        show_area: bool
            Specifies whether the area under profile line should be displayed.
        
        data: tuple, list, numpy.ndarray or UNDEF
            Specifies the sequence of the raw data points.
        
        x: int, float, tuple, list, numpy.ndarray, callable, None or UNDEF
            Specifies the sequence of x-coordinates in real data units or a
            function to retrieve the coordinates from the raw data.
        
        y: int, float, tuple, list, numpy.ndarray, callable, None or UNDEF
            Specifies the sequence of y-coordinates in real data units or a
            function to retrieve the coordinates from the raw data.
        
        base: int, float, None or UNDEF
            Specifies the area base value in real data units.
        
        marker: pero.MARKER, pero.Path, callable, None or UNDEF
            Specifies the marker to draw actual data points with. The value
            can be specified by any item from the pero.MARKER enum or as
            pero.Path.
        
        marker_size: int, float or callable
            Specifies the marker size.
        
        marker_line properties:
            Includes pero.LineProperties to specify the marker line.
        
        marker_fill properties:
            Includes pero.FillProperties to specify the marker fill.
        
        steps: pero.LINE_STEP
            Specifies the way stepped profile should be drawn as any item from
            the pero.LINE_STEP enum.
        
        spacing: int, float
            Specifies the minimum x-distance between points in device units to
            enable automatic points display.
        
        line properties:
            Includes pero.LineProperties to specify the line.
        
        fill properties:
            Includes pero.FillProperties to specify the area fill.
    """
    
    show_line = BoolProperty(True, dynamic=False)
    show_points = BoolProperty(UNDEF, dynamic=False)
    show_area = BoolProperty(False, dynamic=False)
    
    data = SequenceProperty(UNDEF, dynamic=False)
    x = Property(UNDEF)
    y = Property(UNDEF)
    base = NumProperty(UNDEF, dynamic=False, nullable=True)
    steps = EnumProperty(None, enum=LINE_STEP, nullable=True)
    spacing = NumProperty(20, dynamic=False)
    
    marker = Property(MARKER_CIRCLE, types=(str, Path, Marker), nullable=True)
    marker_size = NumProperty(6)
    marker_line = Include(LineProperties, prefix='marker_', line_color=UNDEF)
    marker_fill = Include(FillProperties, prefix='marker_', fill_color=UNDEF)
    
    line = Include(LineProperties, line_color=UNDEF, dynamic=False)
    fill = Include(FillProperties, fill_color=UNDEF, dynamic=False)
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of Profile series."""
        
        # init legend
        if 'legend' not in overrides:
            overrides['legend'] = MarkerLegend(
                text = lambda d: d.title,
                show_marker = lambda d: d.show_points,
                show_line = lambda d: d.show_line,
                marker = lambda d: d.marker,
                marker_line_color = lambda d: d.color.darker(0.2),
                marker_fill_color = lambda d: d.color,
                line_color = lambda d: d.color,
                line_width = lambda d: d.line_width,
                line_style = lambda d: d.line_style,
                line_dash = lambda d: d.line_dash)
        
        # init base
        super().__init__(**overrides)
        
        # init profile glyph
        self._glyph = ProfileGlyph()
        
        # init buffers
        self._x_data = []
        self._y_data = []
        self._raw_data = []
        self._limits = None
        
        # extract data
        self.extract_data()
    
    
    def get_limits(self, x_range=None, y_range=None, exact=False):
        """Gets current data limits using whole range or specified crops."""
        
        # check data
        if self._limits is None:
            return None
        
        # init limits
        limits = self._limits
        
        # apply crop
        if x_range:
            
            limits = utils.calc_limits_sorted(
                data = (self._x_data, self._y_data),
                crop = x_range,
                extend = False,
                interpolate = True)
            
            if self.base not in (UNDEF, None) and limits[1] is not None:
                limits[1][0] = min(self.base, limits[1][0])
                limits[1][1] = max(self.base, limits[1][1])
        
        # finalize limits
        return self.finalize_limits(limits, exact)
    
    
    def get_labels(self, canvas=None, source=UNDEF, **overrides):
        """Gets series labels."""
        
        return self.prepare_labels(self._x_data, self._y_data, self._raw_data)
    
    
    def get_tooltip(self, x, y, limit):
        """Gets nearest data point tooltip."""
        
        return self.prepare_tooltip(self._x_data, self._y_data, self._raw_data, x, y, limit)
    
    
    def extract_data(self):
        """Extracts coordinates from raw data."""
        
        # reset buffers
        self._x_data = []
        self._y_data = []
        self._raw_data = []
        self._limits = None
        
        # get data size
        size = utils.extract_data_size(self, 'data', 'x', 'y')
        
        # extract data
        self._x_data, x_raw = utils.extract_data(self, 'x', self.data, size, self.x_mapper)
        self._y_data, y_raw = utils.extract_data(self, 'y', self.data, size, self.y_mapper)
        
        # set raw data
        if self.data is not UNDEF:
            self._raw_data = numpy.array(self.data, dtype=object)
        else:
            self._raw_data = numpy.array([x_raw, y_raw]).T
        
        # check data
        if not utils.is_sorted(self._x_data):
            raise ValueError("X-coordinates must be sorted!")
        
        # init full limits
        if len(self._raw_data) > 0:
            self._limits = (
                (self._x_data.min(), self._x_data.max()),
                (self._y_data.min(), self._y_data.max()))
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw the series."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # get properties
        tag = self.get_property('tag', source, overrides)
        x_scale = self.get_property('x_scale', source, overrides)
        y_scale = self.get_property('y_scale', source, overrides)
        base = self.get_property('base', source, overrides)
        color = self.get_property('color', source, overrides)
        
        # set overrides to skip
        skip = {'x', 'y', 'base'}
        
        # crop data
        i1, i2 = utils.crop_indices(self._x_data, x_scale.in_range, True)
        if i1 == i2:
            return
        
        x_data = self._x_data[i1:i2]
        y_data = self._y_data[i1:i2]
        raw_data = self._raw_data[i1:i2]
        
        # scale coords
        x_data = x_scale.scale(x_data)
        y_data = y_scale.scale(y_data)
        
        # scale base
        if base is not UNDEF:
            base = y_scale.scale(base)
        
        # start drawing group
        with canvas.group(tag, "series"):
            
            # update glyph
            self._glyph.set_properties_from(self, source=source, overrides=overrides, skip=skip, native=True)
            
            # get glyph colors
            line_color = self._glyph.get_property('line_color', native=True)
            if line_color is UNDEF:
                line_color = color
            
            fill_color = self._glyph.get_property('fill_color', native=True)
            if fill_color is UNDEF:
                fill_color = color.trans(0.4)
            
            marker_line_color = self._glyph.get_property('marker_line_color', native=True)
            if marker_line_color is UNDEF:
                marker_line_color = color.darker(0.2)
            
            marker_fill_color = self._glyph.get_property('marker_fill_color', native=True)
            if marker_fill_color is UNDEF:
                marker_fill_color = color
            
            # set overrides
            glyph_overrides = overrides.copy()
            glyph_overrides['data'] = raw_data
            glyph_overrides['x'] = x_data
            glyph_overrides['y'] = y_data
            glyph_overrides['base'] = base
            glyph_overrides['line_color'] = line_color
            glyph_overrides['fill_color'] = fill_color
            glyph_overrides['marker_line_color'] = marker_line_color
            glyph_overrides['marker_fill_color'] = marker_fill_color
            
            # draw profile
            self._glyph.draw(canvas, raw_data, **glyph_overrides)
