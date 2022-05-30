#*######### Imports ###########
import io
import base64
from GUI import *
import numpy as np
import pandas as pd
from functools import partial
from scipy.signal import zpk2tf, freqz, lfilter

#? To run the code write python -m bokeh serve --show test.py in terminal <3 

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

                                            ##########? Zeros and Poles Functionality ##########

# Update zeros and poles mode
def UpdateZerosAndPolesMode():
    global marker; marker = poleOrZeroSelection.active
    if marker == 0: marker = 'circle'
    else: marker = 'x'

# Draw zeros and poles on the graph
def DrawZerosAndPoles(event):
    global marker
    if marker == 'circle': StremSource(zerosSource, { 'x': [event.x], 'y': [event.y], 'marker': [marker] })
    else: StremSource(polesSource, { 'x': [event.x], 'y': [event.y], 'marker': [marker] })
        
# Delete both zeros and poles
def DeleteZerosAndPoles():
    ClearSource(zerosSource, {'x': [], 'y': [], 'marker': []}); ClearSource(polesSource, {'x': [], 'y': [], 'marker': []}); ClearSource(magnitudeSource, {'frequencies': [], 'magnitude': []}); ClearSource(phaseSource, {'frequencies': [], 'phase': []}); ClearSource(zerosConjugateSource, {'real': [], 'img': [], 'marker': []}); ClearSource(polesConjugateSource, {'real': [], 'img': [], 'marker': []})
    ZerosAndPolesCalculations()

# Delete all zeros or all poles
def DeleteAllZerosOrAllPoles(zerosOrPolesSource, zerosOrPolesConjugateSource):
    ClearSource(zerosOrPolesSource, {'x': [], 'y': [], 'marker': []}); ClearSource(zerosOrPolesConjugateSource, {'real': [], 'img': [], 'marker': []})

# Update the Conjugate Mode  
def UpdateConjugateMode():
    global conjugate
    conjugate = conjugateSelection.active
    if conjugate == 0: 
        ClearSource(zerosConjugateSource, {'real': [], 'img': [], 'marker': []}); ClearSource(polesConjugateSource, {'real': [], 'img': [], 'marker': []}); ZerosAndPolesCalculations()
    else: DrawConjugate()

# Draw the Conjugate
def DrawConjugate():
    global conjugate
    conjugate = conjugateSelection.active
    if conjugate == 1: 
        ClearSource(zerosConjugateSource, {'real': [], 'img': [], 'marker': []}); ClearSource(polesConjugateSource, {'real': [], 'img': [], 'marker': []}); ZerosAndPolesCalculations()
        ConjugateForm(zerosSource, zerosConjugateSource, 'x', 'y', 'real', 'img'); ConjugateForm(polesSource, polesConjugateSource, 'x', 'y', 'real', 'img')
    ZerosAndPolesCalculations()

# Put zeros and poles in a complex form then call function to plot magnitude and phase
def ZerosAndPolesCalculations():
    global zerosComplexList, polesComplexList
    zerosComplexList, polesComplexList = [], []
    ComplexForm(zerosSource, zerosComplexList, 'x', 'y'); ComplexForm(zerosConjugateSource, zerosComplexList, 'real', 'img'); ComplexForm(polesSource, polesComplexList, 'x', 'y'); ComplexForm(polesConjugateSource, polesComplexList, 'real', 'img')
    PlotMagnitudeAndPhase()

# Plot Magnitude and phase
def PlotMagnitudeAndPhase():
    global zerosComplexList, polesComplexList
    numeratorOfTransferFunction, denominatorOfTransferFunction = zpk2tf(zerosComplexList, polesComplexList, 1)
    frequencies, z_transform = freqz(numeratorOfTransferFunction, denominatorOfTransferFunction); frequencies = frequencies/max(frequencies)
    phase = np.unwrap(np.angle(z_transform)); magnitude = np.sqrt(z_transform.real**2 + z_transform.imag**2)
    if len(zerosSource.data['x']) == 0 and len(polesSource.data['x']) == 0:
        magnitude, frequencies, phase = [], [], []
        ClearSource(magnitudeSource, {'frequencies': [], 'magnitude': []}); ClearSource(phaseSource, {'frequencies': [], 'phase': []})
    EmptyAndStreamSource(magnitudeSource, {'frequencies': [], 'magnitude': []}, {'frequencies': frequencies, 'magnitude': magnitude}); EmptyAndStreamSource(phaseSource, {'frequencies': [], 'phase': []}, {'frequencies': frequencies, 'phase': phase})

