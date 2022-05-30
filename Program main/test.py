#*######### Imports ###########

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import io
import base64
import GUI
import numpy as np
import pandas as pd
from functools import partial
from scipy.signal import zpk2tf, freqz, lfilter

#? To run the code write python -m bokeh serve --show test.py in terminal  

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
    global marker; marker = GUI.poleOrZeroSelection.active
    if marker == 0: marker = 'circle'
    else: marker = 'x'

# Draw zeros and poles on the graph
def DrawZerosAndPoles(event):
    global marker
    if marker == 'circle': StremSource(GUI.zerosSource, { 'x': [event.x], 'y': [event.y], 'marker': [marker] })
    else: StremSource(GUI.polesSource, { 'x': [event.x], 'y': [event.y], 'marker': [marker] })
        
# Delete both zeros and poles
def DeleteZerosAndPoles():
    ClearSource(GUI.zerosSource, {'x': [], 'y': [], 'marker': []}); ClearSource(GUI.polesSource, {'x': [], 'y': [], 'marker': []}); ClearSource(GUI.magnitudeSource, {'frequencies': [], 'magnitude': []}); ClearSource(GUI.phaseSource, {'frequencies': [], 'phase': []}); ClearSource(GUI.zerosConjugateSource, {'real': [], 'img': [], 'marker': []}); ClearSource(GUI.polesConjugateSource, {'real': [], 'img': [], 'marker': []})
    ZerosAndPolesCalculations()

# Delete all zeros or all poles
def DeleteAllZerosOrAllPoles(zerosOrPolesSource, zerosOrPolesConjugateSource):
    ClearSource(zerosOrPolesSource, {'x': [], 'y': [], 'marker': []}); ClearSource(zerosOrPolesConjugateSource, {'real': [], 'img': [], 'marker': []})

# Update the Conjugate Mode  
def UpdateConjugateMode():
    global conjugate
    conjugate = GUI.conjugateSelection.active
    if conjugate == 0: 
        ClearSource(GUI.zerosConjugateSource, {'real': [], 'img': [], 'marker': []}); ClearSource(GUI.polesConjugateSource, {'real': [], 'img': [], 'marker': []}); ZerosAndPolesCalculations()
    else: DrawConjugate()

# Draw the Conjugate
def DrawConjugate():
    global conjugate
    conjugate = GUI.conjugateSelection.active
    if conjugate == 1: 
        ClearSource(GUI.zerosConjugateSource, {'real': [], 'img': [], 'marker': []}); ClearSource(GUI.polesConjugateSource, {'real': [], 'img': [], 'marker': []}); ZerosAndPolesCalculations()
        ConjugateForm(GUI.zerosSource, GUI.zerosConjugateSource, 'x', 'y', 'real', 'img'); ConjugateForm(GUI.polesSource, GUI.polesConjugateSource, 'x', 'y', 'real', 'img')
    ZerosAndPolesCalculations()

# Put zeros and poles in a complex form then call function to plot magnitude and phase
def ZerosAndPolesCalculations():
    global zerosComplexList, polesComplexList
    zerosComplexList, polesComplexList = [], []
    ComplexForm(GUI.zerosSource, zerosComplexList, 'x', 'y'); ComplexForm(GUI.zerosConjugateSource, zerosComplexList, 'real', 'img'); ComplexForm(GUI.polesSource, polesComplexList, 'x', 'y'); ComplexForm(GUI.polesConjugateSource, polesComplexList, 'real', 'img')
    PlotMagnitudeAndPhase()

# Plot Magnitude and phase
def PlotMagnitudeAndPhase():
    global zerosComplexList, polesComplexList
    numeratorOfTransferFunction, denominatorOfTransferFunction = zpk2tf(zerosComplexList, polesComplexList, 1)
    frequencies, z_transform = freqz(numeratorOfTransferFunction, denominatorOfTransferFunction); frequencies = frequencies/max(frequencies)
    phase = np.unwrap(np.angle(z_transform)); magnitude = np.sqrt(z_transform.real**2 + z_transform.imag**2)
    if len(GUI.zerosSource.data['x']) == 0 and len(GUI.polesSource.data['x']) == 0:
        magnitude, frequencies, phase = [], [], []
        ClearSource(GUI.magnitudeSource, {'frequencies': [], 'magnitude': []}); ClearSource(GUI.phaseSource, {'frequencies': [], 'phase': []})
    EmptyAndStreamSource(GUI.magnitudeSource, {'frequencies': [], 'magnitude': []}, {'frequencies': frequencies, 'magnitude': magnitude}); EmptyAndStreamSource(GUI.phaseSource, {'frequencies': [], 'phase': []}, {'frequencies': frequencies, 'phase': phase})

