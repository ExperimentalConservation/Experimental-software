from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# from datasetBuilder_AnnotationsWidget import DatasetBuilder_AnnotationsWidget
from datasetBuilder_FolderControls import DatasetBuilder_FolderControlsWidget
from datasetBuilder_ImageParameters import DatasetBuilder_ImageParametersWidget
from datasetBuilder_ImageDisplay import DatasetBuilder_ImageDisplayWidget
from datasetBuilder_ProgressBar import DatasetBuilder_ProgressBarWidget
from datasetBuilder_GenerateDataset import DatasetBuilder_GenerateDatasetWidget
from datasetBuilder_DatasetGenerationThread import DatasetBuilder_DatasetGenerationThread

class MainWidgetDatasetBuilder(QWidget):
    def __init__(self):
        super().__init__()
        self.initWidget()
        # self.makeAnnotationsWidget()
        self.makeFolderControlsWidget()
        self.makeGenerateDatasetWidget()
        self.makeImageParameters()
        self.makeImageDisplay()
        self.makeProgressBar()
    
    def initWidget(self):
        self.mainLayout = QGridLayout(self)
        self.mainLayout.setRowStretch(0, 2)
        self.mainLayout.setRowStretch(1, 4)
        self.mainLayout.setRowStretch(2, 1)
        self.mainLayout.setColumnStretch(0, 2)
        self.mainLayout.setColumnStretch(1, 1)
    
    def makeFolderControlsWidget(self):
        self.folderControlsWidget = DatasetBuilder_FolderControlsWidget()
        self.folderControlsWidget.foldersLoaded.connect(self.foldersLoaded)
        self.mainLayout.addWidget(self.folderControlsWidget, 0, 0, 1, 1)
    
    def makeGenerateDatasetWidget(self):
        self.generateDatasetWidget = DatasetBuilder_GenerateDatasetWidget()
        self.generateDatasetWidget.launchDatasetGeneration.connect(self.generateDataset)
        self.mainLayout.addWidget(self.generateDatasetWidget, 0, 1, 1, 1)
    
    def makeImageParameters(self):
        self.imageParametersWidget = DatasetBuilder_ImageParametersWidget()
        self.mainLayout.addWidget(self.imageParametersWidget, 1, 0, 1, 1)
    
    def makeImageDisplay(self):
        self.imageDisplayWidget = DatasetBuilder_ImageDisplayWidget()
        self.mainLayout.addWidget(self.imageDisplayWidget, 1, 1, 1, 1)
    
    def makeProgressBar(self):
        self.progressBarWidget = DatasetBuilder_ProgressBarWidget()
        self.progressBarWidget.stopDatasetGenerationThread.connect(self.stopDatasetGenerationThread)
        self.mainLayout.addWidget(self.progressBarWidget, 2, 0, 1, 2)
    
    def foldersLoaded(self, signal):
        self.generateDatasetWidget.updateStatus(signal)
    
    def generateDataset(self, signal):
        if signal is True:
            self.datasetGenerationThread = DatasetBuilder_DatasetGenerationThread(self.folderControlsWidget, self.imageParametersWidget)
            self.datasetGenerationThread.totalFramesToProcess.connect(self.progressBarWidget.updateTotalFramesToProcess)
            self.datasetGenerationThread.barText.connect(self.progressBarWidget.updateBarText)
            self.datasetGenerationThread.currentFrame.connect(self.progressBarWidget.updateCurrentFrame)
            self.datasetGenerationThread.start()
    
    def stopDatasetGenerationThread(self, signal):
        if signal is True:
            self.datasetGenerationThread.stopThread()



    # def annotationsThreadsUpdateStatus(self, signal):
    #     if signal is True:
    #         self.generateDatasetWidget.setEnabled(False)
    #     else:
    #         self.generateDatasetWidget.setEnabled(True)

    
    # def datasetThreadsUpdateStatus(self, signal):
    #     if signal is True:
    #         self.generateAnnotationsWidget.setEnabled(False)
    #     else:
    #         self.generateAnnotationsWidget.setEnabled(True)

