#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import numpy

from pero.enums import *
from pero.properties import *
from pero import Frame, Path, Marker
from pero import MarkerLegend

from . series import Series
from . import utils


class Scatter(Series):
    """
    This type of series plots raw data as individual points. Data can be
    provided either directly by specifying the 'x' and 'y' properties or as a
    sequence of raw 'data' points together with 'x' and 'y' coordinates
    selectors. All the coordinates are expected to be in real data units.
    
    Any property of the 'marker' can be dynamic (including the 'marker' property
    itself), expecting the raw data point as a 'source'. By this, its color,
    fill and other properties, as well as the marker itself can be set
    independently for each data point. However, be sure that all dynamic
    properties return reasonable value for UNDEF to be used for legend. If raw
    'data' property is not specified a sequence of internal raw data is created
    as ((x,y),) coordinates.
    
    Properties:
        
        show_points: bool or UNDEF
            Specifies whether individual points should be displayed.
        
        show_line: bool
            Specifies whether the connection line should be displayed between
            points.
        
        data: tuple, list, numpy.ndarray or UNDEF
            Specifies the sequence of the raw data points.
        
        x: int, float, tuple, list, numpy.ndarray, callable, None or UNDEF
            Specifies the sequence of x-coordinates in real data units or a
            function to retrieve the coordinates from the raw data.
        
        y: int, float, tuple, list, numpy.ndarray, callable, None or UNDEF
            Specifies the sequence of y-coordinates in real data units or a
            function to retrieve the coordinates from the raw data.
        
        marker: pero.MARKER, pero.Path, callable
            Specifies the marker to draw actual data points with. The value
            can be specified by any item from the pero.MARKER enum or as
            pero.Path.
        
        marker_size: int, float or callable
            Specifies the marker size.
        
        marker_line properties:
            Includes pero.LineProperties to specify the marker line.
        
        marker_fill properties:
            Includes pero.FillProperties to specify the marker fill.
        
        line properties:
            Includes pero.LineProperties to specify the points connection line.
    """
    
    show_points = BoolProperty(True, dynamic=False)
    show_line = BoolProperty(False, dynamic=False)
    
    data = SequenceProperty(UNDEF, dynamic=False)
    
    x = Property(lambda d: d[0])
    y = Property(lambda d: d[1])
    
    marker = Property(MARKER_CIRCLE, types=(str, Path))
    marker_size = NumProperty(8)
    marker_line = Include(LineProperties, prefix='marker_', line_color=UNDEF)
    marker_fill = Include(FillProperties, prefix='marker_', fill_color=UNDEF)
    
    line = Include(LineProperties, line_color=UNDEF, dynamic=False)
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of the Scatter series."""
        
        # init legend
        if 'legend' not in overrides:
            overrides['legend'] = MarkerLegend(
                text = lambda d: d.title,
                show_marker = lambda d: d.show_points,
                show_line = lambda d: d.show_line,
                line_color = lambda d: d.color.darker(0.2),
                line_width = lambda d: d.line_width,
                line_style = lambda d: d.line_style,
                marker = lambda d: d.marker,
                marker_line_color = lambda d: d.color.darker(0.2),
                marker_fill_color = lambda d: d.color)
        
        # init base
        super().__init__(**overrides)
        
        # init buffers
        self._x_data = []
        self._y_data = []
        self._raw_data = []
        self._limits = None
        
        # extract data
        self.extract_data()
        
        # lock properties
        self.lock_property('data')
        self.lock_property('x')
        self.lock_property('y')
    
    
    def get_limits(self, x_range=None, y_range=None, exact=False):
        """Gets current data limits using whole range or specified crops."""
        
        # check data
        if self._limits is None:
            return None
        
        # init limits
        limits = self._limits
        
        # apply crop
        if x_range or y_range:
            
            limits = utils.calc_limits_unsorted(
                data = (self._x_data, self._y_data),
                crops = (x_range, y_range),
                extend = False)
        
        # finalize limits
        return self.finalize_limits(limits, exact)
    
    
    def get_labels(self, canvas, source=UNDEF, **overrides):
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
        show_points = self.get_property('show_points', source, overrides)
        show_line = self.get_property('show_line', source, overrides)
        x_scale = self.get_property('x_scale', source, overrides)
        y_scale = self.get_property('y_scale', source, overrides)
        frame = self.get_property('frame', source, overrides)
        color = self.get_property('color', source, overrides)
        line_color = self.get_property('line_color', source, overrides)
        
        # get marker overrides
        marker_overrides = self.get_child_overrides('marker', overrides)
        marker_overrides_fin = marker_overrides.copy()
        
        # get data
        x_data = self._x_data
        y_data = self._y_data
        raw_data = self._raw_data
        
        # check data
        if len(raw_data) == 0:
            return
        
        # scale coords
        x_data = x_scale.scale(x_data)
        y_data = y_scale.scale(y_data)
        
        # get default colors
        default_line_color = color.darker(0.2)
        default_fill_color = color
        
        # start drawing group
        with canvas.group(tag, "series"):
            
            # draw line
            if show_line:
                
                # set pen and brush
                canvas.fill_color = None
                canvas.set_pen_by(self, source=source, overrides=overrides)
                
                # use default line color
                if line_color is UNDEF:
                    canvas.line_color = color
                
                # init points
                points = numpy.stack((x_data, y_data), axis=1)
                
                # draw line
                canvas.draw_lines(points)
            
            # draw points
            if show_points:
                for i, point_data in enumerate(raw_data):
                    
                    # get marker
                    marker = self.get_property('marker', point_data, marker_overrides)
                    if not marker:
                        continue
                    
                    # init glyph
                    if not isinstance(marker, Marker):
                        marker = Marker.create(marker)
                        marker.set_properties_from(self, src_prefix='marker_', overrides=marker_overrides, native=True)
                    
                    # check visibility
                    if not marker or not marker.is_visible(point_data, marker_overrides):
                        continue
                    
                    # get coords
                    x = x_data[i]
                    y = y_data[i]
                    size = marker.get_property('size', point_data, marker_overrides)
                    
                    # apply clipping
                    bbox = Frame(x-0.5*size, y-0.5*size, size, size)
                    if not frame.overlaps(bbox):
                        continue
                    
                    # get marker color
                    line_color = marker.get_property('line_color', point_data, overrides=marker_overrides)
                    if line_color is UNDEF:
                        line_color = default_line_color
                    
                    fill_color = marker.get_property('fill_color', point_data, overrides=marker_overrides)
                    if fill_color is UNDEF:
                        fill_color = default_fill_color
                    
                    # set overrides
                    marker_overrides_fin['x'] = x
                    marker_overrides_fin['y'] = y
                    marker_overrides_fin['size'] = size
                    marker_overrides_fin['line_color'] = line_color
                    marker_overrides_fin['fill_color'] = fill_color
                    
                    # draw marker
                    marker.draw(canvas, point_data, **marker_overrides_fin)


class Asterisks(Scatter):
    marker = MARKER_ASTERISK


class Circles(Scatter):
    marker = MARKER_CIRCLE


class Crosses(Scatter):
    marker = MARKER_CROSS


class Diamonds(Scatter):
    marker = MARKER_DIAMOND


class Pluses(Scatter):
    marker = MARKER_PLUS


class Triangles(Scatter):
    marker = MARKER_TRIANGLE


class Squares(Scatter):
    marker = MARKER.SQUARE