# Update magnitude and phase graph and conjugate
def update(attr, old, new):
    DrawConjugate()
    ZerosAndPolesCalculations()

#! ---------------------------------------------------------------------------------------------------------------------------------------------- #

                                            ##########? All-Pass Correction Functionality ##########

# Adding New User-Definied All-Pass Filter to Website Library
def AddNewAllPassFilter():
    realPartOfA, imaginaryPartOfA = GUI.realInputOfFilter.value_input, GUI.imgInputOfFilter.value_input; GUI.realInputOfFilter.value, GUI.imgInputOfFilter.value = '', ''
    if float(imaginaryPartOfA) < 0: GUI.filtersLibrary.append((FormulateSelectedAllPassFilter(realPartOfA, np.abs(float(imaginaryPartOfA)), '-'), str(len(GUI.filtersLibrary))))
    else: GUI.filtersLibrary.append((FormulateSelectedAllPassFilter(realPartOfA, imaginaryPartOfA, '+'), str(len(GUI.filtersLibrary))))
    GUI.filtersDropdownMenu.menu = GUI.filtersLibrary 

# Updating All-Pass Unit Circle and All-Pass Phase Response According to Selected All-Pass Filter
def UpdatingAllPassUnitCircleAndPhaseResponseAccordingToSelectedFilter(event, filterState):
    indexOfSelectedItem = int(event.item)
    if filterState == 'Not Applied': selectedAllPassFilter = GUI.filtersLibrary[indexOfSelectedItem][0]
    elif filterState == 'Applied':
        for allPassFilter in GUI.appliedAllPassFilters:
            if allPassFilter[1] == str(indexOfSelectedItem): selectedAllPassFilter = allPassFilter[0]
    GUI.allPassUnitCirclePlot.title.text, GUI.phaseResponseOfFilter.title.text = 'Zero-Pole Combination Of Selected All-pass Filter: ' + selectedAllPassFilter, 'Phase Response of selected All-pass Filter: ' + selectedAllPassFilter
    allPassFilterPole, allPassFilterZero = complex(selectedAllPassFilter), 1/np.conj(complex(selectedAllPassFilter))
    EmptyAndStreamSource(GUI.allPassFilterZeroSource, {'x': [], 'y': [], 'marker': []}, {'x':[allPassFilterZero.real], 'y':[allPassFilterZero.imag], 'marker':['circle']}); EmptyAndStreamSource(GUI.allPassFilterPoleSource, {'x': [], 'y': [], 'marker': []}, {'x':[allPassFilterPole.real], 'y':[allPassFilterPole.imag], 'marker':['x']})

# Updating All-Pass Phase Response Plot According to Selected All-Pass Filter
def UpdateAllPassPhaseResponsePlot(attribute, oldSourceValue, newSourceValue):
    if newSourceValue['x'] != []:
        valueOfA = complex(newSourceValue['x'][0],newSourceValue['y'][0]); frequencies, z_transform = freqz([-np.conj(valueOfA), 1.0], [1.0, -valueOfA])
        frequencies, phaseResponseOfAllPassFilter = frequencies/max(frequencies), np.unwrap(np.angle(z_transform))
        EmptyAndStreamSource(GUI.phaseResponseOfAllPassFilterSource, {'frequencies': [], 'phases': []}, {'frequencies': frequencies, 'phases': phaseResponseOfAllPassFilter})

