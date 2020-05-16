'''fast_video.py'''

# External libraries
import cv2
import numpy as np
from scipy.io import wavfile
from audiotsm import phasevocoder
from arrayWav import ArrReader, ArrWriter

# Internal libraries
import math
import sys
import time
import os
from datetime import timedelta
import subprocess
import argparse


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
