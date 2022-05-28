from matplotlib.pyplot import show
import numpy as np
from bokeh.plotting import figure, Column,Row
from bokeh.models import PointDrawTool, ColumnDataSource,Button,Div
from bokeh.models.widgets import RadioButtonGroup
from bokeh.layouts import *
from bokeh.io import curdoc
from bokeh.events import DoubleTap
from scipy.signal import zpk2tf, freqz
import numpy as np
from bokeh.models import Dropdown,RadioGroup

#? To run the code write python -m bokeh serve --show test.py in terminal <3 
 
## Plots and Graphs 
unitCirclePlot = figure(x_range=(-2,2), y_range=(-2,2), tools=[],
           title='zPolar',plot_width=500, plot_height=500)
allPassUnitCirclePlot = figure(x_range=(-2,2), y_range=(-2,2), tools=[],
           title='Filter Designer',plot_width=500, plot_height=500)
phasePlot=figure(x_range=(0,3.14), y_range=(-3.14,3.14), tools=['pan,box_zoom'],
           title='Phase',plot_width=500, plot_height=500)
magnitudePlot=figure(x_range=(0,3.14), y_range=(0,3), tools=['pan,box_zoom'],
           title='Magnitude',plot_width=500, plot_height=500)           
phaseResponseOfFilter=figure(x_range=(0,3.14), y_range=(-3.14,3.14), tools=['pan,box_zoom'],
title='Phase Response',plot_width=500, plot_height=500)
magResponseOfFilter=figure(x_range=(0,3.14), y_range=(-3.14,3.14), tools=['pan,box_zoom'],
title='Magnitude Response',plot_width=500, plot_height=500)
originalSignal=figure(x_range=(0,10), y_range=(-10,10), tools=['pan,box_zoom'],
title='Original Signal',plot_width=500, plot_height=500)
filteredSignal=figure(x_range=(0,10), y_range=(-10,10), tools=['pan,box_zoom'],
title='Filtered Signal',plot_width=500, plot_height=500)

#sources
source = ColumnDataSource({
    'x': [], 'y': [], 'marker': []
})
conjSource = ColumnDataSource({
    'x': [], 'y': [], 'marker': []
})
filterSource = ColumnDataSource({
    'x': [], 'y': [], 'marker': []
})
source2= ColumnDataSource({
    'w':[], 'h':[]
})
source3= ColumnDataSource({
    'w':[], 'p':[]
})
filterP=ColumnDataSource({
    'w':[], 'p':[]
})

##Buttons
poleOrZeroSelection = RadioButtonGroup(labels=['Zero', 'Pole'], active=0)
conjugateSelection = RadioButtonGroup(labels=['No conjugate', 'Conjugate'], active=0)
resetAll = Button(label='Reset all')
clearZeros= Button(label='Clear Zeros')
clearPoles= Button(label='Clear Poles')
filtersMenu = [("Filter 1", "0"), ("Filter 2", "1"), ("Filter 3", "2")]
applyFilterButton = Button(label='Apply')
resetFilterButton = Button(label='Reset filter')
addToFiltersList = Button(label='Add to filters list')
filtersDropdownMenu = Dropdown(label="Filters picker", button_type="warning", menu=filtersMenu)
openFile= Button(label='Open Signal')
applyToSignal= Button(label='Apply Filter on Signal')
##Unit Circles
unitCirclePlot.circle(0,0,radius=1,fill_color=None,line_color='red')
allPassUnitCirclePlot.circle(0,0,radius=1,fill_color=None,line_color='red')

#rendering
renderer = unitCirclePlot.scatter(x='x', y='y',marker='marker', source=source,size=15)
renderer2 = unitCirclePlot.scatter(x='x', y='y',marker='marker', source=conjSource,size=15)
renderer3 = allPassUnitCirclePlot.scatter(x='x', y='y',marker='marker', source=filterSource,size=15)

magnitudePlot.line(x='w',y='h',source=source2)
phasePlot.line(x='w',y='p',source=source3)
phaseResponseOfFilter.line(x='w',y='p',source=filterP)
draw_tool = PointDrawTool(renderers=[renderer,renderer2],add=False)
unitCirclePlot.add_tools(draw_tool)
unitCirclePlot.toolbar.active_tap = draw_tool
draw_tool2 = PointDrawTool(renderers=[renderer3],add=False)
allPassUnitCirclePlot.add_tools(draw_tool2)
allPassUnitCirclePlot.toolbar.active_tap = draw_tool2



layout=Column(Row(poleOrZeroSelection,conjugateSelection,clearPoles,clearZeros,resetAll),Row(unitCirclePlot,phasePlot,magnitudePlot),Row(filtersDropdownMenu,applyFilterButton,resetFilterButton,addToFiltersList),Row(allPassUnitCirclePlot,phaseResponseOfFilter,magResponseOfFilter),Row(openFile,applyToSignal),Row(originalSignal,filteredSignal))
curdoc().add_root(layout)

