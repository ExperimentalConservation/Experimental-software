from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os

class ModelBuilder_DataAugmentationParamsWidget(QGroupBox):

    threadIsOn = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.initWidget()
        self.makeParamSpinBoxes()

    def initWidget(self):
        self.setTitle("Data Augmentation Parameters")
        self.setStyleSheet("""
                QGroupBox{font-weight: bold; border: 1px solid black; border-radius: 5px; margin-top: 0.6em;}
                QGroupBox::title{top: -0.5em; subcontrol-position: top center;}
                """)
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setAlignment(Qt.AlignTop)
        self.rotationRangeLayout = QHBoxLayout()
        self.mainLayout.addLayout(self.rotationRangeLayout)
        self.zoomRangeLayout = QHBoxLayout()
        self.mainLayout.addLayout(self.zoomRangeLayout)
        self.widthShiftRangeLayout = QHBoxLayout()
        self.mainLayout.addLayout(self.widthShiftRangeLayout)
        self.heightShiftRangeLayout = QHBoxLayout()
        self.mainLayout.addLayout(self.heightShiftRangeLayout)
        self.shearRangeLayout = QHBoxLayout()
        self.mainLayout.addLayout(self.shearRangeLayout)
        self.horizontalFlipLayout = QHBoxLayout()
        self.horizontalFlipLayout.setAlignment(Qt.AlignLeft)
        self.mainLayout.addLayout(self.horizontalFlipLayout)
        self.verticalFlipLayout = QHBoxLayout()
        self.verticalFlipLayout.setAlignment(Qt.AlignLeft)
        self.mainLayout.addLayout(self.verticalFlipLayout)
        self.fillModeLayout = QHBoxLayout()
        self.mainLayout.addLayout(self.fillModeLayout)
    
    def makeParamSpinBoxes(self):
        # Learning Rate
        self.rotationRangeLabel = QLabel()
        self.rotationRangeLabel.setText("Rotation Range:")
        self.rotationRangeLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.rotationRangeLayout.addWidget(self.rotationRangeLabel)
        self.rotationRange = QDoubleSpinBox()
        self.rotationRange.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.rotationRange.setMinimum(0)
        self.rotationRange.setMaximum(360)
        self.rotationRange.setSingleStep(5)
        self.rotationRange.setValue(20)
        self.rotationRange.setDecimals(0)
        self.rotationRangeLayout.addWidget(self.rotationRange)

        # Zoom Range
        self.zoomRangeLabel = QLabel()
        self.zoomRangeLabel.setText("Zoom Range:")
        self.zoomRangeLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.zoomRangeLayout.addWidget(self.zoomRangeLabel)
        self.zoomRange = QDoubleSpinBox()
        self.zoomRange.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.zoomRange.setMinimum(0)
        self.zoomRange.setMaximum(1)
        self.zoomRange.setSingleStep(0.05)
        self.zoomRange.setValue(0.15)
        self.zoomRange.setDecimals(2)
        self.zoomRangeLayout.addWidget(self.zoomRange)

        # Width Shift Range
        self.widthShiftRangeLabel = QLabel()
        self.widthShiftRangeLabel.setText("Width Shift Range:")
        self.widthShiftRangeLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.widthShiftRangeLayout.addWidget(self.widthShiftRangeLabel)
        self.widthShiftRange = QDoubleSpinBox()
        self.widthShiftRange.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.widthShiftRange.setMinimum(0)
        self.widthShiftRange.setMaximum(1)
        self.widthShiftRange.setSingleStep(0.05)
        self.widthShiftRange.setValue(0.20)
        self.widthShiftRange.setDecimals(2)
        self.widthShiftRangeLayout.addWidget(self.widthShiftRange)

        # Height Shift Range
        self.heightShiftRangeLabel = QLabel()
        self.heightShiftRangeLabel.setText("Height Shift Range")
        self.heightShiftRangeLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.heightShiftRangeLayout.addWidget(self.heightShiftRangeLabel)
        self.heightShiftRange = QDoubleSpinBox()
        self.heightShiftRange.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.heightShiftRange.setMinimum(0)
        self.heightShiftRange.setMaximum(1)
        self.heightShiftRange.setSingleStep(0.05)
        self.heightShiftRange.setValue(0.20)
        self.heightShiftRange.setDecimals(2)
        self.heightShiftRangeLayout.addWidget(self.heightShiftRange)

        # Shear Range
        self.shearRangeLabel = QLabel()
        self.shearRangeLabel.setText("Shear Range:")
        self.shearRangeLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.shearRangeLayout.addWidget(self.shearRangeLabel)
        self.shearRange = QDoubleSpinBox()
        self.shearRange.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.shearRange.setMinimum(0)
        self.shearRange.setMaximum(1)
        self.shearRange.setSingleStep(0.05)
        self.shearRange.setValue(0.20)
        self.shearRange.setDecimals(2)
        self.shearRangeLayout.addWidget(self.shearRange)

        # Horizontal Flip
        self.horizontalFlipLabel = QLabel()
        self.horizontalFlipLabel.setText("Horizontal Flip:")
        self.horizontalFlipLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.horizontalFlipLayout.addWidget(self.horizontalFlipLabel)
        self.horizontalFlip = QCheckBox()
        self.horizontalFlip.setChecked(True)
        self.horizontalFlipLayout.addWidget(self.horizontalFlip)

        # Vertical Flip
        self.verticalFlipLabel = QLabel()
        self.verticalFlipLabel.setText("Vertical Flip:")
        self.verticalFlipLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.verticalFlipLayout.addWidget(self.verticalFlipLabel)
        self.verticalFlip = QCheckBox()
        self.verticalFlip.setChecked(True)
        self.verticalFlipLayout.addWidget(self.verticalFlip)

        # Fill Mode
        self.fillModeLabel = QLabel()
        self.fillModeLabel.setText("Fill Mode:")
        self.fillModeLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.fillModeLayout.addWidget(self.fillModeLabel)
        self.fillMode = QComboBox()
        self.fillMode.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.fillMode.addItems(["nearest", "reflect", "wrap"])
        self.fillMode.setCurrentIndex(0)
        self.fillModeLayout.addWidget(self.fillMode)
