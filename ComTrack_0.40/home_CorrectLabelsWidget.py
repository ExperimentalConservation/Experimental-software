from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os


class Home_CorrectLabelsWidget(QFrame):

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
        self.correctLabelsTitle = QLabel()
        self.correctLabelsTitle.setText("T2. Correct ID & Labelling")
        self.correctLabelsTitle.setFont(QFont('Helvetica', 15, weight=QFont.Bold))
        self.mainLayout.addWidget(self.correctLabelsTitle, alignment=Qt.AlignCenter)

    def makeImage(self):
        self.correctLabelsImage = QLabel()
        self.correctLabelsImage.setAlignment(Qt.AlignCenter)
        self.correctLabelsImagePixmap = QPixmap(os.path.join(os.path.dirname(__file__), 'images/home/home_2.png'))
        self.correctLabelsImagePixmap = self.correctLabelsImagePixmap.scaled(int(self.correctLabelsImage.width()/1.2), int(self.correctLabelsImage.height()/1.2), Qt.KeepAspectRatio, Qt.FastTransformation)
        self.correctLabelsImage.setPixmap(self.correctLabelsImagePixmap)
        self.mainLayout.addWidget(self.correctLabelsImage)