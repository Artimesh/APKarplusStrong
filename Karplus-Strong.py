import numpy as np
import math as m
import random
import sounddevice as sd
import msvcrt

def karplusStrong(noiseBurst, combParameter, combDelay, allPassParameter, nData):
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

sampleRate = 44100
simulationTime = 1.5
nData = np.int(simulationTime*sampleRate)
noiseBurst = np.r_[np.random.randn(200),np.zeros(nData-200)]
combParameter = 0.99 #aka filter coefficient

while True:
    #x = input("What note should be played?: ")
    print('Input note to play: ')
    x = msvcrt.getch().lower().decode()
    print(x)
    if x == "c":
        pitch = 130.81
    elif x == "csharp":
        pitch = 138.59
    elif x == "d":
        pitch = 146.83
    elif x == "dsharp":
        pitch = 155.56
    elif x == "e":
        pitch = 164.81
    elif x == "f":
        pitch = 174.61
    elif x == "fsharp":
        pitch = 185
    elif x == "g":
        pitch = 196
    elif x == "gsharp":
        pitch = 207.65
    elif x == "a":
        pitch = 220
    elif x == "asharp":
        pitch = 233.08
    elif x == "b":
        pitch = 246.94

    pitchPeriod = sampleRate/pitch
    combDelay = int(m.floor(pitchPeriod-0.5))
    print(combDelay)
    fractionalDelay = pitchPeriod-combDelay-0.5
    print(fractionalDelay)
    allpassParameter = (1-fractionalDelay)/(1+fractionalDelay)

    outputSignal, samplingIndicies = karplusStrong(noiseBurst, combParameter, combDelay, allpassParameter, nData)

    sd.play(outputSignal, sampleRate)
    sd.wait()
