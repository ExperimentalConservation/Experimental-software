from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import cv2
import numpy as np
import os
import pandas as pd

class DatasetBuilder_DatasetGenerationThread(QThread):

    totalFramesToProcess = pyqtSignal(int)
    currentFrame = pyqtSignal(int)
    barText = pyqtSignal(object)

    def __init__(self, folderControlsWidget, imageParametersWidget):
        super().__init__()
        self.rawVideosFolderPath = folderControlsWidget.rawVideosFolderPath
        self.trackingDataFolderPath = folderControlsWidget.trackingDataFolderPath
        self.outputdatasetFolderPath = folderControlsWidget.outputdatasetFolderPath
        self.extractionMethod = imageParametersWidget.extractionMethod.currentText()
        self.imageMarginsMethod = imageParametersWidget.imageMarginsMethod.currentText()
        self.imageMargins = int(imageParametersWidget.imageMargins.value())
        self.imageDims = int(imageParametersWidget.imageDims.value())
        self.labels = [] 
        self.threadActive = True 

    def stopThread(self):
        self.threadActive = False
        self.currentFrame.emit(int(0))
        self.barText.emit("Dataset Generation Cancelled")

    def run(self):
        # 1. Initialization
        # Here we calculate the number of frames we'll need to process, and update the progress bar max value accordingly.
        # We also look at how many different species are present in the dataset
        self.barText.emit("Initialization")
        self.framesToProcess = 0
        for video in os.listdir(self.rawVideosFolderPath):
            if self.threadActive is True:
                if video.endswith(".mp4") or video.endswith(".avi") or video.endswith(".mov"):
                    videoID = os.path.splitext(video)[0]
                    for trackingData in os.listdir(self.trackingDataFolderPath):
                        if self.threadActive is True:
                            if trackingData.endswith(".txt"):
                                trackingDataPath = os.path.join(self.trackingDataFolderPath, trackingData)
                                trackingDataID = os.path.splitext(trackingData)[0]
                                if trackingDataID == videoID:
                                    trackingDataDF = pd.read_csv(trackingDataPath, sep='\t', engine='python')
                                    maxFrame = max(trackingDataDF.loc[:, 'Frame'])
                                    self.framesToProcess += maxFrame
                                    uniqueSpeciesValues = trackingDataDF['Label'].unique()
                                    for species in enumerate(uniqueSpeciesValues):
                                        if self.threadActive is True:
                                            if species not in self.labels:
                                                self.labels.append(species[1])
        self.totalFramesToProcess.emit(int(self.framesToProcess))


        # 2. Species SubFolders
        # First we create the dataset subfolders (one per species)
        for label in self.labels:
            if self.threadActive is True:
                self.imageLabelPath = os.path.join(self.outputdatasetFolderPath, label)
                if not os.path.exists(self.imageLabelPath): os.makedirs(self.imageLabelPath)

        # Second we loop again, this time to create the images
        self.frameCounter = 0
        for video in os.listdir(self.rawVideosFolderPath):
            if self.threadActive is True:
                if video.endswith(".mp4") or video.endswith(".avi") or video.endswith(".mov"):
                    videoPath = os.path.join(self.rawVideosFolderPath, video)
                    videoID = os.path.splitext(video)[0]
                    for trackingData in os.listdir(self.trackingDataFolderPath):
                        if self.threadActive is True:
                            if trackingData.endswith(".txt"):
                                trackingDataPath = os.path.join(self.trackingDataFolderPath, trackingData)
                                trackingDataID = os.path.splitext(trackingData)[0]
                                if trackingDataID == videoID:
                                    trackingDataDF = pd.read_csv(trackingDataPath, sep='\t', engine='python')

                                    # Creating a column containing the contours
                                    allContours = []
                                    for i in range(len(trackingDataDF)):
                                        contourXCoord = trackingDataDF.loc[i, 'ContourXCoord']
                                        contourXCoord = contourXCoord.replace("[","")
                                        contourXCoord = contourXCoord.replace("]","")
                                        contourXCoord = contourXCoord.split(", ")
                                        contourXCoord = [int(x) for x in contourXCoord]
                                        contourYCoord = trackingDataDF.loc[i, 'ContourYCoord']
                                        contourYCoord = contourYCoord.replace("[","")
                                        contourYCoord = contourYCoord.replace("]","")
                                        contourYCoord = contourYCoord.split(", ")
                                        contourYCoord = [int(y) for y in contourYCoord]
                                        contourCoords = []
                                        for i in range(len(contourXCoord)):
                                            contourCoord = [contourXCoord[i],contourYCoord[i]]
                                            contourCoords.append(contourCoord)
                                        contourCoordsArray = np.array(contourCoords).reshape((-1,1,2)).astype(np.int32)
                                        allContours.append(contourCoordsArray)
                                    trackingDataDF['Contours'] = allContours

                                    minFrame = int(min(trackingDataDF.loc[:, 'Frame']))
                                    maxFrame = int(max(trackingDataDF.loc[:, 'Frame']))
                                    videoCapture = cv2.VideoCapture(videoPath)
                                    videoFrameNumber = 0
                                    while videoFrameNumber < maxFrame:
                                        if self.threadActive is True:
                                            videoFrameNumber += 1
                                            ret, frame = videoCapture.read()
                                            if ret is True:
                                                if videoFrameNumber >= minFrame:
                                                    trackingDataDFCurrentFrame = trackingDataDF[trackingDataDF["Frame"] == videoFrameNumber]
                                                    if len(trackingDataDFCurrentFrame) > 0:
                                                        textFrameNumber = str(videoFrameNumber).zfill(6)
                                                        for i in range(len(trackingDataDFCurrentFrame)):
                                                            if self.threadActive is True:
                                                                label = str(trackingDataDFCurrentFrame.iloc[i, trackingDataDFCurrentFrame.columns.get_loc('Label')])
                                                                objectID = str(trackingDataDFCurrentFrame.iloc[i, trackingDataDFCurrentFrame.columns.get_loc('ID')]).zfill(4)
                                                                contour = trackingDataDFCurrentFrame.iloc[i, trackingDataDFCurrentFrame.columns.get_loc('Contours')]
                                                                nBbox_Xtopleft = int(trackingDataDFCurrentFrame.iloc[i, trackingDataDFCurrentFrame.columns.get_loc('Box_TLX')])
                                                                nBbox_Ytopleft = int(trackingDataDFCurrentFrame.iloc[i, trackingDataDFCurrentFrame.columns.get_loc('Box_TLY')])
                                                                nBbox_Xbottomright = int(trackingDataDFCurrentFrame.iloc[i, trackingDataDFCurrentFrame.columns.get_loc('Box_BRX')])
                                                                nBbox_Ybottomright = int(trackingDataDFCurrentFrame.iloc[i, trackingDataDFCurrentFrame.columns.get_loc('Box_BRY')])
                                                                if self.imageMarginsMethod == "Enlarged":
                                                                    lBbox_Xtopleft = int(max(0, nBbox_Xtopleft - self.imageMargins))
                                                                    lBbox_Ytopleft = int(max(0, nBbox_Ytopleft - self.imageMargins))
                                                                    lBbox_Xbottomright = int(min(frame.shape[1], nBbox_Xbottomright + self.imageMargins))
                                                                    lBbox_Ybottomright = int(min(frame.shape[0], nBbox_Ybottomright + self.imageMargins))
                                                                    bBoxCoords = [lBbox_Xtopleft, lBbox_Ytopleft, lBbox_Xbottomright, lBbox_Ybottomright, label]
                                                                elif self.imageMarginsMethod == "Minimal":
                                                                    bBoxCoords = [nBbox_Xtopleft, nBbox_Ytopleft, nBbox_Xbottomright, nBbox_Ybottomright, label]

                                                                try:
                                                                    bBoxCoords
                                                                except:
                                                                    pass
                                                                else:
                                                                    if self.extractionMethod == "Cropping":
                                                                        roi = frame[bBoxCoords[1]:bBoxCoords[3], bBoxCoords[0]:bBoxCoords[2]]
                                                                    elif self.extractionMethod == "Contouring":
                                                                        # prepare the target image
                                                                        target = np.zeros(shape=frame.shape, dtype=np.uint8)
                                                                        target.fill(0)
                                                                        # prepare the mask
                                                                        mask = np.zeros(shape=frame.shape, dtype=np.uint8)
                                                                        mask.fill(0)
                                                                        cv2.drawContours(image=mask, contours=[contour], contourIdx=0, color=(255, 255, 255), thickness=-1)
                                                                        # create image containing only what's inside the selected contours
                                                                        target = cv2.bitwise_and(src1=frame, src2=mask, mask=None)
                                                                        roi = target[bBoxCoords[1]:bBoxCoords[3], bBoxCoords[0]:bBoxCoords[2]]
                                                                    
                                                                    try:
                                                                        roi
                                                                    except:
                                                                        pass
                                                                    else:
                                                                        newROI = cv2.resize(src=roi, dsize=(self.imageDims, self.imageDims), interpolation=cv2.INTER_LINEAR)
                                                                        imageFilename = "{}_{}_{}.png".format(str(videoID), textFrameNumber, objectID)
                                                                        imageOutputPath = os.path.join(self.outputdatasetFolderPath, label, imageFilename)
                                                                        savingText = "Saving image " + imageFilename
                                                                        self.barText.emit(savingText)
                                                                        cv2.imwrite(imageOutputPath, newROI)
                                            self.frameCounter += 1
                                            if self.threadActive is True:
                                                self.currentFrame.emit(int(self.frameCounter))
                                            if (self.frameCounter == self.framesToProcess):
                                                self.threadActive = False
                                                self.barText.emit("All images saved")

