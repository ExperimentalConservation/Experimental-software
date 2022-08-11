from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class CorrectLabels_IDsControls_IDChangeWidget(QWidget):

    changeIDsSignal = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.makeWidget()

    def makeWidget(self):
        self.correctLabels_IDsControls_IDChangeWidgetLayout = QHBoxLayout(self)
        self.correctLabels_IDsControls_IDChangeWidgetLayout.setAlignment(Qt.AlignTop)

        self.correctLabels_IDsControls_IDChangeTitle = QLabel("Replace selected ID(s) by:")
        self.correctLabels_IDsControls_IDChangeTitle.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.correctLabels_IDsControls_IDChangeWidgetLayout.addWidget(self.correctLabels_IDsControls_IDChangeTitle)

        self.correctLabels_IDsControls_IDChangeNewID = QDoubleSpinBox(self)
        self.correctLabels_IDsControls_IDChangeNewID.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.correctLabels_IDsControls_IDChangeNewID.setMinimum(0)
        self.correctLabels_IDsControls_IDChangeNewID.setMaximum(999999)
        self.correctLabels_IDsControls_IDChangeNewID.setSingleStep(1)
        self.correctLabels_IDsControls_IDChangeNewID.setValue(0)
        self.correctLabels_IDsControls_IDChangeNewID.setDecimals(0)
        self.correctLabels_IDsControls_IDChangeWidgetLayout.addWidget(self.correctLabels_IDsControls_IDChangeNewID)

        self.correctLabels_IDsControls_IDChangeApplyButton = QPushButton('APPLY')
        self.correctLabels_IDsControls_IDChangeApplyButton.setEnabled(False)
        self.correctLabels_IDsControls_IDChangeApplyButton.clicked.connect(self.changeIDs)
        self.correctLabels_IDsControls_IDChangeWidgetLayout.addWidget(self.correctLabels_IDsControls_IDChangeApplyButton)
    
    def changeIDs(self):
        self.changeIDsSignal.emit(True)
