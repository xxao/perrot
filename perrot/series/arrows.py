#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import numpy

from pero.enums import *
from pero.properties import *
from pero import Frame
from pero import Arrow, Head

from . series import Series
from . import utils


class Arrows(Series):
    """
    This type of series plots raw data as individual arrows. Data can be
    provided either directly by specifying 'x1, y1, x2, y2' properties
    or as a sequence of raw 'data' points together with respective coordinate
    selectors. All the coordinates are expected to be in real data units.
    """
    
    data = SequenceProperty(UNDEF, dynamic=False)
    x1 = Property(UNDEF)
    y1 = Property(UNDEF)
    x2 = Property(UNDEF)
    y2 = Property(UNDEF)

    arrow_props = Include(Arrow, prefix='arrow_', line_color=UNDEF)
    arrow_start_props = Include(Head, prefix='arrow_start_head_')
    arrow_end_props = Include(Head, prefix='arrow_end_head_')
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of the Band series."""
        
        # init base
        super().__init__(**overrides)
        
        # init buffers
        self._x1_data = []
        self._y1_data = []
        self._x2_data = []
        self._y2_data = []
        self._raw_data = []
        self._limits = None
        
        # extract data
        self.extract_data()
        
        # lock properties
        self.lock_property('data')
        self.lock_property('x1')
        self.lock_property('y1')
        self.lock_property('x2')
        self.lock_property('y2')
    
    
    def get_limits(self, x_range=None, y_range=None, exact=False):
        """Gets current data limits using whole range or specified crops."""
        
        # check data
        if self._limits is None:
            return None
        
        # init limits
        limits = self._limits
        
        # apply crop
        if x_range or y_range:
            
            limits_1 = utils.calc_limits_unsorted(
                data = (self._x1_data, self._y1_data),
                crops = (x_range, y_range),
                extend = False)
            
            limits_2 = utils.calc_limits_unsorted(
                data = (self._x2_data, self._y2_data),
                crops = (x_range, y_range),
                extend = False)
            
            limits = utils.combine_limits(limits_1, limits_2)
        
        # finalize limits
        return self.finalize_limits(limits, exact)
    
    
    def extract_data(self):
        """Extracts coordinates from raw data."""
        
        # reset buffers
        self._x1_data = []
        self._y1_data = []
        self._x2_data = []
        self._y2_data = []
        self._raw_data = []
        self._limits = None
        
        # get data size
        size = utils.extract_data_size(self, 'data', 'x1', 'y1', 'x2', 'y2')
        
        # extract data
        self._x1_data, x1_raw = utils.extract_data(self, 'x1', self.data, size, self.x_mapper)
        self._y1_data, y1_raw = utils.extract_data(self, 'y1', self.data, size, self.x_mapper)
        self._x2_data, x2_raw = utils.extract_data(self, 'x2', self.data, size, self.y_mapper)
        self._y2_data, y2_raw = utils.extract_data(self, 'y2', self.data, size, self.y_mapper)
        
        # set raw data
        if self.data is not UNDEF:
            self._raw_data = numpy.array(self.data, dtype=object)
        else:
            self._raw_data = numpy.array([x1_raw, y1_raw, x2_raw, y2_raw]).T
        
        # init full limits
        if len(self._raw_data) > 0:
            self._limits = (
                (min(self._x1_data.min(), self._x2_data.min()),
                    max(self._x1_data.max(), self._x2_data.max())),
                (min(self._y1_data.min(), self._y2_data.min()),
                    max(self._y1_data.max(), self._y2_data.max())))
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw the series."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # get properties
        tag = self.get_property('tag', source, overrides)
        x_scale = self.get_property('x_scale', source, overrides)
        y_scale = self.get_property('y_scale', source, overrides)
        frame = self.get_property('frame', source, overrides)
        color = self.get_property('color', source, overrides)
        
        # get arrow overrides
        arrow_overrides = self.get_child_overrides('arrow', overrides)
        arrow_overrides_fin = arrow_overrides.copy()
        
        # get data
        x1_data = self._x1_data
        y1_data = self._y1_data
        x2_data = self._x2_data
        y2_data = self._y2_data
        raw_data = self._raw_data
        
        # check data
        if len(raw_data) == 0:
            return
        
        # scale coords
        x1_data = x_scale.scale(x1_data)
        y1_data = y_scale.scale(y1_data)
        x2_data = x_scale.scale(x2_data)
        y2_data = y_scale.scale(y2_data)
        
        # get default colors
        default_line_color = color
        default_fill_color = color.lighter(0.2)
        
        # start drawing group
        with canvas.group(tag, "series"):
            
            # draw lines
            for i, line_data in enumerate(raw_data):
                
                # get coords
                x1 = x1_data[i]
                y1 = y1_data[i]
                x2 = x2_data[i]
                y2 = y2_data[i]
                
                # apply clipping
                bbox = Frame(x1, y1, x2-x2, y2-y1)
                if not frame.overlaps(bbox):
                    continue
                
                # init glyph
                arrow = Arrow.create(ARROW_LINE)
                arrow.set_properties_from(self, src_prefix='arrow_', overrides=arrow_overrides, native=True)
                
                # check visibility
                if not arrow or not arrow.is_visible(line_data, arrow_overrides):
                    continue
                
                # get colors
                line_color = arrow.get_property('line_color', line_data, overrides=arrow_overrides)
                if line_color is UNDEF:
                    line_color = default_line_color
                
                fill_color = arrow.get_property('fill_color', line_data, overrides=arrow_overrides)
                if fill_color is UNDEF:
                    fill_color = default_fill_color
                
                # set overrides
                arrow_overrides_fin['x1'] = x1
                arrow_overrides_fin['y1'] = y1
                arrow_overrides_fin['x2'] = x2
                arrow_overrides_fin['y2'] = y2
                arrow_overrides_fin['line_color'] = line_color
                arrow_overrides_fin['fill_color'] = fill_color
                
                # draw arrow
                arrow.draw(canvas, line_data, **arrow_overrides_fin)
