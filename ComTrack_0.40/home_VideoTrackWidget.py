from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os


class Home_VideoTrackWidget(QFrame):

    def __init__(self):
        super().__init__()
        self.initWidget()
        self.makeTitle()
        self.makeImage()

    def initWidget(self):
        self.setStyleSheet("""
                QFrame{background-color: #f4fbfc; border: 1px solid black; border-radius: 5px;}
                QFrame:hover{background-color: #d7f6fa;}
                QLabel{background-color: rgba(0, 0, 0, 0); border: 0px solid black;}
                QLabel:hover{background-color: rgba(0, 0, 0, 0);}
                """)
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setAlignment(Qt.AlignCenter)
        
    def makeTitle(self):
        self.videoTrackTitle = QLabel()
        self.videoTrackTitle.setText("T1. Generate Detections")
        self.videoTrackTitle.setFont(QFont('Helvetica', 15, weight=QFont.Bold))
        self.mainLayout.addWidget(self.videoTrackTitle, alignment=Qt.AlignCenter)

    def makeImage(self):
        self.videoTrackImage = QLabel()
        self.videoTrackImage.setAlignment(Qt.AlignCenter)
        self.videoTrackImagePixmap = QPixmap(os.path.join(os.path.dirname(__file__), 'images/home/home_1.png'))
        self.videoTrackImagePixmap = self.videoTrackImagePixmap.scaled(int(self.videoTrackImage.width()/1.2), int(self.videoTrackImage.height()/1.2), Qt.KeepAspectRatio, Qt.FastTransformation)
        self.videoTrackImage.setPixmap(self.videoTrackImagePixmap)
        self.mainLayout.addWidget(self.videoTrackImage)