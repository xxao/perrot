#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from pero.properties import *
from pero import StraitAxis
from pero import Scale, ContinuousScale, LinScale, LogScale, OrdinalScale
from pero import Ticker, LinTicker, LogTicker, FixTicker, TimeTicker
from pero import Formatter, IndexFormatter

from .. enums import *
from . graphics import OutGraphics


class Axis(OutGraphics):
    """
    Axis provides a wrapper for the pero.StraitAxis glyph to draw axes in
    charts. It is using specified 'scale' and 'ticker' instances to convert
    coordinates between original data units to device output positions.
    
    There are some additional properties like 'autoscale', 'symmetric',
    'check_limits', 'includes' etc., which have no direct effect on the
    axis but can be used by parent chart to correctly adjust the scaling along
    particular axis and influence chart interactivity.
    
    For some tools it might be convenient to 'format' a real value using axis
    scale and ticker formatter. If specific formatter is needed it can be
    provided by the 'tooltip' property.
    
    Properties:
        
        mapper: pero.Scale, None or UNDEF
            Specifies the additional scale to initially map categorical data
            values into continuous range.
        
        scale: pero.ContinuousScale
            Specifies the scale providing actual range to use and to
            re-calculate the ticks values into final coordinates.
        
        ticker: pero.Ticker
            Specifies the ticks generator to provide ticks positions and labels.
        
        title: str, None or UNDEF
            Specifies the title to show.
        
        title_text properties:
            Includes pero.TextProperties to specify the title text
            properties. Some of them (e.g. alignment, angle, baseline) are
            typically set automatically according to other axis properties.
        
        title_position: str
            Specifies the title position relative to the axis origin as any item
            from the pero.POSITION_SEM enum.
        
        title_offset: int or float
            Specifies the shift of the title from the labels, ticks or main
            line.
        
        label_text properties:
            Includes pero.TextProperties to specify the labels text
            properties. Some of them (e.g. alignment, angle, baseline) are
            typically set automatically according to other axis properties.
        
        label_offset: int or float
            Specifies the shift of the labels from the ticks or the main line.
        
        label_angle properties:
            Includes pero.AngleProperties to specify the labels angle.
        
        label_overlap: bool
            Specifies whether the labels can overlap (True) or should be removed
            automatically (False).
        
        line properties:
            Includes pero.LineProperties to specify the main line.
        
        major_tick_line properties:
            Includes pero.LineProperties to specify the major ticks line.
        
        major_tick_size: int or float
            Specifies the length of the major ticks.
        
        major_tick_offset: int or float
            Specifies the shift of the major ticks from the main line.
        
        minor_tick_line properties:
            Includes pero.LineProperties to specify the minor ticks line.
        
        minor_tick_size: int or float
            Specifies the length of the minor ticks.
        
        minor_tick_offset: int or float
            Specifies the shift of the minor ticks from the main line.
        
        level: int
            Specifies the dependency level on other plot axes.
        
        static: bool
            Specifies whether the range should be fixed (True) or whether it
            should be changed by current data, zooming and panning.
        
        autoscale: bool
            Specifies whether the range should be set automatically according to
            currently displayed data.
        
        symmetric: bool
            Specifies whether the range should always be adjusted to be
            symmetrical along zero.
        
        includes: tuple, None or UNDEF
            Specifies the values to be always within the displayed range.
        
        check_limits: bool
            Specifies whether displayed range should not exceed the limits
            defined by current data. This value is used to limit zooming and
            panning.
        
        empty_range: tuple
            Specifies the default range to be used if there are no data in the
            chart.
        
        tooltip: pero.Formatter, None or UNDEF
            Specifies the explicit formatter to be used by the 'format' method.
            If set to None the empty string is returned. If set to UNDEF the
            formatter defined by current ticker is used.
        
        tooltip_resaware: bool
            Specifies whether custom tooltip formatter domain and precision
            should be set automatically based on current axis resolution.
        
        show_title: bool
            Specifies whether the title should be displayed.
        
        show_labels: bool
            Specifies whether the labels should be displayed.
        
        show_line: bool
            Specifies whether the major axis line should be displayed.
        
        show_major_ticks: bool
            Specifies whether the major ticks should be displayed.
        
        show_minor_ticks: bool
            Specifies whether the minor ticks should be displayed.
    """
    
    mapper = Property(UNDEF, types=(Scale,), dynamic=False, nullable=True)
    scale = Property(UNDEF, types=(ContinuousScale,), dynamic=False)
    ticker = Property(UNDEF, types=(Ticker,), dynamic=False)
    
    title = StringProperty(None, dynamic=False, nullable=True)
    title_text = Include(TextProperties, prefix="title_", dynamic=False, font_weight=FONT_WEIGHT_BOLD, font_size=12)
    title_position = EnumProperty(POS_MIDDLE, enum=POSITION_SEM, dynamic=False)
    title_offset = NumProperty(5, dynamic=False)
    
    label_text = Include(TextProperties, prefix="label_", dynamic=False, font_size=11)
    label_offset = NumProperty(3, dynamic=False)
    label_angle = Include(AngleProperties, prefix="label_", dynamic=False)
    label_overlap = BoolProperty(False, dynamic=False)
    
    line = Include(LineProperties, dynamic=False, line_color="#000")
    
    major_tick_line = Include(LineProperties, prefix="major_tick_", dynamic=False, line_color="#000")
    major_tick_size = NumProperty(6, dynamic=False)
    major_tick_offset = NumProperty(0, dynamic=False)
    
    minor_tick_line = Include(LineProperties, prefix="minor_tick_", dynamic=False, line_color="#000")
    minor_tick_size = NumProperty(3, dynamic=False)
    minor_tick_offset = NumProperty(0, dynamic=False)
    
    level = IntProperty(2, dynamic=False)
    static = BoolProperty(False, dynamic=False)
    autoscale = BoolProperty(False, dynamic=False)
    symmetric = BoolProperty(False, dynamic=False)
    includes = TupleProperty(UNDEF, intypes=(float, int), dynamic=False, nullable=True)
    check_limits = BoolProperty(False, dynamic=False)
    empty_range = TupleProperty((0., 1.), intypes=(float, int), dynamic=False)
    
    tooltip = Property(UNDEF, types=(Formatter,), dynamic=False, nullable=True)
    tooltip_resaware = BoolProperty(True, dynamic=False)
    
    show_title = BoolProperty(True, dynamic=False)
    show_labels = BoolProperty(True, dynamic=False)
    show_line = BoolProperty(True, dynamic=False)
    show_major_ticks = BoolProperty(True, dynamic=False)
    show_minor_ticks = BoolProperty(True, dynamic=False)
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of the Axis."""
        
        # init scale
        if 'scale' not in overrides:
            overrides['scale'] = LinScale(in_range=(0., 1.))
        
        # init ticker
        if 'ticker' not in overrides:
            overrides['ticker'] = LinTicker()
        
        # init base
        super().__init__(**overrides)
        
        # init axis glyph
        self._glyph = StraitAxis()
        
        # set defaults by position
        self._update_position(**overrides)
        
        # bind events
        self.bind(EVT_PROPERTY_CHANGED, self._on_axis_property_changed)
    
    
    def get_extent(self, canvas, source=UNDEF, **overrides):
        """
        This method is automatically called by parent chart to get amount of
        logical space needed to draw the object.
        """
        
        extent = self._get_ticks_extent(canvas, source, **overrides)
        extent += self._get_labels_extent(canvas, source, **overrides)
        extent += self._get_title_extent(canvas, source, **overrides)
        
        return extent
    
    
    def get_range(self, device=False):
        """
        Gets current displayed range of the axis using device or data units.
        
        Args:
            device: bool
                If set to True, device units are returned instead of real data
                units.
        
        Returns:
            (float, float)
                Current range.
        """
        
        return self.scale.out_range if device else self.scale.in_range
    
    
    def get_tooltip(self, value):
        """
        Formats given value using defined tooltip or ticker formatter.
        
        Args:
            value: any
                Raw value to be formatted.
        
        Returns:
            str
                Formatted value.
        """
        
        # tooltip disabled
        if self.tooltip is None:
            return ""
        
        # use ticker formatter
        if self.tooltip is UNDEF:
            formatter = self.ticker.formatter
        
        # use custom formatter
        else:
            formatter = self.tooltip
            if self.tooltip_resaware:
                in_range = self.scale.in_range[1] - self.scale.in_range[0]
                out_range = self.scale.out_range[1] - self.scale.out_range[0]
                formatter.domain = in_range
                formatter.precision = in_range / out_range
        
        # format value
        return formatter.format(value) + formatter.suffix()
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw the axis."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # update scale
        self._update_scale(canvas, source, **overrides)
        
        # update axis glyph
        self._update_glyph(canvas, source, **overrides)
        
        # draw axis
        self._glyph.draw(canvas)
    
    
    def zoom(self, start=None, end=None):
        """
        Sets current displayed range of the axis using real data units. If None
        is set for particular value, current value is kept.
        
        Args:
            start: float or None
                Axis start value.
            
            end: float or None
                Axis end value.
        """
        
        # get limits if not set
        if start is None:
            start = self.scale.in_range[0]
        if end is None:
            end = self.scale.in_range[1]
        
        # update scale
        self.scale.in_range = (start, end)
        
        # update ticker
        self.ticker.start = self.scale.in_range[0]
        self.ticker.end = self.scale.in_range[1]
    
    
    def _get_ticks_extent(self, canvas=None, source=UNDEF, **overrides):
        """Calculates the space needed for ticks."""
        
        extent = 0
        
        # get properties
        show_major_ticks = self.get_property('show_major_ticks', source, overrides)
        show_minor_ticks = self.get_property('show_minor_ticks', source, overrides)
        
        # add major ticks
        if show_major_ticks:
            size = self.get_property('major_tick_size', source, overrides)
            offset = self.get_property('major_tick_offset', source, overrides)
            extent = size + offset
        
        # add minor ticks
        if show_minor_ticks:
            size = self.get_property('minor_tick_size', source, overrides)
            offset = self.get_property('minor_tick_offset', source, overrides)
            extent = max(extent, size + offset)
        
        return max(0, extent)
    
    
    def _get_labels_extent(self, canvas, source=UNDEF, **overrides):
        """Calculates the space needed for labels."""
        
        # check if enabled
        show_labels = self.get_property('show_labels', source, overrides)
        if not show_labels:
            return 0
        
        # get properties
        position = self.get_property('position', source, overrides)
        scale = self.get_property('scale', source, overrides)
        ticker = self.get_property('ticker', source, overrides)
        offset = self.get_property('label_offset', source, overrides)
        angle = AngleProperties.get_angle(self, 'label_', ANGLE_RAD, source, overrides)
        
        # make labels
        ticker.start = scale.in_range[0]
        ticker.end = scale.in_range[1]
        labels = ticker.labels()
        
        # check labels
        if not labels:
            return max(0, offset)
        
        # get longest
        max_label = max(labels, key=lambda x: len(x))
        
        # set text
        canvas.set_text_by(self, prefix="label_", source=source, overrides=overrides)
        
        # get extent
        bbox = canvas.get_text_bbox(max_label, angle=angle)
        extent = bbox.height if position in POSITION_TB else bbox.width
        
        return max(0, offset + extent)
    
    
    def _get_title_extent(self, canvas, source=UNDEF, **overrides):
        """Calculates the space needed for title."""
        
        # get title
        title = self.get_property('title', source, overrides)
        if not title:
            return 0
        
        # get properties
        offset = self.get_property('title_offset', source, overrides)
        
        # set text
        canvas.set_text_by(self, prefix="title_", source=source, overrides=overrides)
        
        # get size
        return offset + canvas.get_text_size(title)[1]
    
    
    def _update_glyph(self, canvas, source=UNDEF, **overrides):
        """Updates axis glyph."""
        
        # get properties
        frame = self.get_property('frame', source, overrides)
        position = self.get_property('position', source, overrides)
        scale = self.get_property('scale', source, overrides)
        ticker = self.get_property('ticker', source, overrides)
        title = self.get_property('title', source, overrides)
        title_offset = self.get_property('title_offset', source, overrides)
        label_offset = self.get_property('label_offset', source, overrides)
        
        # make ticks
        ticker.start = scale.in_range[0]
        ticker.end = scale.in_range[1]
        major_ticks = tuple(map(scale.scale, ticker.major_ticks()))
        minor_ticks = tuple(map(scale.scale, ticker.minor_ticks()))
        
        # make title and labels
        labels = ticker.labels()
        title = title + ticker.suffix() if title else ""
        
        # get offsets
        ticks_extent = self._get_ticks_extent(canvas, source, **overrides)
        labels_extent = self._get_labels_extent(canvas, source, **overrides)
        label_offset += ticks_extent
        title_offset += ticks_extent + labels_extent
        
        # get anchor
        if position == POS_LEFT:
            x = frame.x2
            y = frame.y1
        
        elif position == POS_RIGHT:
            x = frame.x1
            y = frame.y1
        
        elif position == POS_TOP:
            x = frame.x1
            y = frame.y2
        
        elif position == POS_BOTTOM:
            x = frame.x1
            y = frame.y1
        
        else:
            x = frame.x1
            y = frame.y1
        
        # get length
        length = abs(scale.out_range[1] - scale.out_range[0])
        
        # update glyph shared
        self._glyph.set_properties_from(self, source=source, overrides=overrides)
        
        # update glyph
        self._glyph.x = x
        self._glyph.y = y
        self._glyph.length = length
        self._glyph.title = title
        self._glyph.labels = labels
        self._glyph.major_ticks = major_ticks
        self._glyph.minor_ticks = minor_ticks
        self._glyph.title_offset = title_offset
        self._glyph.label_offset = label_offset
    
    
    def _update_scale(self, canvas=None, source=UNDEF, **overrides):
        """Updates scale according to current frame."""
        
        # get properties
        frame = self.get_property('frame', source, overrides)
        position = self.get_property('position', source, overrides)
        scale = self.get_property('scale', source, overrides)
        
        # update scale
        if position == POS_LEFT:
            scale.out_range = frame.y2, frame.y1
        
        elif position == POS_RIGHT:
            scale.out_range = frame.y2, frame.y1
        
        elif position == POS_TOP:
            scale.out_range = frame.x1, frame.x2
        
        elif position == POS_BOTTOM:
            scale.out_range = frame.x1, frame.x2
        
        else:
            scale.out_range = frame.x1, frame.x2
    
    
    def _update_position(self, canvas=None, source=UNDEF, **overrides):
        """Updates properties according to current position."""
        
        # get properties
        position = self.get_property('position', source, overrides)
        
        # init values
        title_text_align = UNDEF
        title_text_base = UNDEF
        label_text_align = UNDEF
        label_text_base = UNDEF
        
        # left axis
        if position == POS_LEFT:
            title_text_align = TEXT_ALIGN_CENTER
            title_text_base = TEXT_BASE_BOTTOM
            label_text_align = TEXT_ALIGN_RIGHT
            label_text_base = TEXT_BASE_MIDDLE
        
        # right axis
        elif position == POS_RIGHT:
            title_text_align = TEXT_ALIGN_CENTER
            title_text_base = TEXT_BASE_BOTTOM
            label_text_align = TEXT_ALIGN_LEFT
            label_text_base = TEXT_BASE_MIDDLE
        
        # top axis
        elif position == POS_TOP:
            title_text_align = TEXT_ALIGN_CENTER
            title_text_base = TEXT_BASE_BOTTOM
            label_text_align = TEXT_ALIGN_CENTER
            label_text_base = TEXT_BASE_BOTTOM
        
        # bottom axis
        elif position == POS_BOTTOM:
            title_text_align = TEXT_ALIGN_CENTER
            title_text_base = TEXT_BASE_TOP
            label_text_align = TEXT_ALIGN_CENTER
            label_text_base = TEXT_BASE_TOP
        
        # automatic
        elif position != UNDEF:
            return
        
        # apply
        if 'title_text_align' not in overrides:
            self.title_text_align = title_text_align
        
        if 'title_text_base' not in overrides:
            self.title_text_base = title_text_base
        
        if 'label_text_align' not in overrides:
            self.label_text_align = label_text_align
        
        if 'label_text_base' not in overrides:
            self.label_text_base = label_text_base
    
    
    def _on_axis_property_changed(self, evt):
        """Called after any property has changed."""
        
        if evt.name == 'frame':
            self._update_scale()
        
        # position changed
        if evt.name == 'position':
            self._update_position()


class LinAxis(Axis):
    """Predefined axis with linear scale and ticker."""
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of the LinAxis."""
        
        # init defaults
        if 'scale' not in overrides:
            overrides['scale'] = LinScale(in_range=(0., 1.))
        
        if 'ticker' not in overrides:
            overrides['ticker'] = LinTicker()
        
        # init base
        super().__init__(**overrides)
        
        # lock scale and ticker
        self.lock_property('scale')
        self.lock_property('ticker')


