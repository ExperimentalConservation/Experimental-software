from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os

class VideoTrack_FileControlsWidget(QGroupBox):

    videoPath = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.initWidget()
        self.makeButtons()
    
    def initWidget(self):
        self.setTitle("File Controls")
        self.setStyleSheet("""
                QGroupBox{font-weight: bold; border: 1px solid black; border-radius: 5px; margin-top: 0.6em;}
                QGroupBox::title{top: -0.5em; subcontrol-position: top center;}
                """)
        self.videoTrackFileControlsLayout = QVBoxLayout(self)
        self.videoTrackFileControlsLayout.setAlignment(Qt.AlignTop)  
    
    def makeButtons(self):
        # Load Button
        self.fileControlsLoadButton = QPushButton("Load Video")
        self.fileControlsLoadButton.setToolTip("No file selected")
        self.fileControlsLoadButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.fileControlsLoadButton.setIcon(QIcon(os.path.join(os.path.dirname(__file__), 'images/icons/load.png')))
        self.fileControlsLoadButton.clicked.connect(self.loadVideo)
        self.videoTrackFileControlsLayout.addWidget(self.fileControlsLoadButton, alignment=Qt.AlignTop)

    def loadVideo(self):
        self.selectedVideoPath = QFileDialog.getOpenFileName(self,'Open Video File', "", "Video files (*.mp4 *.avi *.mov)")
        self.videoPath.emit(self.selectedVideoPath)
        if self.selectedVideoPath[0] != '':
            self.fileControlsLoadButton.setToolTip(str(self.selectedVideoPath[0]))
        else:
            self.fileControlsLoadButton.setToolTip("No file selected")
    
    def enableVideoLoading(self):
        self.fileControlsLoadButton.setEnabled(True)

    def disableVideoLoading(self):
        self.fileControlsLoadButton.setEnabled(False)