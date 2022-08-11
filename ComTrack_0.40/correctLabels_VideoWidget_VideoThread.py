from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import cv2
import numpy as np
import os
import pandas as pd

class CorrectLabels_VideoThread(QThread):
    frameImageUpdate = pyqtSignal(QImage)
    frameNumberUpdate = pyqtSignal(int)
    frameDims = pyqtSignal(object)
    scaleRatio = pyqtSignal(object)
    videoEnded = pyqtSignal(object)

    def __init__(self, videoPath, maxWidth, maxHeight, dataframe):
        super().__init__()
        self.videoPath = videoPath
        self.maxWidth = 0.95*maxWidth
        self.maxHeight = 0.95*maxHeight
        self.dataframe = dataframe
        self.threadActive = False
        self.calculateScaleRatio = False
        self.playingStatus = False
        self.videoFPS = 1
        self.fullScreenChanged = False
        self.minimizedSize = False
        self.maximizedSize = False
        self.fullScreenStatus = "Minimized"
        self.exportVideo = False
        self.exportVideoPath = []
        self.initVizParams()
        self.initImgArray()
        
    def initVizParams(self):
        self.vizParams = {
            "drawCentroid": False,
            "centroidRed": 255,
            "centroidGreen": 255,
            "centroidBlue": 255,
            "centroidRadius": 0,
            "centroidThickness": 0,
            "drawNBBox": False,
            "nBBoxRed": 255,
            "nBBoxGreen": 255,
            "nBBoxBlue": 255,
            "nBBoxThickness": 0,
            "drawLBBox": False,
            "lBBoxRed": 255,
            "lBBoxGreen": 255,
            "lBBoxBlue": 255,
            "lBBoxThickness": 0,
            "drawRBBox": False,
            "rBBoxRed": 250,
            "rBBoxGreen": 255,
            "rBBoxBlue": 255,
            "rBBoxThickness": 0,
            "drawTrackingIDs": False,
            "drawClassification": False,
            "trackingIDsRed": 255,
            "trackingIDsGreen": 255,
            "trackingIDsBlue": 255,
            "trackingIDsFontFace":  cv2.FONT_HERSHEY_PLAIN,
            "trackingIDsFontScale": 0,
            "trackingIDsThickness": 0,
            "drawContours": False,
            "contoursRed": 255,
            "contoursGreen": 255,
            "contoursBlue": 255,
            "contoursThickness": 0,
        }
    
    def updateVizParams(self, params):
        self.vizParams["drawCentroid"] = params[0]
        self.vizParams["centroidRed"] = params[1]
        self.vizParams["centroidGreen"] = params[2]
        self.vizParams["centroidBlue"] = params[3]
        self.vizParams["centroidRadius"] = params[4]
        self.vizParams["centroidThickness"] = params[5]
        self.vizParams["drawNBBox"] = params[6]
        self.vizParams["nBBoxRed"] = params[7]
        self.vizParams["nBBoxGreen"] = params[8]
        self.vizParams["nBBoxBlue"] = params[9]
        self.vizParams["nBBoxThickness"] = params[10]
        self.vizParams["drawLBBox"] = params[11]
        self.vizParams["lBBoxRed"] = params[12]
        self.vizParams["lBBoxGreen"] = params[13]
        self.vizParams["lBBoxBlue"] = params[14]
        self.vizParams["lBBoxThickness"] = params[15]
        self.vizParams["drawRBBox"] = params[16]
        self.vizParams["rBBoxRed"] = params[17]
        self.vizParams["rBBoxGreen"] = params[18]
        self.vizParams["rBBoxBlue"] = params[19]
        self.vizParams["rBBoxThickness"] = params[20]
        self.vizParams["drawTrackingIDs"] = params[21]
        self.vizParams["drawClassification"] = params[22]
        self.vizParams["trackingIDsRed"] = params[23]
        self.vizParams["trackingIDsGreen"] = params[24]
        self.vizParams["trackingIDsBlue"] = params[25]
        self.vizParams["trackingIDsFontFace"] =  params[26]
        self.vizParams["trackingIDsFontScale"] = params[27]
        self.vizParams["trackingIDsThickness"] = params[28]
        self.vizParams["drawContours"] = params[29]
        self.vizParams["contoursRed"] = params[30]
        self.vizParams["contoursGreen"] = params[31]
        self.vizParams["contoursBlue"] = params[32]
        self.vizParams["contoursThickness"] = params[33]

    def initImgArray(self):
        self.img_array = [] 
    
    def updateFrameNumber(self, framenumber):
        self.framenumber = framenumber

    def updatePlayingStatus(self, playingStatus):
        self.playingStatus = playingStatus
    
    def updateVideoFPS(self, fps):
        self.videoFPS = fps
    
    def updateVideoResize(self, maxWidth, maxHeight):
        self.fullScreenChanged = True
        if self.fullScreenStatus == "Minimized":
            self.fullScreenStatus = "Maximized"
            if self.maximizedSize is False:
                self.maxWidth = 0.95*maxWidth
                self.maxHeight = 0.95*maxHeight
            elif self.maximizedSize is True:
                self.maxWidth = self.maximizedWidth
                self.maxHeight = self.maximizedHeight
        elif self.fullScreenStatus == "Maximized":
            self.fullScreenStatus = "Minimized"
            if self.minimizedSize is False:
                self.maxWidth = 0.95*maxWidth
                self.maxHeight = 0.95*maxHeight
            elif self.minimizedSize is True:
                self.maxWidth = self.minimizedWidth
                self.maxHeight = self.minimizedHeight
    
    def updateExportVideo(self, videoPath):
        if videoPath[0] != '':
            self.exportVideo = True
            self.exportVideoPath = videoPath[0]
        else:
            self.exportVideo = False
            self.exportVideoPath = []
    
    def activateThread(self):
        self.threadActive = True

    def stopThread(self):
        self.threadActive = False  

    def run(self):
        if self.videoPath[0] != '':
            # 1. Initializing the video
            self.videoCapture = cv2.VideoCapture(self.videoPath[0])
            self.videoTotalFrames = int(self.videoCapture.get(cv2.CAP_PROP_FRAME_COUNT))
            self.videoCapture.set(cv2.CAP_PROP_POS_FRAMES, self.framenumber - 1)

            # 2. Video reading loop
            while self.threadActive is True:
                ret, frame = self.videoCapture.read()
                # print(int(self.videoCapture.get(cv2.CAP_PROP_POS_FRAMES)))

                # If no frame is found, then check if this is because of encoding issue (then pursue) or because of video end (then end the loop)             
                if ret is False:
                    if (self.framenumber >= self.videoTotalFrames):
                        self.framenumber = self.videoTotalFrames
                        self.frameNumberUpdate.emit(self.framenumber)
                        break
                    elif (self.framenumber < self.videoTotalFrames):
                        self.framenumber = self.framenumber + 1
                        self.frameNumberUpdate.emit(self.framenumber)
                
                # If frame is found then we process it
                elif ret is True:
                    # Frame has been succesfully loaded , so we can emit its number to update the slider
                    self.frameNumberUpdate.emit(self.framenumber)

                    # Frame shape params
                    height, width, layers = frame.shape
                    size = (width, height)

                    # Adding & Drawing information on image Frame
                    dataframe_Frame = self.dataframe.loc[self.dataframe.Frame == self.framenumber]
                    dataframe_Frame = dataframe_Frame.reset_index(drop=True)

                    if self.vizParams["drawCentroid"] is True:
                        if len(dataframe_Frame) > 0:
                            for i in range(len(dataframe_Frame)):
                                centerX = dataframe_Frame.loc[i, 'CentroidX']
                                centerY = dataframe_Frame.loc[i, 'CentroidY']
                                cv2.circle(
                                    img=frame,
                                    center=(centerX, centerY),
                                    radius=self.vizParams["centroidRadius"],
                                    color=(self.vizParams["centroidBlue"], self.vizParams["centroidGreen"], self.vizParams["centroidRed"]),
                                    thickness=self.vizParams["centroidThickness"]
                                    )
                    if self.vizParams["drawNBBox"] is True:
                        if len(dataframe_Frame) > 0:
                            for i in range(len(dataframe_Frame)):
                                bBoxTLX = dataframe_Frame.loc[i, 'Box_TLX']
                                bBoxTLY = dataframe_Frame.loc[i, 'Box_TLY']
                                bBoxBRX = dataframe_Frame.loc[i, 'Box_BRX']
                                bBoxBRY = dataframe_Frame.loc[i, 'Box_BRY']
                                cv2.rectangle(
                                    img=frame,
                                    pt1=(bBoxTLX, bBoxTLY),
                                    pt2=(bBoxBRX, bBoxBRY),
                                    color=(self.vizParams["nBBoxBlue"], self.vizParams["nBBoxGreen"], self.vizParams["nBBoxRed"]),
                                    thickness=self.vizParams["nBBoxThickness"]
                                    )
                    if self.vizParams["drawLBBox"] is True:
                        if len(dataframe_Frame) > 0:
                            for i in range(len(dataframe_Frame)):
                                lBoxTLX = dataframe_Frame.loc[i, 'lBox_TLX']
                                lBoxTLY = dataframe_Frame.loc[i, 'lBox_TLY']
                                lBoxBRX = dataframe_Frame.loc[i, 'lBox_BRX']
                                lBoxBRY = dataframe_Frame.loc[i, 'lBox_BRY']
                                cv2.rectangle(
                                    img=frame,
                                    pt1=(lBoxTLX, lBoxTLY),
                                    pt2=(lBoxBRX, lBoxBRY),
                                    color=(self.vizParams["lBBoxBlue"], self.vizParams["lBBoxGreen"], self.vizParams["lBBoxRed"]),
                                    thickness=self.vizParams["lBBoxThickness"]
                                    )
                    if self.vizParams["drawRBBox"] is True:
                        if len(dataframe_Frame) > 0:
                            for i in range(len(dataframe_Frame)):
                                rBoxTLX = dataframe_Frame.loc[i, 'rBox_TLX']
                                rBoxTLY = dataframe_Frame.loc[i, 'rBox_TLY']
                                rBoxTRX = dataframe_Frame.loc[i, 'rBox_TRX']
                                rBoxTRY = dataframe_Frame.loc[i, 'rBox_TRY']
                                rBoxBRX = dataframe_Frame.loc[i, 'rBox_BRX']
                                rBoxBRY = dataframe_Frame.loc[i, 'rBox_BRY']
                                rBoxBLX = dataframe_Frame.loc[i, 'rBox_BLX']
                                rBoxBLY = dataframe_Frame.loc[i, 'rBox_BLY']
                                cnt = np.array([
                                    [[rBoxTLX, rBoxTLY]],
                                    [[rBoxTRX, rBoxTRY]],
                                    [[rBoxBRX, rBoxBRY]],
                                    [[rBoxBLX, rBoxBLY]]
                                ])
                                rect = cv2.minAreaRect(cnt)
                                box = cv2.boxPoints(rect)
                                box = np.int0(box)
                                cv2.drawContours(
                                    image=frame,
                                    contours=[box],
                                    contourIdx=0,
                                    color=(self.vizParams["rBBoxBlue"], self.vizParams["rBBoxGreen"], self.vizParams["rBBoxRed"]),
                                    thickness=self.vizParams["rBBoxThickness"]
                                    )
                    
                    if self.vizParams["drawContours"] is True:
                        if len(dataframe_Frame) > 0:
                            for i in range(len(dataframe_Frame)):
                                contour = dataframe_Frame.loc[i, 'Contours']
                                cv2.drawContours(
                                    image=frame,
                                    contours=[contour],
                                    contourIdx=0,
                                    color=(self.vizParams["contoursBlue"], self.vizParams["contoursGreen"], self.vizParams["contoursRed"]),
                                    thickness=self.vizParams["contoursThickness"]
                                )

                    if (self.vizParams["drawTrackingIDs"] is True) or (self.vizParams["drawClassification"] is True):
                        if len(dataframe_Frame) > 0:
                            for i in range(len(dataframe_Frame)):
                                lBoxTLX = dataframe_Frame.loc[i, 'lBox_TLX']
                                lBoxTLY = dataframe_Frame.loc[i, 'lBox_TLY']
                                lBoxBRX = dataframe_Frame.loc[i, 'lBox_BRX']
                                lBoxBRY = dataframe_Frame.loc[i, 'lBox_BRY']
                                trackingID = dataframe_Frame.loc[i, 'ID']
                                classification = dataframe_Frame.loc[i, 'Label']
                                text_X = lBoxTLX if lBoxTLX + 40 < frame.shape[1] else lBoxTLX - 40
                                text_Y = lBoxTLY - 5 if lBoxTLY > 40 else lBoxBRY + 45
                                if (self.vizParams["drawTrackingIDs"] == True) and (self.vizParams["drawClassification"] == False):
                                    trackingClassText = str(trackingID)
                                elif (self.vizParams["drawTrackingIDs"] == False) and (self.vizParams["drawClassification"] == True):
                                    trackingClassText = str(classification)
                                elif (self.vizParams["drawTrackingIDs"] == True) and (self.vizParams["drawClassification"] == True):
                                    trackingClassText = str(trackingID) + '|' + str(classification)
                                cv2.putText(
                                    img=frame,
                                    text=trackingClassText,
                                    org=(text_X, text_Y),
                                    fontFace=self.vizParams["trackingIDsFontFace"],
                                    fontScale=self.vizParams["trackingIDsFontScale"],
                                    color=(self.vizParams["trackingIDsBlue"], self.vizParams["trackingIDsGreen"], self.vizParams["trackingIDsRed"]),
                                    thickness=self.vizParams["trackingIDsThickness"]
                                    )
                    
                    # Scaling Image to the GUI display characteristics and send it to GUI to display
                    self.image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    self.imageQtFormat = QImage(self.image.data, self.image.shape[1], self.image.shape[0], QImage.Format_RGB888)
                    self.imageQtFormatScaled = self.imageQtFormat.scaled(self.maxWidth, self.maxHeight, Qt.KeepAspectRatio)
                    # On first video loading, emit image dimensions to rescale the QLabel accordingly, and scaleRatio for ROI matching on image
                    if (self.framenumber == 1) and (self.playingStatus is False) and (self.calculateScaleRatio is False):
                        if self.minimizedSize is False:
                            self.minimizedWidth = self.imageQtFormatScaled.width()
                            self.minimizedHeight = self.imageQtFormatScaled.height()
                            self.minimizedSize = True
                        self.frameDims.emit([self.imageQtFormatScaled.width(), self.imageQtFormatScaled.height()])
                        widthRatio = round(self.imageQtFormat.width() / self.imageQtFormatScaled.width(), 4)
                        heightRatio = round(self.imageQtFormat.height() / self.imageQtFormatScaled.height(), 4)
                        self.scaleRatio.emit([widthRatio, heightRatio])
                        self.calculateScaleRatio = True
                    # When Full Screen option has been changed, update the image and scaling ratio accordingly
                    if (self.fullScreenChanged is True):
                        if self.fullScreenStatus == "Maximized" and self.maximizedSize is False:
                            self.maximizedWidth = self.imageQtFormatScaled.width()
                            self.maximizedHeight = self.imageQtFormatScaled.height()
                            self.maximizedSize = True
                        self.frameDims.emit([self.imageQtFormatScaled.width(), self.imageQtFormatScaled.height()])
                        widthRatio = round(self.imageQtFormat.width() / self.imageQtFormatScaled.width(), 4)
                        heightRatio = round(self.imageQtFormat.height() / self.imageQtFormatScaled.height(), 4)
                        self.scaleRatio.emit([widthRatio, heightRatio])
                        self.fullScreenChanged = False
                    # Finally, emit the scaled image
                    self.frameImageUpdate.emit(self.imageQtFormatScaled)

                    # Store the frame
                    if (self.exportVideo is True) and (self.playingStatus is True):
                        self.img_array.append(frame)
                    
                    # Update the frame number
                    if (self.framenumber < self.videoTotalFrames):
                        self.framenumber = self.framenumber + 1
                    else:
                        break

                if self.playingStatus is False:
                    break
  
            self.videoCapture.release()
            
            # 3. Saving tracking Video
            if self.exportVideo is True:
                try:
                    size
                except NameError:
                    pass
                else:
                    fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
                    output = cv2.VideoWriter(self.exportVideoPath, fourcc, self.videoFPS, size)
                    for i in range(len(self.img_array)):
                        output.write(self.img_array[i])
                    output.release()
            self.exportVideo = False
            self.exportVideoPath = []
            self.img_array = []  # reinitializing the storage of images once video saved
            
            # 4. Sending signal that video is ended
            self.videoEnded.emit(True)
        
        self.threadActive = False
        self.playingStatus = False