class LogAxis(Axis):
    """
    Predefined axis with logarithmic scale and ticker.
    
    Properties:
        
        base: int or float
            Specifies the logarithm base.
    """
    
    base = NumProperty(UNDEF, dynamic=False)
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of the LogAxis."""
        
        # init defaults
        if 'scale' not in overrides:
            overrides['scale'] = LogScale(in_range=(1., 10.))
        
        if 'ticker' not in overrides:
            overrides['ticker'] = LogTicker()
        
        if 'empty_range' not in overrides:
            overrides['empty_range'] = (1., 10.)
        
        # init base
        super().__init__(**overrides)
        
        # lock scale and ticker
        self.lock_property('scale')
        self.lock_property('ticker')
        
        # bind events
        self.bind(EVT_PROPERTY_CHANGED, self._on_log_axis_property_changed)
        
        # update base
        if 'base' in overrides:
            self._update_base()
    
    
    def _update_base(self):
        """Updates ticker by current base."""
        
        self.ticker.base = self.base
        self.ticker.formatter.base = self.base
    
    
    def _on_log_axis_property_changed(self, evt):
        """Called after any property has changed."""
        
        # base changed
        if evt.name == 'base':
            self._update_base()


class OrdinalAxis(Axis):
    """
    Predefined axis for categorical data.
    
    Properties:
        
        labels: tuple
            Specifies the labels to be displayed.
    """
    
    labels = TupleProperty(UNDEF, intypes=(str,), dynamic=False)
    
    major_tick_size = NumProperty(0, dynamic=False)
    minor_tick_size = NumProperty(6, dynamic=False)
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of the OrdinalAxis."""
        
        # init defaults
        if 'scale' not in overrides:
            overrides['scale'] = LinScale(in_range=(-0.5, 0.5))
        
        if 'ticker' not in overrides:
            overrides['ticker'] = FixTicker(formatter=IndexFormatter())
        
        # init base
        super().__init__(**overrides)
        
        # lock scale and ticker
        self.lock_property('scale')
        self.lock_property('ticker')
        
        # update labels
        self._update_labels()
        
        # bind events
        self.bind(EVT_PROPERTY_CHANGED, self._on_ordinal_axis_property_changed)
    
    
    def _update_labels(self):
        """Updates mapper, scale and ticker by current labels."""
        
        # remove labels
        if not self.labels:
            self.mapper = UNDEF
            self.empty_range = (-0.5, 0.5)
            self.scale.in_range = (-0.5, 0.5)
            self.ticker.major_values = ()
            self.ticker.minor_values = ()
            self.ticker.formatter.labels = ()
            return
        
        # init values
        count = len(self.labels)
        mapper_values = tuple(range(count))
        major_ticks = tuple(range(count))
        minor_ticks = tuple([-0.5] + [t + 0.5 for t in major_ticks])
        full_range = (-0.5, count-0.5)
        
        # make mapper
        self.mapper = OrdinalScale(
            in_range = self.labels,
            out_range = mapper_values,
            default = UNDEF,
            implicit = False,
            recycle = False)
        
        # update scale
        self.empty_range = full_range
        self.scale.in_range = full_range
        
        # update ticker
        self.ticker.major_values = major_ticks
        self.ticker.minor_values = minor_ticks
        self.ticker.formatter.labels = self.labels
    
    
    def _on_ordinal_axis_property_changed(self, evt):
        """Called after any property has changed."""
        
        # labels changed
        if evt.name == 'labels':
            self._update_labels()


class TimeAxis(Axis):
    """Predefined axis with linear scale and time ticker."""
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of the TimeAxis."""
        
        # init defaults
        if 'scale' not in overrides:
            overrides['scale'] = LinScale(in_range=(0., 1.))
        
        if 'ticker' not in overrides:
            overrides['ticker'] = TimeTicker()
        
        # init base
        super().__init__(**overrides)
        
        # lock scale and ticker
        self.lock_property('scale')
        self.lock_property('ticker')
