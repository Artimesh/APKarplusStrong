import numpy as np
import math as m
import random
import sounddevice as sd

def karplusStrong(noiseBurst, combParameter, combDelay, allPassParameter, nData):
    #an arary with evenly spaced variables with nData length.
    samplingIndicies = np.arange(nData)
    outputSignal = np.zeros(nData)
    lowpassFilterState = np.zeros(1)
    allpassFilterState = np.zeros(2)
    for n in samplingIndicies:
        if n < combDelay:
            lpInput = noiseBurst[n]
        else:
            lpInput = noiseBurst[n] + combParameter * outputSignal[n-combDelay]
        allpassInput = 0.5*lpInput + 0.5*lowpassFilterState
        lowpassFilterState = lpInput
        outputSignal[n] = allpassParameter*(allpassInput-allpassFilterState[1]) + allpassFilterState[0]
        allpassFilterState[0] = allpassInput
        allpassFilterState[1] = outputSignal[n]
    return outputSignal, samplingIndicies

sampleRate = 44100 #Hertz
simulationTime = 1.5 #Defines the length of the sound generated.

#Takes the simpulation time and multiplies with the sample rate
#Which ends up having the desired length for the array the sound values
#are stored in.
nData = np.int(simulationTime*sampleRate)

#noiseBurst is used as the input signal for the Karplus Strong algorithm.
noiseBurst = np.r_[np.random.randn(200),np.zeros(nData-200)]

#The filter coefficient for the comb filter.
combParameter = 0.99

print('Instructions: ')
print('Play notes by pressing the following buttons: A, W, S, E, D, F, T, G, Y, H, U, J')
print('The keys correspond to the following chords: ')
print('C3, C3#, D3, D3#, E3, F3, F3#, G3, G3#, A3, A3#, B3')

while True:
    x = input('Press a key: ')
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

    pitchPeriod = sampleRate/pitch
    combDelay = int(m.floor(pitchPeriod-0.5)) #The delay in the comb filter
    fractionalDelay = pitchPeriod-combDelay-0.5 #the fractional delay used to create the allpass parameter
    allpassParameter = (1-fractionalDelay)/(1+fractionalDelay)

    outputSignal, samplingIndicies = karplusStrong(noiseBurst, combParameter, combDelay, allpassParameter, nData)

    sd.play(outputSignal, sampleRate)
    sd.wait()
