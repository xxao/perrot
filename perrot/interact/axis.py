#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import sys
import time

from pero.enums import *
from pero.properties import *
from pero.events import ZoomEvt
from pero import Tool, ToolControl

from .. chart import Axis

# init events
_EVT_SHIFT = 'shift'
_EVT_SCALE = 'scale'


class AxisControl(ToolControl):
    """
    Axis view control provides convenient methods to apply zoom or enable zoom
    undos and sets default interactivity tool.
    """
    
    graphics = Property(None, types=Axis, dynamic=False, nullable=True)
    
    zoom_undo = IntProperty(256, dynamic=False, nullable=False)
    zoom_wait = FloatProperty(0.5, dynamic=False, nullable=False)
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of AxisControl."""
        
        super().__init__(**overrides)
        
        # init buffers
        self._zoom_ranges = []
        self._zoom_time = 0
        
        # save current zoom
        self.save_zoom()
        
        # bind events
        self.bind(EVT_ZOOM, self.on_zoom)
        self.bind(EVT_PROPERTY_CHANGED, self._on_axiscontrol_property_changed)
        
        # init main tool
        if self.main_tool is UNDEF:
            self.main_tool = AxisTool()
    
    
    def on_zoom(self, evt):
        """Handles zoom event."""
        
        # save current zoom
        self.save_zoom()
        
        # redraw plot
        self.refresh()
    
    
    def zoom(self, minimum=None, maximum=None, save=True, silent=True):
        """
        Sets given range to current axis.
        
        Args:
            minimum: float or None
                Minimum value to be set.
            
            maximum: float or None
                Maximum value to be set.
            
            save: bool
                If set to True the new zoom state is saved.
            
            silent: bool
                If set to False, the pero.EVENT.ZOOM event is fired.
        """
        
        # check axis
        if not self.graphics:
            return
        
        # set range
        self.graphics.scale.in_range = (minimum, maximum)
        
        # save current zoom
        if save:
            self.save_zoom()
        
        # fire zoom event
        if not silent:
            
            evt = ZoomEvt(
                native = None,
                view = self._parent,
                control = self)
            
            self.graphics.fire(evt)
    
    
    def zoom_back(self, silent=True):
        """
        Applies previous axis range.
        
        Args:
            silent: bool
                If set to False, the pero.EVENT.ZOOM event is fired.
        """
        
        # check plot
        if not self.graphics:
            return
        
        # check zooms
        if not self._zoom_ranges:
            return
        
        # remove latest (current) if not last
        if len(self._zoom_ranges) > 1:
            del self._zoom_ranges[-1]
        
        # set range
        self.graphics.scale.in_range = self._zoom_ranges[-1]
        
        # fire zoom event
        if not silent:
            
            evt = ZoomEvt(
                native = None,
                view = self._parent,
                control = self)
            
            self.graphics.fire(evt)
    
    
    def save_zoom(self):
        """Remembers current axis range."""
        
        # check axis
        if not self.graphics:
            return
        
        # check last zoom
        if self._zoom_ranges:
            
            # check same ranges
            if self._zoom_ranges[-1] == self.graphics.scale.in_range:
                return
            
            # remove last if too recent (probably scrolling)
            if (time.time() - self._zoom_time) < self.zoom_wait:
                del self._zoom_ranges[-1]
        
        # save current range
        self._zoom_ranges.append(self.graphics.scale.in_range)
        if len(self._zoom_ranges) > self.zoom_undo:
            del self._zoom_ranges[0]
        
        # save time stamp
        self._zoom_time = time.time()
    
    
    def _on_axiscontrol_property_changed(self, evt):
        """Called after any property has changed."""
        
        # plot changed
        if evt.name == 'graphics':
            
            # reset zoom memory
            self._zoom_ranges = []
            self._zoom_time = 0
            
            # save current zoom
            if self.graphics:
                self.save_zoom()


class AxisTool(Tool):
    """
    This tool provides various ways to shift and scale axis by mouse scrolling
    or dragging.
    
    Properties:
        
        reverse_scroll: bool
            Specifies whether the scroll direction should be reversed.
        
        reverse_move: bool
            Specifies whether the keyboard move direction should be reversed.
        
        scroll_factor: float
            Specifies the relative scrolling step.
        
        scale_factor: float
            Specifies the relative scaling multiplier.
        
        move_factor: float
            Specifies the relative keyboard moving step.
    """
    
    reverse_scroll = BoolProperty(UNDEF, dynamic=False)
    reverse_move = BoolProperty(UNDEF, dynamic=False)
    scroll_factor = RangeProperty(UNDEF, minimum=0, maximum=1, dynamic=False)
    scale_factor = RangeProperty(UNDEF, minimum=0, maximum=1, dynamic=False)
    move_factor = RangeProperty(0.1, minimum=0, maximum=1, dynamic=False)
    
    
    def __init__(self, **overrides):
        """Initializes a new instance of NavigatorTool."""
        
        # init scrolling
        if 'reverse_scroll' not in overrides:
            overrides['reverse_scroll'] = sys.platform == 'darwin'
        
        if 'scroll_factor' not in overrides:
            overrides['scroll_factor'] = 0.02 if sys.platform == 'darwin' else 0.05
        
        if 'scale_factor' not in overrides:
            overrides['scale_factor'] = 0.02 if sys.platform == 'darwin' else 0.05
        
        # init base
        super().__init__(**overrides)
        
        # init buffers
        self._event = None
        self._dragging = None
    
    
    def on_mouse_leave(self, evt):
        """Handles mouse-leave event."""
        
        # clear keys
        self.clear_keys()
        
        # check if active
        if not self._event:
            return
        
        # cancel current tool event
        self._escape_event(evt)
    
    
    def on_mouse_motion(self, evt):
        """Handles mouse-motion event."""
        
        # no event set
        if not self._event:
            self._set_cursor_by_location(evt)
            return
        
        # shift axis
        if self._event == _EVT_SHIFT:
            self._shift_by_dragging(evt)
            self._dragging = (evt.x_pos, evt.y_pos)
        
        # scale axis
        elif self._event == _EVT_SCALE:
            self._scale_by_dragging(evt)
            self._dragging = (evt.x_pos, evt.y_pos)
        
        # stop event propagation
        evt.cancel()
    
    
    def on_mouse_scroll(self, evt):
        """Handles mouse-scroll wheel event."""
        
        # cancel event if active
        if self._event:
            evt.cancel()
            return
        
        # check rotation
        rotation = evt.y_rot or evt.x_rot
        if not rotation:
            return
        
        # get scroll direction
        direction = -1 if rotation < 0 else 1
        if self.reverse_scroll:
            direction *= -1
        
        # scale axis from cursor position
        if evt.alt_down or evt.ctrl_down:
            self._scale_by_scrolling(evt, direction, True)
        
        # shift axis
        else:
            self._shift_by_scrolling(evt, direction)
        
        # stop event propagation
        evt.cancel()
    
    
    def on_mouse_down(self, evt):
        """Handles mouse-button-down event."""
        
        # check control
        if not evt.control:
            return
        
        # remember dragging origin
        self._dragging = (evt.x_pos, evt.y_pos)
        
        # start axis shift
        if evt.left_down:
            self._event = _EVT_SHIFT
        
        # start axis scale
        elif evt.right_down:
            self._event = _EVT_SCALE
        
        # no event to start
        else:
            return
        
        # stop event propagation
        evt.cancel()
    
    
    def on_mouse_up(self, evt):
        """Handles mouse-button-up event."""
        
        # check if active
        if not self._event:
            return
        
        # cancel event
        self._escape_event(evt)
        
        # stop event propagation
        evt.cancel()
    
    
    def on_touch_move(self, evt):
        """Handles touch-move event."""
        
        # no event set
        if not self._event:
            self._set_cursor_by_location(evt)
            return
        
        # shift axis
        if self._event == _EVT_SHIFT:
            self._shift_by_dragging(evt)
            self._dragging = (evt.x_pos, evt.y_pos)
        
        # scale axis
        elif self._event == _EVT_SCALE:
            self._scale_by_dragging(evt)
            self._dragging = (evt.x_pos, evt.y_pos)
        
        # stop event propagation
        evt.cancel()
    
    
    def on_touch_start(self, evt):
        """Handles touch-start event."""
        
        # check control
        if not evt.control:
            return
        
        # remember dragging origin
        self._dragging = (evt.x_pos, evt.y_pos)
        
        # start axis scale
        if evt.alt_down or evt.ctrl_down:
            self._event = _EVT_SCALE
        
        # start axis shift
        else:
            self._event = _EVT_SHIFT
        
        # stop event propagation
        evt.cancel()
    
    
    def on_touch_end(self, evt):
        """Handles touch-end event."""
        
        # check if active
        if not self._event:
            return
        
        # cancel event
        self._escape_event(evt)
        
        # stop event propagation
        evt.cancel()
    
    
    def _set_cursor_by_location(self, evt):
        """Sets cursor according to axis position."""
        
        # check control
        if not evt.control:
            return
        
        # get axis
        axis = evt.control.graphics
        
        # use up/down arrow for vertical axes
        if axis.position in (POS_LEFT, POS_RIGHT):
            evt.control.set_cursor(CURSOR_SIZENS)
        
        # use left/right arrow for horizontal axes
        elif axis.position in (POS_TOP, POS_BOTTOM):
            evt.control.set_cursor(CURSOR_SIZEWE)
    
    
    def _escape_event(self, evt):
        """Cancels current tool event."""
        
        # cancel current event
        self._event = None
        
        # reset dragging origin
        self._dragging = None
        
        # clear overlay
        if evt.control:
            evt.control.set_cursor(CURSOR_ARROW)
            evt.control.clear_overlay()
    
    
    def _shift_by_scrolling(self, evt, direction):
        """Shifts axis by mouse scrolling."""
        
        # check control
        if not evt.control:
            return
        
        # get axis
        axis = evt.control.graphics
        
        # skip symmetric axis
        if axis.symmetric:
            return
        
        # get factor
        factor = self.scroll_factor * direction
        
        # get shift
        start, end = axis.scale.out_range
        shift = (start - end) * factor
        start += shift
        end += shift
        
        # recalculate range
        start = axis.scale.invert(start)
        end = axis.scale.invert(end)
        
        # apply scale
        axis.zoom(start, end)
        
        # fire zoom event
        evt.control.fire(ZoomEvt.from_evt(evt))
    
    
    def _shift_by_dragging(self, evt):
        """Shifts axis by mouse dragging."""
        
        # check control
        if not evt.control:
            return
        
        # check dragging
        if self._dragging is None:
            self._dragging = (evt.x_pos, evt.y_pos)
            return
        
        # get axis
        axis = evt.control.graphics
        
        # skip symmetric axis
        if axis.symmetric:
            return
        
        # get cursors
        if axis.position in (POS_BOTTOM, POS_TOP):
            drag = self._dragging[0]
            cursor = evt.x_pos
        else:
            drag = self._dragging[1]
            cursor = evt.y_pos
        
        # get shift
        start, end = axis.scale.out_range
        shift = drag - cursor
        start += shift
        end += shift
        
        # recalculate range
        start = axis.scale.invert(start)
        end = axis.scale.invert(end)
        
        # apply scale
        axis.zoom(start, end)
        
        # fire zoom event
        evt.control.fire(ZoomEvt.from_evt(evt))
    
    
    def _scale_by_scrolling(self, evt, direction, from_cursor):
        """Scales axis by mouse scrolling."""
        
        # check control
        if not evt.control:
            return
        
        # get axis
        axis = evt.control.graphics
        
        # get factor
        factor = self.scale_factor * direction
        
        # get current range
        start, end = axis.scale.out_range
        
        # scale symmetric
        if axis.symmetric:
            end += (end - start) * factor
            start = axis.scale.scale(-axis.scale.invert(end))
        
        # scale from cursor
        elif from_cursor:
            
            # get cursor position
            if axis.position in (POS_BOTTOM, POS_TOP):
                cursor = evt.x_pos
            else:
                cursor = evt.y_pos
            
            # get ratio
            ratio = abs((cursor - start) / (end - start))
            
            # apply scaling
            shift = (end - start) * factor
            start -= shift * ratio
            end += shift * (1-ratio)
        
        # scale from start
        else:
            end += (start - end) * factor
        
        # recalculate range
        start = axis.scale.invert(start)
        end = axis.scale.invert(end)
        
        # apply scale
        axis.zoom(start, end)
        
        # fire zoom event
        evt.control.fire(ZoomEvt.from_evt(evt))
    
    
    def _scale_by_dragging(self, evt):
        """Scales axes by mouse dragging."""
        
        # check control
        if not evt.control:
            return
        
        # check dragging
        if self._dragging is None:
            self._dragging = (evt.x_pos, evt.y_pos)
            return
        
        # get axis
        axis = evt.control.graphics
        
        # get cursors
        if axis.position in (POS_BOTTOM, POS_TOP):
            drag = self._dragging[0]
            cursor = evt.x_pos
        else:
            drag = self._dragging[1]
            cursor = evt.y_pos
        
        # get shift
        start, end = axis.scale.out_range
        shift = drag - cursor
        end += shift
        start = -end if axis.symmetric else start
        
        # scale start also
        if axis.symmetric:
            start = axis.scale.scale(-axis.scale.invert(end))
        
        # recalculate range
        start = axis.scale.invert(start)
        end = axis.scale.invert(end)
        
        # apply scale
        axis.zoom(start, end)
        
        # fire zoom event
        evt.control.fire(ZoomEvt.from_evt(evt))
