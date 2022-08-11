from tkinter import Label
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import functions_misc


class CorrectLabels_IDsControls_CorrespondenceWidget(QWidget):
    def __init__(self, dataframe):
        super().__init__()
        self.dataframe = dataframe
        self.identities = self.dataframe.loc[:, 'ID'].unique()
        self.correspondenceWidgets = []
        self.makeWidget()

    def makeWidget(self):
        self.correctLabels_IDsControls_CorrespondenceWidgetLayout = QVBoxLayout(self)
        self.correctLabels_IDsControls_CorrespondenceWidgetLayout.setAlignment(Qt.AlignTop)
        for i, identity in enumerate(self.identities):
            dataframe_ID = self.dataframe.loc[self.dataframe.ID == identity]
            labels = dataframe_ID.loc[:, 'Label'].unique()
            for label in labels:
                dataframe_ID_Label = dataframe_ID.loc[dataframe_ID.Label == label]
                minFrame = int(min(dataframe_ID_Label.loc[:, 'Frame']))
                maxFrame = int(max(dataframe_ID_Label.loc[:, 'Frame']))
                singleCorrespondence = SingleCorrespondence(self, identity, label, minFrame, maxFrame)
                self.correctLabels_IDsControls_CorrespondenceWidgetLayout.addWidget(singleCorrespondence)
    
    def updateCorrespondences(self, dataframe):
        functions_misc.clearPyQtLayout(self.correctLabels_IDsControls_CorrespondenceWidgetLayout)
        self.identities = dataframe.loc[:, 'ID'].unique()
        self.identities = sorted(self.identities)
        for i, identity in enumerate(self.identities):
            dataframe_ID = dataframe.loc[dataframe.ID == identity]
            labels = dataframe_ID.loc[:, 'Label'].unique()
            for label in labels:
                dataframe_ID_Label = dataframe_ID.loc[dataframe_ID.Label == label]
                minFrame = int(min(dataframe_ID_Label.loc[:, 'Frame']))
                maxFrame = int(max(dataframe_ID_Label.loc[:, 'Frame']))
                singleCorrespondence = SingleCorrespondence(self, identity, label, minFrame, maxFrame)
                self.correctLabels_IDsControls_CorrespondenceWidgetLayout.addWidget(singleCorrespondence)

    # def updateLabels(self, selectedIDs, newLabel, minFrame, maxFrame, frameFrom, frameTo):
    #     selectedIDsText = str(selectedIDs)
    #     for qLabelWidget in self.children():
    #         if isinstance(qLabelWidget, QLabel):
    #             if qLabelWidget.objectName() in selectedIDsText:
    #                 newText = str(qLabelWidget.objectName()) + ' = ' + str(newLabel)
    #                 qLabelWidget.setText(str(newText))
    
    # def updateIDs(self, selectedIDs, newID, minFrame, maxFrame, frameFrom, frameTo):
    #     selectedIDsText = str(selectedIDs)
    #     if str(newID) not in selectedIDsText:
    #         singleCorrespondence = SingleCorrespondence(self, newID, newID)
    #     if (minFrame < frameFrom) or (maxFrame > frameTo):
    #         for identity in selectedIDs:
    #             singleCorrespondence = SingleCorrespondence(self, identity, newID)
    #     else:
    #         for qLabelWidget in self.children():
    #             if isinstance(qLabelWidget, QLabel):
    #                 if qLabelWidget.objectName() in selectedIDsText:
    #                     qLabelWidget.setObjectName(str(newID))
    #                     label = qLabelWidget.text().split()[2]
    #                     newText = str(qLabelWidget.objectName()) + ' = ' + str(label)
    #                     qLabelWidget.setText(str(newText))


class SingleCorrespondence(QLabel):
    def __init__(self, parent, identity, label, minFrame, maxFrame, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        fulltext = str(identity) + ' = ' + str(label) + ' (F' + str(minFrame) + '-F' + str(maxFrame) + ')'
        self.setObjectName(str(identity))
        self.setText(str(fulltext))
        self.show()
