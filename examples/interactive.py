#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import numpy
import perrot


def on_key_down(evt):
    """Defines custom handling of the pero.KeyDown event."""
    
    # check key
    if evt.char != "r":
        return
    
    # cancel event propagation
    evt.cancel()
    
    # get plot
    plt = evt.control.graphics
    
    # remove current series
    for series in plt.series:
        plt.remove(series)
    
    # prepare data
    count = 50
    x_data = numpy.linspace(-5, 5, count)
    y_data = numpy.random.normal(0, 1., count)
    
    # add new series
    plt.scatter(
        x = x_data,
        y = y_data,
        color = "g")
    
    # refresh view
    evt.control.zoom()
    evt.control.refresh()


# init plot
plot = perrot.Plot(title_text="Hit -R- to refresh")

# init viewer
view = perrot.PlotControl(graphics=plot)

# bind custom event handler
view.bind(perrot.EVT_KEY_DOWN, on_key_down)

# show viewer
view.show()
