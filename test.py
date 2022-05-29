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

#global marker
marker = 'circle'
conjugate = 0
zerosComplexForm = []
polesComplexForm = []

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
transferFunctionZerosSource  = ColumnDataSource({
    'x': [], 'y': []
})
transferFunctionPolesSource  = ColumnDataSource({
    'x': [], 'y': []
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
applyToSignal= Button(label='Apply Filter on Signal', width = 150)

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

welcomeMsg= Div(text='<h2>Welcome to Our Digital Filter Designer! </h2>', align= 'center')
allPassTitle= Div(text='<h2>Phase Correction using All-pass Filter </h2>', align= 'start')
realTimeFilteringTitle= Div(text='<h2>Real-time Signal Filtering</h2>', align= 'start')

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
        # print(transferFunctionZerosSource.data)
        zerosSource.stream({ 'x': [event.x], 'y': [event.y], 'marker': [marker] })
        # transferFunctionZerosSource.stream({ 'x': [event.x], 'y': [event.y]})
    else: 
        # print(transferFunctionPolesSource.data)
        polesSource.stream({ 'x': [event.x], 'y': [event.y], 'marker': [marker] })
        # transferFunctionPolesSource.stream({ 'x': [event.x], 'y': [event.y]})


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
    realValuesOfZerosToBeDeleted = zerosSource.data['x']
    imgValuesOfZerosToBeDeleted = zerosSource.data['y']
    for realValue in realValuesOfZerosToBeDeleted: transferFunctionZerosSource.data['x'].remove(realValue)
    for imgValue in imgValuesOfZerosToBeDeleted: transferFunctionZerosSource.data['y'].remove(imgValue)
    zerosSource.data = {'x': [], 'y': [], 'marker': []}
    zerosConjugateSource.data = {'x': [], 'y': [], 'marker': []}
    # print(transferFunctionZerosSource.data)

# Deletes all poles
def DeletePoles():
    realValuesOfPolesToBeDeleted = polesSource.data['x']
    imgValuesOfPolesToBeDeleted = polesSource.data['y']
    for realValue in realValuesOfPolesToBeDeleted: transferFunctionPolesSource.data['x'].remove(realValue)
    for imgValue in imgValuesOfPolesToBeDeleted: transferFunctionPolesSource.data['y'].remove(imgValue)
    polesSource.data = {'x': [], 'y': [], 'marker': []}
    polesConjugateSource.data = {'x': [], 'y': [], 'marker': []}
    # print(transferFunctionPolesSource.data)

# Update the Conjugate Mode  
def UpdateConjugateMode():
    global conjugate
    conjugate = conjugateSelection.active
    if conjugate == 0: 
        zerosConjugateSource.data = {'x': [], 'y': [], 'marker': []}
        polesConjugateSource.data = {'x': [], 'y': [], 'marker': []}
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
    # print(zerosConjugateSource.data)
    # print(polesConjugateSource.data)

def ZerosAndPolesCalculations():
    global zerosComplexForm, polesComplexForm
    zerosComplexForm = []
    polesComplexForm = []
    for i in  range(len(zerosSource.data['x'])): 
        zerosComplexForm.append(zerosSource.data['x'][i]+zerosSource.data['y'][i]*1j)
    for i in  range(len(zerosConjugateSource.data['x'])): 
        zerosComplexForm.append(zerosConjugateSource.data['x'][i]+zerosConjugateSource.data['y'][i]*1j)
    for i in  range(len(polesSource.data['x'])): 
        polesComplexForm.append(polesSource.data['x'][i]+polesSource.data['y'][i]*1j)
    for i in  range(len(polesConjugateSource.data['x'])):     
        polesComplexForm.append(polesConjugateSource.data['x'][i]+polesConjugateSource.data['y'][i]*1j)
    # print(zerosComplexForm)
    # print(polesComplexForm)
    DrawMagnitudeAndPhase()

# Draw Magnitude and phase
def DrawMagnitudeAndPhase():
    global zerosComplexForm, polesComplexForm
    magnitudeSource.data = {'w': [], 'h': []}
    phaseSource.data = {'w': [], 'p': []}
    numeratorOfTransferFunction, denominatorOfTransferFunction = zpk2tf(zerosComplexForm, polesComplexForm, 1)
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
    # UpdateTransferFunctionZeros(attr, old, new)
    # UpdateTransferFunctionPoles(attr, old, new)
zerosSource.on_change('data', update)
polesSource.on_change('data', update)


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
        transferFunctionPolesSource.data['x'].append(valueOfA.real)
        transferFunctionPolesSource.data['y'].append(valueOfA.imag)
        transferFunctionZerosSource.data['x'].append((1/np.conj(valueOfA)).real)
        transferFunctionZerosSource.data['y'].append((1/np.conj(valueOfA)).imag)
        allPassPhaseResponseCorrectionSource.stream({'frequencies': frequencies, 'phases': phaseResponseOfAllPassFilter})
    elif applicationKind == 'Remove':
        transferFunctionPolesSource.data['x'].remove(valueOfA.real)
        transferFunctionPolesSource.data['y'].remove(valueOfA.imag)
        transferFunctionZerosSource.data['x'].remove((1/np.conj(valueOfA)).real)
        transferFunctionZerosSource.data['y'].remove((1/np.conj(valueOfA)).imag)
        allPassPhaseResponseCorrectionSource.stream({'frequencies': frequencies, 'phases': phaseResponseOfAllPassFilter*-1})

def correctDesignedFilterPhasePlot(attr, old, newSourceValue):
    if newSourceValue['frequencies'] != []:
        correctedPhases = phaseSource.data['p'] + newSourceValue['phases']
        phaseSource.data = {'w': [], 'p': []}
        phaseSource.stream({'w': newSourceValue['frequencies'], 'p': correctedPhases})
        # print(phaseSource.data)

# def UpdateTransferFunctionZeros(attr, oldSourceValue, newSourceValue):
#     print(oldSourceValue)
#     print(newSourceValue)
#     if len(newSourceValue['x']) > len(oldSourceValue['x']):
#         realOfNewElement = newSourceValue['x'][-1]
#         transferFunctionZerosSource.data['x'].append(realOfNewElement)
#         imagOfNewElement = newSourceValue['y'][-1]
#         transferFunctionZerosSource.data['y'].append(imagOfNewElement)
#     elif len(newSourceValue['x']) < len(oldSourceValue['x']):
#         realOfOldElement = oldSourceValue['x'][-1]
#         transferFunctionZerosSource.data['x'].remove(realOfOldElement)
#         imagOfOldElement = oldSourceValue['y'][-1]
#         transferFunctionZerosSource.data['y'].remove(imagOfOldElement)
#     print(transferFunctionZerosSource.data)

# def UpdateTransferFunctionPoles(attr, oldSourceValue, newSourceValue):
#     if len(newSourceValue['x']) > len(oldSourceValue['x']):
#         realOfNewElement = newSourceValue['x'][-1]
#         transferFunctionPolesSource.data['x'].append(realOfNewElement)
#         imagOfNewElement = newSourceValue['y'][-1]
#         transferFunctionPolesSource.data['y'].append(imagOfNewElement)
#     elif len(newSourceValue['x']) < len(oldSourceValue['x']):
#         realOfOldElement = oldSourceValue['x'][-1]
#         transferFunctionPolesSource.data['x'].remove(realOfOldElement)
#         imagOfOldElement = oldSourceValue['y'][-1]
#         transferFunctionPolesSource.data['y'].remove(imagOfOldElement)
#     print(transferFunctionPolesSource.data)

#? Controls

clearZeros.on_click(DeleteZeros)
clearPoles.on_click(DeletePoles)
resetAll.on_click(DeleteZerosAndPoles)
unitCirclePlot.on_event(DoubleTap, DrawZerosAndPoles)
poleOrZeroSelection.on_change('active', lambda attr, old, new: UpdateZerosAndPolesMode())
conjugateSelection.on_change('active', lambda attr, old, new: UpdateConjugateMode())

addToFiltersLibraryButton.on_click(AddNewAllPassFilter)

filtersDropdownMenu.on_click(SelectAllPassFilter)
allPassFilterPoleSource.on_change('data', updateAllPassPhaseResponsePlot)

applySelectedFilter.on_click(applyAllPassFilterOnDesignedFilter)
removeSelectedFilter.on_click(removeAllPassFilterFromDesignedFilter)

appliedFiltersDropdownMenu.on_click(SelectAppliedAllPassFilter)
allPassPhaseResponseCorrectionSource.on_change('data', correctDesignedFilterPhasePlot)
# zerosSource.on_change('data', UpdateTransferFunctionZeros)
# polesSource.on_change('data', UpdateTransferFunctionPoles)
#########################################################################################################################################
layout=Column(welcomeMsg,Row(poleOrZeroSelection,conjugateSelection,clearPoles,clearZeros,resetAll),Row(unitCirclePlot,phasePlot,magnitudePlot),allPassTitle,Row(filtersDropdownMenu,applySelectedFilter,removeSelectedFilter,appliedFiltersDropdownMenu ),Row(allPassUnitCirclePlot,phaseResponseOfFilter,Column(Row(Div(text='a ='),realInputOfFilter, Div(text='+ j'), imgInputOfFilter),addToFiltersLibraryButton)),realTimeFilteringTitle,Row(openFile,applyToSignal),Row(originalSignal,filteredSignal))
curdoc().add_root(layout)