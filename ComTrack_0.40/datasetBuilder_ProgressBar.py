from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os

class DatasetBuilder_ProgressBarWidget(QGroupBox):

    stopDatasetGenerationThread = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.setTitle("Progress Bar")
        self.setStyleSheet("""
                QGroupBox{font-weight: bold; border: 1px solid black; border-radius: 5px; margin-top: 0.6em;}
                QGroupBox::title{top: -0.5em; subcontrol-position: top center;}
                """)
        self.makeLayouts()
        self.makeProgressBar()
        self.makeBarText()


    def makeLayouts(self):
        self.mainLayout = QVBoxLayout(self)
        self.barLayout = QHBoxLayout()
        self.mainLayout.addLayout(self.barLayout)
        self.barTextLayout = QHBoxLayout()
        self.mainLayout.addLayout(self.barTextLayout)
    
    def makeProgressBar(self):
        # Progress Bar Label
        self.progressBarLabel = QLabel()
        self.progressBarLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.progressBarLabel.setText("Progress:")
        self.barLayout.addWidget(self.progressBarLabel)

        # Progress Bar
        self.progressBar = QProgressBar()
        self.progressBar.setAlignment(Qt.AlignCenter)
        self.progressBar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.barLayout.addWidget(self.progressBar)

        # Stop Button
        self.stopButton = QPushButton("Stop")
        self.stopButton.setEnabled(False)
        self.stopButton.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.stopButton.setIcon(QIcon(os.path.join(os.path.dirname(__file__), 'images/icons/stop.png')))
        self.stopButton.clicked.connect(self.stopDatasetGeneration)
        self.barLayout.addWidget(self.stopButton)
    
    def makeBarText(self):
        self.barText = QLabel()
        self.barText.setText("...")
        self.barTextLayout.addWidget(self.barText, alignment=Qt.AlignCenter)
    
    def stopDatasetGeneration(self):
        self.stopDatasetGenerationThread.emit(True)

    def updateTotalFramesToProcess(self, totalFramesToProcess):
        self.totalFramesToProcess = totalFramesToProcess
        self.progressBar.setRange(0, self.totalFramesToProcess)
        self.progressBar.setValue(0)
    
    def updateBarText(self, text):
        self.barText.setText(text)
        if (text != "...") and (text != "All images saved") and (text != "Dataset Generation Cancelled"):
            self.stopButton.setEnabled(True)
        else:
            self.stopButton.setEnabled(False)

    def updateCurrentFrame(self, currentFrame):
        self.progressBar.setValue(currentFrame)
        if currentFrame == self.totalFramesToProcess:
            self.stopButton.setEnabled(False)