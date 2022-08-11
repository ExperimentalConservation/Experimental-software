from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class CorrectLabels_IDsControls_FrameParamsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.makeWidget()

    def makeWidget(self):
        self.correctLabels_IDsControls_FrameParamsWidgetLayout = QVBoxLayout(self)
        self.correctLabels_IDsControls_FrameParamsWidgetLayout.setAlignment(Qt.AlignTop)

        self.correctLabels_IDsControls_FromFrameLayout = QHBoxLayout()
        self.correctLabels_IDsControls_FrameParamsWidgetLayout.addLayout(self.correctLabels_IDsControls_FromFrameLayout)
        self.correctLabels_IDsControls_ToFrameLayout = QHBoxLayout()
        self.correctLabels_IDsControls_FrameParamsWidgetLayout.addLayout(self.correctLabels_IDsControls_ToFrameLayout)

        self.correctLabels_IDsControls_FromFrameLabel = QLabel("From Frame:")
        self.correctLabels_IDsControls_FromFrameLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.correctLabels_IDsControls_FromFrameLayout.addWidget(self.correctLabels_IDsControls_FromFrameLabel)

        self.correctLabels_IDsControls_FromFrame = QDoubleSpinBox(self)
        self.correctLabels_IDsControls_FromFrame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.correctLabels_IDsControls_FromFrame.setMinimum(0)
        self.correctLabels_IDsControls_FromFrame.setMaximum(0)
        self.correctLabels_IDsControls_FromFrame.setSingleStep(1)
        self.correctLabels_IDsControls_FromFrame.setValue(0)
        self.correctLabels_IDsControls_FromFrame.setDecimals(0)
        self.correctLabels_IDsControls_FromFrameLayout.addWidget(self.correctLabels_IDsControls_FromFrame)

        self.correctLabels_IDsControls_ToFrameLabel = QLabel("To Frame:")
        self.correctLabels_IDsControls_ToFrameLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.correctLabels_IDsControls_ToFrameLayout.addWidget(self.correctLabels_IDsControls_ToFrameLabel)

        self.correctLabels_IDsControls_ToFrame = QDoubleSpinBox(self)
        self.correctLabels_IDsControls_ToFrame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.correctLabels_IDsControls_ToFrame.setMinimum(0)
        self.correctLabels_IDsControls_ToFrame.setMaximum(0)
        self.correctLabels_IDsControls_ToFrame.setSingleStep(1)
        self.correctLabels_IDsControls_ToFrame.setValue(0)
        self.correctLabels_IDsControls_ToFrame.setDecimals(0)
        self.correctLabels_IDsControls_ToFrameLayout.addWidget(self.correctLabels_IDsControls_ToFrame)