# Handling Functionality to Applying or Removing Selected All-Pass Filter on User Designed Digital Filter
def ActionOfSelectedAllPassFilterOnDesignedFilter(actionType):
    if GUI.allPassFilterPoleSource.data['y'][0] < 0: stringOfAOfSelectedFilter = FormulateSelectedAllPassFilter(GUI.allPassFilterPoleSource.data['x'][0], np.abs(GUI.allPassFilterPoleSource.data['y'][0]), '-')
    else: stringOfAOfSelectedFilter = FormulateSelectedAllPassFilter(GUI.allPassFilterPoleSource.data['x'][0], GUI.allPassFilterPoleSource.data['y'][0], '+')
    if actionType == 'Add': GUI.appliedAllPassFilters.append((stringOfAOfSelectedFilter, str(len(GUI.appliedAllPassFilters))))
    elif actionType == 'Remove':
        for allPassFilter in GUI.appliedAllPassFilters:
            if allPassFilter[0] == stringOfAOfSelectedFilter: allPassFilterToBeRemoved = allPassFilter; GUI.appliedAllPassFilters.remove(allPassFilterToBeRemoved)
    GUI.appliedFiltersDropdownMenu.menu = GUI.appliedAllPassFilters; CalculateDesignedFilterPhaseResponseAfterAllPassCorrection(complex(stringOfAOfSelectedFilter), actionType)

# Calculating Phase Reponse of Selected All-Pass Filter to be Applied or Removed
def CalculateDesignedFilterPhaseResponseAfterAllPassCorrection(valueOfA, applicationKind):
    frequencies, z_transform = freqz([-np.conj(valueOfA), 1.0], [1.0, -valueOfA]); frequencies = frequencies/max(frequencies)
    phaseResponseOfAllPassFilter = np.unwrap(np.angle(z_transform))
    if applicationKind == 'Add': ApplyAllPassCorrectionOnDesignedFilter(valueOfA, 1, "append", frequencies, phaseResponseOfAllPassFilter)
    elif applicationKind == 'Remove': ApplyAllPassCorrectionOnDesignedFilter(valueOfA, -1, "remove", frequencies, phaseResponseOfAllPassFilter)

# Helper Function for Determining Action of Selected Calculated All-Pass Filter on User Designed Digital Filter
def ApplyAllPassCorrectionOnDesignedFilter(valueOfA, multiplicationParameter, applicationMethod, frequencies, phaseResponseOfAllPassFilter):
    getattr(GUI.appliedAllPassZerosAndPolesSource.data['zeros'], applicationMethod)(1/np.conj(valueOfA)); getattr(GUI.appliedAllPassZerosAndPolesSource.data['poles'], applicationMethod)(valueOfA)
    EmptyAndStreamSource(GUI.allPassPhaseResponseCorrectionSource, {'frequencies': [], 'phases': []}, {'frequencies': frequencies, 'phases': phaseResponseOfAllPassFilter*multiplicationParameter})

# Correcting User Designed Digital Filter with Calculated Phase Reponse of Selected All-Pass Filter
def CorrectDesignedFilterPhasePlot(attribute, oldSourceValue, newSourceValue):
    if newSourceValue['frequencies'] != []:
        correctedPhases = GUI.phaseSource.data['phase'] + newSourceValue['phases']; GUI.phaseSource.data = {'frequencies': [], 'phase': []}; GUI.phaseSource.stream({'frequencies': newSourceValue['frequencies'], 'phase': correctedPhases})

#! ---------------------------------------------------------------------------------------------------------------------------------------------- #
                                            
                                            ##########? Real-time Filtering Functionality ##########

#  Open csv file 
def open_file(attr, old, new):
    global time, amp, speed, newamp, zerosList, polesList 
    decoded = base64.b64decode(new); fileinput = io.BytesIO(decoded); col_list = ["x", "y"]
    data=pd.read_csv(fileinput, usecols=col_list); time=data["x"]; amp=data["y"]
    applyFilterOnSignal()
    newamp = lfilter(zerosList, polesList, amp).real
    GUI.curdoc().add_periodic_callback(update_plot, speed)

