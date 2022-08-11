from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from trackNClass_ControlsWidget import TrackNClass_ControlsWidget
from trackNClass_VideoWidget import TrackNClass_VideoWidget

class MainWidgetTrackNClass(QWidget):

    def __init__(self):
        super().__init__()
        self.minimizedSize = False
        self.maximizedSize = False
        self.initWidget()
        self.makeControlsWidget()
        self.makeVideoWidget()
        self.makeSignalConnections()
    
    def initWidget(self):
        self.mainLayout = QGridLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setAlignment(Qt.AlignTop)
        self.mainLayout.setColumnStretch(0, 1)
        self.mainLayout.setColumnStretch(1, 3)
    
    def makeControlsWidget(self):
        self.controlsWidget =  TrackNClass_ControlsWidget()
        self.mainLayout.addWidget(self.controlsWidget, 0, 0, 1, 1)
        
    def makeVideoWidget(self):
        self.videoWidget =  TrackNClass_VideoWidget()
        self.videoWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.mainLayout.addWidget(self.videoWidget, 0, 1, 1, 1)

    def makeSignalConnections(self):
        self.controlsWidget.videoPath.connect(self.videoLoadVideo)
        self.controlsWidget.drawArena.connect(self.videoWidget.videoDrawArena)
        self.controlsWidget.saveArena.connect(self.videoWidget.videoSaveArena)
        self.controlsWidget.cancelArena.connect(self.videoWidget.videoCancelArena)
        self.controlsWidget.objectBBtoTrackDefine.connect(self.videoWidget.videoDrawObjectBB)
        self.controlsWidget.objectBBtoTrackSave.connect(self.videoWidget.videoSaveObjectBB)
        self.controlsWidget.objectBBtoTrackCancel.connect(self.videoWidget.videoCancelObjectBB)
        self.controlsWidget.smoothingControls.connect(self.videoWidget.updateSmoothingControls)
        self.controlsWidget.detectionControls.connect(self.videoWidget.updateDetectionControls)
        self.controlsWidget.trackingControls.connect(self.videoWidget.updateTrackingControls)
        self.controlsWidget.classifierControls.connect(self.videoWidget.updateClassifierControls)
        self.controlsWidget.outputControls.connect(self.videoWidget.updateOutputControls)
        self.controlsWidget.startImageProcessing.connect(self.videoWidget.startImageProcessing)

        self.videoWidget.videoPlayStatus.connect(self.controlsWidget.videoPlayStatusUpdate)
        self.videoWidget.signalVideoTotalFrames.connect(self.controlsWidget.updateVideoTotalFrames)
        self.videoWidget.signalVideoFPS.connect(self.controlsWidget.updateVideoFPS)
        self.videoWidget.signalVideoDuration.connect(self.controlsWidget.updateVideoDuration)
        self.videoWidget.fullScreenSignal.connect(self.updateFullScreen)

    def videoLoadVideo(self, path):
        self.videoWidget.loadVideo(path)

    def updateFullScreen(self, signal):
        if signal == 0:
            if self.minimizedSize is True:
                self.videoWidget.setFixedSize(self.minimizedWidth, self.minimizedHeight)

            self.mainLayout.addWidget(self.controlsWidget, 0, 0, 1, 1)
            self.mainLayout.addWidget(self.videoWidget, 0, 1, 1, 1)
            self.controlsWidget.show()
    
        elif signal == 1:
            if self.minimizedSize is False:
                self.minimizedWidth = self.videoWidget.width()
                self.minimizedHeight = self.videoWidget.height()
                self.minimizedSize = True
            
            if self.maximizedSize is False:
                self.maximizedWidth = self.width()
                self.maximizedHeight = self.height()
                self.maximizedSize = True

            self.controlsWidget.hide()

            if self.maximizedSize is True:
                self.videoWidget.setFixedSize(self.maximizedWidth, self.maximizedHeight)

            self.mainLayout.addWidget(self.videoWidget, 0, 0, 1, 2)
