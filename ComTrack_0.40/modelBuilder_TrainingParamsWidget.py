from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os

class ModelBuilder_TrainingParamsWidget(QGroupBox):

    threadIsOn = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.initWidget()
        self.makeParamSpinBoxes()

    def initWidget(self):
        self.setTitle("Training Parameters")
        self.setStyleSheet("""
                QGroupBox{font-weight: bold; border: 1px solid black; border-radius: 5px; margin-top: 0.6em;}
                QGroupBox::title{top: -0.5em; subcontrol-position: top center;}
                """)
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setAlignment(Qt.AlignTop)
        self.learningRateLayout = QHBoxLayout()
        self.mainLayout.addLayout(self.learningRateLayout)
        self.epochsLayout = QHBoxLayout()
        self.mainLayout.addLayout(self.epochsLayout)
        self.batchSizeLayout = QHBoxLayout()
        self.mainLayout.addLayout(self.batchSizeLayout)
        self.testTrainSplitLayout = QHBoxLayout()
        self.mainLayout.addLayout(self.testTrainSplitLayout)
        self.imagesDimsLayout = QHBoxLayout()
        self.mainLayout.addLayout(self.imagesDimsLayout)
    
    def makeParamSpinBoxes(self):
        # Learning Rate
        self.learningRateLabel = QLabel()
        self.learningRateLabel.setText("Learning Rate:")
        self.learningRateLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.learningRateLayout.addWidget(self.learningRateLabel)
        self.learningRate = QDoubleSpinBox()
        self.learningRate.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.learningRate.setMinimum(0.000001)
        self.learningRate.setMaximum(1)
        self.learningRate.setSingleStep(0.000001)
        self.learningRate.setDecimals(6)
        self.learningRate.setValue(0.0001)
        self.learningRateLayout.addWidget(self.learningRate)

        # EPOCHS
        self.epochsLabel = QLabel()
        self.epochsLabel.setText("EPOCHS:")
        self.epochsLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.epochsLayout.addWidget(self.epochsLabel)
        self.epochs = QDoubleSpinBox()
        self.epochs.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.epochs.setMinimum(1)
        self.epochs.setMaximum(999999)
        self.epochs.setSingleStep(1)
        self.epochs.setValue(10)
        self.epochs.setDecimals(0)
        self.epochsLayout.addWidget(self.epochs)

        # Batch Size
        self.batchSizeLabel = QLabel()
        self.batchSizeLabel.setText("Batch Size:")
        self.batchSizeLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.batchSizeLayout.addWidget(self.batchSizeLabel)
        self.batchSize = QDoubleSpinBox()
        self.batchSize.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.batchSize.setMinimum(1)
        self.batchSize.setMaximum(999999)
        self.batchSize.setSingleStep(1)
        self.batchSize.setValue(16)
        self.batchSize.setDecimals(0)
        self.batchSizeLayout.addWidget(self.batchSize)

        # Test/Train Split
        self.testTrainSplitLabel = QLabel()
        self.testTrainSplitLabel.setText("Test/Train Split (%):")
        self.testTrainSplitLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.testTrainSplitLayout.addWidget(self.testTrainSplitLabel)
        self.testTrainSplit = QDoubleSpinBox()
        self.testTrainSplit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.testTrainSplit.setMinimum(0.05)
        self.testTrainSplit.setMaximum(0.95)
        self.testTrainSplit.setSingleStep(0.05)
        self.testTrainSplit.setValue(0.20)
        self.testTrainSplit.setDecimals(2)
        self.testTrainSplitLayout.addWidget(self.testTrainSplit)

        # Image Dimensions
        self.imagesDimsLabel = QLabel()
        self.imagesDimsLabel.setText("Images Dimensions (D x D):")
        self.imagesDimsLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.imagesDimsLayout.addWidget(self.imagesDimsLabel)
        self.imagesDims = QDoubleSpinBox()
        self.imagesDims.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.imagesDims.setMinimum(1)
        self.imagesDims.setMaximum(999999)
        self.imagesDims.setSingleStep(1)
        self.imagesDims.setValue(128)
        self.imagesDims.setDecimals(0)
        self.imagesDimsLayout.addWidget(self.imagesDims)
