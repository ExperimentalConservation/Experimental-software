from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import numpy as np
import pandas as pd
import os

class CorrectLabels_FileControlsWidget(QGroupBox):

    trackingData = pyqtSignal(object)
    rawVideoPath = pyqtSignal(object)
    exportVideoPath = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.initWidget()
        self.makeButtons()
        self.dataframe = []
    
    def initWidget(self):
        self.setTitle("File Controls")
        self.setStyleSheet("""
                QGroupBox{font-weight: bold; border: 1px solid black; border-radius: 5px; margin-top: 0.6em;}
                QGroupBox::title{top: -0.5em; subcontrol-position: top center;}
                """)
        self.correctLabels_FileControlsLayout = QGridLayout(self)
        self.correctLabels_FileControlsLayout.setAlignment(Qt.AlignTop)  
    
    def makeButtons(self):
        # Load Tracking Data Button
        self.correctLabels_FileControlsLoadTrackingDataButton = QPushButton("Load Tracking Data", self)
        self.correctLabels_FileControlsLoadTrackingDataButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.correctLabels_FileControlsLoadTrackingDataButton.setIcon(QIcon(os.path.join(os.path.dirname(__file__), 'images/icons/load.png')))
        self.correctLabels_FileControlsLoadTrackingDataButton.clicked.connect(self.loadTrackingData)
        self.correctLabels_FileControlsLayout.addWidget(self.correctLabels_FileControlsLoadTrackingDataButton, 0, 0, 1, 1)

        # Load Raw Video Button
        self.correctLabels_FileControlsLoadRawVideoButton = QPushButton("Load Raw Video", self)
        self.correctLabels_FileControlsLoadRawVideoButton.setEnabled(False)
        self.correctLabels_FileControlsLoadRawVideoButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.correctLabels_FileControlsLoadRawVideoButton.setIcon(QIcon(os.path.join(os.path.dirname(__file__), 'images/icons/load.png')))
        self.correctLabels_FileControlsLoadRawVideoButton.clicked.connect(self.loadRawVideo)
        self.correctLabels_FileControlsLayout.addWidget(self.correctLabels_FileControlsLoadRawVideoButton, 1, 0, 1, 1)

        # Export Corrected Tracking Data Button
        self.correctLabels_FileControlsExportCorrectedTrackingDataButton = QPushButton("Export Corrected Data", self)
        self.correctLabels_FileControlsExportCorrectedTrackingDataButton.setEnabled(False)
        self.correctLabels_FileControlsExportCorrectedTrackingDataButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.correctLabels_FileControlsExportCorrectedTrackingDataButton.setIcon(QIcon(os.path.join(os.path.dirname(__file__), 'images/icons/export.png')))
        self.correctLabels_FileControlsExportCorrectedTrackingDataButton.clicked.connect(self.exportTrackingData)
        self.correctLabels_FileControlsLayout.addWidget(self.correctLabels_FileControlsExportCorrectedTrackingDataButton, 0, 1, 1, 1)

        self.correctLabels_FileControlsExportCorrectedTrackedVideoButton = QPushButton("Export Corrected Video", self)
        self.correctLabels_FileControlsExportCorrectedTrackedVideoButton.setEnabled(False)
        self.correctLabels_FileControlsExportCorrectedTrackedVideoButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.correctLabels_FileControlsExportCorrectedTrackedVideoButton.setIcon(QIcon(os.path.join(os.path.dirname(__file__), 'images/icons/export.png')))
        self.correctLabels_FileControlsExportCorrectedTrackedVideoButton.clicked.connect(self.exportTrackedVideo)
        self.correctLabels_FileControlsLayout.addWidget(self.correctLabels_FileControlsExportCorrectedTrackedVideoButton, 1, 1, 1, 1)
    
    def loadTrackingData(self):
        self.inputTrackingData_path = QFileDialog.getOpenFileName(self,'Open Tracking data', "", "Text files (*.txt)")
        if self.inputTrackingData_path[0] == '':
            self.correctLabels_FileControlsLoadRawVideoButton.setEnabled(False)
            self.correctLabels_FileControlsExportCorrectedTrackingDataButton.setEnabled(False)
            self.correctLabels_FileControlsExportCorrectedTrackedVideoButton.setEnabled(False)
            self.dataframe = []
        elif self.inputTrackingData_path[0] != '':
            self.correctLabels_FileControlsLoadRawVideoButton.setEnabled(True)
            self.correctLabels_FileControlsExportCorrectedTrackingDataButton.setEnabled(True)
            self.correctLabels_FileControlsLoadTrackingDataButton.setToolTip(str(self.inputTrackingData_path[0]))
            self.correctLabels_SelectedIDs = []
            # self.dataframe = pd.read_csv(self.inputTrackingData_path[0], sep=r'\s{1,}', engine='python')
            self.dataframe = pd.read_csv(self.inputTrackingData_path[0], sep='\t', engine='python')
            allContours = []
            for i in range(len(self.dataframe)):
                contourXCoord = self.dataframe.loc[i, 'ContourXCoord']
                contourXCoord = contourXCoord.replace("[","")
                contourXCoord = contourXCoord.replace("]","")
                contourXCoord = contourXCoord.split(", ")
                contourXCoord = [int(x) for x in contourXCoord]
                contourYCoord = self.dataframe.loc[i, 'ContourYCoord']
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
            self.dataframe['Contours'] = allContours

        self.trackingData.emit(self.dataframe)

    def loadRawVideo(self):
        self.selectedVideoPath = QFileDialog.getOpenFileName(self,'Open Video File', "", "Video files (*.mp4 *.avi *.mov)")
        if self.selectedVideoPath[0] == '':
            self.correctLabels_FileControlsExportCorrectedTrackedVideoButton.setEnabled(False)
        elif self.selectedVideoPath[0] != '':
            self.correctLabels_FileControlsExportCorrectedTrackedVideoButton.setEnabled(True)
            self.correctLabels_FileControlsLoadRawVideoButton.setToolTip(str(self.selectedVideoPath[0]))
        self.rawVideoPath.emit(self.selectedVideoPath)
    
    def exportTrackingData(self):
        self.outputTrackingData_path = QFileDialog.getSaveFileName(self,'Save Data File', "", "Text files (*.txt)")
        if self.outputTrackingData_path[0] != '':
            if os.path.exists(self.outputTrackingData_path[0]):
                os.remove(self.outputTrackingData_path[0])
            exportDataframe = self.dataframe.copy()
            exportDataframe = exportDataframe.drop(labels='Contours', axis=1)
            exportDataframe.to_csv(self.outputTrackingData_path[0], index = False, sep='\t')
            # tfile = open(self.outputTrackingData_path[0], 'a')
            # tfile.write(self.dataframe.to_string(index=False))
            # tfile.close()
    
    def exportTrackedVideo(self):
        self.outputTrackedVideo_path = QFileDialog.getSaveFileName(self,'Save Video File', "", "Video files (*.avi)")
        if self.outputTrackedVideo_path[0] != '':
            if os.path.exists(self.outputTrackedVideo_path[0]):
                os.remove(self.outputTrackedVideo_path[0])
        self.exportVideoPath.emit(self.outputTrackedVideo_path)
    
    def enableButtons(self):
        self.correctLabels_FileControlsLoadTrackingDataButton.setEnabled(True)
        self.correctLabels_FileControlsLoadRawVideoButton.setEnabled(True)

    def disableButtons(self):
        self.correctLabels_FileControlsLoadRawVideoButton.setEnabled(False)
        self.correctLabels_FileControlsLoadTrackingDataButton.setEnabled(False)
    
    def updateDataframe(self, dataframe):
        if isinstance(self.dataframe, pd.DataFrame):
            self.dataframe = dataframe