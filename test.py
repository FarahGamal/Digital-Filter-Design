#*######### Imports ###########
import io
import base64
from GUI import *
import numpy as np
import pandas as pd
from scipy.signal import zpk2tf, freqz, lfilter

#! To run the code write python -m bokeh serve --show test.py in terminal <3 

#! --------------------------------------------------------------------------------------------------------------------------------------------------- #

#? Global Variables

counter=0
speed=500
conjugate = 0
marker = 'circle'
zerosComplexList = []
polesComplexList = []

#! ---------------------------------------------------------------------------------------------------------------------------------------------- #

                                            ##########? Methods ##########

# Update zeros and poles mode
def UpdateZerosAndPolesMode():
    global marker
    marker = poleOrZeroSelection.active
    if marker == 0: marker = 'circle'
    else: marker = 'x'

# Draw zeros and poles on the graph
def DrawZerosAndPoles(event):
    global marker
    if marker == 'circle': zerosSource.stream({ 'x': [event.x], 'y': [event.y], 'marker': [marker] })
    else: polesSource.stream({ 'x': [event.x], 'y': [event.y], 'marker': [marker] })

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
def DeleteZeros(): ClearSource(zerosSource); ClearSource(zerosConjugateSource)

# Deletes all poles
def DeletePoles(): ClearSource(polesSource); ClearSource(polesConjugateSource)

# Update the Conjugate Mode  
def UpdateConjugateMode():
    global conjugate
    conjugate = conjugateSelection.active
    if conjugate == 0: 
        ClearSource(zerosConjugateSource); ClearSource(polesConjugateSource); ZerosAndPolesCalculations()
    else: DrawConjugate()

# Draw the Conjugate
def DrawConjugate():
    global conjugate
    conjugate = conjugateSelection.active
    if conjugate == 1: 
        ClearSource(zerosConjugateSource); ClearSource(polesConjugateSource); ZerosAndPolesCalculations()
        ConjugateForm(zerosSource, zerosConjugateSource); ConjugateForm(polesSource, polesConjugateSource)
    ZerosAndPolesCalculations()

def ZerosAndPolesCalculations():
    global zerosComplexList, polesComplexList
    zerosComplexList, polesComplexList = [], []
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

###############################################################!

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

####################################################################!

def open_file(attr, old, new):
    global time, amp, speed, newamp, zerosList, polesList 
    decoded = base64.b64decode(new)
    fileinput = io.BytesIO(decoded)
    col_list = ["x", "y"]
    data=pd.read_csv(fileinput, usecols=col_list)
    time=data["x"]; amp=data["y"]
    applyFilterOnSignal()
    newamp = lfilter(zerosList, polesList, amp).real
    print(newamp)
    curdoc().add_periodic_callback(update_plot, speed)

def update_plot():
    global counter
    originalSignal.line(x = time[:counter], y = amp[:counter]); filteredSignal.line(x = time[:counter], y = newamp[:counter])
    counter=counter+1

def applyFilterOnSignal():
    global zerosComplexList, polesComplexList, zerosList, polesList 
    zerosList, polesList = [], []
    zerosList.extend(appliedAllPassZerosAndPolesSource.data['zeros'])
    zerosList.extend(zerosComplexList)
    polesList.extend(appliedAllPassZerosAndPolesSource.data['poles'])
    polesList.extend(polesComplexList)
    print(zerosList)
    print(polesList)

#! ---------------------------------------------------------------------------------------------------------------------------------------------- #

                                            ##########? Helper Functions ##########

# Clear sources 
def ClearSource(sourceName):
    sourceName.data = {'x': [], 'y': [], 'marker': []}

# Create Conjugate for zeros and poles
def ConjugateForm(sourceName, conjugateName):
    for i in range(len(sourceName.data['y'])): conjugateName.stream({'x':[sourceName.data['x'][i]], 'marker':[sourceName.data['marker'][i]], 'y':[sourceName.data['y'][i]*-1]})



#! ---------------------------------------------------------------------------------------------------------------------------------------------- #

#?######### Links of GUI Elements to Methods ##########

clearZeros.on_click(DeleteZeros)
clearPoles.on_click(DeletePoles)
zerosSource.on_change('data', update)
polesSource.on_change('data', update)
resetAll.on_click(DeleteZerosAndPoles)
openFile.on_change('value', open_file)
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

#! ---------------------------------------------------------------------------------------------------------------------------------------------- #

#?############# Layout ################

layout=Column(welcomeMsg,Row(poleOrZeroSelection,conjugateSelection,clearPoles,clearZeros,resetAll),instructionsLine,Row(unitCirclePlot,phasePlot,magnitudePlot),Div(height=15),allPassTitle,Row(filtersDropdownMenu,applySelectedFilter,removeSelectedFilter,appliedFiltersDropdownMenu ),Row(allPassUnitCirclePlot,phaseResponseOfFilter,Column(Row(Div(text='a ='),realInputOfFilter, Div(text='+ j'), imgInputOfFilter),addToFiltersLibraryButton)),Div(height=20),realTimeFilteringTitle,Row(openFile,applyToSignal,speedControlSlider),Row(originalSignal,filteredSignal),Div(height=20))
curdoc().add_root(layout)