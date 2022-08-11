from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class CorrectLabels_IDsControls_IDSwitchWidget(QWidget):

    switchIDsSignal = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.makeWidget()

    def makeWidget(self):
        self.correctLabels_IDsControls_IDSwitchWidgetLayout = QHBoxLayout(self)
        self.correctLabels_IDsControls_IDSwitchWidgetLayout.setAlignment(Qt.AlignTop)

        self.correctLabels_IDsControls_IDSwitchTitle = QLabel("Switch the two selected IDs:")
        self.correctLabels_IDsControls_IDSwitchTitle.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.correctLabels_IDsControls_IDSwitchWidgetLayout.addWidget(self.correctLabels_IDsControls_IDSwitchTitle)

        self.correctLabels_IDsControls_IDSwitchApplyButton = QPushButton('APPLY')
        self.correctLabels_IDsControls_IDSwitchApplyButton.setEnabled(False)
        self.correctLabels_IDsControls_IDSwitchApplyButton.clicked.connect(self.switchIDs)
        self.correctLabels_IDsControls_IDSwitchWidgetLayout.addWidget(self.correctLabels_IDsControls_IDSwitchApplyButton, alignment=Qt.AlignRight)
    
    def switchIDs(self):
        self.switchIDsSignal.emit(True)
