from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import pandas as pd

from correctLabels_ControlsWidget_FileControls import CorrectLabels_FileControlsWidget
from correctLabels_ControlsWidget_IDsControls import CorrectLabels_IDsControlsWidget

class CorrectLabels_ControlsWidget(QWidget):

    trackingData = pyqtSignal(object)
    rawVideoPath = pyqtSignal(object)
    exportVideoPath = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.initWidget()
        self.makeFileControls()
        self.makeIDsControls()
        self.makeSignalConnexions()
    
    def initWidget(self):
        self.correctLabels_ControlsWidgetLayout = QVBoxLayout(self)
        self.correctLabels_ControlsWidgetLayout.setContentsMargins(5, 5, 5, 5)
    
    def makeFileControls(self):
        self.correctLabels_fileControlsWidget = CorrectLabels_FileControlsWidget()
        self.correctLabels_ControlsWidgetLayout.addWidget(self.correctLabels_fileControlsWidget)
    
    def makeIDsControls(self):
        self.correctLabels_IDsControlsWidget = CorrectLabels_IDsControlsWidget()
        self.correctLabels_IDsControlsWidget.updatedDataframe.connect(self.updateDataframe)
        self.correctLabels_IDsControlsWidget.setEnabled(False)
        self.correctLabels_ControlsWidgetLayout.addWidget(self.correctLabels_IDsControlsWidget)
    
    def makeSignalConnexions(self):
        self.correctLabels_fileControlsWidget.trackingData.connect(self.trackingDataLoaded)
        self.correctLabels_fileControlsWidget.rawVideoPath.connect(self.rawVideoLoaded)
        self.correctLabels_fileControlsWidget.exportVideoPath.connect(self.exportTrackedVideo)
    
    def trackingDataLoaded(self, dataframe):
        self.correctLabels_IDsControlsWidget.loadTrackingData(dataframe)
        if isinstance(dataframe, pd.DataFrame):
            self.correctLabels_IDsControlsWidget.setEnabled(True)
            self.trackingData.emit(dataframe)
        else:
            self.correctLabels_IDsControlsWidget.setEnabled(False)
            self.rawVideoPath.emit([''])
            
    def rawVideoLoaded(self, rawVideoPath):
        self.rawVideoPath.emit(rawVideoPath)
    
    def exportTrackedVideo(self, outputVideoPath):
        self.exportVideoPath.emit(outputVideoPath)

    def updateDataframe(self, dataframe):
        self.correctLabels_fileControlsWidget.updateDataframe(dataframe)