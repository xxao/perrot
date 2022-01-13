#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import numpy

from pero.enums import *
from pero.properties import *
from pero import Scale, ContinuousScale
from pero import Legend, MarkerLegend
from pero import Label, TextLabel
from pero import Tooltip, TextTooltip

from .. chart import InGraphics
from . import utils


class Series(InGraphics):
    """
    Abstract base class for various types of plot data series. Besides others,
    it defines the main data mappers and scales. The scales are used to convert
    coordinates from real data units into device coordinates. The mappers are
    mainly used to internally convert original categorical data into a sequence
    of continuous numbers to enable plot zooming and panning. The mappers are
    applied upon series initialization within data extraction, while the scales
    are applied upon series drawing and limits calculation.
    
    Properties:
        
        x_scale: pero.ContinuousScale
            Specifies the scale to be used to convert x-coordinates from real
            data units into device coordinates.
        
        y_scale: pero.ContinuousScale
            Specifies the scale to be used to convert y-coordinates from real
            data units into device coordinates.
        
        x_mapper: pero.Scale, None or UNDEF
            Specifies the additional scale to initially map categorical
            x-coordinates values into continuous range.
        
        y_mapper : pero.Scale, None or UNDEF
            Specifies the additional scale to initially map categorical
            y-coordinates values into continuous range.
        
        margin: int, float or tuple
            Specifies the relative extend of the full real data ranges as a
            single value or values for individual sides starting from top as
            %/100.
        
        color: pero.Color, tuple, str
            Specifies the main series color as an RGB or RGBA tuple, hex code,
            name or pero.Color.
        
        title: str, None or UNDEF
            Specifies the title to be shown as legend.
        
        legend: pero.InLegend, None or UNDEF
            Specifies the explicit value for the legend or a template to create
            it. When the actual legend is initialized, current series is
            provided as a source, therefore properties can be dynamic to
            retrieve the final value from the series.
        
        label: pero.Label, None or UNDEF
            Specifies a template to create points labels. When the actual label
            is initialized, current data point is provided as a source,
            therefore properties can be dynamic to retrieve the final value from
            the point.
        
        tooltip: pero.Tooltip, None or UNDEF
            Specifies a template to create points tooltips. When the actual
            tooltip is initialized, current data point is provided as a source,
            therefore properties can be dynamic to retrieve the final value from
            the point.
        
        show_legend: bool
            Specifies whether the legend should be shown.
        
        show_labels: bool
            Specifies whether the labels should be shown.
        
        show_tooltip: bool
            Specifies whether the points tooltip should be shown.
    """
    
    x_scale = Property(UNDEF, types=(ContinuousScale,), dynamic=False)
    y_scale = Property(UNDEF, types=(ContinuousScale,), dynamic=False)
    
    x_mapper = Property(UNDEF, types=(Scale,), dynamic=False, nullable=True)
    y_mapper = Property(UNDEF, types=(Scale,), dynamic=False, nullable=True)
    
    margin = QuadProperty(0.05, dynamic=False)
    color = ColorProperty(UNDEF, dynamic=False)
    
    title = StringProperty(UNDEF, dynamic=False, nullable=True)
    legend = Property(UNDEF, types=(Legend,), dynamic=False, nullable=True)
    label = Property(UNDEF, types=(Label,), dynamic=False, nullable=True)
    tooltip = Property(UNDEF, types=(Tooltip,), dynamic=False, nullable=True)
    
    show_legend = BoolProperty(True, dynamic=False)
    show_labels = BoolProperty(UNDEF, dynamic=False)
    show_tooltip = BoolProperty(True, dynamic=False)
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of the Series."""
        
        # init legend
        if 'legend' not in overrides:
            overrides['legend'] = MarkerLegend(
                text = lambda d: d.title,
                marker = MARKER_CIRCLE,
                marker_size = 8,
                marker_line_color = lambda d: d.color.darker(0.2),
                marker_fill_color = lambda d: d.color)
        
        # init label
        if 'label' not in overrides:
            overrides['label'] = TextLabel(
                text = lambda d: str(d),
                y_offset = -4)
        
        # init tooltip
        if 'tooltip' not in overrides:
            overrides['tooltip'] = TextTooltip(
                text = lambda d: str(d))
        
        # init base
        super().__init__(**overrides)
        
        # lock properties
        self.lock_property('x_mapper')
        self.lock_property('y_mapper')
    
    
    def get_limits(self, x_range=None, y_range=None, exact=False):
        """
        Gets current data limits using whole range or specified crop.
        
        Args:
            x_range: (float, float) or None
                X-range limits.
            
            y_range: (float, float) or None
                Y-range limits.
            
            exact: bool
                If set to True, any additional space like margin is ignored.
        
        Returns:
            ((float, float),)
                Data limits as sequence of (min, max) for each dimension.
        """
        
        raise NotImplementedError("The 'get_limits' method is not implemented for '%s'." % self.__class__.__name__)
    
    
    def get_legends(self, canvas=None, source=UNDEF, **overrides):
        """Gets series legend item(s)."""
        
        # get properties
        show_legend = self.get_property('show_legend', source, overrides)
        legend = self.get_property('legend', source, overrides)
        
        # check legend
        if not show_legend or not legend:
            return ()
        
        # init item
        item = legend.clone(self, deep=True)
        
        # set title
        if item.text is UNDEF:
            item.text = self.title
        
        return [item]
    
    
    def prepare_labels(self, x_data, y_data, raw_data, v_flip=False, h_flip=False):
        """
        Prepares labels for given data range.
        
        Args:
            x_data: 1D numpy.ndarray
                X-coordinate data.
            
            y_data: 1D numpy.ndarray
                Y-coordinate data.
            
            raw_data: 1D numpy.ndarray
                Original data points.
            
            v_flip: bool
                If set to True, y_offset and text base are flipped to their
                complementary values.
            
            h_flip: bool
                If set to True, x_offset and text alignment are flipped to their
                complementary values.
        
        Returns:
            (pero.Label,)
                Labels for given data.
        """
        
        labels = []
        
        # check label
        if not self.show_labels or not self.label:
            return labels
        
        # crop data
        x_data, y_data, raw_data = utils.crop_unsorted(
            data = (x_data, y_data, raw_data),
            crops = (self.x_scale.in_range, self.y_scale.in_range),
            extend = False)
        
        # check data
        if len(raw_data) == 0:
            return labels
        
        # scale coords
        x_data = self.x_scale.scale(x_data)
        y_data = self.y_scale.scale(y_data)
        
        # create labels
        for i in range(len(raw_data)):
            overrides = {'x': x_data[i], 'y': y_data[i]}
            labels.append(self.label.clone(raw_data[i], overrides, deep=True))
        
        # apply vertical flip
        if v_flip:
            for label in labels:
                label.y_offset *= -1
                if label.text_base == TEXT_BASE_TOP:
                    label.text_base = TEXT_BASE_BOTTOM
                elif label.text_base == TEXT_BASE_BOTTOM:
                    label.text_base = TEXT_BASE_TOP
        
        # apply horizontal flip
        if h_flip:
            for label in labels:
                label.x_offset *= -1
                if label.text_align == TEXT_ALIGN_LEFT:
                    label.text_align = TEXT_ALIGN_RIGHT
                elif label.text_align == TEXT_ALIGN_RIGHT:
                    label.text_align = TEXT_ALIGN_LEFT
        
        return labels
    
    
    def prepare_tooltip(self, x_data, y_data, raw_data, x, y, limit):
        """
        Prepares nearest data point tooltip within limits from cursor position.
        
        Args:
            x_data: 1D numpy.ndarray
                X-coordinate data.
            
            y_data: 1D numpy.ndarray
                Y-coordinate data.
            
            raw_data: 1D numpy.ndarray
                Original data points.
            
            x: int or float
                Cursor x-coordinate in device units.
            
            y: int or float
                Cursor y-coordinate in device units.
            
            limit: int or float
                Maximum allowed distance in device units.
        
        Returns:
            pero.Tooltip or None
                Tooltip item.
        """
        
        # check tooltip
        if not self.show_tooltip or not self.tooltip:
            return None
        
        # calc limits
        min_x = self.x_scale.invert(x-limit)
        max_x = self.x_scale.invert(x+limit)
        min_y = self.y_scale.invert(y+limit)
        max_y = self.y_scale.invert(y-limit)
        
        # crop data
        x_data, y_data, raw_data = utils.crop_unsorted(
            data = (x_data, y_data, raw_data),
            crops = ((min_x, max_x), (min_y, max_y)),
            extend = False)
        
        # check data
        if len(raw_data) == 0:
            return None
        
        # scale coords
        x_data = self.x_scale.scale(x_data)
        y_data = self.y_scale.scale(y_data)
        
        # get nearest
        x_dist = x_data - x
        y_dist = y_data - y
        dist = numpy.sqrt(x_dist*x_dist + y_dist*y_dist)
        idx = numpy.argmin(dist)
        
        # check index
        if idx is None:
            return None
        
        # get overrides
        overrides = {
            'x': x_data[idx],
            'y': y_data[idx],
            'z_index': 1./dist[idx]}
        
        # make tooltip
        return self.tooltip.clone(raw_data[idx], overrides)
    
    
    def finalize_limits(self, limits, exact):
        """
        Finalizes given x and y data limits by applying margins etc.
        
        Args:
            limits: ((float, float),)
                Data limits as series of (min, max) for each dimension.
            
            exact: bool
                If set to True, any additional space like margin is ignored.
        
        Returns:
            ((float, float),)
                Data limits as sequence of (min, max) for each dimension.
        """
        
        # check limits
        if limits is None:
            return None
        
        # break links
        limits = list(limits)
        for i, item in enumerate(limits):
            if item is not None:
                limits[i] = list(item)
        
        # add margin to x and y axes
        if self.margin and not exact:
            
            if limits[0] is not None:
                delta = limits[0][1] - limits[0][0]
                limits[0][0] -= delta * self.margin[3]
                limits[0][1] += delta * self.margin[1]
            
            if limits[1] is not None:
                delta = limits[1][1] - limits[1][0]
                limits[1][0] -= delta * self.margin[2]
                limits[1][1] += delta * self.margin[0]
        
        # avoid zero range
        for item in limits:
            if item is not None and item[0] == item[1]:
                item[0] -= item[0]*0.1
                item[1] += item[1]*0.1
        
        return limits
