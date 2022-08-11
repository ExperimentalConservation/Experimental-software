from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import functions_misc

class CorrectLabels_IDsControls_IDCheckBoxesWidget(QWidget):

    updatedSelectedIDs = pyqtSignal(object)

    def __init__(self, dataframe):
        super().__init__()
        self.dataframe = dataframe
        self.identities = self.dataframe.loc[:, 'ID'].unique()
        self.identities = sorted(self.identities)
        self.selectedIDs = []
        self.updatedSelectedIDs.emit(self.selectedIDs)
        self.makeWidget()

    def makeWidget(self):
        # Layout
        self.correctLabels_IDsControls_IDCheckBoxesLayout = QVBoxLayout(self)
        self.correctLabels_IDsControls_IDCheckBoxesLayout.setAlignment(Qt.AlignTop)

        # Master CheckBox controlling all individual ID checkboxes
        self.correctLabels_IDsControls_MasterCheckBox = QCheckBox("Select All")
        self.correctLabels_IDsControls_MasterCheckBox.toggled.connect(self.selectAll)
        self.correctLabels_IDsControls_IDCheckBoxesLayout.addWidget(self.correctLabels_IDsControls_MasterCheckBox)

        self.correctLabels_IDsControls_AllIDCheckBoxes = []
        for i, identity in enumerate(self.identities):
            self.singleID_CheckBox = SingleID_QCheckBox(self, i, identity, self.selectedIDs)
            self.correctLabels_IDsControls_IDCheckBoxesLayout.addWidget(self.singleID_CheckBox)
            self.correctLabels_IDsControls_AllIDCheckBoxes.append(self.singleID_CheckBox)
            self.singleID_CheckBox.addID.connect(self.addID)
            self.singleID_CheckBox.removeID.connect(self.removeID)
    
    def selectAll(self, state):
        for checkbox in self.correctLabels_IDsControls_AllIDCheckBoxes:
            checkbox.setChecked(state)
        
    def addID(self, id):
        self.selectedIDs.append(id)
        self.updatedSelectedIDs.emit(self.selectedIDs)

    def removeID(self, id):
        if id in self.selectedIDs:
            self.selectedIDs.remove(id)
            self.updatedSelectedIDs.emit(self.selectedIDs)
    
    def updateIDCheckBoxes(self, dataframe):
        functions_misc.clearPyQtLayout(self.correctLabels_IDsControls_IDCheckBoxesLayout)

        self.correctLabels_IDsControls_MasterCheckBox = QCheckBox("Select All")
        self.correctLabels_IDsControls_MasterCheckBox.toggled.connect(self.selectAll)
        self.correctLabels_IDsControls_IDCheckBoxesLayout.addWidget(self.correctLabels_IDsControls_MasterCheckBox)

        self.correctLabels_IDsControls_AllIDCheckBoxes = []
        self.identities = dataframe.loc[:, 'ID'].unique()
        self.identities = sorted(self.identities)
        for i, identity in enumerate(self.identities):
            self.singleID_CheckBox = SingleID_QCheckBox(self, i, identity, self.selectedIDs)
            self.correctLabels_IDsControls_IDCheckBoxesLayout.addWidget(self.singleID_CheckBox)
            self.correctLabels_IDsControls_AllIDCheckBoxes.append(self.singleID_CheckBox)
            self.singleID_CheckBox.addID.connect(self.addID)
            self.singleID_CheckBox.removeID.connect(self.removeID)
        
        # removing the IDs that may have been lost while renaming some IDs
        lostIDs = []
        for selectedID in self.selectedIDs:
            if selectedID not in self.identities:
                lostIDs.append(selectedID)
        for lostID in lostIDs:
            self.selectedIDs.remove(lostID)
        self.updatedSelectedIDs.emit(self.selectedIDs)


class SingleID_QCheckBox(QCheckBox):

    addID = pyqtSignal(int)
    removeID = pyqtSignal(int)

    def __init__(self, parent, i, identity, selectedIDs, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.i = i
        self.identity = int(identity)
        self.selectedIDs = selectedIDs
        self.setText(str(self.identity))
        if self.identity in self.selectedIDs:
            self.setChecked(True)
        self.stateChanged.connect(self.updateSelectedIDs)
    
    def updateSelectedIDs(self):
        if self.isChecked() is True:
            self.addID.emit(self.identity)
        else:
            self.removeID.emit(self.identity)


