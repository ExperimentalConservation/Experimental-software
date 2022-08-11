from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os

class VideoTrack_LoadSaveControlsWidget(QGroupBox):

    loadControlsSignal = pyqtSignal(object)
    saveControlsSignal = pyqtSignal(object)

    def __init__(self):
        super().__init__()

        # initializing variables with random values, which will be updated when upload video
        self.videoTotalFrames = 100
        self.videoFPS = 10
        self.videoDuration = 10

        # running initialisation functions
        self.initWidget()
        self.makeButtons()
    
    def initWidget(self):
        self.setTitle("Load && Save Controls")
        self.setStyleSheet("""
                QGroupBox{font-weight: bold; border: 1px solid black; border-radius: 5px; margin-top: 0.6em;}
                QGroupBox::title{top: -0.5em; subcontrol-position: top center;}
                """)
        self.mainLayout = QHBoxLayout(self)
        self.mainLayout.setAlignment(Qt.AlignTop)

    def makeButtons(self):
        self.loadControlsButton = QPushButton("Load Controls")
        self.loadControlsButton.setIcon(QIcon(os.path.join(os.path.dirname(__file__), 'images/icons/load.png')))
        self.loadControlsButton.setEnabled(True)
        self.loadControlsButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.loadControlsButton.clicked.connect(self.loadControls)
        self.mainLayout.addWidget(self.loadControlsButton)

        self.saveControlsButton = QPushButton("Save Controls")
        self.saveControlsButton.setIcon(QIcon(os.path.join(os.path.dirname(__file__), 'images/icons/export.png')))
        self.saveControlsButton.setEnabled(True)
        self.saveControlsButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.saveControlsButton.clicked.connect(self.saveControls)
        self.mainLayout.addWidget(self.saveControlsButton)

    def loadControls(self):
        self.loadControlsFilePath = QFileDialog.getOpenFileName(self,'Select Controls File', "", "Txt files (*.txt)")
        if self.loadControlsFilePath[0] != '':
            self.loadControlsButton.setToolTip(str(self.loadControlsFilePath[0]))
            self.loadControlsSignal.emit(self.loadControlsFilePath)
        else:
            self.loadControlsButton.setToolTip("No file selected")

    def saveControls(self):
        self.saveControlsFilePath = QFileDialog.getSaveFileName(self,'Save Controls File', "", "Txt files (*.txt)")
        if self.saveControlsFilePath[0] != '':
            self.saveControlsButton.setToolTip(str(self.saveControlsFilePath[0]))
            self.saveControlsSignal.emit(self.saveControlsFilePath)
        else:
            self.saveControlsButton.setToolTip("No file selected")
