#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from pero.properties import *
from pero import Graphics, Path, Frame, Framer
from pero import OrdinalScale
from pero import colors

from .. enums import *
from . graphics import InGraphics, OutGraphics


class ChartBase(Graphics):
    """
    ChartBase provides a base for different types of charts.
    
    Properties:
        
        x: int or float
            Specifies the x-coordinate of the top-left corner
        
        y: int or float
            Specifies the y-coordinate of the top-left corner
        
        width: int, float or UNDEF
            Specifies the full chart width. If set to UNDEF the full area of
            given canvas is used.
        
        height: int, float or UNDEF
            Specifies the full chart height. If set to UNDEF the full area of
            given canvas is used.
        
        padding: int, float or tuple
            Specifies the inner space of the chart as a single value or values
            for individual sides starting from top.
        
        frame_x1: int, float or UNDEF
            Specifies the fixed x-coordinate of the left edge of the inside
            data frame. If not provided it is determined automatically by chart
            graphics.
        
        frame_x2: int, float or UNDEF
            Specifies the fixed x-coordinate of the right edge of the inside
            data frame. If not provided it is determined automatically by chart
            graphics.
        
        frame_y1: int, float or UNDEF
            Specifies the fixed y-coordinate of the top edge of the inside
            data frame. If not provided it is determined automatically by chart
            graphics.
        
        frame_y2: int, float or UNDEF
            Specifies the fixed y-coordinate of the bottom edge of the inside
            data frame. If not provided it is determined automatically by chart
            graphics.
        
        frame_line properties:
            Includes pero.LineProperties to specify the data frame outline.
        
        frame_fill properties:
            Includes pero.FillProperties to specify the data frame fill.
        
        frame_radius: int, float, (int,), (float,) or UNDEF
            Specifies the corner radius of the data frame as a single value
            or values for individual corners starting from top-left.
        
        bgr_line properties:
            Includes pero.LineProperties to specify the full chart outline.
        
        bgr_fill properties:
            Includes pero.FillProperties to specify the full chart fill.
        
        bgr_radius: int, float, (int,), (float,) or UNDEF
            Specifies the corner radius of the full chart box as a single value
            or values for individual corners starting from top-left.
    """
    
    x = NumProperty(0, dynamic=False)
    y = NumProperty(0, dynamic=False)
    width = NumProperty(UNDEF, dynamic=False)
    height = NumProperty(UNDEF, dynamic=False)
    padding = QuadProperty(10, dynamic=False)
    
    frame_x1 = NumProperty(UNDEF)
    frame_x2 = NumProperty(UNDEF)
    frame_y1 = NumProperty(UNDEF)
    frame_y2 = NumProperty(UNDEF)
    
    frame_line = Include(LineProperties, prefix="frame_", dynamic=False, line_width=0)
    frame_fill = Include(FillProperties, prefix="frame_", dynamic=False)
    frame_radius = QuadProperty(UNDEF, dynamic=False)
    
    bgr_line = Include(LineProperties, prefix="bgr_", dynamic=False, line_width=0)
    bgr_fill = Include(FillProperties, prefix="bgr_", dynamic=False, fill_color="#fff")
    bgr_radius = QuadProperty(UNDEF, dynamic=False)
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of the ChartBase."""
        
        # init base
        super().__init__(**overrides)
        
        # init containers
        self._graphics = {}  # {tag, obj}
        self._mapping = {}  # {dst_tag: {dst_prop: (src_tag, src_prop)}}
        
        # init frames
        self._chart_frame = Frame(0, 0, 1, 1)
        self._data_frame = Frame(0, 0, 1, 1)
    
    
    @property
    def graphics(self):
        """
        Gets all registered graphics.
        
        Returns:
            (pero.Graphics,)
                Registered graphics.
        """
        
        return tuple(self._graphics.values())
    
    
    def get_frame(self, tag=DATA_FRAME, silent=False):
        """
        Gets logical frame of an object specified by given tag.
        
        Args:
            tag: str
                Object's unique tag.
            
            silent: bool
                If set to True, no error message is shown for unknown objects
                and None is returned.
        
        Returns:
            pero.Frame or None
                Bounding box of specified object or None if object not known.
        """
        
        # main frames
        if tag == CHART_FRAME:
            return self._chart_frame
        
        if tag == DATA_FRAME:
            return self._data_frame
        
        # object frame
        obj = self.get_obj(tag, silent)
        return obj.frame if obj is not None else None
    
    
    def get_obj(self, tag, silent=False):
        """
        Gets object for given tag.
        
        Args:
            tag: str
                Object's unique tag.
            
            silent: bool
                If set to True, no error message is shown for unknown objects
                and None is returned.
        
        Returns:
            pero.Graphics or None
                Requested object or None if not available.
        """
        
        # get object tag
        tag = tag.tag if isinstance(tag, Graphics) else tag
        
        # get object
        obj = self._graphics.get(tag, None)
        
        # check if known
        if obj is None and not silent:
            message = "Cannot find the object by tag '%s'!" % tag
            raise KeyError(message)
        
        return obj
    
    
    def get_obj_below(self, x, y):
        """
        Gets the top-most object for which given coordinates fall into its
        logical frame.
        
        Note that this method only checks the objects positioned outside the
        main data frame. If given position is anywhere inside data frame, the
        perrot.DATA_FRAME constant is returned.
        
        Args:
            x: int or float
                X-coordinate of the point.
            
            y: int or float
                Y-coordinate of the point.
        
        Returns:
            pero.Graphics, str or None
                Corresponding object, perrot.DATA_FRAME or None.
        """
        
        # check data frame first
        if self._data_frame.contains(x, y):
            return DATA_FRAME
        
        # get all matching objects
        objects = [o for o in self._graphics.values() if o.frame.contains(x, y)]
        if not objects:
            return None
        
        # sort by z-axis
        objects.sort(key=lambda d: d.z_index, reverse=True)
        
        return objects[0]
    
    
    def add(self, obj):
        """
        Adds additional graphics to the chart.
        
        This method only serves to register a new object. Consider overriding in
        derived classes to perform any required checks and initializations and
        call this base method inside.
        
        Args:
            obj: perrot.InGraphics or perrot.OutGraphics
                Object to be added.
        """
        
        # check type
        if not isinstance(obj, (InGraphics, OutGraphics)):
            message = "Object must be of type perrot.InGraphics or perrot.OutGraphics! -> %s" % type(obj)
            raise TypeError(message)
        
        # check tag
        if not obj.tag or obj.tag in self._graphics or obj.tag == DATA_FRAME:
            message = "Object must have unique tag specified."
            raise ValueError(message)
        
        # set z-index
        if obj.z_index is UNDEF:
            z_indices = [0] + [o.z_index for o in self.graphics if o.z_index]
            obj.z_index = max(z_indices) + 1
        
        # register object
        self._graphics[obj.tag] = obj
    
    
    def remove(self, obj):
        """
        Removes specified object.
        
        This method only serves to de-register the object. Consider overriding
        in derived classes to perform any required checks and call this base
        method afterwards.
        
        Args:
            obj: str or pero.Graphics
                Object's unique tag or the object itself.
        """
        
        # get object
        obj = self.get_obj(obj)
        
        # check mapping
        for mapping in self._mapping.values():
            for src in mapping.values():
                if obj.tag == src[0]:
                    message = "Object '%s' is mapped by another object and cannot be removed!" % obj.tag
                    raise ValueError(message)
        
        # remove mapping
        if obj.tag in self._mapping:
            del self._mapping[obj.tag]
        
        # remove object
        del self._graphics[obj.tag]
    
    
    def map(self, obj, obj_prop, src, src_prop):
        """
        Maps object property to specified property of the source. This method is
        mainly used to synchronize scales between data and relevant axis.
        
        Args:
            obj: str
                Object's unique tag.
            
            obj_prop: str
                Object's property name.
            
            src: str
                Source object's unique tag.
            
            src_prop: str
                Source object's property name.
        """
        
        # skip if source undefined
        if not src:
            return
        
        # get objects
        obj = self.get_obj(obj)
        src = self.get_obj(src)
        
        # get mapping
        obj_map = self._mapping.get(obj.tag, {})
        
        # check props
        obj.get_property(obj_prop)
        src.get_property(src_prop)
        
        # set prop
        obj_map[obj_prop] = (src.tag, src_prop)
        
        # update mapping
        self._mapping[obj.tag] = obj_map
    
    
    def draw(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw the chart."""
        
        # check if visible
        if not self.is_visible(source, overrides):
            return
        
        # init objects
        self.init_objects(canvas, source, **overrides)
        
        # draw main bgr
        self.draw_bgr(canvas, source, **overrides)
        
        # refuse to draw if "negative" size
        if self._data_frame.reversed:
            return
        
        # draw data frame fill
        self.draw_frame(canvas, source, frame_line_width=0, **overrides)
        
        # get objects
        objects = list(self._graphics.values())
        objects.sort(key=lambda o: o.z_index)
        in_objects = [o for o in objects if isinstance(o, InGraphics)]
        out_objects = [o for o in objects if isinstance(o, OutGraphics)]
        
        # draw inside objects
        with canvas.clip(Path().rect(*self._data_frame.rect)):
            for obj in in_objects:
                if obj.visible:
                    obj.draw(canvas)
        
        # draw data frame outline
        self.draw_frame(canvas, source, frame_fill_style=TRANS, **overrides)
        
        # draw outside objects
        for obj in out_objects:
            if obj.visible:
                obj.draw(canvas)
        
        # draw debug frames
        # self.draw_debug_frames(canvas, source, **overrides)
    
    
    def draw_bgr(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw the chart background."""
        
        # get properties
        x = self.get_property('x', source, overrides)
        y = self.get_property('y', source, overrides)
        width = self.get_property('width', source, overrides)
        height = self.get_property('height', source, overrides)
        radius = self.get_property('bgr_radius', source, overrides)
        
        # get size from canvas
        if width is UNDEF:
            width = canvas.viewport.width
        if height is UNDEF:
            height = canvas.viewport.height
        
        # draw bgr
        canvas.set_pen_by(self, prefix="bgr_", source=source, overrides=overrides)
        canvas.set_brush_by(self, prefix="bgr_", source=source, overrides=overrides)
        canvas.draw_rect(x, y, width, height, radius)
    
    
    def draw_frame(self, canvas, source=UNDEF, **overrides):
        """Uses given canvas to draw the data frame."""
        
        # get properties
        radius = self.get_property('frame_radius', source, overrides)
        
        # draw frame
        canvas.set_pen_by(self, prefix="frame_", source=source, overrides=overrides)
        canvas.set_brush_by(self, prefix="frame_", source=source, overrides=overrides)
        canvas.draw_rect(*self._data_frame.rect, radius)
    
    
    def draw_debug_frames(self, canvas, source=UNDEF, **overrides):
        """Draws main objects frames (for debugging)."""
        
        # init color scale
        color_scale = OrdinalScale(
            out_range = colors.Pero,
            implicit = True,
            recycle = True)
        
        # init glyph
        glyph = Framer(
            x = lambda d: d.x,
            y = lambda d: d.y,
            width = lambda d: d.width,
            height = lambda d: d.height)
        
        # set pen and brush
        canvas.line_width = 1
        canvas.line_style = LINE_STYLE_SOLID
        canvas.fill_style = FILL_STYLE_SOLID
        
        # draw data frame
        color = color_scale.scale(DATA_FRAME)
        glyph.draw(canvas, self._data_frame,
            label = DATA_FRAME,
            line_color = color,
            fill_color = color.opaque(0.7))
        
        # draw outside frames
        for tag, obj in self._graphics.items():
            
            # skip inside objects
            if not isinstance(obj, OutGraphics):
                continue
            
            # draw frame
            color = color_scale.scale(tag)
            glyph.draw(canvas, obj.frame,
                label = obj.tag,
                line_color = color,
                fill_color = color.opaque(0.7))
    
    
    def init_objects(self, canvas, source=UNDEF, **overrides):
        """Prepares objects to be drawn."""
        
        # get and sort objects
        objects = list(self._graphics.values())
        objects.sort(key=lambda o: o.z_index)
        
        # set mapped properties
        for obj in objects:
            for name, mapping in self._mapping.get(obj.tag, {}).items():
                src = self.get_obj(mapping[0])
                obj.set_property(name, src.get_property(mapping[1]))
        
        # prepare objects
        for obj in objects:
            obj.prepare(self, canvas, source, **overrides)
        
        # init frames
        self.init_frames(canvas, source, **overrides)
        
        # finalize objects
        for obj in objects:
            obj.finalize(self, canvas, source, **overrides)
    
    
    def init_frames(self, canvas, source=UNDEF, **overrides):
        """Calculates and sets objects frames."""
        
        # clean frames
        for obj in self._graphics.values():
            obj.frame = Frame(0, 0, 0, 0)
        
        # get properties
        x = self.get_property('x', source, overrides)
        y = self.get_property('y', source, overrides)
        width = self.get_property('width', source, overrides)
        height = self.get_property('height', source, overrides)
        padding = self.get_property('padding', source, overrides)
        
        frame_x1 = self.get_property('frame_x1', source, overrides)
        frame_x2 = self.get_property('frame_x2', source, overrides)
        frame_y1 = self.get_property('frame_y1', source, overrides)
        frame_y2 = self.get_property('frame_y2', source, overrides)
        
        # get size from canvas
        if width is UNDEF:
            width = canvas.viewport.width
        if height is UNDEF:
            height = canvas.viewport.height
        
        # get and sort objects
        objects = list(self._graphics.values())
        objects.sort(key=lambda o: o.z_index)
        in_objects = [o for o in objects if isinstance(o, InGraphics)]
        out_objects = [o for o in objects if isinstance(o, OutGraphics)]
        
        # init buffers
        left_obj = []
        left_extents = []
        left_margins = [0]
        
        right_obj = []
        right_extents = []
        right_margins = [0]
        
        top_obj = []
        top_extents = []
        top_margins = [0]
        
        bottom_obj = []
        bottom_extents = []
        bottom_margins = [0]
        
        # get extents and margins
        for obj in out_objects:
            
            position = obj.position
            extent = obj.get_extent(canvas) if obj.visible else 0
            margin = obj.margin if (obj.visible and extent) else (0, 0, 0, 0)
            
            if position == POS_LEFT:
                left_obj.append(obj)
                left_extents.append(extent)
                left_margins[-1] = max(margin[1], left_margins[-1])
                left_margins.append(margin[3])
            
            elif position == POS_RIGHT:
                right_obj.append(obj)
                right_extents.append(extent)
                right_margins[-1] = max(margin[3], right_margins[-1])
                right_margins.append(margin[1])
            
            elif position == POS_TOP:
                top_obj.append(obj)
                top_extents.append(extent)
                top_margins[-1] = max(margin[2], top_margins[-1])
                top_margins.append(margin[0])
            
            elif position == POS_BOTTOM:
                bottom_obj.append(obj)
                bottom_extents.append(extent)
                bottom_margins[-1] = max(margin[0], bottom_margins[-1])
                bottom_margins.append(margin[2])
            
            else:
                message = "Unknown position '%s' for '%s' object." % (position, obj.tag)
                raise ValueError(message)
        
        # init inside data frame
        if frame_x1 is UNDEF:
            frame_x1 = x + padding[3] + sum(left_extents) + sum(left_margins[:-1])
        
        if frame_x2 is UNDEF:
            frame_x2 = x - padding[1] + width - sum(right_extents) - sum(right_margins[:-1])
        
        if frame_y1 is UNDEF:
            frame_y1 = y + padding[0] + sum(top_extents) + sum(top_margins[:-1])
        
        if frame_y2 is UNDEF:
            frame_y2 = y - padding[2] + height - sum(bottom_extents) - sum(bottom_margins[:-1])
        
        # set frames
        self._chart_frame = Frame(x, y, width, height)
        self._data_frame = Frame(
            frame_x1,
            frame_y1,
            frame_x2-frame_x1,
            frame_y2-frame_y1)
        
        # make frame for left objects
        shift = self._data_frame.x1 - left_margins[0]
        for i, obj in enumerate(left_obj):
            extent = left_extents[i]
            obj.frame = Frame(shift-extent, self._data_frame.y1, extent, self._data_frame.h)
            if obj.visible:
                shift -= extent + left_margins[i+1]
        
        # make frame for right objects
        shift = self._data_frame.x2 + right_margins[0]
        for i, obj in enumerate(right_obj):
            extent = right_extents[i]
            obj.frame = Frame(shift, self._data_frame.y1, extent, self._data_frame.h)
            if obj.visible:
                shift += extent + right_margins[i+1]
        
        # make frame for top objects
        shift = self._data_frame.y1 - top_margins[0]
        for i, obj in enumerate(top_obj):
            extent = top_extents[i]
            obj.frame = Frame(self._data_frame.x1, shift-extent, self._data_frame.w, extent)
            if obj.visible:
                shift -= extent + top_margins[i+1]
        
        # make frame for bottom objects
        shift = self._data_frame.y2 + bottom_margins[0]
        for i, obj in enumerate(bottom_obj):
            extent = bottom_extents[i]
            obj.frame = Frame(self._data_frame.x1, shift, self._data_frame.w, extent)
            if obj.visible:
                shift += extent + bottom_margins[i+1]
        
        # set data frame to all inside objects
        for obj in in_objects:
            obj.frame = self._data_frame
