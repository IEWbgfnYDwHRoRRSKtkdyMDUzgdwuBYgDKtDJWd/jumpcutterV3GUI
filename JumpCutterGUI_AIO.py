from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import os
import os.path
import shutil
from subprocess import call
import cv2
import numpy as np
from scipy.io import wavfile
from audiotsm import phasevocoder
from arrayWav import ArrReader, ArrWriter
import math
import sys
import time
import os
from datetime import timedelta
import subprocess
import argparse


window = Tk()
window.title("Jumpcutter GUI")
window.geometry('320x330')
window.resizable(False, False)


videoFileGUI = ""
silentSpeedGUI = ""
silentThresholdGUI = ""
frameMarginGUI = ""
stemCommand = "python fast_video.py"

# First group of widgets - select original file and place to save jumpcutted version
group1 = LabelFrame(window, text="Main", padx=1, pady=1)
group1.grid(padx=1, pady=1)

labelLocalFile = Label(group1, text="Video File Location")
labelLocalFile.grid(column=0, row=1)

fileLocation = Entry(group1,width=48)
fileLocation.grid(column=0, row=2)



# Action after pressing ... button to selectfile
def selectFileItem():
    # Open file selecter and making path variable
    global videoFileGUI
    videoFileGUI = filedialog.askopenfilename()
    # Writing path to label
    fileLocation.insert(END, videoFileGUI)
    # Getting table with base filename
    baseFileName = os.path.basename(videoFileGUI)
    # Variable only with extension
    extension = os.path.splitext(baseFileName)[1]
    # Original path to file without file and extension
    originalPath = videoFileGUI.replace(baseFileName, '')
    # Combining original Path with filename (without extension)
    finalname = (originalPath + os.path.splitext(baseFileName)[0])
    # Inserting original Path with filename + _jumpcut suffix + original extension


# Button to open file item selection box
selectFile = Button(group1, text="...", command=selectFileItem)
selectFile.grid(column=2, row=2)


labelLocalFile.grid()
fileLocation.grid()
selectFile.grid()


# Group 2 - it is for general manipulation, FPS, sounded speed, silent threshold, silent speed
group2 = LabelFrame(window, text="General", padx=1, pady=1)
group2.grid(padx=0, pady=0)

label3 = Label(group2, text="Frame Margin (default=1)")
label3.grid(column=0,row=5)
frameMarginGUI = Entry(group2,width=4)
frameMarginGUI.insert(0, '1')
frameMarginGUI.grid(column=4, row=5)

label4 = Label(group2, text="Silent threshold (from 0 to 1) (default=0.04)")
label4.grid(column=0,row=7)
silentThresholdGUI = Entry(group2,width=4)
silentThresholdGUI.insert(0, '0.04')
silentThresholdGUI.grid(column=4, row=7)

label5 = Label(group2, text="Silent speed (default=99)")
label5.grid(column=0,row=9)
silentSpeedGUI = Entry(group2,width=4)
silentSpeedGUI.insert(0, '99')
silentSpeedGUI.grid(column=4, row=9)






# Action after clicking start button
def execute():
    fast_video_function(videoFileGUI, float(silentSpeedGUI.get()), float(silentThresholdGUI.get()), int(frameMarginGUI.get()))

