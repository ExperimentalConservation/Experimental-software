from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os

class DatasetBuilder_ImageDisplayWidget(QGroupBox):

    def __init__(self):
        super().__init__()
        self.initWidget()
        self.makeDisplay()


    def initWidget(self):
        self.totalNumberAnnotations = 0
        self.speciesLabels = []
        self.setTitle("Image Display")
        self.setStyleSheet("""
                QGroupBox{font-weight: bold; border: 1px solid black; border-radius: 5px; margin-top: 0.6em;}
                QGroupBox::title{top: -0.5em; subcontrol-position: top center;}
                """)
        self.mainLayout = QHBoxLayout(self)
    
    def makeDisplay(self):
        # Display
        self.imageDisplay = QLabel()
        self.imageDisplay.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.mainLayout.addWidget(self.imageDisplay, alignment=Qt.AlignCenter)
