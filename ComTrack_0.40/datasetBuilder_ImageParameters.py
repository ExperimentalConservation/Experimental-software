from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os

class DatasetBuilder_ImageParametersWidget(QGroupBox):

    def __init__(self):
        super().__init__()
        self.initWidget()
        self.makeParams()


    def initWidget(self):
        self.totalNumberAnnotations = 0
        self.speciesLabels = []
        self.setTitle("Image Parameters")
        self.setStyleSheet("""
                QGroupBox{font-weight: bold; border: 1px solid black; border-radius: 5px; margin-top: 0.6em;}
                QGroupBox::title{top: -0.5em; subcontrol-position: top center;}
                """)
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setAlignment(Qt.AlignTop)
    
    def makeParams(self):
        # Extraction Method
        self.extractionMethod_Layout = QHBoxLayout()
        self.mainLayout.addLayout(self.extractionMethod_Layout)
        self.extractionMethod_Label = QLabel("Image Extraction Method:")
        self.extractionMethod_Label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.extractionMethod_Layout.addWidget(self.extractionMethod_Label)
        self.extractionMethod = QComboBox()
        self.extractionMethod.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.extractionMethod.addItems(["Cropping", "Contouring"])
        self.extractionMethod.setCurrentIndex(0)
        self.extractionMethod.currentIndexChanged.connect(self.extractionMethodChanged)
        self.extractionMethod_Layout.addWidget(self.extractionMethod)
    
        # Image Margins Method
        self.imageMarginsMethod_Layout = QHBoxLayout()
        self.mainLayout.addLayout(self.imageMarginsMethod_Layout)
        self.imageMarginsMethod_Label = QLabel("Image Margins Method:")
        self.imageMarginsMethod_Label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.imageMarginsMethod_Layout.addWidget(self.imageMarginsMethod_Label)
        self.imageMarginsMethod = QComboBox()
        self.imageMarginsMethod.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.imageMarginsMethod.addItems(["Minimal", "Enlarged"])
        self.imageMarginsMethod.setCurrentIndex(0)
        self.imageMarginsMethod.currentIndexChanged.connect(self.imageMarginsMethodChanged)
        self.imageMarginsMethod_Layout.addWidget(self.imageMarginsMethod)
    
        # Margins
        self.imageMargins_Layout = QHBoxLayout()
        self.mainLayout.addLayout(self.imageMargins_Layout)
        self.imageMargins_Label = QLabel("Margins:")
        self.imageMargins_Label.setEnabled(False)
        self.imageMargins_Label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.imageMargins_Layout.addWidget(self.imageMargins_Label)
        self.imageMargins = QDoubleSpinBox()
        self.imageMargins.setEnabled(False)
        self.imageMargins.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.imageMargins.setRange(0, 999999)
        self.imageMargins.setSingleStep(5)
        self.imageMargins.setValue(25)
        self.imageMargins.setDecimals(0)
        self.imageMargins_Layout.addWidget(self.imageMargins)

        # Image Dimensions
        self.imageDims_Layout = QHBoxLayout()
        self.mainLayout.addLayout(self.imageDims_Layout)
        self.imageDims_Label = QLabel("Image Dimensions:")
        self.imageDims_Label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.imageDims_Layout.addWidget(self.imageDims_Label)
        self.imageDims = QDoubleSpinBox()
        self.imageDims.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.imageDims.setRange(0, 999999)
        self.imageDims.setSingleStep(2)
        self.imageDims.setValue(128)
        self.imageDims.setDecimals(0)
        self.imageDims_Layout.addWidget(self.imageDims)
    
    def extractionMethodChanged(self):
        self.extractionMethodSelected = self.extractionMethod.currentText()
    
    def imageMarginsMethodChanged(self):
        self.imageMarginsSelected = self.imageMarginsMethod.currentText()
        if self.imageMarginsSelected == "Enlarged":
            self.imageMargins_Label.setEnabled(True)
            self.imageMargins.setEnabled(True)
        elif self.imageMarginsSelected == "Minimal":
            self.imageMargins_Label.setEnabled(False)
            self.imageMargins.setEnabled(False)
