#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from pero.properties import *
from pero import Graphics

from .. enums import *


class ChartGraphics(Graphics):
    """
    Abstract base class for all graphical components of charts.
    
    Properties:
        
        frame: pero.Frame
            Specifies the logical frame available for the object. Typically,
            this is calculated and set by parent chart.
    """
    
    frame = FrameProperty(UNDEF, dynamic=False)
    
    
    def prepare(self, chart, canvas, source=UNDEF, **overrides):
        """
        This method is automatically called by parent chart to prepare the
        object. It is typically used to retrieve position independent data like
        legends from other objects. Note that the correct 'frame' property is
        not set yet.
        
        This method should be overwritten by derived classed.
        
        Args:
            chart: perrot.ChartBase
                Parent chart.
            
            canvas: pero.Canvas
                Canvas used to draw the graphics.
            
            source: any
                Data source to be used for calculating callable properties.
            
            overrides: str:any pairs
                Specific properties to be overwritten.
        """
        
        pass
    
    
    def finalize(self, chart, canvas, source=UNDEF, **overrides):
        """
        This method is automatically called by parent chart to finalize the
        object. It is typically used to retrieve position dependent data like
        labels from other objects. Note that the correct 'frame' property is set
        already.
        
        This method should be overwritten by derived classed.
        
        Args:
            chart: perrot.ChartBase
                Parent chart.
            
            canvas: pero.Canvas
                Canvas used to draw the graphics.
            
            source: any
                Data source to be used for calculating callable properties.
            
            overrides: str:any pairs
                Specific properties to be overwritten.
        """
        
        pass


class InGraphics(ChartGraphics):
    """
    Abstract base class for all graphical components of a chart laying inside
    the main data area.
    """
    
    
    def get_legends(self, canvas, source=UNDEF, **overrides):
        """
        Returns all legend items of the object.
        
        This method should be overwritten by derived classed.
        
        Args:
            canvas: pero.Canvas
                Canvas used to draw the graphics.
            
            source: any
                Data source to be used for calculating callable properties.
            
            overrides: str:any pairs
                Specific properties to be overwritten.
        
        Returns:
            (pero.Legend,)
                Legend items.
        """
        
        return ()
    
    
    def get_labels(self, canvas, source=UNDEF, **overrides):
        """
        Returns all labels of the object.
        
        This method should be overwritten by derived classed.
        
        Args:
            canvas: pero.Canvas
                Canvas used to draw the graphics.
            
            source: any
                Data source to be used for calculating callable properties.
            
            overrides: str:any pairs
                Specific properties to be overwritten.
        
        Returns:
            (pero.Label,)
                Label items.
        """
        
        return ()
    
    
    def get_tooltip(self, x, y, limit):
        """
        Gets the nearest object tooltip (e.g. data point, region etc.).
        
        This method should be overwritten by derived classed.
        
        Args:
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
        
        return None


class OutGraphics(ChartGraphics):
    """
    Abstract base class for all graphical components of a chart laying outside
    the main data area.
    
    Properties:
        
        position: str
            Specifies the object position within parent chart as any value from
            the pero.POSITION_LRTB enum.
        
        margin: int, float, tuple
            Specifies the space around the object box as a single value or
            values for individual sides starting from top.
    """
    
    position = EnumProperty(UNDEF, enum=POSITION_LRTB, dynamic=False)
    margin = QuadProperty(10, dynamic=False)
    
    
    def get_extent(self, canvas, source=UNDEF, **overrides):
        """
        This method is automatically called by parent chart to get amount of
        logical space needed to draw the object. This method should be
        overwritten by derived classes to provide specific extent.
        
        The value should only reflect the necessary space in the relevant
        direction specified by 'position' property. The value should not include
        specified object margin.
        
        Args:
            canvas: pero.Canvas
                Canvas used to draw the graphics.
            
            source: any
                Data source to be used for calculating callable properties.
            
            overrides: str:any pairs
                Specific properties to be overwritten.
        
        Returns:
            float
                Space needed.
        """
        
        return 0
