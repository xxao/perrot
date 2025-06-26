#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from pero.properties import *
from pero import colors
from pero import Line, Bar, Text, Textbox, Marker
from pero import OrdinalScale

from .. enums import *
from .. chart import ChartBase, Axis, Grid, Labels, Annotation
from .. chart import Title, InLegend, OutLegend, PositionBar
from .. series import Series, Scatter, Profile, Band
from .. series import Rects, Bars, HBars, VBars
from .. series.utils import calc_histogram


class Plot(ChartBase):
    """
    Plot provides a pre-build simple chart with included X and Y axes, title,
    legend and labels container. In addition, convenient methods to add various
    types of series are available.
    
    Properties:
        
        title: perrot.Title, None or UNDEF
            Specifies the title display graphics.
        
        legend: perrot.Legend, None or UNDEF
            Specifies the legend display graphics.
        
        label: pero.TextLabel
            Specifies the glyph to be used to draw labels.
        
        x_axis: perrot.Axis
            Specifies the x-axis graphics.
        
        x_major_grid: perrot.Grid, None or UNDEF
            Specifies the x-axis major gridlines graphics.
        
        x_minor_grid: perrot.Grid, None or UNDEF
            Specifies the x-axis minor gridlines graphics.
        
        y_axis: perrot.Axis
            Specifies the y-axis graphics.
        
        y_major_grid: perrot.Grid, None or UNDEF
            Specifies the y-axis major gridlines graphics.
        
        y_minor_grid: perrot.Grid, None or UNDEF
            Specifies the y-axis minor gridlines graphics.
    """
    
    title = Property(UNDEF, types=(Title,), dynamic=False, nullable=True)
    legend = Property(UNDEF, types=(InLegend, OutLegend), dynamic=False, nullable=True)
    labels = Property(UNDEF, types=(Labels,), dynamic=False, nullable=True)
    
    x_axis = Property(UNDEF, types=(Axis,), dynamic=False)
    x_major_grid = Property(UNDEF, types=(Grid,), dynamic=False, nullable=True)
    x_minor_grid = Property(UNDEF, types=(Grid,), dynamic=False, nullable=True)
    
    y_axis = Property(UNDEF, types=(Axis,), dynamic=False)
    y_major_grid = Property(UNDEF, types=(Grid,), dynamic=False, nullable=True)
    y_minor_grid = Property(UNDEF, types=(Grid,), dynamic=False, nullable=True)
    
    palette = PaletteProperty(colors.Pero, dynamic=False)
    
    frame_line_color = ColorProperty("#000", dynamic=False)
    frame_line_width = NumProperty(1, dynamic=False)
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of the Plot."""
        
        # init title
        if 'title' not in overrides:
            overrides['title'] = Title(
                tag = 'title',
                z_index = TITLE_Z,
                position = POS_TOP)
        
        # init legend
        if 'legend' not in overrides:
            overrides['legend'] = InLegend(
                tag = 'legend',
                z_index = LEGEND_Z,
                position = POS_NE,
                orientation = ORI_VERTICAL)
        
        # init labels
        if 'labels' not in overrides:
            overrides['labels'] = Labels(
                tag = 'labels',
                z_index = LABELS_Z)
        
        # init x-axis
        if 'x_axis' not in overrides:
            overrides['x_axis'] = Axis(
                tag = 'x_axis',
                position = POS_BOTTOM,
                level = 1,
                margin = 0)
        
        # init x-axis gridlines
        if 'x_major_grid' not in overrides:
            overrides['x_major_grid'] = Grid(
                tag = 'x_major_grid',
                z_index = GRID_MAJOR_Z,
                orientation = VERTICAL,
                mode = GRID_MAJOR,
                line_color = "#e6e6e6ff")
        
        if 'x_minor_grid' not in overrides:
            overrides['x_minor_grid'] = Grid(
                tag = 'x_minor_grid',
                z_index = GRID_MINOR_Z,
                orientation = VERTICAL,
                mode = GRID_MINOR,
                line_color = "#f5f5f5ff")
        
        # init y-axis
        if 'y_axis' not in overrides:
            overrides['y_axis'] = Axis(
                tag = 'y_axis',
                position = POS_LEFT,
                level = 2,
                margin = 0)
        
        # init y-axis gridlines
        if 'y_major_grid' not in overrides:
            overrides['y_major_grid'] = Grid(
                tag = 'y_major_grid',
                z_index = GRID_MAJOR_Z,
                orientation = HORIZONTAL,
                mode = GRID_MAJOR,
                line_color = "#e6e6e6ff")
        
        if 'y_minor_grid' not in overrides:
            overrides['y_minor_grid'] = Grid(
                tag = 'y_minor_grid',
                z_index = GRID_MINOR_Z,
                orientation = HORIZONTAL,
                mode = GRID_MINOR,
                line_color = "#f5f5f5ff")
        
        # init base
        super().__init__(**overrides)
        
        # init graphics
        self._init_graphics()
        
        # init color scale
        self._init_colors()
        
        # bind events
        self.bind(EVT_PROPERTY_CHANGED, self._on_plot_property_changed)
    
    
    @property
    def axes(self):
        """
        Gets all registered axes.
        
        Returns:
            (perrot.Axis,)
                Registered axes.
        """
        
        return tuple(obj for obj in self.graphics if isinstance(obj, Axis))
    
    
    @property
    def series(self):
        """
        Gets all registered data series.
        
        Returns:
            (perrot.Series,)
                Registered series.
        """
        
        return tuple(obj for obj in self.graphics if isinstance(obj, Series))
    
    
    @property
    def annotations(self):
        """
        Gets all registered annotations.
        
        Returns:
            (perrot.Annotation,)
                Registered annotations.
        """
        
        return tuple(obj for obj in self.graphics if isinstance(obj, Annotation))
    
    
    def get_limits(self, axis, x_range=None, y_range=None, exact=False):
        """
        Gets minimum and maximum value from all visible series connected to
        specified axis. The range can be used to crop data in particular
        dimension (e.g. provide x_range to get minimum and maximum values of the
        cropped data in y dimension).
        
        Args:
            axis: str or perrot.plot.Axis
                Axis's unique tag or the axis itself.
            
            x_range: (float, float) or None
                X-range limits.
            
            y_range: (float, float) or None
                Y-range limits.
            
            exact: bool
                If set to True, the limits are retrieved for data only, i.e. any
                additional space like margin is ignored.
        
        Returns:
            (float, float)
                Minimum and maximum value of the axis from related series.
        """
        
        return self._get_series_limits(axis, x_range, y_range, exact)
    
    
    def grid(self, axis, **overrides):
        """
        This method provides a convenient way to add grid lines to current
        chart and assign specified axis scale and ticker, so that the ticks and
        labels are automatically created and synchronized with the axis.
        
        The order in which the grids are drawn is not guaranteed, so if
        important, the z_index property should be set. The perrot.GRID_MAJOR_Z
        or perrot.GRID_MINOR_Z values should be used as a starting point for all
        grids.
        
        Args:
            axis: str or perrot.plot.Axis
                Parent axis tag or the axis itself.
            
            overrides: key:value pairs
                Specific properties to be set to the grid.
        
        Returns:
            perrot.Grid
                Final grid object.
        """
        
        # get axis
        axis = self.get_obj(axis)
        
        # init grid
        grid = Grid(**overrides)
        
        # set orientation
        grid.orientation = HORIZONTAL
        if axis.position in POSITION_TB:
            grid.orientation = VERTICAL
        
        # set z-index
        if grid.z_index is UNDEF:
            grid.z_index = GRID_MINOR_Z if grid.mode == GRID_MINOR else GRID_MAJOR_Z
        
        # register object
        self.add(grid)
        
        # map axis
        self.map(grid, 'scale', axis, 'scale')
        self.map(grid, 'ticker', axis, 'ticker')
        
        return grid
    
    
    def posbar(self, axis, **overrides):
        """
        This method provides a convenient way to add position bar to current
        chart and assign specified axis scale, so that the actual range is
        automatically synchronized with the axis.
        
        Args:
            axis: str or perrot.plot.Axis
                Parent axis tag or the axis itself.
            
            overrides: key:value pairs
                Specific properties to be set to the bar.
        
        Returns:
            perrot.PositionBar
                Final position bar object.
        """
        
        # get axis
        axis = self.get_obj(axis)
        
        # init bar
        bar = PositionBar(**overrides)
        
        # set orientation
        bar.position = POS_TOP
        if axis.position in POSITION_LR:
            bar.position = POS_RIGHT
        
        # register object
        self.add(bar)
        
        # map axis
        self.map(bar, 'scale', axis, 'scale')
        
        return bar
    
    
    def plot(self, series, x_axis='x_axis', y_axis='y_axis', **overrides):
        """
        This method provides a convenient way to add data series to current
        chart and assign specified axes scales, so that the series is
        automatically scaled/positioned to device coordinates.
        
        The order in which the series are drawn is not guaranteed, so if
        important, the z_index property should be set. The perrot.SERIES_Z value
        should be used as a starting point for all series.
        
        Args:
            series: perrot.Series
                Series data to be added.
            
            x_axis: str or perrot.plot.Axis
                X-axis tag or the axis itself.
            
            y_axis: str or perrot.plot.Axis
                Y-axis tag or the axis itself.
            
            overrides: key:value pairs
                Specific properties to be set additionally to the series.
        """
        
        # check type
        if not isinstance(series, Series):
            message = "Series must be of type perrot.Series! -> %s" % type(series)
            raise TypeError(message)
        
        # apply overrides
        if overrides:
            series.set_properties(overrides, True)
        
        # set z-index
        if series.z_index is UNDEF:
            current = [obj.z_index for obj in self.series]
            series.z_index = 1 + max([SERIES_Z]+current)
        
        # set color
        if series.color is UNDEF and self._colors:
            series.color = self._colors.scale(series.tag)
        
        # get axes
        x_axis = self.get_obj(x_axis)
        y_axis = self.get_obj(y_axis)
        
        # register object
        self.add(series)
        
        # map axis
        self.map(series, 'x_scale', x_axis, 'scale')
        self.map(series, 'y_scale', y_axis, 'scale')
    
    
    def annotate(self, annotation, x_axis='x_axis', y_axis='y_axis', **overrides):
        """
        This method provides a convenient way to add annotations to current
        chart and assign specified axes scales, so that the annotation is
        automatically scaled/positioned to device coordinates.
        
        The order in which the annotations are drawn is not guaranteed, so if
        important, the z_index property should be set. The perrot.ANNOTS_Z value
        should be used as a starting point for all annotations.
        
        Args:
            annotation: perrot.Annotation or pero.Glyph
                Annotation or glyph to be added.
            
            x_axis: str, perrot.Axis
                X-axis tag or the axis itself.
            
            y_axis: str, perrot.Axis
                Y-axis tag or the axis itself.
            
            overrides: key:value pairs
                Specific properties to be set additionally to the annotation.
        
        Returns:
            perrot.Annotation
                Final annotation object.
        """
        
        # create annotation
        if not isinstance(annotation, Annotation):
            annotation = Annotation(glyph=annotation, **overrides)
        
        # apply overrides
        elif overrides:
            annotation.set_properties(overrides)
        
        # set z-index
        if annotation.z_index is UNDEF:
            
            # get from glyph
            annotation.z_index = annotation.glyph.z_index
            
            # get next
            if annotation.z_index is UNDEF:
                current = [obj.z_index for obj in self.annotations]
                annotation.z_index = 1 + max([ANNOTS_Z]+current)
        
        # get axes
        x_axis = self.get_obj(x_axis) if x_axis else UNDEF
        y_axis = self.get_obj(y_axis) if y_axis else UNDEF
        
        # register object
        self.add(annotation)
        
        # map axes
        self.map(annotation, 'x_scale', x_axis, 'scale')
        self.map(annotation, 'y_scale', y_axis, 'scale')
        
        return annotation
    
    
    def scatter(self, x_axis='x_axis', y_axis='y_axis', **overrides):
        """
        This method provides a convenient way to automatically initialize and
        plot data using perrot.Scatter series.
        
        Args:
            x_axis: str or perrot.plot.Axis
                X-axis tag or the axis itself.
            
            y_axis: str or perrot.plot.Axis
                Y-axis tag or the axis itself.
            
            overrides: key:value pairs
                Specific properties to be set to the series.
        
        Returns:
            perrot.Scatter
                Final series object.
        """
        
        # init series
        series = Scatter(**overrides)
        
        # add annotation
        self.plot(series, x_axis=x_axis, y_axis=y_axis)
        
        return series
    
    
    def profile(self, x_axis='x_axis', y_axis='y_axis', **overrides):
        """
        This method provides a convenient way to automatically initialize and
        plot data using perrot.Profile series.
        
        Args:
            x_axis: str or perrot.plot.Axis
                X-axis tag or the axis itself.
            
            y_axis: str or perrot.plot.Axis
                Y-axis tag or the axis itself.
            
            overrides: key:value pairs
                Specific properties to be set to the series.
        
        Returns:
            perrot.Scatter
                Final series object.
        """
        
        # init series
        series = Profile(**overrides)
        
        # add series
        self.plot(series, x_axis=x_axis, y_axis=y_axis)
        
        return series
    
    
    def histogram(self, values, bins, minimum=None, maximum=None, base=None, x_axis='x_axis', y_axis='y_axis', **overrides):
        """
        This method provides a convenient way to calculate and plot histogram
        bars from given data using perrot.Bars series.
        
        Args:
            values: (float,)
                Data from which to calculate the histogram.
            
            bins: int or (float,)
                If integer value is provided, it specifies number of equal bins to
                create using specified range or given data range. If a collection
                of values is provided, it specifies the ranges of individual bins.
            
            minimum: float or None
                Specifies the minimum value to be used for bins calculation. If set
                to None, minimum of given data is used. This value is ignored if
                exact bins definitions is provided.
            
            maximum: float or None
                Specifies the maximum value to be used for bins calculation. If set
                to None, maximum of given data is used. This value is ignored if
                exact bins definitions is provided.
            
            base: int or None
                Specifies logarithm base to create logarithmic bins. This value is
                ignored if exact bins definitions is provided.
                
            x_axis: str or perrot.plot.Axis
                X-axis tag or the axis itself.
            
            y_axis: str or perrot.plot.Axis
                Y-axis tag or the axis itself.
            
            overrides: key:value pairs
                Specific properties to be set to the series.
        
        Returns:
            perrot.Bars
                Final series object.
        """
        
        # calc histogram
        bins, hist, cumsum = calc_histogram(values, bins, minimum, maximum, base)
        
        # init series
        series = Bars(
            top = hist,
            left = bins[:-1],
            right = bins[1:],
            bottom = 0,
            anchor = TOP,
            **overrides)
        
        # add series
        self.plot(series, x_axis=x_axis, y_axis=y_axis)
        
        return series
    
    
    def cumsum(self, values, bins, minimum=None, maximum=None, base=None, normalize=True, x_axis='x_axis', y_axis='y_axis', **overrides):
        """
        This method provides a convenient way to calculate and plot histogram
        cumulative sum from given data using perrot.Profile series.
        
        Args:
            values: (float,)
                Data from which to calculate the histogram.
            
            bins: int or (float,)
                If integer value is provided, it specifies number of equal bins to
                create using specified range or given data range. If a collection
                of values is provided, it specifies the ranges of individual bins.
            
            minimum: float or None
                Specifies the minimum value to be used for bins calculation. If set
                to None, minimum of given data is used. This value is ignored if
                exact bins definitions is provided.
            
            maximum: float or None
                Specifies the maximum value to be used for bins calculation. If set
                to None, maximum of given data is used. This value is ignored if
                exact bins definitions is provided.
            
            base: int or None
                Specifies logarithm base to create logarithmic bins. This value is
                ignored if exact bins definitions is provided.
            
            normalize: bool
                If set to True, the histogram will be normalized to 100 %.
            
            x_axis: str or perrot.plot.Axis
                X-axis tag or the axis itself.
            
            y_axis: str or perrot.plot.Axis
                Y-axis tag or the axis itself.
            
            overrides: key:value pairs
                Specific properties to be set to the series.
        
        Returns:
            perrot.Profile
                Final series object.
        """
        
        # calc histogram
        bins, hist, cumsum = calc_histogram(values, bins, minimum, maximum, base)
        
        # normalize
        if normalize:
            cumsum = cumsum / len(values) * 100
        
        # set default steps
        if "steps" not in overrides:
            overrides["steps"] = BEFORE
        
        # set data according to steps
        if overrides["steps"] == MIDDLE:
            x = 0.5*(bins[:-1] + bins[1:])
            y = cumsum
        
        else:
            x = bins
            y = [0] + list(cumsum)
        
        # init series
        series = Profile(
            x = x,
            y = y,
            **overrides)
        
        # add series
        self.plot(series, x_axis=x_axis, y_axis=y_axis)
        
        return series
    
    
    def band(self, x_axis='x_axis', y_axis='y_axis', **overrides):
        """
        This method provides a convenient way to automatically initialize and
        plot data using perrot.Band series.
        
        Args:
            x_axis: str or perrot.plot.Axis
                X-axis tag or the axis itself.
            
            y_axis: str or perrot.plot.Axis
                Y-axis tag or the axis itself.
            
            overrides: key:value pairs
                Specific properties to be set to the series.
        
        Returns:
            perrot.Scatter
                Final series object.
        """
        
        # init series
        series = Band(**overrides)
        
        # add series
        self.plot(series, x_axis=x_axis, y_axis=y_axis)
        
        return series
    
    
    def rects(self, x_axis='x_axis', y_axis='y_axis', **overrides):
        """
        This method provides a convenient way to automatically initialize and
        plot data using perrot.Rects series.
        
        Args:
            x_axis: str or perrot.plot.Axis
                X-axis tag or the axis itself.
            
            y_axis: str or perrot.plot.Axis
                Y-axis tag or the axis itself.
            
            overrides: key:value pairs
                Specific properties to be set to the series.
        
        Returns:
            perrot.Scatter
                Final series object.
        """
        
        # init series
        series = Rects(**overrides)
        
        # add series
        self.plot(series, x_axis=x_axis, y_axis=y_axis)
        
        return series
    
    
    def bars(self, x_axis='x_axis', y_axis='y_axis', **overrides):
        """
        This method provides a convenient way to automatically initialize and
        plot data using perrot.Bars series.
        
        Args:
            x_axis: str or perrot.plot.Axis
                X-axis tag or the axis itself.
            
            y_axis: str or perrot.plot.Axis
                Y-axis tag or the axis itself.
            
            overrides: key:value pairs
                Specific properties to be set to the series.
        
        Returns:
            perrot.Scatter
                Final series object.
        """
        
        # init series
        series = Bars(**overrides)
        
        # add series
        self.plot(series, x_axis=x_axis, y_axis=y_axis)
        
        return series
    
    
    def hbars(self, x_axis='x_axis', y_axis='y_axis', **overrides):
        """
        This method provides a convenient way to automatically initialize and
        plot data using perrot.HBars series.
        
        Args:
            x_axis: str or perrot.plot.Axis
                X-axis tag or the axis itself.
            
            y_axis: str or perrot.plot.Axis
                Y-axis tag or the axis itself.
            
            overrides: key:value pairs
                Specific properties to be set to the series.
        
        Returns:
            perrot.Scatter
                Final series object.
        """
        
        # init series
        series = HBars(**overrides)
        
        # add series
        self.plot(series, x_axis=x_axis, y_axis=y_axis)
        
        return series
    
    
    def vbars(self, x_axis='x_axis', y_axis='y_axis', **overrides):
        """
        This method provides a convenient way to automatically initialize and
        plot data using perrot.VBars series.
        
        Args:
            x_axis: str or perrot.plot.Axis
                X-axis tag or the axis itself.
            
            y_axis: str or perrot.plot.Axis
                Y-axis tag or the axis itself.
            
            overrides: key:value pairs
                Specific properties to be set to the series.
        
        Returns:
            perrot.Scatter
                Final series object.
        """
        
        # init series
        series = VBars(**overrides)
        
        # add series
        self.plot(series, x_axis=x_axis, y_axis=y_axis)
        
        return series
    
    
    def textbox(self, text, x, y, x_offset=5, y_offset=-5, x_axis='x_axis', y_axis='y_axis', tag=UNDEF, **overrides):
        """
        This method provides a convenient way to add a text box annotation
        to current chart and assign specified axes scales, so that the
        annotation is automatically scaled/positioned to device coordinates.
        
        Args:
            text: str
                Text to show.
            
            x: float
                X-coordinate of the text box anchor in data units.
            
            y: float
                Y-coordinate of the text box anchor in data units.
            
            x_offset: int or float
                Specifies the additional shift in device units to be applied to
                x-coordinate.
            
            y_offset: int or float
                Specifies the additional shift in device units to be applied to
                y-coordinate.
            
            x_axis: str or perrot.Axis
                X-axis tag or the axis itself.
            
            y_axis: str or perrot.Axis
                Y-axis tag or the axis itself.
            
            tag: str
                Unique tag to be assigned to the annotation.
            
            overrides: key:value pairs
                Specific properties to be set additionally to the text box.
        
        Returns:
            perrot.Annotation
                Final annotation object.
        """
        
        # set defaults
        if 'text_color' not in overrides:
            overrides['text_color'] = colors.Gray
        
        if 'text_align' not in overrides:
            overrides['text_align'] = LEFT
        
        if 'text_base' not in overrides:
            overrides['text_base'] = BOTTOM
        
        if 'line_color' not in overrides:
            overrides['line_color'] = colors.DarkGray
        
        if 'fill_color' not in overrides:
            overrides['fill_color'] = colors.White
        
        if 'fill_alpha' not in overrides:
            overrides['fill_alpha'] = 200
        
        if 'radius' not in overrides:
            overrides['radius'] = 3
        
        # init props
        x_props = ('x',)
        y_props = ('y',)
        
        # set coordinates by constants
        if x == POS_LEFT:
            x = lambda _: self._data_frame.x1 + x_offset
            x_props = UNDEF
        
        elif x == POS_RIGHT:
            x = lambda _: self._data_frame.x2 + x_offset
            x_props = UNDEF
        
        if y == POS_TOP:
            y = lambda _: self._data_frame.y1 + y_offset
            y_props = UNDEF
        
        elif y == POS_BOTTOM:
            y = lambda _: self._data_frame.y2 + y_offset
            y_props = UNDEF
        
        # init glyph
        glyph = Textbox(
            x = x,
            y = y,
            text = text,
            **overrides)
        
        # init annotation
        annotation = Annotation(
            glyph = glyph,
            x_props = x_props,
            y_props = y_props,
            x_offset = x_offset,
            y_offset = y_offset,
            tag = tag)
        
        # add annotation
        return self.annotate(annotation, x_axis=x_axis, y_axis=y_axis)
    
    
    def text(self, text, x, y, x_offset=5, y_offset=-5, x_axis='x_axis', y_axis='y_axis', tag=UNDEF, **overrides):
        """
        This method provides a convenient way to add a simple text annotation
        to current chart and assign specified axes scales, so that the
        annotation is automatically scaled/positioned to device coordinates.
        
        Args:
            text: str
                Text to show.
            
            x: float
                X-coordinate of the text box anchor in data units.
            
            y: float
                Y-coordinate of the text box anchor in data units.
            
            x_offset: int or float
                Specifies the additional shift in device units to be applied to
                x-coordinate.
            
            y_offset: int or float
                Specifies the additional shift in device units to be applied to
                y-coordinate.
            
            x_axis: str or perrot.Axis
                X-axis tag or the axis itself.
            
            y_axis: str or perrot.Axis
                Y-axis tag or the axis itself.
            
            tag: str
                Unique tag to be assigned to the annotation.
            
            overrides: key:value pairs
                Specific properties to be set additionally to the text.
            
        Returns:
            perrot.Annotation
                Final annotation object.
        """
        
        # set defaults
        if 'text_color' not in overrides:
            overrides['text_color'] = colors.Gray
        
        if 'text_align' not in overrides:
            overrides['text_align'] = LEFT
        
        if 'text_base' not in overrides:
            overrides['text_base'] = BOTTOM
        
        # init props
        x_props = ('x',)
        y_props = ('y',)
        
        # set coordinates by constants
        if x == POS_LEFT:
            x = lambda _: self._data_frame.x1 + x_offset
            x_props = UNDEF
        
        elif x == POS_RIGHT:
            x = lambda _: self._data_frame.x2 + x_offset
            x_props = UNDEF
        
        if y == POS_TOP:
            y = lambda _: self._data_frame.y1 + y_offset
            y_props = UNDEF
        
        elif y == POS_BOTTOM:
            y = lambda _: self._data_frame.y2 + y_offset
            y_props = UNDEF
        
        # init glyph
        glyph = Text(
            x = x,
            y = y,
            text = text,
            **overrides)
        
        # init annotation
        annotation = Annotation(
            glyph = glyph,
            x_props = x_props,
            y_props = y_props,
            x_offset = x_offset,
            y_offset = y_offset,
            tag = tag)
        
        # add annotation
        return self.annotate(annotation, x_axis=x_axis, y_axis=y_axis)
    
    
    def marker(self, x, y, marker='o', x_axis='x_axis', y_axis='y_axis', tag=UNDEF, **overrides):
        """
        This method provides a convenient way to add a marker annotation
        to current chart and assign specified axes scales, so that the
        annotation is automatically scaled/positioned to device coordinates.
        
        Args:
            x: float
                X-coordinate of the marker in data units.
            
            y: float
                Y-coordinate of the marker in data units.
            
            x_axis: str or perrot.Axis
                X-axis tag or the axis itself.
            
            y_axis: str or perrot.Axis
                Y-axis tag or the axis itself.
            
            tag: str
                Unique tag to be assigned to the annotation.
            
            overrides: key:value pairs
                Specific properties to be set additionally to the marker.
        
        Returns:
            perrot.Annotation
                Final annotation object.
        """
        
        # set defaults
        if 'size' not in overrides:
            overrides['size'] = 7
        
        if 'line_color' not in overrides:
            overrides['line_color'] = colors.DarkGray
        
        if 'fill_color' not in overrides:
            overrides['fill_color'] = colors.DarkGray
        
        # init glyph
        glyph = Marker.create(
            marker,
            x = x,
            y = y,
            **overrides)
        
        # init annotation
        annotation = Annotation(
            glyph = glyph,
            x_props = ('x',),
            y_props = ('y',),
            tag = tag)
        
        # add annotation
        return self.annotate(annotation, x_axis=x_axis, y_axis=y_axis)
    
    
    def line(self, p1, p2, full_scale=False, x_axis='x_axis', y_axis='y_axis', tag=UNDEF, **overrides):
        """
        This method provides a convenient way to add a line annotation
        to current chart and assign specified axes scales, so that the
        annotation is automatically scaled/positioned to device coordinates.
        
        Args:
            p1: (float, float)
                Coordinates of the first line point in data units.
            
            p2: (float, float)
                Coordinates of the second line point in data units.
            
            full_scale: bool
                If set to True, the line will always be drawn using full axes
                range. If set to False, only the line between specified points
                will be drawn.
            
            x_axis: str or perrot.Axis
                X-axis tag or the axis itself.
            
            y_axis: str or perrot.Axis
                Y-axis tag or the axis itself.
            
            tag: str
                Unique tag to be assigned to the annotation.
            
            overrides: key:value pairs
                Specific properties to be set additionally to the line.
        
        Returns:
            perrot.Annotation
                Final annotation object.
        """
        
        if 'line_color' not in overrides:
            overrides['line_color'] = colors.DarkGray
        
        # get axes
        x_axis = self.get_obj(x_axis)
        y_axis = self.get_obj(y_axis)
        
        # draw line between points
        if not full_scale:
            
            # init glyph
            glyph = Line(
                x1 = p1[0],
                x2 = p2[0],
                y1 = p1[1],
                y2 = p2[1],
                **overrides)
            
            # init annotation
            annotation = Annotation(glyph=glyph, x_props=('x1', 'x2'), y_props=('y1', 'y2'), tag=tag)
        
        # draw line full range
        else:
            
            # calc line
            a = (p2[1] - p1[1]) / (p2[0] - p1[0])
            b = p1[1] - a * p1[0]
            
            # init glyph
            glyph = Line(
                x1 = lambda _: self._data_frame.x1,
                x2 = lambda _: self._data_frame.x2,
                y1 = lambda _: a*x_axis.scale.in_range[0] + b,
                y2 = lambda _: a*x_axis.scale.in_range[1] + b,
                **overrides)
            
            # init annotation
            annotation = Annotation(glyph=glyph, y_props=('y1', 'y2'), tag=tag)
        
        # add annotation
        return self.annotate(annotation, x_axis=x_axis, y_axis=y_axis)
    
    
    def vline(self, x, axis='x_axis', tag=UNDEF, **overrides):
        """
        This method provides a convenient way to add a vertical line annotation
        to current chart and assign specified axes scales, so that the
        annotation is automatically scaled/positioned to device coordinates.
        
        Args:
            x: float
                X-coordinate of the line in data units.
            
            axis: str or perrot.Axis
                X-axis tag or the axis itself.
            
            tag: str
                Unique tag to be assigned to the annotation.
            
            overrides: key:value pairs
                Specific properties to be set additionally to the line.
        
        Returns:
            perrot.Annotation
                Final annotation object.
        """
        
        # get axis
        axis = self.get_obj(axis)
        
        # init glyph
        glyph = Line(
            x1 = x,
            x2 = x,
            y1 = lambda _: self._data_frame.y1,
            y2 = lambda _: self._data_frame.y2,
            **overrides)
        
        # init annotation
        annotation = Annotation(glyph=glyph, x_props=('x1', 'x2'), tag=tag)
        
        # add annotation
        return self.annotate(annotation, x_axis=axis, y_axis=UNDEF)
    
    
    def hline(self, y, axis='y_axis', tag=UNDEF, **overrides):
        """
        This method provides a convenient way to add a horizontal line
        annotation to current chart and assign specified axes scales, so that
        the annotation is automatically scaled/positioned to device coordinates.
        
        Args:
            y: float
                Y-coordinate of the line in data units.
            
            axis: str or perrot.Axis
                Y-axis tag or the axis itself.
            
            tag: str
                Unique tag to be assigned to the annotation.
            
            overrides: key:value pairs
                Specific properties to be set additionally to the line.
        
        Returns:
            perrot.Annotation
                Final annotation object.
        """
        
        # get axis
        axis = self.get_obj(axis)
        
        # init glyph
        glyph = Line(
            x1 = lambda _: self._data_frame.x1,
            x2 = lambda _: self._data_frame.x2,
            y1 = y,
            y2 = y,
            **overrides)
        
        # init annotation
        annotation = Annotation(glyph=glyph, y_props=('y1', 'y2'), tag=tag)
        
        # add annotation
        return self.annotate(annotation, x_axis=UNDEF, y_axis=axis)
    
    
    def bar(self, left, right, top, bottom, x_axis='x_axis', y_axis='y_axis', tag=UNDEF, **overrides):
        """
        This method provides a convenient way to add a bar annotation
        to current chart and assign specified axes scales, so that the
        annotation is automatically scaled/positioned to device coordinates.
        
        Args:
            left: float
                X-coordinate of the bar left position in data units.
            
            right: float
                X-coordinate of the bar right position in data units.
            
            top: float
                Y-coordinate of the bar top position in data units.
            
            bottom: float
                Y-coordinate of the bar bottom position in data units.
            
            x_axis: str or perrot.Axis
                X-axis tag or the axis itself.
            
            y_axis: str or perrot.Axis
                Y-axis tag or the axis itself.
            
            tag: str
                Unique tag to be assigned to the annotation.
            
            overrides: key:value pairs
                Specific properties to be set additionally to the band.
            
        Returns:
            perrot.Bar
                Final annotation object.
        """
        
        # update overrides
        if 'line_color' not in overrides:
            overrides['line_color'] = None
        
        # init props
        x_props = ['left', 'right']
        y_props = ['top', 'bottom']
        
        # set coordinates by constants
        if left == POS_LEFT:
            left = lambda _: self._data_frame.x1
            x_props.remove('left')
        
        if right == POS_RIGHT:
            right = lambda _: self._data_frame.x2
            x_props.remove('right')
        
        if top == POS_TOP:
            top = lambda _: self._data_frame.y1
            y_props.remove('top')
        
        if bottom == POS_BOTTOM:
            bottom = lambda _: self._data_frame.y2
            y_props.remove('bottom')
        
        # init glyph
        glyph = Bar(
            left = left,
            right = right,
            top = top,
            bottom = bottom,
            **overrides)
        
        # init annotation
        annotation = Annotation(
            glyph = glyph,
            x_props = x_props,
            y_props = y_props,
            tag = tag)
        
        # add annotation
        return self.annotate(annotation, x_axis=x_axis, y_axis=y_axis)
    
    
    def vband(self, left, right, axis='x_axis', tag=UNDEF, **overrides):
        """
        This method provides a convenient way to add a vertical band annotation
        to current chart and assign specified axes scales, so that the
        annotation is automatically scaled/positioned to device coordinates.
        
        Args:
            left: float
                X-coordinate of the band left position in data units.
            
            right: float
                X-coordinate of the band right position in data units.
            
            axis: str or perrot.Axis
                X-axis tag or the axis itself.
            
            tag: str
                Unique tag to be assigned to the annotation.
            
            overrides: key:value pairs
                Specific properties to be set additionally to the band.
        
        Returns:
            perrot.Annotation
                Final annotation object.
        """
        
        return self.bar(
            left = left,
            right = right,
            top = POS_TOP,
            bottom = POS_BOTTOM,
            x_axis = axis,
            y_axis = UNDEF,
            tag = tag,
            **overrides)
    
    
    def hband(self, top, bottom, axis='y_axis', tag=UNDEF, **overrides):
        """
        This method provides a convenient way to add a horizontal band annotation
        to current chart and assign specified axes scales, so that the
        annotation is automatically scaled/positioned to device coordinates.
        
        Args:
            top: float
                Y-coordinate of the band top position in data units.
            
            bottom: float
                Y-coordinate of the band bottom position in data units.
            
            axis: str or perrot.Axis
                Y-axis tag or the axis itself.
            
            tag: str
                Unique tag to be assigned to the annotation.
            
            overrides: key:value pairs
                Specific properties to be set additionally to the band.
        
        Returns:
            perrot.Annotation
                Final annotation object.
        """
        
        return self.bar(
            left = POS_LEFT,
            right = POS_RIGHT,
            top = top,
            bottom = bottom,
            x_axis = UNDEF,
            y_axis = axis,
            tag = tag,
            **overrides)
    
    
    def zoom(self, axis=None, minimum=None, maximum=None, propagate=True):
        """
        Sets given range to specific axis.
        
        If 'axis' is set to None, given range will be applied to all axes.
        This make only sense if minimum and maximum are both set to None, so all
        the axes will be set to cover full range of connected data series.
        
        If minimum or maximum is set to None, the value will be set by minimum
        or maximum value to cover full range of connected data series.
        
        Args:
            axis: str, perrot.Axis or None
                Unique tag of the axis or the axis itself.
            
            minimum: float or None
                Minimum value to be set.
            
            maximum: float or None
                Maximum value to be set.
            
            propagate: bool
                If set to True, dependent axes will be zoomed accordingly.
        """
        
        # zoom all axes
        if axis is None:
            axes = list(self.axes)
        
        # zoom specified axis
        else:
            axis = self.get_obj(axis)
            axes = [axis]
        
        # sort axes by level
        axes.sort(key=lambda a: a.level)
        
        # set axes
        for item in axes:
            
            # init limits
            lo, hi = minimum, maximum
            
            # get limits from series
            if lo is None and hi is None:
                lo, hi = self._get_series_limits(item)
            
            # use current axis limits
            if lo is None:
                lo = item.scale.in_range[0]
            if hi is None:
                hi = item.scale.in_range[1]
            
            # finalize axis
            self.finalize_axis(item, lo, hi)
        
        # propagate main axis change
        if propagate and axis is not None:
            self.finalize_zoom(axis)
    
    
    def finalize_zoom(self, *axes):
        """
        For each given axis this method finalizes all related axes according to
        individual settings. This mainly ensures the axes autoscaling.
        
        Args:
            axes: (str,) or (perrot.Axis,)
                Unique tags of the axes or the axes itself.
        """
        
        # get unique axes
        axes = list({self.get_obj(a) for a in axes})
        changed = {a.tag for a in axes}
        
        # process each axis
        for axis in axes:
            
            # process dependent axes
            for child in self._get_child_axes(axis):
                
                # skip processed
                if child.tag in changed:
                    continue
                
                # skip independent
                if child.static or not child.autoscale:
                    continue
                
                # remember axis
                changed.add(child)
                
                # get parent axes
                parents = self._get_parent_axes(child)
                if not parents:
                    continue
                
                # init ranges
                x_range = None
                y_range = None
                
                # get ranges from parents
                for parent in parents:
                    if parent.position in POSITION_TB:
                        x_range = parent.scale.in_range
                    elif parent.position in POSITION_LR:
                        y_range = parent.scale.in_range
                
                # get axis limits
                start, end = self._get_series_limits(child, x_range, y_range, exact=False)
                
                # finalize axis
                self.finalize_axis(child, start, end)
    
    
    def finalize_axis(self, axis, start, end):
        """
        Finalizes and sets range for given axis according to its settings. This
        ensures specified limits, margins, symmetry etc.
        
        Args:
            axis: str or perrot.Axis
                Unique tag of the axis or the axis itself.
            
            start: float or None
                Start value to be set.
            
            end: float or None
                End value to be set.
        """
        
        # get axis
        axis = self.get_obj(axis)
        
        # get range from series
        range_min, range_max = self._get_series_limits(axis.tag)
        
        # use full range if not set
        if start is None or end is None:
            start = range_min
            end = range_max
        
        # check range
        if start is None or end is None:
            start = axis.empty_range[0]
            end = axis.empty_range[1]
        
        # check data limits
        if axis.check_limits and range_min is not None and range_max is not None:
            
            if start < range_min and end > range_max:
                start = range_min
                end = range_max
            
            elif start < range_min:
                shift = range_min - start
                start += shift
                end += shift
            
            elif end > range_max:
                shift = end - range_max
                start -= shift
                end -= shift
        
        # check required values
        if axis.includes:
            
            incl_min = min(axis.includes)
            incl_max = max(axis.includes)
            
            if start > incl_min:
                start = incl_min
            
            if end < incl_max:
                end = incl_max
        
        # check range
        if start == end and start == 0:
            end = 1.
        
        # check symmetry
        if axis.symmetric:
            maximum = max(abs(start), abs(end))
            start, end = -maximum, maximum
        
        # check range
        if start == end:
            start -= 0.1*start
            end += 0.1*end
        
        # apply to axis
        axis.scale.in_range = (start, end)
    
    
    def view(self, title=None, width=None, height=None, backend=None, **options):
        """
        Shows current plot as interactive viewer app.
        
        Note that is just a convenient scripting shortcut and this method cannot
        be used if the plot is already part of any UI app.
        
        Args:
            title: str or None
                Viewer frame title. If set to None, current plot title is used.
            
            width: float or None
                Image width in device units. If set to None, current plot width
                is used.
            
            height: float or None
                Image height in device units. If set to None, current plot
                height is used.
            
            backend: pero.BACKEND or None
                Specific backend to be used. The value must be an item from the
                pero.BACKEND enum.
            
            options: str:any pairs
                Additional parameters for specific backend.
        """
        
        # get size
        if width is None:
            width = self.width
        if height is None:
            height = self.height
        
        # init control
        from .. interact import PlotControl
        control = PlotControl(graphics=self)
        
        # show viewer
        control.show(title, width, height, backend, **options)
    
    
    def _get_related_axes(self, obj):
        """Gets the axes associated with specified object."""
        
        axes = []
        
        # get object
        obj = self.get_obj(obj)
        
        # get object mapping
        mappings = self._mapping.get(obj.tag, None)
        if mappings is None:
            return axes
        
        # get axes from mapping
        for src, _ in mappings.values():
            src = self.get_obj(src)
            if isinstance(src, Axis):
                axes.append(src)
        
        return axes
    
    
    def _get_parent_axes(self, axis):
        """Gets related axes with higher level (smaller value)."""
        
        parents = set()
        
        # get axis
        axis = self.get_obj(axis)
        
        # check series
        for series in self.series:
            
            # ignore invisible
            if not series.visible:
                continue
            
            # get related axes
            related = self._get_related_axes(series)
            if axis not in related:
                continue
            
            # get parents
            for item in related:
                if item.level < axis.level:
                    parents.add(item)
        
        return parents
    
    
    def _get_child_axes(self, axis):
        """Gets related axes with lower level (bigger value)."""
        
        children = set()
        
        # get axis
        axis = self.get_obj(axis)
        
        # check series
        for series in self.series:
            
            # ignore invisible
            if not series.visible:
                continue
            
            # get related axes
            related = self._get_related_axes(series)
            if axis not in related:
                continue
            
            # get parents
            for item in related:
                if item.level > axis.level:
                    children.add(item)
        
        return children
    
    
    def _get_series_limits(self, axis, x_range=None, y_range=None, exact=False):
        """
        Gets minimum and maximum value from all visible series connected to
        specified axis.
        """
        
        minimum = None
        maximum = None
        
        # get axis
        axis = self.get_obj(axis)
        
        # add series
        for series in self.series:
            
            # skip invisible
            if not series.visible:
                continue
            
            # get related axes
            related = self._get_related_axes(series)
            if axis not in related:
                continue
            
            # get series limits
            limits = series.get_limits(x_range=x_range, y_range=y_range, exact=exact)
            if limits is None:
                continue
            
            # get limits for correct dimension
            limits = limits[0] if axis.position in POSITION_TB else limits[1]
            if limits is None:
                continue
            
            # update range
            lo, hi = limits
            if minimum is None or lo < minimum:
                minimum = lo
            if maximum is None or hi > maximum:
                maximum = hi
        
        return minimum, maximum
    
    
    def _init_graphics(self):
        """Initializes and registers required graphics."""
        
        # register objects
        if self.title:
            self.add(self.title)
        
        if self.legend:
            self.add(self.legend)
        
        if self.labels:
            self.add(self.labels)
        
        if self.x_axis:
            self.add(self.x_axis)
        
        if self.x_major_grid:
            self.add(self.x_major_grid)
            self.map(self.x_major_grid, 'scale', self.x_axis, 'scale')
            self.map(self.x_major_grid, 'ticker', self.x_axis, 'ticker')
        
        if self.x_minor_grid:
            self.add(self.x_minor_grid)
            self.map(self.x_minor_grid, 'scale', self.x_axis, 'scale')
            self.map(self.x_minor_grid, 'ticker', self.x_axis, 'ticker')
        
        if self.y_axis:
            self.add(self.y_axis)
        
        if self.y_major_grid:
            self.add(self.y_major_grid)
            self.map(self.y_major_grid, 'scale', self.y_axis, 'scale')
            self.map(self.y_major_grid, 'ticker', self.y_axis, 'ticker')
        
        if self.y_minor_grid:
            self.add(self.y_minor_grid)
            self.map(self.y_minor_grid, 'scale', self.y_axis, 'scale')
            self.map(self.y_minor_grid, 'ticker', self.y_axis, 'ticker')
    
    
    def _init_colors(self):
        """Initializes default color scale."""
        
        # init color scale
        self._colors = OrdinalScale(
            out_range = self.palette or colors.Pero,
            implicit = True,
            recycle = True)
    
    
    def _on_plot_property_changed(self, evt):
        """Called after any property has changed."""
        
        # color palette changed
        if evt.name == 'palette':
            self._init_colors()
        
        # main objects
        if evt.name in ('title', 'legend', 'labels', 'x_axis', 'x_major_grid', 'x_minor_grid', 'y_axis', 'y_major_grid', 'y_minor_grid'):
            
            # remove old
            if evt.old_value:
                self.remove(evt.old_value.tag)
            
            # register new
            if evt.new_value:
                self.add(evt.new_value)
