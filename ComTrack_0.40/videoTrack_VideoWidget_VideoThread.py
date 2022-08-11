from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import cv2
import numpy as np
import os
import pandas as pd

from functions_smoothing import applySmoothing
from functions_detectors import detectBSubAndThresh, detectSOBBandCSRT
from functions_trackers import trackKalmanFilter, trackSOBBandCSRT

class VideoTrack_VideoThread(QThread):
    frameImageUpdate = pyqtSignal(QImage)
    frameNumberUpdate = pyqtSignal(int)
    frameDims = pyqtSignal(object)
    scaleRatio = pyqtSignal(object)
    videoEnded = pyqtSignal(object)

    def __init__(self, videoPath, maxWidth, maxHeight):
        super().__init__()
        self.videoPath = videoPath
        self.maxWidth = 0.95*maxWidth
        self.maxHeight = 0.95*maxHeight
        self.threadActive = False
        self.calculateScaleRatio = False
        self.playingStatus = False
        self.imageProcessingStatus = False
        self.videoFPS = 1
        self.fullScreenChanged = False
        self.minimizedSize = False
        self.maximizedSize = False
        self.fullScreenStatus = "Minimized"
        self.initArenaParams()
        self.initObjectBBParams()
        self.initSmoothingParams()
        self.initDetectionParams()
        self.initTrackingParams()
        self.initOutputParams()
        self.initVizParams()
        self.initImgArray()
        self.initOutputData()
    
    def initArenaParams(self):
        self.drawArena = False
        self.arenaCoords = [0, 0, 0, 0]
    
    def updateArenaParams(self, drawArena, arenaCoords):
        self.drawArena = drawArena
        self.arenaCoords = arenaCoords

    def initObjectBBParams(self):
        self.drawObjectBB = False
        self.objectBBCoords = [0, 0, 0, 0]
    
    def updateObjectBBParams(self, drawObjectBB, objectBBCoords):
        self.drawObjectBB = drawObjectBB
        self.objectBBCoords = objectBBCoords

    def initSmoothingParams(self):
        smoothingParams1 = {
            "smoothingActivated": False,
            "smoothingType": "None",
            "smoothingAverageBlurKernel": 1,
            "smoothingAverageBlurBorderType": "BORDER_DEFAULT",
            "smoothingMedianBlurKernel": 1,
            "smoothingGaussianBlurKernel": 1,
            "smoothingGaussianBlurSigmaX": 0,
            "smoothingGaussianBlurSigmaY": 0,
            "smoothingGaussianBlurBorderType": "BORDER_DEFAULT",
            "smoothingBilateralFilterFilterSize": 5,
            "smoothingBilateralFilterSigmaColor": 150,
            "smoothingBilateralFilterSigmaSpace": 150,
            "smoothingBilateralFilterBorderType": "BORDER_DEFAULT"
        }
        smoothingParams2 = smoothingParams1.copy()
        smoothingParams3 = smoothingParams1.copy()
        smoothingParams4 = smoothingParams1.copy()
        self.smoothingParams = [smoothingParams1, smoothingParams2, smoothingParams3, smoothingParams4]
    
    def updateSmoothingControls(self, smoothingControls):
        self.smoothingParams[0]["smoothingActivated"] = False
        self.smoothingParams[1]["smoothingActivated"] = False
        self.smoothingParams[2]["smoothingActivated"] = False
        self.smoothingParams[3]["smoothingActivated"] = False
        index = 0
        for item in smoothingControls.smoothingItemWidgets:
            try:
                smoothingmethod = item[1].smoothingItem.currentText()
                if smoothingmethod != "None":
                    self.smoothingParams[index]["smoothingActivated"] = True
                    self.smoothingParams[index]["smoothingType"] = item[1].smoothingItem.currentText()
                    self.smoothingParams[index]["smoothingAverageBlurKernel"] = int(item[1].smoothingAverageBlurKernelEntry.value())
                    self.smoothingParams[index]["smoothingAverageBlurBorderType"] = item[1].smoothingAverageBlurBorderTypeEntry.currentText()
                    self.smoothingParams[index]["smoothingMedianBlurKernel"] = int(item[1].smoothingMedianBlurKernelEntry.value())
                    self.smoothingParams[index]["smoothingGaussianBlurKernel"] = int(item[1].smoothingGaussianBlurKernelEntry.value())
                    self.smoothingParams[index]["smoothingGaussianBlurSigmaX"] = round(item[1].smoothingGaussianBlurSigmaXEntry.value(), 3)
                    self.smoothingParams[index]["smoothingGaussianBlurSigmaY"] = round(item[1].smoothingGaussianBlurSigmaYEntry.value(), 3)
                    self.smoothingParams[index]["smoothingGaussianBlurBorderType"] = item[1].smoothingGaussianBlurBorderTypeEntry.currentText()
                    self.smoothingParams[index]["smoothingBilateralFilterFilterSize"] = int(item[1].smoothingBilateralFilterFilterSizeEntry.value())
                    self.smoothingParams[index]["smoothingBilateralFilterSigmaColor"] = int(item[1].smoothingBilateralFilterSigmaColorEntry.value())
                    self.smoothingParams[index]["smoothingBilateralFilterSigmaSpace"] = int(item[1].smoothingBilateralFilterSigmaSpaceEntry.value())
                    self.smoothingParams[index]["smoothingBilateralFilterBorderType"] = item[1].smoothingBilateralFilterBorderTypeEntry.currentText()
                index += 1
            except:
                return
    
    def initDetectionParams(self):
        self.detectionParams = {
            "selectDetectionMethod": "None",
            "detectionMethodThresh_ThreshVal": 100,
            "detectionMethodThresh_MaxVal": 255,
            "detectionMethodThresh_Type": "THRESH_BINARY",
            "detectionMethodBackSub_BackSubMethod": "None",
            "backgroundSubtractionMethodKNNHistory": 20,
            "backgroundSubtractionMethodKNNThreshold": 2000,
            "backgroundSubtractionMethodKNNDetectShadows": False,
            "backgroundSubtractionMethodKNNShadowsValue": 127,
            "backgroundSubtractionMethodKNNShadowsThreshold": 0.5,
            "contoursDetectionMethod": "CHAIN_APPROX_SIMPLE",
            "contoursDetectionMode": "RETR_EXTERNAL",
            "contoursDetectionMinArea": 60,
            "contoursDetectionMaxArea": 5000,
            "detectionFeaturesPreLabelDetections": False,
            "detectionFeaturesPreLabelDetectionsEntry": "Species",
            "detectionFeaturesEnlargeBBoxes": False,
            "detectionFeaturesEnlargeBBoxesEntry": 25,
            "detectionFeaturesIgnoreOverlappingBBoxes": False,
            "detectionFeaturesIgnoreOverlappingBBoxesEntry": 0,
            "detectionFeaturesRemoveBG": False,
        }

    def updateDetectionControls(self, detectionControls):
        self.detectionParams["selectDetectionMethod"] = detectionControls.selectDetectionMethod.currentText()
        self.detectionParams["detectionMethodThresh_ThreshVal"] = int(detectionControls.detectionMethodThresh_ThreshVal.value())
        self.detectionParams["detectionMethodThresh_MaxVal"] = int(detectionControls.detectionMethodThresh_MaxVal.value())
        self.detectionParams["detectionMethodThresh_Type"] = detectionControls.detectionMethodThresh_Type.currentText()
        self.detectionParams["detectionMethodBackSub_BackSubMethod"] = detectionControls.detectionMethodBackSub_BackSubMethod.currentText()
        self.detectionParams["backgroundSubtractionMethodKNNHistory"] = int(detectionControls.backgroundSubtractionMethodKNNHistory.value())
        self.detectionParams["backgroundSubtractionMethodKNNThreshold"] = int(detectionControls.backgroundSubtractionMethodKNNThreshold.value())
        self.detectionParams["backgroundSubtractionMethodKNNDetectShadows"] = detectionControls.backgroundSubtractionMethodKNNDetectShadows.isChecked()
        self.detectionParams["backgroundSubtractionMethodKNNShadowsValue"] = int(detectionControls.backgroundSubtractionMethodKNNShadowsValue.value())
        self.detectionParams["backgroundSubtractionMethodKNNShadowsThreshold"] = round(detectionControls.backgroundSubtractionMethodKNNShadowsThreshold.value(), 2)
        self.detectionParams["contoursDetectionMethod"] = detectionControls.contoursDetectionMethod.currentText()
        self.detectionParams["contoursDetectionMode"] = detectionControls.contoursDetectionMode.currentText()
        self.detectionParams["contoursDetectionMinArea"] = int(detectionControls.contoursDetectionMinArea.value())
        self.detectionParams["contoursDetectionMaxArea"] = int(detectionControls.contoursDetectionMaxArea.value())
        self.detectionParams["detectionFeaturesPreLabelDetections"] = detectionControls.detectionFeaturesPreLabelDetections.isChecked()
        self.detectionParams["detectionFeaturesPreLabelDetectionsEntry"] = detectionControls.detectionFeaturesPreLabelDetectionsEntry.text()
        self.detectionParams["detectionFeaturesEnlargeBBoxes"] = detectionControls.detectionFeaturesEnlargeBBoxes.isChecked()
        self.detectionParams["detectionFeaturesEnlargeBBoxesEntry"] = int(detectionControls.detectionFeaturesEnlargeBBoxesEntry.value())
        self.detectionParams["detectionFeaturesIgnoreOverlappingBBoxes"] = detectionControls.detectionFeaturesIgnoreOverlappingBBoxes.isChecked()
        self.detectionParams["detectionFeaturesIgnoreOverlappingBBoxesEntry"] = round(detectionControls.detectionFeaturesIgnoreOverlappingBBoxesEntry.value(), 2)
        self.detectionParams["detectionFeaturesRemoveBG"] = detectionControls.detectionFeaturesRemoveBG.isChecked()
    
    def initTrackingParams(self):
        self.trackingParams = {
            "selectTrackingMethod": "None",
            "trackingMethodKalmanFilterParametersNoise": 1,
            "trackingMethodKalmanFilterParametersTimeStep": 0.01,
            "trackingMethodKalmanFilterParametersMaxDistance": 20000
        }
    
    def updateTrackingControls(self, trackingControls):
        self.trackingParams["selectTrackingMethod"] = trackingControls.selectTrackingMethod.currentText()
        self.trackingParams["trackingMethodKalmanFilterParametersNoise"] = trackingControls.trackingMethodKalmanFilterParametersNoise.value()
        self.trackingParams["trackingMethodKalmanFilterParametersTimeStep"] = trackingControls.trackingMethodKalmanFilterParametersTimeStep.value()
        self.trackingParams["trackingMethodKalmanFilterParametersMaxDistance"] = trackingControls.trackingMethodKalmanFilterParametersMaxDistance.value()
    
    def initOutputParams(self):
        self.outputParams = {
            "outputStartFrame": 0,
            "outputStopFrame": 0,
            "outputExportData": False,
            "outputDataFile": "None",
            "outputExportTrackedVideo": False,
            "outputTrackedVideoFile": "None",
            "outputExportnoBGVideo": False,
            "outputnoBGVideoFile": "None",
            "outputExportTrackednoBGVideo": False,
            "outputTrackednoBGVideoFile": "None"
        }
    
    def updateOutputControls(self, outputControls):
        self.startingFramenumber = outputControls.outputStartFrame.value()
        self.framenumber = outputControls.outputStartFrame.value()

        self.outputParams["outputStartFrame"] = outputControls.outputStartFrame.value()
        self.outputParams["outputStopFrame"] = outputControls.outputStopFrame.value()
        self.outputParams["outputExportData"] = outputControls.outputExportData.isChecked()
        if self.outputParams["outputExportData"] == True:
            if outputControls.outputDataPath[0] != "":
                self.outputParams["outputDataFile"] = outputControls.outputDataPath[0]
        self.outputParams["outputExportTrackedVideo"] = outputControls.outputExportTrackedVideo.isChecked()
        if self.outputParams["outputExportTrackedVideo"] == True:
            if outputControls.outputTrackedVideoPath[0] != "":
                self.outputParams["outputTrackedVideoFile"] = outputControls.outputTrackedVideoPath[0]
        self.outputParams["outputExportnoBGVideo"] = outputControls.outputExportnoBGVideo.isChecked()
        if self.outputParams["outputExportnoBGVideo"] == True:
            if outputControls.outputnoBGVideoPath[0] != "":
                self.outputParams["outputnoBGVideoFile"] = outputControls.outputnoBGVideoPath[0]
        self.outputParams["outputExportTrackednoBGVideo"] = outputControls.outputExportTrackednoBGVideo.isChecked()
        if self.outputParams["outputExportTrackednoBGVideo"] == True:
            if outputControls.outputTrackednoBGVideoPath[0] != "":
                self.outputParams["outputTrackednoBGVideoFile"] = outputControls.outputTrackednoBGVideoPath[0]

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
            "noBGFrame": False,
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
        self.vizParams["noBGFrame"] = params[34]

    def initImgArray(self):
        self.img_array = []
        self.img_array_noBG = []
        self.img_array_TrackednoBG = []  
    
    def initOutputData(self):
        # Loading the dataframe where data will be stored
        self.header_outputData = [
            'Frame',  # 0
            'ID',  # 1
            'CentroidX',  # 2
            'CentroidY',  # 3
            'Width',  # 4
            'Length',  # 5
            'Area',  # 6
            'Angle',  # 7
            'Box_TLX',  # 8
            'Box_TLY',  # 9
            'Box_BRX',  # 10
            'Box_BRY',  # 11
            'Box_W',  # 12
            'Box_H',  # 13
            'rBox_TLX',  # 14
            'rBox_TLY',  # 15
            'rBox_TRX',  # 16
            'rBox_TRY',  # 17
            'rBox_BRX',  # 18
            'rBox_BRY',  # 19
            'rBox_BLX',  # 20
            'rBox_BLY',  # 21
            'lBox_TLX',  # 22
            'lBox_TLY',  # 23
            'lBox_BRX',  # 24
            'lBox_BRY',  # 25
            'ContourXCoord',  # 26
            'ContourYCoord',  # 27
            'Contour',  # 28
            'Label'  # 29
        ]
        self.outputData = pd.DataFrame(columns=self.header_outputData)
    
    def updateImageProcessingStatus(self, status):
        self.imageProcessingStatus = status

    def updateFrameNumber(self, framenumber):
        self.framenumber = framenumber
    
    def updateStartingFrameNumber(self, framenumber):
        self.startingFramenumber = framenumber

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

    def activateThread(self):
        self.threadActive = True

    def stopThread(self):
        self.threadActive = False    

    def run(self):
        if self.videoPath[0] != '':
            # 1. Initializing the detection operators
            # 1.1. Init Background Subtractors
            if self.detectionParams["selectDetectionMethod"] == "Background Subtraction":
                if self.detectionParams["detectionMethodBackSub_BackSubMethod"] == "KNN":
                    backSub = cv2.createBackgroundSubtractorKNN(self.detectionParams["backgroundSubtractionMethodKNNHistory"], self.detectionParams["backgroundSubtractionMethodKNNThreshold"], self.detectionParams["backgroundSubtractionMethodKNNDetectShadows"])
                    backSub.setShadowValue(self.detectionParams["backgroundSubtractionMethodKNNShadowsValue"])
                    backSub.setShadowThreshold(self.detectionParams["backgroundSubtractionMethodKNNShadowsThreshold"])
                else:
                    backSub = "None"
            else:
                backSub = "None"
            
            # 2. Initializing the tracking operators
            if self.trackingParams["selectTrackingMethod"] != "None":
                # 2.1. Init CSRT tracker
                if self.trackingParams["selectTrackingMethod"] == "CSRT":
                    trackerCSRT = cv2.legacy.TrackerCSRT_create()
                # 2.1. Init Kalman Filter objects
                elif self.trackingParams["selectTrackingMethod"] == "Kalman Filter":
                    objets_points = []  # X_centroid, Y_centroid, object_width, object_length
                    objets_KF = []  # Objects from KF
                    object_IDs = []  # Objects identities
                    id_objet = 0  # start the identification of objects with the number 0 

            # 3. Initializing the video
            self.videoCapture = cv2.VideoCapture(self.videoPath[0])
            self.videoTotalFrames = int(self.videoCapture.get(cv2.CAP_PROP_FRAME_COUNT))
            self.videoCapture.set(cv2.CAP_PROP_POS_FRAMES, self.framenumber - 1)

            # 4. Video reading loop
            while self.threadActive is True:
                ret, frame = self.videoCapture.read()
                # print(self.framenumber)
                # print(int(self.videoCapture.get(cv2.CAP_PROP_POS_FRAMES)))
                # print(ret)
                
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
                    
                    # Creation of a frame copy on which to apply the smoothing effects, detector and tracker
                    frameCopy = frame.copy()
                    for smoothingParam in self.smoothingParams:
                        frameCopy = applySmoothing(frameCopy, smoothingParam)
                    
                    # Initializing the detection and tracking data of the current frame
                    detections = []
                    outputData_frame = []
                    if self.imageProcessingStatus is True:
                        # STEP 1: Detect the objects of interest in the frame
                        # step 1.1. If detection method is "Single Object Bounding Box"
                        if self.detectionParams["selectDetectionMethod"] == "Single Object Bounding Box":
                            # This detection method can only be updated if a tracker is also detected
                            if self.trackingParams["selectTrackingMethod"] == "None":
                                detections = self.objectBBCoords
                            elif self.trackingParams["selectTrackingMethod"] == "CSRT":
                                detections, trackerCSRT = detectSOBBandCSRT(self.framenumber, frameCopy, self.detectionParams, self.outputParams, self.arenaCoords, trackerCSRT, self.objectBBCoords)
                        # step 1.2. If detection method is "Thresholding"
                        elif (self.detectionParams["selectDetectionMethod"] == "Thresholding"):
                            detections, noBGFrame = detectBSubAndThresh(frameCopy, self.detectionParams, backSub, self.framenumber, self.startingFramenumber, self.arenaCoords)
                            if (self.outputParams["outputExportnoBGVideo"] is True) and (self.outputParams["outputnoBGVideoFile"] != "None"):
                                self.img_array_noBG.append(noBGFrame)
                        # step 1.3. If detection method is "Background Subtraction"
                        elif (self.detectionParams["selectDetectionMethod"] == "Background Subtraction"):
                            detections, noBGFrame = detectBSubAndThresh(frameCopy, self.detectionParams, backSub, self.framenumber, self.startingFramenumber, self.arenaCoords)
                            if (self.outputParams["outputExportnoBGVideo"] is True) and (self.outputParams["outputnoBGVideoFile"] != "None"):
                                self.img_array_noBG.append(noBGFrame)
                        # step 1.4. If no detection method
                        else:
                            detections = []


                        # STEP 2: Track the detected objects
                        if self.trackingParams["selectTrackingMethod"] == "CSRT":
                            self.outputData, outputData_frame = trackSOBBandCSRT(self.framenumber, detections, self.outputData, self.detectionParams, self.trackingParams, self.outputParams)
                        elif self.trackingParams["selectTrackingMethod"] == "Kalman Filter":
                            objets_points, objets_KF, object_IDs, id_objet, self.outputData, outputData_frame = trackKalmanFilter(self.framenumber, frameCopy, detections, objets_points, objets_KF, object_IDs, id_objet, self.outputData, self.detectionParams, self.trackingParams, self.outputParams)
                        else:
                            for detection in detections:
                                storage_temp = [self.framenumber, 0]  # Only one detection for SOOB and CSRT method, so only ID "0" in the tracked object
                                storage_temp.extend(detection)
                                storage_temp.insert(len(storage_temp), "Species")
                                outputData_frame.append(storage_temp)

                    # STEP 3: Adding & Drawing information on image Frame
                    if self.detectionParams["detectionFeaturesRemoveBG"] is True:
                        try:
                            noBGFrame
                        except:
                            allFrames = [frame]
                        else:
                            trackedNoBGFrame = noBGFrame.copy()
                            allFrames = [frame, trackedNoBGFrame]
                    else:
                        allFrames = [frame]

                    for singleFrame in allFrames:
                        if self.vizParams["drawCentroid"] is True:
                            if len(outputData_frame) > 0:
                                for id_obj in range(len(outputData_frame)):
                                    cv2.circle(
                                        img=singleFrame,
                                        center=(outputData_frame[id_obj][2], outputData_frame[id_obj][3]),
                                        radius=self.vizParams["centroidRadius"],
                                        color=(self.vizParams["centroidBlue"], self.vizParams["centroidGreen"], self.vizParams["centroidRed"]),
                                        thickness=self.vizParams["centroidThickness"]
                                        )
                        if self.vizParams["drawNBBox"] is True:
                            if len(outputData_frame) > 0:
                                for id_obj in range(len(outputData_frame)):
                                    cv2.rectangle(
                                        img=singleFrame,
                                        pt1=(outputData_frame[id_obj][8], outputData_frame[id_obj][9]),
                                        pt2=(outputData_frame[id_obj][10], outputData_frame[id_obj][11]),
                                        color=(self.vizParams["nBBoxBlue"], self.vizParams["nBBoxGreen"], self.vizParams["nBBoxRed"]),
                                        thickness=self.vizParams["nBBoxThickness"]
                                        )
                        if self.vizParams["drawLBBox"] is True:
                            if len(outputData_frame) > 0:
                                for id_obj in range(len(outputData_frame)):
                                    cv2.rectangle(
                                        img=singleFrame,
                                        pt1=(outputData_frame[id_obj][22], outputData_frame[id_obj][23]),
                                        pt2=(outputData_frame[id_obj][24], outputData_frame[id_obj][25]),
                                        color=(self.vizParams["lBBoxBlue"], self.vizParams["lBBoxGreen"], self.vizParams["lBBoxRed"]),
                                        thickness=self.vizParams["lBBoxThickness"]
                                        )
                        if self.vizParams["drawRBBox"] is True:
                            if len(outputData_frame) > 0:
                                for id_obj in range(len(outputData_frame)):
                                    cnt = np.array([
                                        [[outputData_frame[id_obj][14], outputData_frame[id_obj][15]]],
                                        [[outputData_frame[id_obj][16], outputData_frame[id_obj][17]]],
                                        [[outputData_frame[id_obj][18], outputData_frame[id_obj][19]]],
                                        [[outputData_frame[id_obj][20], outputData_frame[id_obj][21]]]
                                    ])
                                    rect = cv2.minAreaRect(cnt)
                                    box = cv2.boxPoints(rect)
                                    box = np.int0(box)
                                    cv2.drawContours(
                                        image=singleFrame,
                                        contours=[box],
                                        contourIdx=0,
                                        color=(self.vizParams["rBBoxBlue"], self.vizParams["rBBoxGreen"], self.vizParams["rBBoxRed"]),
                                        thickness=self.vizParams["rBBoxThickness"]
                                        )
                        
                        if self.vizParams["drawContours"] is True:
                            if len(outputData_frame) > 0:
                                for id_obj in range(len(outputData_frame)):
                                    contour = outputData_frame[id_obj][28]
                                    cv2.drawContours(
                                        image=singleFrame,
                                        contours=[contour],
                                        contourIdx=0,
                                        color=(self.vizParams["contoursBlue"], self.vizParams["contoursGreen"], self.vizParams["contoursRed"]),
                                        thickness=self.vizParams["contoursThickness"]
                                    )

                        if (self.vizParams["drawTrackingIDs"] is True) or (self.vizParams["drawClassification"] is True):
                            if len(outputData_frame) > 0:
                                for id_obj in range(len(outputData_frame)):
                                    text_X = outputData_frame[id_obj][22] if outputData_frame[id_obj][22] + 40 < frame.shape[1] else outputData_frame[id_obj][22] - 40
                                    text_Y = outputData_frame[id_obj][23] - 5 if outputData_frame[id_obj][23] > 40 else outputData_frame[id_obj][25] + 45
                                    if (self.vizParams["drawTrackingIDs"] == True) and (self.vizParams["drawClassification"] == False):
                                        trackingClassText = str(outputData_frame[id_obj][1])
                                    elif (self.vizParams["drawTrackingIDs"] == False) and (self.vizParams["drawClassification"] == True):
                                        trackingClassText = str(outputData_frame[id_obj][29])
                                    elif (self.vizParams["drawTrackingIDs"] == True) and (self.vizParams["drawClassification"] == True):
                                        trackingClassText = str(outputData_frame[id_obj][1]) + '|' + str(outputData_frame[id_obj][29])
                                    cv2.putText(
                                        img=singleFrame,
                                        text=trackingClassText,
                                        org=(text_X, text_Y),
                                        fontFace=self.vizParams["trackingIDsFontFace"],
                                        fontScale=self.vizParams["trackingIDsFontScale"],
                                        color=(self.vizParams["trackingIDsBlue"], self.vizParams["trackingIDsGreen"], self.vizParams["trackingIDsRed"]),
                                        thickness=self.vizParams["trackingIDsThickness"]
                                        )


                    # STEP 4: Scaling Image to the GUI display characteristics and send it to GUI to display
                    if (self.vizParams["noBGFrame"] is True) and (len(allFrames)>1):
                        displayFrame = allFrames[1]
                    else:
                        displayFrame = allFrames[0]
                    self.image = cv2.cvtColor(displayFrame, cv2.COLOR_BGR2RGB)
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


                    # STEP 6: Store the frame
                    if (self.outputParams["outputExportTrackedVideo"] is True) and (self.outputParams["outputTrackedVideoFile"] != "None"):
                        self.img_array.append(allFrames[0])
                    if (self.outputParams["outputExportTrackednoBGVideo"] is True) and (self.outputParams["outputTrackedVideoFile"] != "None") and (len(allFrames)>1):
                        self.img_array_TrackednoBG.append(allFrames[1])

                    # STEP 6: Update the frame number and end the loop if last frame is reached
                    if (self.framenumber < self.videoTotalFrames):
                        # If processing is activated and frame number lower than last frame to operate, then we update frame number, otherwise we end
                        if self.imageProcessingStatus is True:
                            if self.framenumber < self.outputParams["outputStopFrame"]:
                                self.framenumber = self.framenumber + 1
                            else:
                                break
                        # If no tracking activated, then we simply move to the next frame
                        else:
                            self.framenumber = self.framenumber + 1
                    else:
                        break
                
                if self.playingStatus is False:
                    break
            self.videoCapture.release()
            

            # 5. Saving tracking Video
            if (self.imageProcessingStatus is True) & (self.outputParams["outputExportTrackedVideo"] is True) & (self.outputParams["outputTrackedVideoFile"] != "None") & (len(self.img_array) > 0):
                try:
                    size
                except NameError:
                    pass
                else:
                    if os.path.exists(self.outputParams["outputTrackedVideoFile"]):
                        os.remove(self.outputParams["outputTrackedVideoFile"])
                    fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
                    output = cv2.VideoWriter(self.outputParams["outputTrackedVideoFile"], fourcc, self.videoFPS, size)
                    for i in range(len(self.img_array)):
                        output.write(self.img_array[i])
                    output.release()
            self.img_array = []  # reinitializing the storage of images once video saved

            if (self.imageProcessingStatus is True) & (self.outputParams["outputExportnoBGVideo"] is True) & (self.outputParams["outputnoBGVideoFile"] != "None") & (len(self.img_array_noBG) > 0):
                try:
                    size
                except NameError:
                    pass
                else:
                    if os.path.exists(self.outputParams["outputnoBGVideoFile"]):
                        os.remove(self.outputParams["outputnoBGVideoFile"])
                    fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
                    output = cv2.VideoWriter(self.outputParams["outputnoBGVideoFile"], fourcc, self.videoFPS, size)
                    for i in range(len(self.img_array_noBG)):
                        output.write(self.img_array_noBG[i])
                    output.release()
            self.img_array_noBG = []  # reinitializing the storage of images once video saved

            if (self.imageProcessingStatus is True) & (self.outputParams["outputExportTrackednoBGVideo"] is True) & (self.outputParams["outputTrackednoBGVideoFile"] != "None") & (len(self.img_array_TrackednoBG) > 0):
                try:
                    size
                except NameError:
                    pass
                else:
                    if os.path.exists(self.outputParams["outputTrackednoBGVideoFile"]):
                        os.remove(self.outputParams["outputTrackednoBGVideoFile"])
                    fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
                    output = cv2.VideoWriter(self.outputParams["outputTrackednoBGVideoFile"], fourcc, self.videoFPS, size)
                    for i in range(len(self.img_array_TrackednoBG)):
                        output.write(self.img_array_TrackednoBG[i])
                    output.release()
            self.img_array_TrackednoBG = []  # reinitializing the storage of images once video saved


            # 6. Saving tracking Data
            if (self.imageProcessingStatus is True) & (self.outputParams["outputExportData"] is True) & (self.outputParams["outputDataFile"] != "None") & (len(self.outputData) > 0):
                self.outputData = self.outputData.drop(labels='Contour', axis=1)
                self.outputData['Frame'] = self.outputData['Frame'].astype(int)
                self.outputData['ID'] = self.outputData['ID'].astype(int)
                self.outputData['CentroidX'] = self.outputData['CentroidX'].astype(int)
                self.outputData['CentroidY'] = self.outputData['CentroidY'].astype(int)
                self.outputData['Box_TLX'] = self.outputData['Box_TLX'].astype(int)
                self.outputData['Box_TLY'] = self.outputData['Box_TLY'].astype(int)
                self.outputData['Box_BRX'] = self.outputData['Box_BRX'].astype(int)
                self.outputData['Box_BRY'] = self.outputData['Box_BRY'].astype(int)
                self.outputData['Box_W'] = self.outputData['Box_W'].astype(int)
                self.outputData['Box_H'] = self.outputData['Box_H'].astype(int)
                self.outputData['rBox_TLX'] = self.outputData['rBox_TLX'].astype(int)
                self.outputData['rBox_TLY'] = self.outputData['rBox_TLY'].astype(int)
                self.outputData['rBox_TRX'] = self.outputData['rBox_TRX'].astype(int)
                self.outputData['rBox_TRY'] = self.outputData['rBox_TRY'].astype(int)
                self.outputData['rBox_BRX'] = self.outputData['rBox_BRX'].astype(int)
                self.outputData['rBox_BRY'] = self.outputData['rBox_BRY'].astype(int)
                self.outputData['rBox_BLX'] = self.outputData['rBox_BLX'].astype(int)
                self.outputData['rBox_BLY'] = self.outputData['rBox_BLY'].astype(int)
                self.outputData['lBox_TLX'] = self.outputData['lBox_TLX'].astype(int)
                self.outputData['lBox_TLY'] = self.outputData['lBox_TLY'].astype(int)
                self.outputData['lBox_BRX'] = self.outputData['lBox_BRX'].astype(int)
                self.outputData['lBox_BRY'] = self.outputData['lBox_BRY'].astype(int)
                self.outputData['ContourXCoord'] = self.outputData['ContourXCoord'].astype(str)
                self.outputData['ContourYCoord'] = self.outputData['ContourYCoord'].astype(str)
                self.outputData['Label'] = self.outputData['Label'].astype(str)
                if os.path.exists(self.outputParams["outputDataFile"]):
                    os.remove(self.outputParams["outputDataFile"])
                self.outputData.to_csv(self.outputParams["outputDataFile"], index = False, sep='\t')
                # tfile = open(self.outputParams["outputDataFile"], 'a')
                # tfile.write(self.outputData.to_string(index=False))
                # tfile.close()
            self.outputData = pd.DataFrame(columns=self.header_outputData)  # reinitializing the storage dataframe once saved

            # 7. Sending signal that video is ended
            self.videoEnded.emit(True)

        self.threadActive = False
        self.playingStatus = False
        self.detectionStatus = False
        self.trackingStatus = False  
