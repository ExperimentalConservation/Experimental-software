from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os

class Home_ModelBuilderWidget(QFrame):

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
        self.modelBuilderTitle = QLabel()
        self.modelBuilderTitle.setText("T4. Build Classifier")
        self.modelBuilderTitle.setFont(QFont('Helvetica', 15, weight=QFont.Bold))
        self.mainLayout.addWidget(self.modelBuilderTitle, alignment=Qt.AlignCenter)

    def makeImage(self):
        self.modelBuilderImage = QLabel()
        self.modelBuilderImage.setAlignment(Qt.AlignCenter)
        self.modelBuilderImagePixmap = QPixmap(os.path.join(os.path.dirname(__file__), 'images/home/home_4.png'))
        self.modelBuilderImagePixmap = self.modelBuilderImagePixmap.scaled(int(self.modelBuilderImage.width()/1.2), int(self.modelBuilderImage.height()/1.2), Qt.KeepAspectRatio, Qt.FastTransformation)
        self.modelBuilderImage.setPixmap(self.modelBuilderImagePixmap)
        self.mainLayout.addWidget(self.modelBuilderImage)