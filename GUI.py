import fileinput
from bokeh.layouts import *
from bokeh.io import curdoc
from ctypes import alignment
from turtle import color, width
from bokeh.events import DoubleTap
from matplotlib.pyplot import show
from bokeh.models import Dropdown,RadioGroup
from bokeh.plotting import figure, Column,Row
from bokeh.models import PointDrawTool, ColumnDataSource,Button,Div
from bokeh.models.widgets import RadioButtonGroup, FileInput, TextInput, Slider

## Plots and Graphs 

unitCirclePlot = figure(x_range=(-2,2), y_range=(-2,2), tools=[],
           title='zPolar',plot_width=500, plot_height=500)
allPassUnitCirclePlot = figure(x_range=(-2,2), y_range=(-2,2), tools=[],
           title='Zero-Pole Combination Of Selected All-pass Filter',plot_width=650, plot_height=500)
phasePlot=figure(x_range=(0,1), y_range=(-3.14,3.14), tools=['pan,wheel_zoom'],
           title='Phase Response',plot_width=500, plot_height=500)
magnitudePlot=figure(x_range=(0,1), y_range=(0,3), tools=['pan,wheel_zoom'],
           title='Magnitude Response',plot_width=500, plot_height=500)           
phaseResponseOfFilter=figure(x_range=(0,1), y_range=(-3.14,3.14), tools=['pan,wheel_zoom'],
title='Phase Response of selected All-pass Filter',plot_width=650, plot_height=500)
originalSignal=figure(x_range=(0,1), y_range=(-1,1), tools=['pan,wheel_zoom'],
title='Original Signal',plot_width=700, plot_height=500)
filteredSignal=figure(x_range=(0,1), y_range=(-1,1), tools=['pan,wheel_zoom'],
title='Filtered Signal',plot_width=700, plot_height=500)

#sources

zerosSource = ColumnDataSource({
    'x': [], 'y': [], 'marker': []
})
polesSource = ColumnDataSource({
    'x': [], 'y': [], 'marker': []
})
zerosConjugateSource = ColumnDataSource({
    'real': [], 'img': [], 'marker': []
})
polesConjugateSource = ColumnDataSource({
    'real': [], 'img': [], 'marker': []
})
magnitudeSource= ColumnDataSource({
    'frequencies':[], 'magnitude':[]
})
phaseSource= ColumnDataSource({
    'frequencies':[], 'phase':[]
})
allPassFilterZeroSource = ColumnDataSource({
    'x': [], 'y': [], 'marker': []
})
allPassFilterPoleSource = ColumnDataSource({
    'x': [], 'y': [], 'marker': []
})
phaseResponseOfAllPassFilterSource=ColumnDataSource({
    'frequencies':[], 'phases':[]
})

allPassPhaseResponseCorrectionSource=ColumnDataSource({
    'frequencies':[], 'phases':[]
})
appliedAllPassZerosAndPolesSource  = ColumnDataSource({
    'zeros': [], 'poles': []
})

##Buttons and controls

poleOrZeroSelection = RadioButtonGroup(labels=['Zero', 'Pole'], active=0)
conjugateSelection = RadioButtonGroup(labels=['No Conjugate', 'Conjugate'], active=0)
resetAll = Button(label='Reset all', width=270)
clearZeros= Button(label='Clear Zeros', width=270)
clearPoles= Button(label='Clear Poles', width=270)
filtersLibrary = [("-1.9+0j", "0"), ("-0.6+0j", "1"), ("0.5+0.2j", "2"), ("0.6+0j", "3"), ("1.5+1.2j", "4"), ("1.9+0j", "5")]
appliedAllPassFilters=[("...","0" )] 
addToFiltersLibraryButton = Button(label='Add To All-pass Filters Library', width=100)
removeSelectedFilter = Button(label='Remove Selected All-pass Filter')
applySelectedFilter = Button(label='Apply Selected All-pass Filter')
filtersDropdownMenu = Dropdown(label="All-pass Filters Library", button_type="warning", menu=filtersLibrary)
appliedFiltersDropdownMenu = Dropdown(label="Applied All-pass Filters to Designed Digital Filter", button_type="warning", menu=appliedAllPassFilters)
realInputOfFilter= TextInput(title='', width=50)
imgInputOfFilter= TextInput(title='', width=50)
openFile= FileInput(accept= '.csv', width=700)
applyToSignal= Button(label='Add Filter', width = 300)
speedControlSlider=Slider(width=250,start=1,end=100,value=1,step=10 ,title='Speed of filtering process')

##Unit Circles Plotting

unitCirclePlot.circle(0,0,radius=1,fill_color=None,line_color='red')
allPassUnitCirclePlot.circle(0,0,radius=1,fill_color=None,line_color='red')

#rendering

zeroRenderer = unitCirclePlot.scatter(x='x', y='y',marker='marker', source=zerosSource,size=15)
poleRenderer = unitCirclePlot.scatter(x='x', y='y',marker='marker', source=polesSource,size=15)
zerosConjugaterenderer = unitCirclePlot.scatter(x='real', y='img',marker='marker', source=zerosConjugateSource,size=15)
polesConjugaterenderer = unitCirclePlot.scatter(x='real', y='img',marker='marker', source=polesConjugateSource,size=15)
allPassFilterZeroRenderer = allPassUnitCirclePlot.scatter(x='x', y='y',marker='marker', source=allPassFilterZeroSource,size=15)
allPassFilterPoleRenderer = allPassUnitCirclePlot.scatter(x='x', y='y',marker='marker', source=allPassFilterPoleSource,size=15)

magnitudePlot.line(x='frequencies',y='magnitude',source=magnitudeSource)
phasePlot.line(x='frequencies',y='phase',source=phaseSource)
phaseResponseOfFilter.line(x='frequencies',y='phases',source=phaseResponseOfAllPassFilterSource)

draw_tool = PointDrawTool(renderers=[zeroRenderer,poleRenderer,zerosConjugaterenderer,polesConjugaterenderer],add=False)
unitCirclePlot.add_tools(draw_tool)
unitCirclePlot.toolbar.active_tap = draw_tool

draw_tool2 = PointDrawTool(renderers=[allPassFilterZeroRenderer, allPassFilterPoleRenderer],add=False)
allPassUnitCirclePlot.add_tools(draw_tool2)
allPassUnitCirclePlot.toolbar.active_tap = draw_tool2

welcomeMsg= Div(text='<h1><FONT COLOR= "#e1773e">Welcome to Our Digital Filter Designer!</FONT> </h1>', align= 'center')
instructionsLine= Div(text='<h3><FONT COLOR= "#e1773e">Double click the plotter to add Zero/Pole.  Select a Zero/Pole then click backspace to delete it.</FONT> </h3>', align= 'start')
allPassTitle= Div(text='<h2><FONT COLOR= "#e1773e">Phase Correction using All-pass Filter </FONT></h2>', align= 'start')
realTimeFilteringTitle= Div(text='<h2><FONT COLOR= "#e1773e">Real-time Signal Filtering</FONT></h2>', align= 'start')

