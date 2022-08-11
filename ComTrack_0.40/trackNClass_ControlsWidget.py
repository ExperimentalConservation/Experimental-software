from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from bs4 import BeautifulSoup
import os

from trackNClass_ControlsWidget_FileControls import TrackNClass_FileControlsWidget
from trackNClass_ControlsWidget_ArenaControls import TrackNClass_ArenaControlsWidget
from trackNClass_ControlsWidget_ImageSmoothingControls import TrackNClass_ImageSmoothingControlsWidget
from trackNClass_ControlsWidget_DetectionsControls import TrackNClass_DetectionsControlsWidget
from trackNClass_ControlsWidget_OutputControls import TrackNClass_OutputControlsWidget
from trackNClass_ControlsWidget_TrackingControls import TrackNClass_TrackingControlsWidget
from trackNClass_ControlsWidget_ClassifierControls import TrackNClass_ClassifierControlsWidget
from trackNClass_ControlsWidget_LoadSaveControls import TrackNClass_LoadSaveControlsWidget
from functions_ControlsAnnotator import getControlsAnnotations


class TrackNClass_ControlsWidget(QWidget):
    videoPath = pyqtSignal(object)

    drawArena = pyqtSignal(bool)
    saveArena = pyqtSignal(bool)
    cancelArena = pyqtSignal(bool)

    objectBBtoTrackDefine = pyqtSignal(bool)
    objectBBtoTrackSave = pyqtSignal(bool)
    objectBBtoTrackCancel = pyqtSignal(bool)

    smoothingControls = pyqtSignal(object)
    detectionControls = pyqtSignal(object)
    trackingControls = pyqtSignal(object)
    classifierControls = pyqtSignal(object)
    outputControls = pyqtSignal(object)
    startImageProcessing = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.initWidget()
        self.makeScrollArea()
        self.makeInsideWidget()
        self.makeFileControls()
        self.makeArenaControls()
        self.makeLoadSaveControls()
        self.makeImageSmoothingControls()
        self.makeDetectionsControls()
        self.makeTrackingControls()
        self.makeClassifierControls()
        self.makeOutputControls()
        self.makeApplyAndRunButton()
    
    def initWidget(self):
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(5, 5, 5, 5)
        self.mainLayout.setAlignment(Qt.AlignTop)

    def makeScrollArea(self):
        self.controlsScrollArea = QScrollArea()
        self.controlsScrollArea.setFrameShape(QFrame.NoFrame)
        self.controlsScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.controlsScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.controlsScrollArea.setWidgetResizable(True)  
        self.mainLayout.addWidget(self.controlsScrollArea)
    
    def makeInsideWidget(self):
        self.insideWidget = QWidget()
        self.insideWidgetLayout = QGridLayout(self.insideWidget)
        self.insideWidgetLayout.setContentsMargins(0, 0, 0, 0)
        self.insideWidgetLayout.setRowStretch(0, 0)
        self.insideWidgetLayout.setRowStretch(1, 0)
        self.insideWidgetLayout.setRowStretch(2, 1)
        self.insideWidgetLayout.setRowStretch(3, 1)
        self.insideWidgetLayout.setRowStretch(4, 1)
        self.insideWidgetLayout.setRowStretch(5, 0)
        self.insideWidgetLayout.setRowStretch(6, 1)
        self.insideWidgetLayout.setAlignment(Qt.AlignTop)
        self.controlsScrollArea.setWidget(self.insideWidget)

    def makeFileControls(self):
        self.fileControlsWidget = TrackNClass_FileControlsWidget()
        self.insideWidgetLayout.addWidget(self.fileControlsWidget, 0, 0, 1, 1)
        self.fileControlsWidget.videoPath.connect(self.videoLoading)

    def makeArenaControls(self):
        self.arenaControlsWidget = TrackNClass_ArenaControlsWidget()
        self.arenaControlsWidget.setEnabled(False)
        self.insideWidgetLayout.addWidget(self.arenaControlsWidget, 0, 1, 1, 1)
        self.arenaControlsWidget.isArenaDrawed.connect(self.arenaBBDrawing)
        self.arenaControlsWidget.isArenaSaved.connect(self.arenaBBSaving)
        self.arenaControlsWidget.isArenaCancelled.connect(self.arenaBBCancelling)
    
    def makeLoadSaveControls(self):
        self.loadSaveControlsWidget = TrackNClass_LoadSaveControlsWidget()
        self.loadSaveControlsWidget.setEnabled(False)
        self.loadSaveControlsWidget.loadControlsSignal.connect(self.loadControls)
        self.loadSaveControlsWidget.saveControlsSignal.connect(self.saveControls)
        self.loadSaveControlsWidget.setEnabled(True)
        self.insideWidgetLayout.addWidget(self.loadSaveControlsWidget, 1, 0, 1, 2)
    
    def makeImageSmoothingControls(self):
        self.imageSmoothingControlsWidget = TrackNClass_ImageSmoothingControlsWidget()
        self.imageSmoothingControlsWidget.setEnabled(False)
        self.insideWidgetLayout.addWidget(self.imageSmoothingControlsWidget, 2, 0, 1, 2)
    
    def makeDetectionsControls(self):
        self.detectionsControlsWidget = TrackNClass_DetectionsControlsWidget()
        self.detectionsControlsWidget.setEnabled(False)
        self.insideWidgetLayout.addWidget(self.detectionsControlsWidget, 3, 0, 1, 2)
        self.detectionsControlsWidget.defineObjectBB.connect(self.objectBBDrawing)
        self.detectionsControlsWidget.saveObjectBB.connect(self.objectBBSaving)
        self.detectionsControlsWidget.cancelObjectBB.connect(self.objectBBCancelling)
        self.detectionsControlsWidget.detectionMethodSelected.connect(self.updateTrackingMethods)
    
    def makeTrackingControls(self):
        self.trackingControlsWidget = TrackNClass_TrackingControlsWidget()
        self.trackingControlsWidget.setEnabled(False)
        self.insideWidgetLayout.addWidget(self.trackingControlsWidget, 4, 0, 1, 2)
    
    def makeClassifierControls(self):
        self.classifierControlsWidget = TrackNClass_ClassifierControlsWidget()
        self.classifierControlsWidget.setEnabled(False)
        self.insideWidgetLayout.addWidget(self.classifierControlsWidget, 5, 0, 1, 2)
    
    def makeOutputControls(self):
        self.outputControlsWidget = TrackNClass_OutputControlsWidget()
        self.outputControlsWidget.setEnabled(False)
        self.insideWidgetLayout.addWidget(self.outputControlsWidget, 6, 0, 1, 2)
    
    def makeApplyAndRunButton(self):
        self.applyAndRunButton = QPushButton("APPLY && RUN")
        self.applyAndRunButton.setEnabled(False)
        self.applyAndRunButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.applyAndRunButton.clicked.connect(self.applyAndRun)
        self.mainLayout.addWidget(self.applyAndRunButton)

    def videoLoading(self, videoPath):
        self.videoPath.emit(videoPath)
        # # Un-comment the following if willing to reset all controls when new video is loaded
        # self.arenaControlsWidget.newVideoLoaded()
        # self.imageSmoothingControlsWidget.newVideoLoaded()
        # self.detectionsControlsWidget.newVideoLoaded()
        # self.trackingControlsWidget.newVideoLoaded()
        # self.classifierControlsWidget.newVideoLoaded()
        # self.outputControlsWidget.newVideoLoaded()
        # # end of the commented part
        if videoPath[0] != '':
            self.arenaControlsWidget.setEnabled(True)
            self.loadSaveControlsWidget.setEnabled(True)
            self.imageSmoothingControlsWidget.setEnabled(True)
            self.detectionsControlsWidget.setEnabled(True)
            self.trackingControlsWidget.setEnabled(True)
            self.classifierControlsWidget.setEnabled(True)
            self.outputControlsWidget.setEnabled(True)
            self.applyAndRunButton.setEnabled(True)
        if videoPath[0] == '':
            # # Un-comment the following if willing to reset the controls when now video is loaded
            # self.arenaControlsWidget.newVideoLoaded()
            # self.imageSmoothingControlsWidget.newVideoLoaded()
            # self.detectionsControlsWidget.newVideoLoaded()
            # self.trackingControlsWidget.newVideoLoaded()
            # self.classifierControlsWidget.newVideoLoaded()
            # self.outputControlsWidget.newVideoLoaded()
            # # end of this test code
            self.arenaControlsWidget.setEnabled(False)
            self.loadSaveControlsWidget.setEnabled(False)
            self.imageSmoothingControlsWidget.setEnabled(False)
            self.detectionsControlsWidget.setEnabled(False)
            self.trackingControlsWidget.setEnabled(False)
            self.classifierControlsWidget.setEnabled(False)
            self.outputControlsWidget.setEnabled(False)
            self.applyAndRunButton.setEnabled(False)

    def videoPlayStatusUpdate(self, videoPlayingStatus):
        if videoPlayingStatus is False:
            self.fileControlsWidget.setEnabled(True)
            self.arenaControlsWidget.setEnabled(True)
            self.loadSaveControlsWidget.setEnabled(True)
            self.imageSmoothingControlsWidget.setEnabled(True)
            self.detectionsControlsWidget.setEnabled(True)
            self.trackingControlsWidget.setEnabled(True)
            self.classifierControlsWidget.setEnabled(True)
            self.outputControlsWidget.setEnabled(True)
            self.applyAndRunButton.setEnabled(True)
        else:
            self.fileControlsWidget.setEnabled(False)
            self.arenaControlsWidget.setEnabled(False)
            self.loadSaveControlsWidget.setEnabled(False)
            self.imageSmoothingControlsWidget.setEnabled(False)
            self.detectionsControlsWidget.setEnabled(False)
            self.trackingControlsWidget.setEnabled(False)
            self.classifierControlsWidget.setEnabled(False)
            self.outputControlsWidget.setEnabled(False)
            self.applyAndRunButton.setEnabled(False)

    def arenaBBDrawing(self):
        self.drawArena.emit(True)
        self.fileControlsWidget.setEnabled(False)
        self.loadSaveControlsWidget.setEnabled(False)
        self.imageSmoothingControlsWidget.setEnabled(False)
        self.detectionsControlsWidget.setEnabled(False)
        self.trackingControlsWidget.setEnabled(False)
        self.classifierControlsWidget.setEnabled(False)
        self.outputControlsWidget.setEnabled(False)
        self.applyAndRunButton.setEnabled(False)
    
    def arenaBBSaving(self):
        self.saveArena.emit(True)
        self.fileControlsWidget.setEnabled(True)
        self.loadSaveControlsWidget.setEnabled(True)
        self.imageSmoothingControlsWidget.setEnabled(True)
        self.detectionsControlsWidget.setEnabled(True)
        self.trackingControlsWidget.setEnabled(True)
        self.classifierControlsWidget.setEnabled(True)
        self.outputControlsWidget.setEnabled(True)
        self.applyAndRunButton.setEnabled(True)
    
    def arenaBBCancelling(self):
        self.cancelArena.emit(True)
        self.fileControlsWidget.setEnabled(True)
        self.loadSaveControlsWidget.setEnabled(True)
        self.imageSmoothingControlsWidget.setEnabled(True)
        self.detectionsControlsWidget.setEnabled(True)
        self.trackingControlsWidget.setEnabled(True)
        self.classifierControlsWidget.setEnabled(True)
        self.outputControlsWidget.setEnabled(True)
        self.applyAndRunButton.setEnabled(True)

    def objectBBDrawing(self):
        self.objectBBtoTrackDefine.emit(True)
        self.fileControlsWidget.setEnabled(False)
        self.arenaControlsWidget.setEnabled(False)
        self.loadSaveControlsWidget.setEnabled(False)
        self.imageSmoothingControlsWidget.setEnabled(False)
        self.trackingControlsWidget.setEnabled(False)
        self.classifierControlsWidget.setEnabled(False)
        self.outputControlsWidget.setEnabled(False)
        self.applyAndRunButton.setEnabled(False)
    
    def objectBBSaving(self):
        self.objectBBtoTrackSave.emit(True)
        self.fileControlsWidget.setEnabled(True)
        self.arenaControlsWidget.setEnabled(True)
        self.loadSaveControlsWidget.setEnabled(True)
        self.imageSmoothingControlsWidget.setEnabled(True)
        self.trackingControlsWidget.setEnabled(True)
        self.classifierControlsWidget.setEnabled(True)
        self.outputControlsWidget.setEnabled(True)
        self.applyAndRunButton.setEnabled(True)
    
    def objectBBCancelling(self):
        self.objectBBtoTrackCancel.emit(True)
        self.fileControlsWidget.setEnabled(True)
        self.arenaControlsWidget.setEnabled(True)
        self.loadSaveControlsWidget.setEnabled(True)
        self.imageSmoothingControlsWidget.setEnabled(True)
        self.trackingControlsWidget.setEnabled(True)
        self.classifierControlsWidget.setEnabled(True)
        self.outputControlsWidget.setEnabled(True)
        self.applyAndRunButton.setEnabled(True)
    
    def updateVideoTotalFrames(self, videoTotalFrames):
        self.videoTotalFrames = videoTotalFrames - 1  # We prevent last frame to being tracked because last frame can cause issue in OpenCV
        self.outputControlsWidget.updateVideoTotalFrames(self.videoTotalFrames)

    def updateVideoFPS(self, videoFPS):
        self.videoFPS = videoFPS
        self.outputControlsWidget.updateVideoFPS(self.videoFPS)

    def updateVideoDuration(self, videoDuration):
        self.videoDuration = videoDuration
        self.outputControlsWidget.updateVideoDuration(self.videoDuration)
    
    def updateTrackingMethods(self, method):
        self.trackingControlsWidget.updateTrackingMethods(method)
    
    def applyAndRun(self):
        self.applyAndRunButton.setEnabled(False)
        self.smoothingControls.emit(self.imageSmoothingControlsWidget)
        self.detectionControls.emit(self.detectionsControlsWidget)
        self.trackingControls.emit(self.trackingControlsWidget)
        self.classifierControls.emit(self.classifierControlsWidget)
        self.outputControls.emit(self.outputControlsWidget)
        startingFrame = self.outputControlsWidget.outputStartFrame.value()
        self.startImageProcessing.emit(startingFrame)

    def loadControls(self, filepath):
        self.imageSmoothingControlsWidget.newVideoLoaded()
        self.detectionsControlsWidget.newVideoLoaded()
        self.trackingControlsWidget.newVideoLoaded()
        controls = open(filepath[0]).read()
        controlsSoup = BeautifulSoup(controls, features="lxml")
        for smoothingSoup in controlsSoup.find_all("smoothing_method"):
            if (smoothingSoup.find("smoothingname").string != "None"):
                self.imageSmoothingControlsWidget.loadSmoothingParamsFromSavedControls(smoothingSoup)
        
        for detectionSoup in controlsSoup.find_all("detection_params"):
            if (detectionSoup.find("detection_method").string != "None"):
                self.detectionsControlsWidget.loadDetectionParamsFromSavedControls(detectionSoup)
        
        for trackingSoup in controlsSoup.find_all("tracking_params"):
            if (trackingSoup.find("tracking_method").string != "None"):
                self.trackingControlsWidget.loadTrackingParamsFromSavedControls(trackingSoup)

    def saveControls(self, filepath):
        self.controlsAnnotation = getControlsAnnotations(self.imageSmoothingControlsWidget, self.detectionsControlsWidget, self.trackingControlsWidget)
        if os.path.exists(filepath[0]):
            os.remove(filepath[0])
        tfile = open(filepath[0], 'a')
        tfile.write(str(self.controlsAnnotation))
        tfile.close()
