from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os


class Home_TrackNClassWidget(QFrame):

    def __init__(self):
        super().__init__()
        self.initWidget()
        self.makeTitle()
        self.makeImage()

    def initWidget(self):
        self.setStyleSheet("""
                QFrame{background-color: #f7f3e4; border: 1px solid black; border-radius: 5px;}
                QFrame:hover{background-color: #fff5cf;}
                QLabel{background-color: rgba(0, 0, 0, 0); border: 0px solid black;}
                QLabel:hover{background-color: rgba(0, 0, 0, 0);}
                """)
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setAlignment(Qt.AlignCenter)
        
    def makeTitle(self):
        self.trackNClassTitle = QLabel()
        self.trackNClassTitle.setText("TRACK & CLASSIFY")
        self.trackNClassTitle.setFont(QFont('Helvetica', 15, weight=QFont.Bold))
        self.mainLayout.addWidget(self.trackNClassTitle, alignment=Qt.AlignCenter)

    def makeImage(self):
        self.trackNClassImage = QLabel()
        self.trackNClassImage.setAlignment(Qt.AlignCenter)
        self.trackNClassImagePixmap = QPixmap(os.path.join(os.path.dirname(__file__), 'images/home/home_2.png'))
        self.trackNClassImagePixmap = self.trackNClassImagePixmap.scaled(int(self.trackNClassImage.width()/1.2), int(self.trackNClassImage.height()/1.2), Qt.KeepAspectRatio, Qt.FastTransformation)
        self.trackNClassImage.setPixmap(self.trackNClassImagePixmap)
        self.mainLayout.addWidget(self.trackNClassImage)