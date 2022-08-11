from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os

class Home_DatasetBuilderWidget(QFrame):

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
        self.datasetBuilderTitle = QLabel()
        self.datasetBuilderTitle.setText("T3. Generate Dataset")
        self.datasetBuilderTitle.setFont(QFont('Helvetica', 15, weight=QFont.Bold))
        self.mainLayout.addWidget(self.datasetBuilderTitle, alignment=Qt.AlignCenter)

    def makeImage(self):
        self.datasetBuilderImage = QLabel()
        self.datasetBuilderImage.setAlignment(Qt.AlignCenter)
        self.datasetBuilderImagePixmap = QPixmap(os.path.join(os.path.dirname(__file__), 'images/home/home_3.png'))
        self.datasetBuilderImagePixmap = self.datasetBuilderImagePixmap.scaled(int(self.datasetBuilderImage.width()/1.2), int(self.datasetBuilderImage.height()/1.2), Qt.KeepAspectRatio, Qt.FastTransformation)
        self.datasetBuilderImage.setPixmap(self.datasetBuilderImagePixmap)
        self.mainLayout.addWidget(self.datasetBuilderImage)