def fast_video_function(videoFile, NEW_SPEEDfloat, silentThreshold, frameMargin):
    global NEW_SPEED
    NEW_SPEED = [NEW_SPEEDfloat, 1]
    global startTime
    startTime = time.time()
    global cap
    cap = cv2.VideoCapture(videoFile)
    #In case files were left behind
    try:
        os.remove('output.wav')
        os.remove('spedup.mp4')
        os.remove('spedupAudio.wav')
    except:
        pass

    global width
    global height
    global fourcc
    global fps
    global extractAudio
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = round(cap.get(cv2.CAP_PROP_FPS))
    extractAudio = 'ffmpeg -i "{}" -ab 160k -ac 2 -ar 44100 -vn output.wav'.format(videoFile)
    subprocess.call(extractAudio, shell=True)

    global out
    out = cv2.VideoWriter('spedup.mp4', fourcc, fps, (width, height))
    sampleRate, audioData = wavfile.read('output.wav')

    global skipped
    skipped = 0
    global nFrames
    nFrames = 0
    global channels
    channels = int(audioData.shape[1])
    framesProcessed = 0
    def getMaxVolume(s):
        maxv = np.max(s)
        minv = np.min(s)
        return max(maxv,-minv)


    def writeFrames(frames, nAudio, speed, samplePerSecond, writer):
        numAudioChunks = round(nAudio / samplePerSecond * fps)
        global nFrames
        numWrites = numAudioChunks - nFrames
        # a = [1, 2, 3], len(a) == 3 but a[3] is error
        limit = len(frames) - 1
        for i in range(numWrites):
            frameIndex = round(i * speed)
            if frameIndex > limit:
                writer.write(frames[-1])
            else:
                writer.write(frames[frameIndex])
            nFrames += 1

    global normal
    normal = 0
    # 0 for silent, 1 for normal
    global switchStart
    switchStart = 0
    global maxVolume
    maxVolume = getMaxVolume(audioData)

    # not used:
    # fadeInSamples = 400
    # preMask = np.arange(fadeInSamples)/fadeInSamples
    # mask = np.repeat(preMask[:, np.newaxis], 2, axis = 1)

    global y
    global yPointer
    global frameBuffer
    y = np.zeros_like(audioData, dtype=np.int16)
    yPointer = 0
    frameBuffer = []


    while (cap.isOpened()):
        ret, frame = cap.read()
        if not ret:
            break
        # since samplerate is in seconds, I need to convert this to second as well
        currentTime = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
        audioSampleStart = math.floor(currentTime * sampleRate)
        
        # more accurate frame counting
        framesProcessed += 1
        # audioSampleStart + one frame worth of samples
        audioSampleEnd = min((audioSampleStart + ((sampleRate // fps) * frameMargin)),(len(audioData)))
        switchEnd = (audioSampleStart + ((sampleRate // fps)))
        audioChunkMod = audioData[audioSampleStart:switchEnd]
        audioChunk = audioData[audioSampleStart:audioSampleEnd]

        # if it's quite
        if getMaxVolume(audioChunk) / maxVolume < silentThreshold:
            skipped += 1
            # if the frame is 'switched'
            frameBuffer.append(frame)
            normal = 0
        else: # if it's 'loud'

            # and the last frame is 'loud'
            if normal:
                out.write(frame)
                nFrames += 1
                switchStart = switchEnd

                yPointerEnd = yPointer + audioChunkMod.shape[0]
                y[yPointer : yPointerEnd] = audioChunkMod
                yPointer = yPointerEnd
            else:
                spedChunk = audioData[switchStart:switchEnd]
                spedupAudio = np.zeros((0,2), dtype=np.int16)
                with ArrReader(spedChunk, channels, sampleRate, 2) as reader:
                    with ArrWriter(spedupAudio, channels, sampleRate, 2) as writer:
                        tsm = phasevocoder(reader.channels, speed=NEW_SPEED[normal])
                        tsm.run(reader, writer)
                        spedupAudio = writer.output

                yPointerEnd = yPointer + spedupAudio.shape[0]
                y[yPointer : yPointerEnd] = spedupAudio
                yPointer = yPointerEnd

                writeFrames(frameBuffer, yPointerEnd, NEW_SPEED[normal], sampleRate, out)
                frameBuffer = []
                switchStart = switchEnd

            normal = 1
        if framesProcessed % 500 == 0:
            print("{} frames processed".format(framesProcessed))
            print("{} frames skipped".format(skipped))

    y = y[:yPointer]
    wavfile.write("spedupAudio.wav", sampleRate, y)

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    outFile = "{}_faster{}".format(videoFile[:videoFile.rfind('.')],videoFile[videoFile.rfind('.'):])
    command = "ffmpeg -y -i spedup.mp4 -i spedupAudio.wav -c:v copy -c:a aac {}".format(outFile)
    subprocess.call(command, shell=True)

    os.remove('output.wav')
    os.remove('spedup.mp4')
    os.remove('spedupAudio.wav')
    timeLength = round(time.time() - startTime, 2)
    minutes = timedelta(seconds=(round(timeLength)))
    print('Finished.')
    print(f'Took {timeLength} seconds ({minutes})')
    print(f'Removed {math.floor(skipped / fps)} seconds from a {math.floor(framesProcessed / fps)} second video.')


executeButton = Button(window, text="Start", command=execute)
executeButton.grid(column=0,row=8)
window.mainloop()