from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class VideoTrack_VideoDisplayWidget(QGroupBox):

    def __init__(self):
        super().__init__()
        self.initWidget()
        self.makeDisplay()

    def initWidget(self):
        self.setTitle("Video")
        self.setStyleSheet("""
                QGroupBox{font-weight: bold; border: 1px solid black; border-radius: 5px; margin-top: 0.6em;}
                QGroupBox::title{top: -0.5em; subcontrol-position: top center;}
                """)
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setAlignment(Qt.AlignCenter|Qt.AlignVCenter)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
    
    def makeDisplay(self):
        # Display
        self.videoDisplayImageLabel = QLabel()
        self.videoDisplayImageLabel.setText("No video loaded")
        self.videoDisplayImageLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.mainLayout.addWidget(self.videoDisplayImageLabel, alignment=Qt.AlignCenter)
