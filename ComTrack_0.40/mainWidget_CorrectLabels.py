from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from correctLabels_ControlsWidget import CorrectLabels_ControlsWidget
from correctLabels_VideoWidget import CorrectLabels_VideoWidget

class MainWidgetCorrectLabels(QWidget):

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
        self.controlsWidget = CorrectLabels_ControlsWidget()
        self.mainLayout.addWidget(self.controlsWidget, 0, 0, 1, 1)
    
    def makeVideoWidget(self):
        self.videoWidget = CorrectLabels_VideoWidget()
        self.videoWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.mainLayout.addWidget(self.videoWidget, 0, 1, 1, 1)
    
    def makeSignalConnections(self):
        self.controlsWidget.trackingData.connect(self.videoWidget.loadData)
        self.controlsWidget.rawVideoPath.connect(self.videoWidget.loadVideo)
        self.controlsWidget.exportVideoPath.connect(self.videoWidget.exportVideo)

        self.videoWidget.fullScreenSignal.connect(self.updateFullScreen)

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
