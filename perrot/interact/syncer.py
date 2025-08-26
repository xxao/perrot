#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from pero.enums import *
from . control import PlotControl
from .. chart import Axis


class Syncer(object):
    """
    Syncer tool enables custom axes synchronization across multiple plot
    controls.
    """
    
    
    def __init__(self):
        """Initializes a new instance of Syncer."""
        
        self._links = []
        self._in_sync = False
    
    
    def sync(self, master, m_axis, slave, s_axis):
        """
        Registers link between two plots axes.
        
        Args:
            master: perrot.PlotControl
                Master plot.
            
            m_axis: str or perrot.Axis
                Unique tag of the master axis or the axis itself.
            
            slave: perrot.PlotControl
                Slave plot.
            
            s_axis: str or perrot.Axis
                Unique tag of the slave axis or the axis itself.
        """
        
        # check plots type
        if not isinstance(master, PlotControl):
            message = "Master plot must be of type perrot.PlotControl! -> %s" % type(master)
            raise TypeError(message)
        
        if not isinstance(slave, PlotControl):
            message = "Slave plot must be of type perrot.PlotControl! -> %s" % type(slave)
            raise TypeError(message)
        
        # check axes type
        if isinstance(m_axis, str):
            m_axis = master.graphics.get_obj(m_axis)
        
        if not isinstance(m_axis, Axis):
            message = "Master axis must be of type perrot.Axis! -> %s" % type(m_axis)
            raise TypeError(message)
        
        if isinstance(s_axis, str):
            s_axis = master.graphics.get_obj(s_axis)
        
        if not isinstance(s_axis, Axis):
            message = "Slave axis must be of type perrot.Axis! -> %s" % type(s_axis)
            raise TypeError(message)
        
        # bind to zoom event if needed
        if not any(d[0] is master for d in self._links):
            master.bind(EVT_ZOOM, self._on_zoom)
        
        # add link
        self._links.append((master, m_axis, slave, s_axis))
    
    
    def sync_x(self, master, slave, mutual=False):
        """
        Registers link between two plots x-axes.
        
        Args:
            master: perrot.PlotControl
                Master plot.
            
            slave: perrot.PlotControl
                Slave plot.
            
            mutual: bool
                If set to True, reversed direction is registered too.
        """
        
        # add main sync
        self.sync(master, master.graphics.x_axis, slave, slave.graphics.x_axis)
        
        # add reversed sync
        if mutual:
            self.sync(slave, slave.graphics.x_axis, master, master.graphics.x_axis)
    
    
    def sync_y(self, master, slave, mutual=False):
        """
        Registers link between two plots y-axes.
        
        Args:
            master: perrot.PlotControl
                Master plot.
            
            slave: perrot.PlotControl
                Slave plot.
            
            mutual: bool
                If set to True, reversed direction is registered too.
        """
        
        # add main sync
        self.sync(master, master.graphics.y_axis, slave, slave.graphics.y_axis)
        
        # add reversed sync
        if mutual:
            self.sync(slave, slave.graphics.y_axis, master, master.graphics.y_axis)
    
    
    def unsync(self, master, m_axis, slave, s_axis):
        """
        Removes link between two plots axes.
        
        Args:
            master: perrot.PlotControl
                Master plot.
            
            m_axis: str or perrot.Axis
                Unique tag of the master axis or the axis itself.
            
            slave: perrot.PlotControl
                Slave plot.
            
            s_axis: str or perrot.Axis
                Unique tag of the slave axis or the axis itself.
        """
        
        # check plots type
        if not isinstance(master, PlotControl):
            message = "Master plot must be of type perrot.PlotControl! -> %s" % type(master)
            raise TypeError(message)
        
        if not isinstance(slave, PlotControl):
            message = "Slave plot must be of type perrot.PlotControl! -> %s" % type(slave)
            raise TypeError(message)
        
        # check axes type
        if isinstance(m_axis, str):
            m_axis = master.graphics.get_obj(m_axis)
        
        if not isinstance(m_axis, Axis):
            message = "Master axis must be of type perrot.Axis! -> %s" % type(m_axis)
            raise TypeError(message)
        
        if isinstance(s_axis, str):
            s_axis = master.graphics.get_obj(s_axis)
        
        if not isinstance(s_axis, Axis):
            message = "Slave axis must be of type perrot.Axis! -> %s" % type(s_axis)
            raise TypeError(message)
        
        # remove if present
        item = (master, m_axis, slave, s_axis)
        if item in self._links:
            
            # remove link
            self._links.remove(item)
            
            # unbind from zoom event if needed
            if not any(d[0] is master for d in self._links):
                master.unbind(EVT_ZOOM, self._on_zoom)
    
    
    def unsync_x(self, master, slave, mutual=False):
        """
        Removes link between two plots x-axes.
        
        Args:
            master: perrot.PlotControl
                Master plot.
            
            slave: perrot.PlotControl
                Slave plot.
            
            mutual: bool
                If set to True, reversed direction is removed too.
        """
        
        # remove main sync
        self.unsync(master, master.graphics.x_axis, slave, slave.graphics.x_axis)
        
        # remove reversed sync
        if mutual:
            self.unsync(slave, slave.graphics.x_axis, master, master.graphics.x_axis)
    
    
    def unsync_y(self, master, slave, mutual=False):
        """
        Removes link between two plots y-axes.
        
        Args:
            master: perrot.PlotControl
                Master plot.
            
            slave: perrot.PlotControl
                Slave plot.
            
            mutual: bool
                If set to True, reversed direction is removed too.
        """
        
        # remove main sync
        self.unsync(master, master.graphics.y_axis, slave, slave.graphics.y_axis)
        
        # remove reversed sync
        if mutual:
            self.unsync(slave, slave.graphics.y_axis, master, master.graphics.y_axis)
    
    
    def force(self, master):
        """
        Forces synchronization from given master.
        
        Args:
            master: perrot.PlotControl
                Master plot.
        """
        
        # check active sync
        if self._in_sync:
            return
        
        # set sync active
        self._in_sync = True
        
        # sync linked axes
        for m_ctrl, m_axis, s_ctrl, s_axis in self._links:
            
            # check master
            if master is not m_ctrl:
                continue
            
            # zoom slave
            rng = m_axis.scale.in_range
            s_ctrl.zoom(s_axis, rng[0], rng[1], True)
        
        # set sync inactive
        self._in_sync = False
    
    
    def _on_zoom(self, evt):
        """Handles zoom events."""
        
        self.force(evt.control)
