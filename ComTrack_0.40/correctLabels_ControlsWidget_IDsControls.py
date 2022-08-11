from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import pandas as pd

from aesthetics import QHLine, QVLine
from correctLabels_ControlsWidget_IDControls_Correspondence import CorrectLabels_IDsControls_CorrespondenceWidget
from correctLabels_ControlsWidget_IDControls_IDCheckboxes import CorrectLabels_IDsControls_IDCheckBoxesWidget
from correctLabels_ControlsWidget_IDControls_LabelChange import CorrectLabels_IDsControls_LabelChangeWidget
from correctLabels_ControlsWidget_IDControls_IDChange import CorrectLabels_IDsControls_IDChangeWidget
from correctLabels_ControlsWidget_IDControls_IDSwitch import CorrectLabels_IDsControls_IDSwitchWidget
from correctLabels_ControlsWidget_IDControls_FrameParams import CorrectLabels_IDsControls_FrameParamsWidget

class CorrectLabels_IDsControlsWidget(QGroupBox):

    rawVideoPath = pyqtSignal(object)
    updatedDataframe = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.selectedIDs = []
        self.initWidget()
        self.makeCorrespondenceCol()
        self.makeIDCheckboxesCol()
        self.makeFrameParams()
        self.makeLabelChangeWidget()
        self.makeIDChangeWidget()
        self.makeIDSwitchWidget()
    
    def initWidget(self):
        self.setTitle("ID && Label Operations")
        self.setStyleSheet("""
                QGroupBox{font-weight: bold; border: 1px solid black; border-radius: 5px; margin-top: 0.6em;}
                QGroupBox::title{top: -0.5em; subcontrol-position: top center;}
                """)
        self.correctLabels_IDsControlsLayout = QVBoxLayout(self)
        self.correctLabels_IDsControlsLayout.setAlignment(Qt.AlignTop)

        self.correctLabels_IDsLabelsDisplayLayout = QHBoxLayout()
        self.correctLabels_IDsLabelsDisplayLayout.setAlignment(Qt.AlignTop)
        self.correctLabels_IDsControlsLayout.addLayout(self.correctLabels_IDsLabelsDisplayLayout)

        separatorH1 = QHLine()
        self.correctLabels_IDsControlsLayout.addWidget(separatorH1)

        self.correctLabels_IDsLabelsOperationsLayout = QVBoxLayout()
        self.correctLabels_IDsControlsLayout.addLayout(self.correctLabels_IDsLabelsOperationsLayout)
    
    def makeCorrespondenceCol(self):
        # Layout
        self.correctLabels_IDsControls_CorrespondenceLayout = QVBoxLayout()
        self.correctLabels_IDsLabelsDisplayLayout.addLayout(self.correctLabels_IDsControls_CorrespondenceLayout)
        # Title
        self.correctLabels_IDsControls_CorrespondenceLabel = QLabel("ID/Label Correspondence")
        self.correctLabels_IDsControls_CorrespondenceLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.correctLabels_IDsControls_CorrespondenceLayout.addWidget(self.correctLabels_IDsControls_CorrespondenceLabel, alignment=Qt.AlignCenter)
        # Correspondence Scroll Area
        self.correctLabels_IDsControls_CorrespondenceScrollArea = QScrollArea()
        self.correctLabels_IDsControls_CorrespondenceScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.correctLabels_IDsControls_CorrespondenceScrollArea.setWidgetResizable(True)
        self.correctLabels_IDsControls_CorrespondenceLayout.addWidget(self.correctLabels_IDsControls_CorrespondenceScrollArea)
    
    def makeIDCheckboxesCol(self):
        # Layout
        self.correctLabels_IDsControls_IDCheckboxesLayout = QVBoxLayout()
        self.correctLabels_IDsLabelsDisplayLayout.addLayout(self.correctLabels_IDsControls_IDCheckboxesLayout)
        # Title
        self.correctLabels_IDsControls_IDCheckboxesLabel = QLabel("ID Selector")
        self.correctLabels_IDsControls_IDCheckboxesLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.correctLabels_IDsControls_IDCheckboxesLayout.addWidget(self.correctLabels_IDsControls_IDCheckboxesLabel, alignment=Qt.AlignCenter)
        # IDCheckboxes Scroll Area
        self.correctLabels_IDsControls_IDCheckboxesScrollArea = QScrollArea()
        self.correctLabels_IDsControls_IDCheckboxesScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.correctLabels_IDsControls_IDCheckboxesScrollArea.setWidgetResizable(True)
        self.correctLabels_IDsControls_IDCheckboxesLayout.addWidget(self.correctLabels_IDsControls_IDCheckboxesScrollArea)
    
    def makeFrameParams(self):
        self.correctLabels_IDsControls_FrameParamsWidget = CorrectLabels_IDsControls_FrameParamsWidget()
        self.correctLabels_IDsLabelsOperationsLayout.addWidget(self.correctLabels_IDsControls_FrameParamsWidget)
    
    def makeLabelChangeWidget(self):
        self.correctLabels_IDsControls_LabelChangeWidget = CorrectLabels_IDsControls_LabelChangeWidget()
        self.correctLabels_IDsControls_LabelChangeWidget.changeLabelsSignal.connect(self.changeLabels)
        self.correctLabels_IDsLabelsOperationsLayout.addWidget(self.correctLabels_IDsControls_LabelChangeWidget)
    
    def makeIDChangeWidget(self):
        self.correctLabels_IDsControls_IDChangeWidget = CorrectLabels_IDsControls_IDChangeWidget()
        self.correctLabels_IDsControls_IDChangeWidget.changeIDsSignal.connect(self.changeIDs)
        self.correctLabels_IDsLabelsOperationsLayout.addWidget(self.correctLabels_IDsControls_IDChangeWidget)

    def makeIDSwitchWidget(self):
        self.correctLabels_IDsControls_IDSwitchWidget = CorrectLabels_IDsControls_IDSwitchWidget()
        self.correctLabels_IDsControls_IDSwitchWidget.switchIDsSignal.connect(self.switchIDs)
        self.correctLabels_IDsLabelsOperationsLayout.addWidget(self.correctLabels_IDsControls_IDSwitchWidget)
    
    def loadTrackingData(self, dataframe):
        self.dataframe = dataframe
        if isinstance(self.dataframe, pd.DataFrame):
            # Make Correspondence Widget
            self.correctLabels_IDsControls_CorrespondenceWidget = CorrectLabels_IDsControls_CorrespondenceWidget(self.dataframe)
            self.correctLabels_IDsControls_CorrespondenceScrollArea.setWidget(self.correctLabels_IDsControls_CorrespondenceWidget)
            # Make ID Checkboxes Widget
            self.correctLabels_IDsControls_IDCheckboxesWidget = CorrectLabels_IDsControls_IDCheckBoxesWidget(self.dataframe)
            self.correctLabels_IDsControls_IDCheckboxesWidget.updatedSelectedIDs.connect(self.updateSelectedIDs)
            self.correctLabels_IDsControls_IDCheckboxesScrollArea.setWidget(self.correctLabels_IDsControls_IDCheckboxesWidget)
            # Update Frame Params
            self.correctLabels_TrackingData_MinFrame = int(min(self.dataframe.loc[:, 'Frame']))
            self.correctLabels_TrackingData_MaxFrame = int(max(self.dataframe.loc[:, 'Frame']))
            self.correctLabels_IDsControls_FrameParamsWidget.correctLabels_IDsControls_FromFrame.setMinimum(self.correctLabels_TrackingData_MinFrame)
            self.correctLabels_IDsControls_FrameParamsWidget.correctLabels_IDsControls_FromFrame.setMaximum(self.correctLabels_TrackingData_MaxFrame)
            self.correctLabels_IDsControls_FrameParamsWidget.correctLabels_IDsControls_FromFrame.setValue(self.correctLabels_TrackingData_MinFrame)
            self.correctLabels_IDsControls_FrameParamsWidget.correctLabels_IDsControls_ToFrame.setMinimum(self.correctLabels_TrackingData_MinFrame)
            self.correctLabels_IDsControls_FrameParamsWidget.correctLabels_IDsControls_ToFrame.setMaximum(self.correctLabels_TrackingData_MaxFrame)
            self.correctLabels_IDsControls_FrameParamsWidget.correctLabels_IDsControls_ToFrame.setValue(self.correctLabels_TrackingData_MaxFrame)
            # Update ID Change Widget
            self.correctLabels_TrackingData_MaxID = int(max(self.dataframe.loc[:, 'ID']))
            self.correctLabels_IDsControls_IDChangeWidget.correctLabels_IDsControls_IDChangeNewID.setValue(int(self.correctLabels_TrackingData_MaxID + 1))
        else:
            try:
                self.correctLabels_IDsControls_CorrespondenceWidget
            except:
                pass
            else:
                self.correctLabels_IDsControls_CorrespondenceWidget.deleteLater()

            try:
                self.correctLabels_IDsControls_IDCheckboxesWidget
            except:
                pass
            else:
                self.correctLabels_IDsControls_IDCheckboxesWidget.deleteLater()

            self.correctLabels_IDsControls_FrameParamsWidget.correctLabels_IDsControls_FromFrame.setMinimum(0)
            self.correctLabels_IDsControls_FrameParamsWidget.correctLabels_IDsControls_FromFrame.setMaximum(0)
            self.correctLabels_IDsControls_FrameParamsWidget.correctLabels_IDsControls_FromFrame.setValue(0)
            self.correctLabels_IDsControls_FrameParamsWidget.correctLabels_IDsControls_ToFrame.setMinimum(0)
            self.correctLabels_IDsControls_FrameParamsWidget.correctLabels_IDsControls_ToFrame.setMaximum(0)
            self.correctLabels_IDsControls_FrameParamsWidget.correctLabels_IDsControls_ToFrame.setValue(0)
            self.correctLabels_IDsControls_IDChangeWidget.correctLabels_IDsControls_IDChangeNewID.setValue(0)

    def updateSelectedIDs(self, selectedIDs):
        self.selectedIDs = selectedIDs
        if (len(self.selectedIDs)>0):
            if (len(self.selectedIDs)==2):
                self.correctLabels_IDsControls_LabelChangeWidget.correctLabels_IDsControls_LabelChangeApplyButton.setEnabled(True)
                self.correctLabels_IDsControls_IDChangeWidget.correctLabels_IDsControls_IDChangeApplyButton.setEnabled(True)
                self.correctLabels_IDsControls_IDSwitchWidget.correctLabels_IDsControls_IDSwitchApplyButton.setEnabled(True)
            else:
                self.correctLabels_IDsControls_LabelChangeWidget.correctLabels_IDsControls_LabelChangeApplyButton.setEnabled(True)
                self.correctLabels_IDsControls_IDChangeWidget.correctLabels_IDsControls_IDChangeApplyButton.setEnabled(True)
                self.correctLabels_IDsControls_IDSwitchWidget.correctLabels_IDsControls_IDSwitchApplyButton.setEnabled(False)
        else:
            self.correctLabels_IDsControls_LabelChangeWidget.correctLabels_IDsControls_LabelChangeApplyButton.setEnabled(False)
            self.correctLabels_IDsControls_IDChangeWidget.correctLabels_IDsControls_IDChangeApplyButton.setEnabled(False)
            self.correctLabels_IDsControls_IDSwitchWidget.correctLabels_IDsControls_IDSwitchApplyButton.setEnabled(False)
    
    def changeLabels(self, signal):
        if signal is True:
            frameFrom = self.correctLabels_IDsControls_FrameParamsWidget.correctLabels_IDsControls_FromFrame.value()
            frameTo = self.correctLabels_IDsControls_FrameParamsWidget.correctLabels_IDsControls_ToFrame.value()
            newLabel = self.correctLabels_IDsControls_LabelChangeWidget.correctLabels_IDsControls_LabelChangeLabel.text()
            for i in range(len(self.dataframe)):
                if self.dataframe.loc[i, 'ID'] in self.selectedIDs:
                    if (self.dataframe.loc[i, 'Frame'] >= frameFrom) and (self.dataframe.loc[i, 'Frame'] <= frameTo):
                        self.dataframe.loc[i, 'Label'] = newLabel
                    else:
                        pass
            self.correctLabels_IDsControls_CorrespondenceWidget.updateCorrespondences(self.dataframe)
        else:
            pass
        self.updatedDataframe.emit(self.dataframe)
    
    def changeIDs(self, signal):
        if signal is True:
            frameFrom = self.correctLabels_IDsControls_FrameParamsWidget.correctLabels_IDsControls_FromFrame.value()
            frameTo = self.correctLabels_IDsControls_FrameParamsWidget.correctLabels_IDsControls_ToFrame.value()
            newID = int(self.correctLabels_IDsControls_IDChangeWidget.correctLabels_IDsControls_IDChangeNewID.text())
            for i in range(len(self.dataframe)):
                if self.dataframe.loc[i, 'ID'] in self.selectedIDs:
                    if (self.dataframe.loc[i, 'Frame'] >= frameFrom) and (self.dataframe.loc[i, 'Frame'] <= frameTo):
                        self.dataframe.loc[i, 'ID'] = newID
                    else:
                        pass
            self.correctLabels_IDsControls_CorrespondenceWidget.updateCorrespondences(self.dataframe)
            self.correctLabels_IDsControls_IDCheckboxesWidget.updateIDCheckBoxes(self.dataframe)
        else:
            pass
        self.updatedDataframe.emit(self.dataframe)

        # Update ID Change Widget
        self.correctLabels_TrackingData_MaxID = int(max(self.dataframe.loc[:, 'ID']))
        self.correctLabels_IDsControls_IDChangeWidget.correctLabels_IDsControls_IDChangeNewID.setValue(int(self.correctLabels_TrackingData_MaxID + 1))
    
    def switchIDs(self, signal):
        if signal is True:
            frameFrom = self.correctLabels_IDsControls_FrameParamsWidget.correctLabels_IDsControls_FromFrame.value()
            frameTo = self.correctLabels_IDsControls_FrameParamsWidget.correctLabels_IDsControls_ToFrame.value()
            id1 = self.selectedIDs[0]
            id2 = self.selectedIDs[1]
            idTemp = -1
            for i in range(len(self.dataframe)):
                if self.dataframe.loc[i, 'ID'] == id1:
                    if (self.dataframe.loc[i, 'Frame'] >= frameFrom) and (self.dataframe.loc[i, 'Frame'] <= frameTo):
                        self.dataframe.loc[i, 'ID'] = idTemp
            for i in range(len(self.dataframe)):
                if self.dataframe.loc[i, 'ID'] == id2:
                    if (self.dataframe.loc[i, 'Frame'] >= frameFrom) and (self.dataframe.loc[i, 'Frame'] <= frameTo):
                        self.dataframe.loc[i, 'ID'] = id1
            for i in range(len(self.dataframe)):
                if self.dataframe.loc[i, 'ID'] == idTemp:
                    if (self.dataframe.loc[i, 'Frame'] >= frameFrom) and (self.dataframe.loc[i, 'Frame'] <= frameTo):
                        self.dataframe.loc[i, 'ID'] = id2
            self.correctLabels_IDsControls_CorrespondenceWidget.updateCorrespondences(self.dataframe)
            self.correctLabels_IDsControls_IDCheckboxesWidget.updateIDCheckBoxes(self.dataframe)
        else:
            pass
