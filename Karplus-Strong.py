import numpy as np
import math as m
import random
import sounddevice as sd
import msvcrt

#Defining the function karplusStrong
def karplusStrong(noiseBurst, combParameter, combDelay, allPassParameter, nData):
    #an arary with evenly spaced variables with nData length.
    samplingIndicies = np.arange(nData)
    #Setting up the output signal array with 'no' data.
    outputSignal = np.zeros(nData)
    lowpassFilterState = np.zeros(1)
    allpassFilterState = np.zeros(2)
    for n in samplingIndicies:
        if n < combDelay:   #If n is lower than the pitch period (comb delay)
            lpInput = noiseBurst[n]
        else:
            lpInput = noiseBurst[n] + combParameter * outputSignal[n-combDelay] #Input + the delayed output sample x comb filter coefficient.
        allpassInput = 0.5*lpInput + 0.5*lowpassFilterState #Output of the lowpass filter
        lowpassFilterState = lpInput    #Saving the input of the lowpass filter to use on next sample
        outputSignal[n] = allpassParameter*(allpassInput-allpassFilterState[1]) + allpassFilterState[0] #output of the allpass filter
        allpassFilterState[0] = allpassInput    #Saving the input of the allpass filter
        allpassFilterState[1] = outputSignal[n] #Saving the output of the allpass filter
    return outputSignal, samplingIndicies


sampleRate = 32000 #Hertz
simulationTime = 3 #Defines the length of the sound generated.

#Takes the simpulation time and multiplies with the sample rate
#Which ends up having the desired length for the array the sound values
#are stored in.
nData = np.int(simulationTime*sampleRate)
noteCount = 0
#noiseBurst is used as the input signal for the Karplus Strong algorithm.
noiseBurst = np.r_[np.random.randn(200),np.zeros(nData-200)]

#The filter coefficient for the comb filter.
combParameter = 0.98

print('Instructions: ')
print('Play notes by pressing the following buttons: A, W, S, E, D, F, T, G, Y, H, U, J')
print('The keys correspond to the following chords: ')
print('C3, C3#, D3, D3#, E3, F3, F3#, G3, G3#, A3, A3#, B3')

while True:
    x = msvcrt.getch().lower().decode()
    #Following is a messy way of checking what the user input is
    #and then sets the pitch based on the input
    if x == "a":    #C3
        pitch = 130.81
    elif x == "w":  #C3Sharp
        pitch = 138.59
    elif x == "s":  #D3
        pitch = 146.83
    elif x == "e":  #D3Sharp
        pitch = 155.56
    elif x == "d":  #E3
        pitch = 164.81
    elif x == "f":  #F3
        pitch = 174.61
    elif x == "t":  #F3Sharp
        pitch = 185
    elif x == "g":  #G3
        pitch = 196
    elif x == "y":  #G3Sharp
        pitch = 207.65
    elif x == "h":  #A3
        pitch = 220
    elif x == "u":  #A3Sharp
        pitch = 233.08
    elif x == "j":  #B3
        pitch = 246.94
    else:
        pitch = 0

    if pitch > 0:
        if noteCount == 0:
            pitchPeriod = sampleRate/pitch
            combDelay = int(m.floor(pitchPeriod-0.5)) #The delay in the comb filter
            fractionalDelay = pitchPeriod-combDelay-0.5 #the fractional delay used to create the allpass parameter
            allpassParameter = (1-fractionalDelay)/(1+fractionalDelay)
            outputSignalA, samplingIndiciesA = karplusStrong(noiseBurst, combParameter, combDelay, allpassParameter, nData)
            print('a')
            noteCount = noteCount + 1
        elif noteCount == 1:
            pitchPeriod = sampleRate/pitch
            combDelay = int(m.floor(pitchPeriod-0.5)) #The delay in the comb filter
            fractionalDelay = pitchPeriod-combDelay-0.5 #the fractional delay used to create the allpass parameter
            allpassParameter = (1-fractionalDelay)/(1+fractionalDelay)
            outputSignalB, samplingIndiciesB = karplusStrong(noiseBurst, combParameter, combDelay, allpassParameter, nData)
            print('b')
            noteCount = noteCount + 1
        elif noteCount == 2:
            pitchPeriod = sampleRate/pitch
            combDelay = int(m.floor(pitchPeriod-0.5)) #The delay in the comb filter
            fractionalDelay = pitchPeriod-combDelay-0.5 #the fractional delay used to create the allpass parameter
            allpassParameter = (1-fractionalDelay)/(1+fractionalDelay)
            outputSignalC, samplingIndiciesC = karplusStrong(noiseBurst, combParameter, combDelay, allpassParameter, nData)
            print('c')

            sd.play(outputSignalA + outputSignalB + outputSignalC, sampleRate)
            sd.wait()
            noteCount = 0