# Update magnitude and phase graph and conjugate
def update(attr, old, new):
    DrawConjugate()
    ZerosAndPolesCalculations()

#! ---------------------------------------------------------------------------------------------------------------------------------------------- #

                                            ##########? All-Pass Correction Functionality ##########

# Adding New User-Definied All-Pass Filter to Website Library
def AddNewAllPassFilter():
    realPartOfA, imaginaryPartOfA = realInputOfFilter.value_input, imgInputOfFilter.value_input; realInputOfFilter.value, imgInputOfFilter.value = '', ''
    if float(imaginaryPartOfA) < 0: filtersLibrary.append((FormulateSelectedAllPassFilter(realPartOfA, np.abs(float(imaginaryPartOfA)), '-'), str(len(filtersLibrary))))
    else: filtersLibrary.append((FormulateSelectedAllPassFilter(realPartOfA, imaginaryPartOfA, '+'), str(len(filtersLibrary))))
    filtersDropdownMenu.menu = filtersLibrary 

# Updating All-Pass Unit Circle and All-Pass Phase Response According to Selected All-Pass Filter
def UpdatingAllPassUnitCircleAndPhaseResponseAccordingToSelectedFilter(event, filterState):
    indexOfSelectedItem = int(event.item)
    if filterState == 'Not Applied': selectedAllPassFilter = filtersLibrary[indexOfSelectedItem][0]
    elif filterState == 'Applied':
        for allPassFilter in appliedAllPassFilters:
            if allPassFilter[1] == str(indexOfSelectedItem): selectedAllPassFilter = allPassFilter[0]
    allPassUnitCirclePlot.title.text, phaseResponseOfFilter.title.text = 'Zero-Pole Combination Of Selected All-pass Filter: ' + selectedAllPassFilter, 'Phase Response of selected All-pass Filter: ' + selectedAllPassFilter
    allPassFilterPole, allPassFilterZero = complex(selectedAllPassFilter), 1/np.conj(complex(selectedAllPassFilter))
    EmptyAndStreamSource(allPassFilterZeroSource, {'x': [], 'y': [], 'marker': []}, {'x':[allPassFilterZero.real], 'y':[allPassFilterZero.imag], 'marker':['circle']}); EmptyAndStreamSource(allPassFilterPoleSource, {'x': [], 'y': [], 'marker': []}, {'x':[allPassFilterPole.real], 'y':[allPassFilterPole.imag], 'marker':['x']})

# Updating All-Pass Phase Response Plot According to Selected All-Pass Filter
def UpdateAllPassPhaseResponsePlot(attribute, oldSourceValue, newSourceValue):
    if newSourceValue['x'] != []:
        valueOfA = complex(newSourceValue['x'][0],newSourceValue['y'][0]); frequencies, z_transform = freqz([-np.conj(valueOfA), 1.0], [1.0, -valueOfA])
        frequencies, phaseResponseOfAllPassFilter = frequencies/max(frequencies), np.unwrap(np.angle(z_transform))
        EmptyAndStreamSource(phaseResponseOfAllPassFilterSource, {'frequencies': [], 'phases': []}, {'frequencies': frequencies, 'phases': phaseResponseOfAllPassFilter})

