from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os

class TrackNClass_ClassifierControlsWidget(QGroupBox):

    def __init__(self):
        super().__init__()
        self.setCheckable(True)
        self.setChecked(False)
        self.toggled.connect(self.classifierControlsChecked)
        self.setTitle("Classifier Controls")
        self.setStyleSheet("""
                QGroupBox{font-weight: bold; border: 1px solid black; border-radius: 5px; margin-top: 0.6em;}
                QGroupBox::title{top: -0.5em; subcontrol-position: top center;}
                """)
        self.makeVariables()
        self.makeLayouts()
        self.makeButtons()
        self.makeEntries()

    def makeVariables(self):
        self.selectedClassifierPath = ['','']
        self.selectedLabelsPath = ['','']
    
    def makeLayouts(self):
        # Main Layout
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setAlignment(Qt.AlignTop)

        # Buttons Layout
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.setAlignment(Qt.AlignTop)
        self.mainLayout.addLayout(self.buttonLayout)

        # Image type Layout
        self.imageTypeLayout = QHBoxLayout()
        self.imageTypeLayout.setAlignment(Qt.AlignTop)
        self.mainLayout.addLayout(self.imageTypeLayout)

        # Image Dims Layout
        self.imageDimsLayout = QHBoxLayout()
        self.imageDimsLayout.setAlignment(Qt.AlignTop)
        self.mainLayout.addLayout(self.imageDimsLayout)
    
    def makeButtons(self):
        # Load Model Button
        self.classifierLoadButton = QPushButton("Load Classifier", self)
        self.classifierLoadButton.setEnabled(False)
        self.classifierLoadButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.classifierLoadButton.setIcon(QIcon(os.path.join(os.path.dirname(__file__), 'images/icons/load.png')))
        self.classifierLoadButton.clicked.connect(self.loadClassifier)
        self.buttonLayout.addWidget(self.classifierLoadButton)

        # Load Labels Button
        self.labelsLoadButton = QPushButton("Load Labels", self)
        self.labelsLoadButton.setEnabled(False)
        self.labelsLoadButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.labelsLoadButton.setIcon(QIcon(os.path.join(os.path.dirname(__file__), 'images/icons/load.png')))
        self.labelsLoadButton.clicked.connect(self.loadLabels)
        self.buttonLayout.addWidget(self.labelsLoadButton)

    def makeEntries(self):
        # Image Type
        self.imageTypeLabels = QLabel("Image Type:", self)
        self.imageTypeLabels.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.imageTypeLayout.addWidget(self.imageTypeLabels)

        self.imageType = QComboBox()
        self.imageType.setEnabled(False)
        self.imageType.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.imageType.addItems(["Cropped Detections", "Contoured Detections"])
        self.imageType.setCurrentIndex(0)
        self.imageTypeLayout.addWidget(self.imageType)
        
        # Image Dims
        self.imageDimsLabels = QLabel("Image Dims (D x D, in pixels):", self)
        self.imageDimsLabels.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.imageDimsLayout.addWidget(self.imageDimsLabels)

        self.imageDims = QDoubleSpinBox()
        self.imageDims.setEnabled(False)
        self.imageDims.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.imageDims.setMinimum(0)
        self.imageDims.setMaximum(999999)
        self.imageDims.setSingleStep(2)
        self.imageDims.setValue(128)
        self.imageDims.setDecimals(0)
        self.imageDimsLayout.addWidget(self.imageDims)


    def classifierControlsChecked(self):
        if self.isChecked() is True:
            self.classifierLoadButton.setEnabled(True)
            self.labelsLoadButton.setEnabled(True)
            self.imageType.setEnabled(True)
            self.imageDims.setEnabled(True)
        else:
            self.classifierLoadButton.setEnabled(False)
            self.labelsLoadButton.setEnabled(False)
            self.imageType.setEnabled(False)
            self.imageDims.setEnabled(False)


    # Function that triggers when loading a new video
    def newVideoLoaded(self):
        self.setChecked(False)

    def loadClassifier(self):
        self.selectedClassifierPath = QFileDialog.getOpenFileName(self,'Select Classifier File', "", "H5 files (*.h5)")
    
    def loadLabels(self):
        self.selectedLabelsPath = QFileDialog.getOpenFileName(self,'Select Labels File', "", "Pickle files (*.pickle)")
