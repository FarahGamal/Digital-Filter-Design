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

## Global Variables

marker = 'circle'
conjugate = 0
zerosComplexList = []
polesComplexList = []

## Plots and Graphs 

unitCirclePlot = figure(x_range=(-2,2), y_range=(-2,2), tools=[],
           title='zPolar',plot_width=500, plot_height=500)
allPassUnitCirclePlot = figure(x_range=(-2,2), y_range=(-2,2), tools=[],
           title='Zero-Pole Combination Of Selected All-pass Filter',plot_width=650, plot_height=500)
phasePlot=figure(x_range=(0,1), y_range=(-3.14,3.14), tools=['pan,box_zoom'],
           title='Phase Response',plot_width=500, plot_height=500)
magnitudePlot=figure(x_range=(0,1), y_range=(0,3), tools=['pan,box_zoom'],
           title='Magnitude Response',plot_width=500, plot_height=500)           
phaseResponseOfFilter=figure(x_range=(0,1), y_range=(-3.14,3.14), tools=['pan,box_zoom'],
title='Phase Response of selected All-pass Filter',plot_width=650, plot_height=500)
originalSignal=figure(x_range=(0,20), y_range=(-10,20), tools=['pan,box_zoom'],
title='Original Signal',plot_width=700, plot_height=500)
filteredSignal=figure(x_range=(0,20), y_range=(-10,20), tools=['pan,box_zoom'],
title='Filtered Signal',plot_width=700, plot_height=500)

#sources