# Handling Functionality to Applying or Removing Selected All-Pass Filter on User Designed Digital Filter
def ActionOfSelectedAllPassFilterOnDesignedFilter(actionType):
    if allPassFilterPoleSource.data['y'][0] < 0: stringOfAOfSelectedFilter = FormulateSelectedAllPassFilter(allPassFilterPoleSource.data['x'][0], np.abs(allPassFilterPoleSource.data['y'][0]), '-')
    else: stringOfAOfSelectedFilter = FormulateSelectedAllPassFilter(allPassFilterPoleSource.data['x'][0], allPassFilterPoleSource.data['y'][0], '+')
    if actionType == 'Add': appliedAllPassFilters.append((stringOfAOfSelectedFilter, str(len(appliedAllPassFilters))))
    elif actionType == 'Remove':
        for allPassFilter in appliedAllPassFilters:
            if allPassFilter[0] == stringOfAOfSelectedFilter: allPassFilterToBeRemoved = allPassFilter; appliedAllPassFilters.remove(allPassFilterToBeRemoved)
    appliedFiltersDropdownMenu.menu = appliedAllPassFilters; CalculateDesignedFilterPhaseResponseAfterAllPassCorrection(complex(stringOfAOfSelectedFilter), actionType)

# Calculating Phase Reponse of Selected All-Pass Filter to be Applied or Removed
def CalculateDesignedFilterPhaseResponseAfterAllPassCorrection(valueOfA, applicationKind):
    frequencies, z_transform = freqz([-np.conj(valueOfA), 1.0], [1.0, -valueOfA]); frequencies = frequencies/max(frequencies)
    phaseResponseOfAllPassFilter = np.unwrap(np.angle(z_transform))
    if applicationKind == 'Add': ApplyAllPassCorrectionOnDesignedFilter(valueOfA, 1, "append", frequencies, phaseResponseOfAllPassFilter)
    elif applicationKind == 'Remove': ApplyAllPassCorrectionOnDesignedFilter(valueOfA, -1, "remove", frequencies, phaseResponseOfAllPassFilter)

# Helper Function for Determining Action of Selected Calculated All-Pass Filter on User Designed Digital Filter
def ApplyAllPassCorrectionOnDesignedFilter(valueOfA, multiplicationParameter, applicationMethod, frequencies, phaseResponseOfAllPassFilter):
    getattr(appliedAllPassZerosAndPolesSource.data['zeros'], applicationMethod)(1/np.conj(valueOfA)); getattr(appliedAllPassZerosAndPolesSource.data['poles'], applicationMethod)(valueOfA)
    EmptyAndStreamSource(allPassPhaseResponseCorrectionSource, {'frequencies': [], 'phases': []}, {'frequencies': frequencies, 'phases': phaseResponseOfAllPassFilter*multiplicationParameter})

# Correcting User Designed Digital Filter with Calculated Phase Reponse of Selected All-Pass Filter
def CorrectDesignedFilterPhasePlot(attribute, oldSourceValue, newSourceValue):
    if newSourceValue['frequencies'] != []:
        correctedPhases = phaseSource.data['phase'] + newSourceValue['phases']; phaseSource.data = {'frequencies': [], 'phase': []}; phaseSource.stream({'frequencies': newSourceValue['frequencies'], 'phase': correctedPhases})

#! ---------------------------------------------------------------------------------------------------------------------------------------------- #
                                            
                                            ##########? Real-time Filtering Functionality ##########

#  Open csv file 
def open_file(attr, old, new):
    global time, amp, speed, newamp, zerosList, polesList 
    decoded = base64.b64decode(new); fileinput = io.BytesIO(decoded); col_list = ["x", "y"]
    data=pd.read_csv(fileinput, usecols=col_list); time=data["x"]; amp=data["y"]
    applyFilterOnSignal()
    newamp = lfilter(zerosList, polesList, amp).real
    curdoc().add_periodic_callback(update_plot, speed)

# Update original and filtered signal graph
def update_plot():
    global counter
    originalSignal.line(x = time[:counter], y = amp[:counter]); filteredSignal.line(x = time[:counter], y = newamp[:counter])
    counter=counter+1


# Apply the filter on choosen signal
def applyFilterOnSignal():
    global zerosComplexList, polesComplexList, zerosList, polesList 
    zerosList, polesList = [], []
    filterList(zerosList, zerosComplexList, appliedAllPassZerosAndPolesSource, 'zeros')
    filterList(polesList, polesComplexList, appliedAllPassZerosAndPolesSource, 'poles')

#! ---------------------------------------------------------------------------------------------------------------------------------------------- #

                                            ##########? Helper Functions ##########

