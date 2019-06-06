import numpy as np
import math as m
import time as t
import random
import _thread
import pyaudio
import msvcrt

#Init pyaudio
pa = pyaudio.PyAudio()

SAMPLERATE = 32000 #Samples per second
CHUNK = SAMPLERATE * 2 #How many samples to generate a pluck over

BUFFERLEN = SAMPLERATE * 3

buffer = np.zeros(BUFFERLEN)
resetBuffer = np.r_[np.zeros(1024), np.ones(BUFFERLEN-1024)] #Used to reset the first 1024 samples in the buffer

noiseburst = np.r_[np.random.randn(200),np.zeros(CHUNK-200)] #Used as the input in karplusStrong

def karplusStrongChunk(frequency, volume):
    #Function for generating karplusStrong samples with a lenth of CHUNK
    #Frequency is essentially the pitch

    combParameter = 0.99 #Value that determines the plucks decay. Must be close to, but less then 1
    pitchPeriod = float(SAMPLERATE/frequency)
    combDelay = int(m.floor(pitchPeriod-0.5)) #Integer Delay required for the comb-filter to achieve the desired pitch

    #apParameter determines the fractional delay required to achieve the desired pitch
    #Used in the All-Pass filter
    d = pitchPeriod-combDelay-0.5
    apParameter = (1-d)/(1+d)

    #Setting up input and output vars
    #Output is lenth of CHUNK samples filled with zeros
    output = np.zeros(CHUNK)
    input = noiseburst * (m.pow(10, volume/20))

    #Delayed values for the combFilter and LowPassFilter.
    #Set to the previous sample later in the code
    combPrev = 0
    lpPrev = 0

    #Applying karplusStrong for every sample in the output: length = CHUNK
    for n in range(CHUNK-1):

        if(combDelay > n):
            comb = input[n] #If the delay would cause array to 'underflow' just use the input at 'n'
        else:
            comb = input[n] + combParameter*output[n-combDelay] #Differential function for combFilter

        lowpass = 0.5*(comb + combPrev) #Differential function for LowPassFilter
        combPrev = comb

        output[n] = apParameter*(lowpass-output[n-1])+lpPrev #Differential function for AllPassFilter
        lpPrev = lowpass

    return output


def addPluckAtTime(freq, volume, time):
    #Function for adding a pluck sound to the buffer
    #freq determines the pitch
    #time is a delay added before the sound is inserted into buffer in samples

    global buffer
    #s_t = t.time() #Starttime for measuring performance
    spacerSamples = time
    input = karplusStrongChunk(freq, volume) #Generate the pluck using karplusStrong

    #Padding input with zeros before adding to the buffer. Must be same length
    input = np.r_[np.zeros(spacerSamples), input, np.zeros(BUFFERLEN-input.size-spacerSamples)]
    buffer = np.add(input, buffer)

    #e_t = t.time() #Endtime for measuring performance
    #print((e_t-s_t)*1000) #Prints time operation took
    return

def callback(in_data, frame_count, time_info, status):
    #Callback used by pyaudio when ready for the next chunk for playback
    #Returns 'frame_count' samples of data from the buffer to be played back
    global buffer

    #Gets first 'frame_count' samples from the array (frame_count should be 1024 samples)
    data = (buffer[0:frame_count]*0.05).astype(np.float32).tostring()

    #Resets the first 1024 samples of the buffer (Since they were already read)
    buffer = np.multiply(buffer, resetBuffer)
    #Roll empty samples to the back of the buffer (Leaving the next chunk to be read)
    buffer = np.roll(buffer, -frame_count)
    #return the data for playback, paContinue indicated there is more data to be read
    return (data, pyaudio.paContinue)

#Opens pyaudio stream for playback
stream = pa.open(
                    format=pyaudio.paFloat32,
                    channels=1,
                    rate = SAMPLERATE,
                    output=True, #Output for playback
                    stream_callback=callback #Which callback function to use
                )

#Start the stream => Start reading and playing from buffer
stream.start_stream()

print('Instructions: ')
print('Play notes by pressing the following buttons: A, S, D, F, G, H and J. If you wish to stop the script, press Q')
print('The keys correspond to the following chords: ')
print('A major, B major, C major, D major, E major, F major and G major')
#Holds the main thread active while sound is playing
#Polling for serial input from Arduino
while stream.is_active:
    x = msvcrt.getch().lower().decode()
    #Following is a messy way of checking what the user input is
    #and then sets the pitch based on the input
    if x == "a":    #A major A, C#, E
        _thread.start_new_thread(addPluckAtTime, (277.18, 0, 0))
        t.sleep(0.07)
        _thread.start_new_thread(addPluckAtTime, (329.63, 0, 0))
        t.sleep(0.07)
        _thread.start_new_thread(addPluckAtTime, (440, 0, 0))
    elif x == "s":  #B Major B, D#, F#
        _thread.start_new_thread(addPluckAtTime, (269.99, 0, 0))
        t.sleep(0.07)
        _thread.start_new_thread(addPluckAtTime, (311.13, 0, 0))
        t.sleep(0.07)
        _thread.start_new_thread(addPluckAtTime, (493.88, 0, 0))
    if x == "d":    #C major, C, E, G
        _thread.start_new_thread(addPluckAtTime, (261.63, 0, 0))
        t.sleep(0.07)
        _thread.start_new_thread(addPluckAtTime, (329.63, 0, 0))
        t.sleep(0.07)
        _thread.start_new_thread(addPluckAtTime, (392, 0, 0))
    elif x == "f":  #D Major, D, F#, A
        _thread.start_new_thread(addPluckAtTime, (293.66, 0, 0))
        t.sleep(0.07)
        _thread.start_new_thread(addPluckAtTime, (349.23, 0, 0))
        t.sleep(0.07)
        _thread.start_new_thread(addPluckAtTime, (440, 0, 0))
    elif x == "g":  #E major, E, G#, B
        _thread.start_new_thread(addPluckAtTime, (329.63, 0, 0))
        t.sleep(0.07)
        _thread.start_new_thread(addPluckAtTime, (415, 0, 0))
        t.sleep(0.07)
        _thread.start_new_thread(addPluckAtTime, (493.88, 0, 0))
    elif x == "h":  #F major, F, A, C
        _thread.start_new_thread(addPluckAtTime, (261.63, 0, 0))
        t.sleep(0.07)
        _thread.start_new_thread(addPluckAtTime, (349.23, 0, 0))
        t.sleep(0.07)
        _thread.start_new_thread(addPluckAtTime, (440, 0, 0))
    elif x == "j":  #G major, G,B,D
        _thread.start_new_thread(addPluckAtTime, (293.66, 0, 0))
        t.sleep(0.07)
        _thread.start_new_thread(addPluckAtTime, (392, 0, 0))
        t.sleep(0.07)
        _thread.start_new_thread(addPluckAtTime, (493.88, 0, 0))
    elif x == "q":
        exit()
    else:
        pitch = 0

#Terminate program (Probably will never be reached atm. Oops)
stream.stop_stream()
stream.close()

p.terminate()