# Update original and filtered signal graph
def update_plot():
    global counter
    while counter>900:
        break
    else:
        counter=counter+ GUI.speedControlSlider.value
    GUI.originalSignal.line(x = time[:counter], y = amp[:counter]); GUI.filteredSignal.line(x = time[:counter], y = newamp[:counter])
    
# Apply the filter on choosen signal
def applyFilterOnSignal():
    global zerosComplexList, polesComplexList, zerosList, polesList 
    zerosList, polesList = [], []
    filterList(zerosList, zerosComplexList, GUI.appliedAllPassZerosAndPolesSource, 'zeros')
    filterList(polesList, polesComplexList, GUI.appliedAllPassZerosAndPolesSource, 'poles')

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

# Add zeros and pole to filter list
def filterList(zerosOrPolesList, zerosOrPolesCoomplexList, appliedSource, data):
    zerosOrPolesList.extend(appliedSource.data[data])
    zerosOrPolesList.extend(zerosOrPolesCoomplexList)

#! ---------------------------------------------------------------------------------------------------------------------------------------------- #

#?######### Links of GUI Elements to Methods ##########

GUI.zerosSource.on_change('data', update)
GUI.polesSource.on_change('data', update)
GUI.resetAll.on_click(DeleteZerosAndPoles)
GUI.openFile.on_change('value', open_file)
GUI.applyToSignal.on_click(applyFilterOnSignal)
GUI.unitCirclePlot.on_event(GUI.DoubleTap, DrawZerosAndPoles)
GUI.addToFiltersLibraryButton.on_click(AddNewAllPassFilter)
GUI.allPassFilterPoleSource.on_change('data', UpdateAllPassPhaseResponsePlot)
GUI.conjugateSelection.on_change('active', lambda attr, old, new: UpdateConjugateMode())
GUI.allPassPhaseResponseCorrectionSource.on_change('data', CorrectDesignedFilterPhasePlot)
GUI.clearZeros.on_click(lambda: DeleteAllZerosOrAllPoles(GUI.zerosSource, GUI.zerosConjugateSource))
GUI.clearPoles.on_click(lambda: DeleteAllZerosOrAllPoles(GUI.polesSource, GUI.polesConjugateSource))
GUI.poleOrZeroSelection.on_change('active', lambda attr, old, new: UpdateZerosAndPolesMode())
GUI.applySelectedFilter.on_click(lambda: ActionOfSelectedAllPassFilterOnDesignedFilter('Add'))
GUI.removeSelectedFilter.on_click(lambda: ActionOfSelectedAllPassFilterOnDesignedFilter('Remove'))
GUI.filtersDropdownMenu.on_click(partial(UpdatingAllPassUnitCircleAndPhaseResponseAccordingToSelectedFilter, filterState='Not Applied'))
GUI.appliedFiltersDropdownMenu.on_click(partial(UpdatingAllPassUnitCircleAndPhaseResponseAccordingToSelectedFilter, filterState='Applied'))

#! ---------------------------------------------------------------------------------------------------------------------------------------------- #

#?############# Layout ################

layout=GUI.Column(GUI.welcomeMsg,GUI.Row(GUI.poleOrZeroSelection,GUI.conjugateSelection,GUI.clearPoles,GUI.clearZeros,GUI.resetAll),GUI.instructionsLine,GUI.Row(GUI.unitCirclePlot,GUI.phasePlot,GUI.magnitudePlot),GUI.Div(height=15),GUI.allPassTitle,GUI.Row(GUI.filtersDropdownMenu,GUI.applySelectedFilter,GUI.removeSelectedFilter,GUI.appliedFiltersDropdownMenu ),GUI.Row(GUI.allPassUnitCirclePlot,GUI.phaseResponseOfFilter,GUI.Column(GUI.Row(GUI.Div(text='a ='),GUI.realInputOfFilter, GUI.Div(text='+ j'), GUI.imgInputOfFilter),GUI.addToFiltersLibraryButton)),GUI.Div(height=20),GUI.realTimeFilteringTitle,GUI.Row(GUI.openFile,GUI.applyToSignal,GUI.speedControlSlider),GUI.Row(GUI.originalSignal,GUI.filteredSignal),GUI.Div(height=20))
GUI.curdoc().add_root(layout)