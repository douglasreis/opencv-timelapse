import os
import sys
import numpy as np
import cv2
import time
import datetime
from pathlib import Path
from config import config


def fadeInFrames(img1, img2, numFrames):
    transitionFrames = []
    for IN in range(0, numFrames):
        fadein = IN/float(numFrames)
        transitionImg = cv2.addWeighted(img1, 1-fadein, img2, fadein, 0)
        transitionFrames.append(transitionImg)
    return transitionFrames


def getImageFiles(dir, fileExt="*", ordered=True):
    imageFiles = []
    if os.path.exists(dir):
        imageList = Path(dir).rglob(f"*.{fileExt}")
        if ordered:
            # key needs an specific lambda to deal with the order of months 1 & 10 for instance
            imageFiles = sorted(imageList, key=lambda x: (
                int(str(x).split('/')[-1].split('_')[4].split('.')[0])))
        else:
            imageFiles = imageList
    return imageFiles


def getFramesForVideo(timelapseImages, numFramesTransition):
    srcFrames = []
    framesWithTransitions = []

    for i, tlImage in enumerate(timelapseImages):
        img = cv2.imread(str(tlImage))
        width = img.shape[0]
        height = img.shape[1]
        print(f"filename: {str(tlImage)}, height: {height}, width: {width}")

        if len(srcFrames) > 0 and i < len(timelapseImages) - 1:
            framesWithTransitions.extend(fadeInFrames(
                srcFrames[-1], img, numFramesTransition))

        srcFrames.append(img)
        framesWithTransitions.append(img)

    return framesWithTransitions


def generateTimelapseVideo(timelapseImages, height, width, outputFilename, fps=10, numFramesTransition=3):
    fourcc = cv2.VideoWriter_fourcc(*"MP4V")
    writer = cv2.VideoWriter(outputFilename, fourcc, fps, (height, width))

    for frame in getFramesForVideo(timelapseImages, numFramesTransition):
        writer.write(frame)
    writer.release()


def processTimelapseVideo(basePath, dateToProcess=datetime.datetime.now(), hourly=False):
    datePattern = f"{dateToProcess.year}##{dateToProcess.month}##{dateToProcess.day}"
    if hourly:
        datePattern = f"{datePattern}##{dateToProcess.hour}"
    imageDir = f"{basePath}/{datePattern.replace('##', '/')}"

    videoFilename = f"tl_{datePattern.replace('##', '_')}.mp4"
    timelapseImages = getImageFiles(imageDir, "jpg")
    if len(timelapseImages) > 0:
        print(f"Generating '{videoFilename}' in '{imageDir}'")
        generateTimelapseVideo(
            timelapseImages, 2048, 1536, videoFilename)
    else:
        print(f"No images to generate video")


def runLoop(basePath, pause, config):
    runHour = config["runHour"]

    print(f"Pause : {pause} hours")

    while True:
        currentDatetime = datetime.datetime.now()

        if currentDatetime.hour == runHour:
            processTimelapseVideo(basePath)
        else:
            print(f"Timelapse video generator will run at next {runHour} hour")

        if runHour != 0:
            hoursAdded = datetime.timedelta(hours=pause)
            print(
                f"Timelapse video generator paused until {datetime.datetime.now() + hoursAdded}")
            time.sleep(pause*60*24)


if(__name__ == '__main__'):
    if len(sys.argv) < 1:
        exit()
    else:
        try:
            pauseInterval = int(sys.argv[1])
            basePath = config["basePath"]
            runLoop(basePath, pauseInterval, config)
        except KeyboardInterrupt:
            print("Cancelling timelapse.py")