zerosSource = ColumnDataSource({
    'x': [], 'y': [], 'marker': []
})
polesSource = ColumnDataSource({
    'x': [], 'y': [], 'marker': []
})
zerosConjugateSource = ColumnDataSource({
    'x': [], 'y': [], 'marker': []
})
polesConjugateSource = ColumnDataSource({
    'x': [], 'y': [], 'marker': []
})
magnitudeSource= ColumnDataSource({
    'w':[], 'h':[]
})
phaseSource= ColumnDataSource({
    'w':[], 'p':[]
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
applyToSignal= Button(label='Apply Filter on Signal', width = 300)

##Unit Circles Plotting

unitCirclePlot.circle(0,0,radius=1,fill_color=None,line_color='red')
allPassUnitCirclePlot.circle(0,0,radius=1,fill_color=None,line_color='red')

#rendering

zeroRenderer = unitCirclePlot.scatter(x='x', y='y',marker='marker', source=zerosSource,size=15)
poleRenderer = unitCirclePlot.scatter(x='x', y='y',marker='marker', source=polesSource,size=15)
zerosConjugaterenderer = unitCirclePlot.scatter(x='x', y='y',marker='marker', source=zerosConjugateSource,size=15)
polesConjugaterenderer = unitCirclePlot.scatter(x='x', y='y',marker='marker', source=polesConjugateSource,size=15)
allPassFilterZeroRenderer = allPassUnitCirclePlot.scatter(x='x', y='y',marker='marker', source=allPassFilterZeroSource,size=15)
allPassFilterPoleRenderer = allPassUnitCirclePlot.scatter(x='x', y='y',marker='marker', source=allPassFilterPoleSource,size=15)

magnitudePlot.line(x='w',y='h',source=magnitudeSource)
phasePlot.line(x='w',y='p',source=phaseSource)
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

#########################################################################################################################################

#? Methods

# Update zeros and poles mode
def UpdateZerosAndPolesMode():
    global marker
    marker = poleOrZeroSelection.active
    if marker == 0: marker = 'circle'
    else: marker = 'x'

# Draw zeros and poles on the graph
def DrawZerosAndPoles(event):
    global marker
    if marker == 'circle': 
        zerosSource.stream({ 'x': [event.x], 'y': [event.y], 'marker': [marker] })
    else: 
        polesSource.stream({ 'x': [event.x], 'y': [event.y], 'marker': [marker] })

# Delete both zeros and poles
def DeleteZerosAndPoles():
    zerosSource.data = {'x': [], 'y': [], 'marker': []}
    polesSource.data = {'x': [], 'y': [], 'marker': []}
    magnitudeSource.data = {'w': [], 'h': []}
    phaseSource.data = {'w': [], 'p': []}
    zerosConjugateSource.data = {'x': [], 'y': [], 'marker': []}
    polesConjugateSource.data = {'x': [], 'y': [], 'marker': []}
    ZerosAndPolesCalculations()

# Deletes all zeros
def DeleteZeros():
    zerosSource.data = {'x': [], 'y': [], 'marker': []}
    zerosConjugateSource.data = {'x': [], 'y': [], 'marker': []}

# Deletes all poles
def DeletePoles():
    polesSource.data = {'x': [], 'y': [], 'marker': []}
    polesConjugateSource.data = {'x': [], 'y': [], 'marker': []}

# Update the Conjugate Mode  
def UpdateConjugateMode():
    global conjugate
    conjugate = conjugateSelection.active
    if conjugate == 0: 
        zerosConjugateSource.data = {'x': [], 'y': [], 'marker': []}
        polesConjugateSource.data = {'x': [], 'y': [], 'marker': []}
        ZerosAndPolesCalculations()
    else: DrawConjugate()

# Draw the Conjugate
def DrawConjugate():
    global conjugate
    conjugate = conjugateSelection.active
    if conjugate == 1: 
        zerosConjugateSource.data = {'x': [], 'y': [], 'marker': []}
        polesConjugateSource.data = {'x': [], 'y': [], 'marker': []}
        for i in range(len(zerosSource.data['y'])): zerosConjugateSource.stream({'x':[zerosSource.data['x'][i]], 'marker':[zerosSource.data['marker'][i]], 'y':[zerosSource.data['y'][i]*-1]})
        for j in range(len(polesSource.data['y'])): polesConjugateSource.stream({'x':[polesSource.data['x'][j]], 'marker':[polesSource.data['marker'][j]], 'y':[polesSource.data['y'][j]*-1]})
    ZerosAndPolesCalculations()

def ZerosAndPolesCalculations():
    global zerosComplexList, polesComplexList
    zerosComplexList = []
    polesComplexList = []
    for i in  range(len(zerosSource.data['x'])): 
        zerosComplexList.append(zerosSource.data['x'][i]+zerosSource.data['y'][i]*1j)
    for i in  range(len(zerosConjugateSource.data['x'])): 
        zerosComplexList.append(zerosConjugateSource.data['x'][i]+zerosConjugateSource.data['y'][i]*1j)
    for i in  range(len(polesSource.data['x'])): 
        polesComplexList.append(polesSource.data['x'][i]+polesSource.data['y'][i]*1j)
    for i in  range(len(polesConjugateSource.data['x'])):     
        polesComplexList.append(polesConjugateSource.data['x'][i]+polesConjugateSource.data['y'][i]*1j)
    DrawMagnitudeAndPhase()

# Draw Magnitude and phase
def DrawMagnitudeAndPhase():
    global zerosComplexList, polesComplexList
    magnitudeSource.data = {'w': [], 'h': []}
    phaseSource.data = {'w': [], 'p': []}
    numeratorOfTransferFunction, denominatorOfTransferFunction = zpk2tf(zerosComplexList, polesComplexList, 1)
    w, h = freqz(numeratorOfTransferFunction, denominatorOfTransferFunction)
    w = w/max(w)
    phase = np.unwrap(np.angle(h))
    magnitude = np.sqrt(h.real**2 + h.imag**2)
    if len(zerosSource.data['x']) == 0 and len(polesSource.data['x']) == 0:
        magnitude = []
        w = []
        phase = []
        magnitudeSource.data = {'w': [], 'h': []}
        phaseSource.data = {'w': [], 'p': []}
    magnitudeSource.stream({'w': w, 'h': magnitude})
    phaseSource.stream({'w': w, 'p': phase})

def update(attr, old, new):
    DrawConjugate()
    ZerosAndPolesCalculations()

def AddNewAllPassFilter():
    realPartOfA = realInputOfFilter.value_input
    imaginaryPartOfA = imgInputOfFilter.value_input
    realInputOfFilter.value = ''
    imgInputOfFilter.value = ''
    if float(imaginaryPartOfA) < 0:
        filtersLibrary.append( ( realPartOfA+'-'+str(np.abs(float(imaginaryPartOfA)))+'j', str(len(filtersLibrary)) ) )
    else:
        filtersLibrary.append( ( realPartOfA+'+'+imaginaryPartOfA+'j', str(len(filtersLibrary)) ) )
    filtersDropdownMenu.menu = filtersLibrary

def SelectAllPassFilter(event):
    indexOfSelectedItem = int(event.item)
    allPassUnitCirclePlot.title.text = 'Zero-Pole Combination Of Selected All-pass Filter: ' + filtersLibrary[indexOfSelectedItem][0]
    phaseResponseOfFilter.title.text = 'Phase Response of selected All-pass Filter: ' + filtersLibrary[indexOfSelectedItem][0]
    allPassFilterPole = complex(filtersLibrary[indexOfSelectedItem][0])
    allPassFilterZero = 1/np.conj(complex(filtersLibrary[indexOfSelectedItem][0]))
    allPassFilterZeroSource.data = {'x': [], 'y': [], 'marker': []}
    allPassFilterPoleSource.data = {'x': [], 'y': [], 'marker': []}
    allPassFilterZeroSource.stream({'x':[allPassFilterZero.real], 'y':[allPassFilterZero.imag], 'marker':['circle']})
    allPassFilterPoleSource.stream({'x':[allPassFilterPole.real], 'y':[allPassFilterPole.imag], 'marker':['x']})

def SelectAppliedAllPassFilter(event):
    indexOfSelectedItem = int(event.item)
    for allPassFilter in appliedAllPassFilters:
        if allPassFilter[1] == str(indexOfSelectedItem): selectedAllPassFilter = allPassFilter
    allPassUnitCirclePlot.title.text = 'Zero-Pole Combination Of Selected All-pass Filter: ' + selectedAllPassFilter[0]
    phaseResponseOfFilter.title.text = 'Phase Response of selected All-pass Filter: ' + selectedAllPassFilter[0]
    allPassFilterPole = complex(selectedAllPassFilter[0])
    allPassFilterZero = 1/np.conj(complex(selectedAllPassFilter[0]))
    allPassFilterZeroSource.data = {'x': [], 'y': [], 'marker': []}
    allPassFilterPoleSource.data = {'x': [], 'y': [], 'marker': []}
    allPassFilterZeroSource.stream({'x':[allPassFilterZero.real], 'y':[allPassFilterZero.imag], 'marker':['circle']})
    allPassFilterPoleSource.stream({'x':[allPassFilterPole.real], 'y':[allPassFilterPole.imag], 'marker':['x']})

def updateAllPassPhaseResponsePlot(attr, old, newSourceValue):
    if newSourceValue['x'] != []:
        phaseResponseOfAllPassFilterSource.data = {'frequencies': [], 'phases': []}
        valueOfA = complex(newSourceValue['x'][0],newSourceValue['y'][0])
        frequencies, z_transform = freqz([-np.conj(valueOfA), 1.0], [1.0, -valueOfA])
        frequencies = frequencies/max(frequencies)
        phaseResponseOfAllPassFilter = np.unwrap(np.angle(z_transform))
        phaseResponseOfAllPassFilterSource.stream({'frequencies': frequencies, 'phases': phaseResponseOfAllPassFilter})

def applyAllPassFilterOnDesignedFilter():
    if allPassFilterPoleSource.data['y'][0] < 0:
        stringOfAOfSelectedFilter = str(allPassFilterPoleSource.data['x'][0])+'-'+str(np.abs(allPassFilterPoleSource.data['y'][0]))+'j'
    else:
        stringOfAOfSelectedFilter = str(allPassFilterPoleSource.data['x'][0])+'+'+str(allPassFilterPoleSource.data['y'][0])+'j'
    appliedAllPassFilters.append((stringOfAOfSelectedFilter, str(len(appliedAllPassFilters))))
    appliedFiltersDropdownMenu.menu = appliedAllPassFilters
    calculateDesignedFilterPhaseResponseAfterAllPassCorrection(complex(stringOfAOfSelectedFilter), 'Add')

def removeAllPassFilterFromDesignedFilter():
    if allPassFilterPoleSource.data['y'][0] < 0:
        stringOfAOfSelectedFilter = str(allPassFilterPoleSource.data['x'][0])+'-'+str(np.abs(allPassFilterPoleSource.data['y'][0]))+'j'
    else:
        stringOfAOfSelectedFilter = str(allPassFilterPoleSource.data['x'][0])+'+'+str(allPassFilterPoleSource.data['y'][0])+'j'
    for allPassFilter in appliedAllPassFilters:
        if allPassFilter[0] == stringOfAOfSelectedFilter: allPassFilterToBeRemoved = allPassFilter
    appliedAllPassFilters.remove(allPassFilterToBeRemoved)
    appliedFiltersDropdownMenu.menu = appliedAllPassFilters
    calculateDesignedFilterPhaseResponseAfterAllPassCorrection(complex(stringOfAOfSelectedFilter), 'Remove')

def calculateDesignedFilterPhaseResponseAfterAllPassCorrection(valueOfA, applicationKind):
    allPassPhaseResponseCorrectionSource.data = {'frequencies': [], 'phases': []}
    frequencies, z_transform = freqz([-np.conj(valueOfA), 1.0], [1.0, -valueOfA])
    frequencies = frequencies/max(frequencies)
    phaseResponseOfAllPassFilter = np.unwrap(np.angle(z_transform))
    if applicationKind == 'Add':
        appliedAllPassZerosAndPolesSource.data['zeros'].append(1/np.conj(valueOfA))
        appliedAllPassZerosAndPolesSource.data['poles'].append(valueOfA)
        allPassPhaseResponseCorrectionSource.stream({'frequencies': frequencies, 'phases': phaseResponseOfAllPassFilter})
    elif applicationKind == 'Remove':
        appliedAllPassZerosAndPolesSource.data['zeros'].remove(1/np.conj(valueOfA))
        appliedAllPassZerosAndPolesSource.data['poles'].remove(valueOfA)
        allPassPhaseResponseCorrectionSource.stream({'frequencies': frequencies, 'phases': phaseResponseOfAllPassFilter*-1})

def correctDesignedFilterPhasePlot(attr, old, newSourceValue):
    if newSourceValue['frequencies'] != []:
        correctedPhases = phaseSource.data['p'] + newSourceValue['phases']
        phaseSource.data = {'w': [], 'p': []}
        phaseSource.stream({'w': newSourceValue['frequencies'], 'p': correctedPhases})

#! Ro'aa
def applyFilterOnSignal():
    global zerosComplexList, polesComplexList
    zerosList, polesList = [], []
    zerosList.extend(appliedAllPassZerosAndPolesSource.data['zeros'])
    zerosList.extend(zerosComplexList)
    polesList.extend(appliedAllPassZerosAndPolesSource.data['poles'])
    polesList.extend(polesComplexList)
    print(zerosList)
    print(polesList)

#? Controls

clearZeros.on_click(DeleteZeros)
clearPoles.on_click(DeletePoles)
zerosSource.on_change('data', update)
polesSource.on_change('data', update)
resetAll.on_click(DeleteZerosAndPoles)
applyToSignal.on_click(applyFilterOnSignal)
filtersDropdownMenu.on_click(SelectAllPassFilter)
unitCirclePlot.on_event(DoubleTap, DrawZerosAndPoles)
addToFiltersLibraryButton.on_click(AddNewAllPassFilter)
appliedFiltersDropdownMenu.on_click(SelectAppliedAllPassFilter)
applySelectedFilter.on_click(applyAllPassFilterOnDesignedFilter)
removeSelectedFilter.on_click(removeAllPassFilterFromDesignedFilter)
allPassFilterPoleSource.on_change('data', updateAllPassPhaseResponsePlot)
conjugateSelection.on_change('active', lambda attr, old, new: UpdateConjugateMode())
allPassPhaseResponseCorrectionSource.on_change('data', correctDesignedFilterPhasePlot)
poleOrZeroSelection.on_change('active', lambda attr, old, new: UpdateZerosAndPolesMode())

#########################################################################################################################################
layout=Column(welcomeMsg,Row(poleOrZeroSelection,conjugateSelection,clearPoles,clearZeros,resetAll),instructionsLine,Row(unitCirclePlot,phasePlot,magnitudePlot),Div(height=15),allPassTitle,Row(filtersDropdownMenu,applySelectedFilter,removeSelectedFilter,appliedFiltersDropdownMenu ),Row(allPassUnitCirclePlot,phaseResponseOfFilter,Column(Row(Div(text='a ='),realInputOfFilter, Div(text='+ j'), imgInputOfFilter),addToFiltersLibraryButton)),Div(height=20),realTimeFilteringTitle,Row(openFile,applyToSignal),Row(originalSignal,filteredSignal),Div(height=20))
curdoc().add_root(layout)