# Clear sources 
def ClearSource(columnSource, emptySource):
    columnSource.data = emptySource

# Stream sources
def StremSource(columnSource, streamedSource):
    columnSource.stream(streamedSource)
    
# Create Conjugate for zeros and poles
def ConjugateForm(sourceName, conjugateName, firstColumn, secondColumn, firstColumnConjugate, secondColumnConjugate):
    for i in range(len(sourceName.data[secondColumn])): conjugateName.stream({firstColumnConjugate:[sourceName.data[firstColumn][i]], 'marker':[sourceName.data['marker'][i]], secondColumnConjugate:[sourceName.data[secondColumn][i]*-1]})

# Clear the source then stream it
def EmptyAndStreamSource(columnSource, emptySource, streamedSource):
    columnSource.data = emptySource; columnSource.stream(streamedSource)

# Create zeros and poles in complex form
def ComplexForm(columnSource, complexList, firstColumn, secondColumn):
    for i in  range(len(columnSource.data[firstColumn])): 
        complexList.append(columnSource.data[firstColumn][i]+columnSource.data[secondColumn][i]*1j)

# Put all pass filter in string complex form
def FormulateSelectedAllPassFilter(realPart, imaginaryPart, sign):
    return str(realPart)+sign+str(imaginaryPart)+'j'

# 
def filterList(zerosOrPolesList, zerosOrPolesCoomplexList, appliedSource, data):
    zerosOrPolesList.extend(appliedSource.data[data])
    zerosOrPolesList.extend(zerosOrPolesCoomplexList)

#! ---------------------------------------------------------------------------------------------------------------------------------------------- #

#?######### Links of GUI Elements to Methods ##########

zerosSource.on_change('data', update)
polesSource.on_change('data', update)
resetAll.on_click(DeleteZerosAndPoles)
openFile.on_change('value', open_file)
applyToSignal.on_click(applyFilterOnSignal)
unitCirclePlot.on_event(DoubleTap, DrawZerosAndPoles)
addToFiltersLibraryButton.on_click(AddNewAllPassFilter)
allPassFilterPoleSource.on_change('data', UpdateAllPassPhaseResponsePlot)
conjugateSelection.on_change('active', lambda attr, old, new: UpdateConjugateMode())
allPassPhaseResponseCorrectionSource.on_change('data', CorrectDesignedFilterPhasePlot)
clearZeros.on_click(lambda: DeleteAllZerosOrAllPoles(zerosSource, zerosConjugateSource))
clearPoles.on_click(lambda: DeleteAllZerosOrAllPoles(polesSource, polesConjugateSource))
poleOrZeroSelection.on_change('active', lambda attr, old, new: UpdateZerosAndPolesMode())
applySelectedFilter.on_click(lambda: ActionOfSelectedAllPassFilterOnDesignedFilter('Add'))
removeSelectedFilter.on_click(lambda: ActionOfSelectedAllPassFilterOnDesignedFilter('Remove'))
filtersDropdownMenu.on_click(partial(UpdatingAllPassUnitCircleAndPhaseResponseAccordingToSelectedFilter, filterState='Not Applied'))
appliedFiltersDropdownMenu.on_click(partial(UpdatingAllPassUnitCircleAndPhaseResponseAccordingToSelectedFilter, filterState='Applied'))

#! ---------------------------------------------------------------------------------------------------------------------------------------------- #

#?############# Layout ################

layout=Column(welcomeMsg,Row(poleOrZeroSelection,conjugateSelection,clearPoles,clearZeros,resetAll),instructionsLine,Row(unitCirclePlot,phasePlot,magnitudePlot),Div(height=15),allPassTitle,Row(filtersDropdownMenu,applySelectedFilter,removeSelectedFilter,appliedFiltersDropdownMenu ),Row(allPassUnitCirclePlot,phaseResponseOfFilter,Column(Row(Div(text='a ='),realInputOfFilter, Div(text='+ j'), imgInputOfFilter),addToFiltersLibraryButton)),Div(height=20),realTimeFilteringTitle,Row(openFile,applyToSignal,speedControlSlider),Row(originalSignal,filteredSignal),Div(height=20))
curdoc().add_root(layout)