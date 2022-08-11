from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class CorrectLabels_IDsControls_LabelChangeWidget(QWidget):

    changeLabelsSignal = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.makeWidget()

    def makeWidget(self):
        self.correctLabels_IDsControls_LabelChangeWidgetLayout = QHBoxLayout(self)
        self.correctLabels_IDsControls_LabelChangeWidgetLayout.setAlignment(Qt.AlignTop)

        self.correctLabels_IDsControls_LabelChangeTitle = QLabel("Replace the Label(s) of selected ID(s) by:")
        self.correctLabels_IDsControls_LabelChangeTitle.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.correctLabels_IDsControls_LabelChangeWidgetLayout.addWidget(self.correctLabels_IDsControls_LabelChangeTitle)

        self.correctLabels_IDsControls_LabelChangeLabel = QLineEdit()
        self.correctLabels_IDsControls_LabelChangeLabel.setText('SpeciesName')
        self.correctLabels_IDsControls_LabelChangeLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.correctLabels_IDsControls_LabelChangeWidgetLayout.addWidget(self.correctLabels_IDsControls_LabelChangeLabel)

        self.correctLabels_IDsControls_LabelChangeApplyButton = QPushButton('APPLY')
        self.correctLabels_IDsControls_LabelChangeApplyButton.setEnabled(False)
        self.correctLabels_IDsControls_LabelChangeApplyButton.clicked.connect(self.changeLabels)
        self.correctLabels_IDsControls_LabelChangeWidgetLayout.addWidget(self.correctLabels_IDsControls_LabelChangeApplyButton)
    
    def changeLabels(self):
        self.changeLabelsSignal.emit(True)
