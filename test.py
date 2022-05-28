import fileinput
import numpy as np
from bokeh.layouts import *
from bokeh.io import curdoc
from ctypes import alignment
from turtle import color, width
from bokeh.events import DoubleTap
from matplotlib.pyplot import show
from scipy.signal import zpk2tf, freqz
from bokeh.models import Dropdown,RadioGroup
from bokeh.plotting import figure, Column,Row
from bokeh.models import PointDrawTool, ColumnDataSource,Button,Div
from bokeh.models.widgets import RadioButtonGroup, FileInput, TextInput


#! To run the code write python -m bokeh serve --show test.py in terminal <3 
 
## Plots and Graphs 
unitCirclePlot = figure(x_range=(-2,2), y_range=(-2,2), tools=[],
           title='zPolar',plot_width=500, plot_height=500)
allPassUnitCirclePlot = figure(x_range=(-2,2), y_range=(-2,2), tools=[],
           title='Zero-Ploe Combination Of Selected All-pass Filter',plot_width=650, plot_height=500)
phasePlot=figure(x_range=(0,3.14), y_range=(-3.14,3.14), tools=['pan,box_zoom'],
           title='Phase Response',plot_width=500, plot_height=500)
magnitudePlot=figure(x_range=(0,3.14), y_range=(0,3), tools=['pan,box_zoom'],
           title='Magnitude Response',plot_width=500, plot_height=500)           
phaseResponseOfFilter=figure(x_range=(0,3.14), y_range=(-3.14,3.14), tools=['pan,box_zoom'],
title='Phase Response of selected All-pass Filter',plot_width=650, plot_height=500)
originalSignal=figure(x_range=(0,20), y_range=(-10,20), tools=['pan,box_zoom'],
title='Original Signal',plot_width=700, plot_height=500)
filteredSignal=figure(x_range=(0,20), y_range=(-10,20), tools=['pan,box_zoom'],
title='Filtered Signal',plot_width=700, plot_height=500)

#sources
zerosAndPolesSource = ColumnDataSource({
    'x': [], 'y': [], 'marker': []
})
conjugateSource = ColumnDataSource({
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

##Buttons and controls
poleOrZeroSelection = RadioButtonGroup(labels=['Zero', 'Pole'], active=0)
conjugateSelection = RadioButtonGroup(labels=['No Conjugate', 'Conjugate'], active=0)
resetAll = Button(label='Reset all', width=270)
clearZeros= Button(label='Clear Zeros', width=270)
clearPoles= Button(label='Clear Poles', width=270)
filtersLibrary = [("Filter 1", "0"), ("Filter 2", "1"), ("Filter 3", "2")]
appliedAllPassFilters=[(" Designed Filter 1","0" )] 
addToFiltersLibraryButton = Button(label='Add To All-pass Filters Library', width=100)
removeFilterButton = Button(label='Remove Selected All-pass Filter')
applySelectedFilter = Button(label='Apply Selected All-pass Filter')
filtersDropdownMenu = Dropdown(label="All-pass Filters Library", button_type="warning", menu=filtersLibrary)
appliedFiltersDropdownMenu = Dropdown(label="Applied All-pass Filters to Designed Digital Filter", button_type="warning", menu=appliedAllPassFilters)
realInputOfFilter= TextInput(title='', width=50)
imgInputOfFilter= TextInput(title='', width=50)
openFile= FileInput(accept= '.csv', width=700)
applyToSignal= Button(label='Apply Filter on Signal', width = 150)

##Unit Circles Plotting
unitCirclePlot.circle(0,0,radius=1,fill_color=None,line_color='red')
allPassUnitCirclePlot.circle(0,0,radius=1,fill_color=None,line_color='red')

#rendering
renderer = unitCirclePlot.scatter(x='x', y='y',marker='marker', source=zerosAndPolesSource,size=15)
renderer2 = unitCirclePlot.scatter(x='x', y='y',marker='marker', source=conjugateSource,size=15)
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

welcomeMsg= Div(text='<h2>Welcome to Our Digital Filter Designer! </h2>', align= 'center')
allPassTitle= Div(text='<h2>Phase Correction using All-pass Filter </h2>', align= 'start')
realTimeFilteringTitle= Div(text='<h2>Real-time Signal Filtering</h2>', align= 'start')

################################################################################################################

#? Methods

marker = 'circle'
def UpdateZerosAndPolesMode():
    global marker
    marker = poleOrZeroSelection.active
    if marker == 0: marker = 'circle'
    else: marker = 'x'

def DrawZerosAndPoles(event):
    zerosAndPolesSource.stream({ 'x': [event.x], 'y': [event.y], 'marker': [marker] })

def DeleteZerosAndPoles():
    zerosAndPolesSource.data = {'x': [], 'y': [], 'marker': []}

#? Controls

unitCirclePlot.on_event(DoubleTap, DrawZerosAndPoles)
poleOrZeroSelection.on_change('active', lambda attr, old, new: UpdateZerosAndPolesMode())
resetAll.on_click(DeleteZerosAndPoles)

####################################################################################################################
layout=Column(welcomeMsg,Row(poleOrZeroSelection,conjugateSelection,clearPoles,clearZeros,resetAll),Row(unitCirclePlot,phasePlot,magnitudePlot),allPassTitle,Row(filtersDropdownMenu,applySelectedFilter,removeFilterButton,appliedFiltersDropdownMenu ),Row(allPassUnitCirclePlot,phaseResponseOfFilter,Column(Row(Div(text='a ='),realInputOfFilter, Div(text='+ j'), imgInputOfFilter),addToFiltersLibraryButton)),realTimeFilteringTitle,Row(openFile,applyToSignal),Row(originalSignal,filteredSignal))
curdoc().add_root(layout)