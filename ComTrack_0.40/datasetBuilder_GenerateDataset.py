from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os

class DatasetBuilder_GenerateDatasetWidget(QGroupBox):

    launchDatasetGeneration = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.setTitle("Generate Dataset")
        self.setStyleSheet("""
                QGroupBox{font-weight: bold; border: 1px solid black; border-radius: 5px; margin-top: 0.6em;}
                QGroupBox::title{top: -0.5em; subcontrol-position: top center;}
                """)
        self.makeLayouts()
        self.makeButton()


    def makeLayouts(self):
        self.mainLayout = QHBoxLayout(self)
    
    def makeButton(self):
        # Generate Button
        self.generateDatasetButton = QPushButton("Generate Dataset")
        self.generateDatasetButton.setEnabled(False)
        self.generateDatasetButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.generateDatasetButton.setIcon(QIcon(os.path.join(os.path.dirname(__file__), 'images/icons/play.png')))
        self.generateDatasetButton.clicked.connect(self.generateDataset)
        self.mainLayout.addWidget(self.generateDatasetButton)
    
    def updateStatus(self, signal):
        if signal is True:
            self.generateDatasetButton.setEnabled(True)
        else:
            self.generateDatasetButton.setEnabled(False)

    def generateDataset(self):
        self.launchDatasetGeneration.emit(True)
