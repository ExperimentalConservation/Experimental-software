from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os

class DatasetBuilder_FolderControlsWidget(QGroupBox):

    foldersLoaded = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.rawVideosFolderPath = ''
        self.trackingDataFolderPath = ''
        self.outputdatasetFolderPath = ''
        self.setTitle("Folder Controls")
        self.setStyleSheet("""
                QGroupBox{font-weight: bold; border: 1px solid black; border-radius: 5px; margin-top: 0.6em;}
                QGroupBox::title{top: -0.5em; subcontrol-position: top center;}
                """)
        self.makeLayouts()
        self.makeButtons()

    def makeLayouts(self):
        self.mainLayout = QHBoxLayout(self)
    
    def makeButtons(self):
        # Raw Videos Folder Selector
        self.rawVideosFolderButton = QPushButton("Raw Videos Input Folder")
        self.rawVideosFolderButton.setToolTip("No folder selected")
        self.rawVideosFolderButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.rawVideosFolderButton.setIcon(QIcon(os.path.join(os.path.dirname(__file__), 'images/icons/load.png')))
        self.rawVideosFolderButton.clicked.connect(self.rawVideosFolderSelection)
        self.mainLayout.addWidget(self.rawVideosFolderButton)

        # Tracking Data Folder Selector
        self.trackingDataFolderButton = QPushButton("Tracking Data Input Folder")
        self.trackingDataFolderButton.setToolTip("No folder selected")
        self.trackingDataFolderButton.setEnabled(False)
        self.trackingDataFolderButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.trackingDataFolderButton.setIcon(QIcon(os.path.join(os.path.dirname(__file__), 'images/icons/load.png')))
        self.trackingDataFolderButton.clicked.connect(self.trackingDataFolderSelection)
        self.mainLayout.addWidget(self.trackingDataFolderButton)

        # Dataset Output Folder Selector
        self.outputDatasetFolderButton = QPushButton("Dataset Output Folder")
        self.outputDatasetFolderButton.setToolTip("No folder selected")
        self.outputDatasetFolderButton.setEnabled(False)
        self.outputDatasetFolderButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.outputDatasetFolderButton.setIcon(QIcon(os.path.join(os.path.dirname(__file__), 'images/icons/export.png')))
        self.outputDatasetFolderButton.clicked.connect(self.outputDatasetFolderSelection)
        self.mainLayout.addWidget(self.outputDatasetFolderButton)


    def rawVideosFolderSelection(self):
        self.rawVideosFolderPath = QFileDialog.getExistingDirectory(self, "Select folder where raw videos are located", "./")
        if self.rawVideosFolderPath != '':
            self.rawVideosFolderButton.setToolTip(str(self.rawVideosFolderPath))
            self.trackingDataFolderButton.setEnabled(True)
        else:
            self.rawVideosFolderButton.setToolTip("No folder selected")
            self.trackingDataFolderButton.setEnabled(False)
            self.outputDatasetFolderButton.setEnabled(False)

        if (self.rawVideosFolderPath != '') and (self.trackingDataFolderPath != '') and (self.outputdatasetFolderPath !=''):
            self.foldersLoaded.emit(True)
        else:
            self.foldersLoaded.emit(False)


    def trackingDataFolderSelection(self):
        self.trackingDataFolderPath = QFileDialog.getExistingDirectory(self, "Select folder where curated tracking data are located", "./")
        if self.trackingDataFolderPath != '':
            self.trackingDataFolderButton.setToolTip(str(self.trackingDataFolderPath))
            self.outputDatasetFolderButton.setEnabled(True)
        else:
            self.trackingDataFolderButton.setToolTip("No folder selected")
            self.outputDatasetFolderButton.setEnabled(False)
        
        if (self.rawVideosFolderPath != '') and (self.trackingDataFolderPath != '') and (self.outputdatasetFolderPath !=''):
            self.foldersLoaded.emit(True)
        else:
            self.foldersLoaded.emit(False)

    
    def outputDatasetFolderSelection(self):
        self.outputdatasetFolderPath = QFileDialog.getExistingDirectory(self, "Select folder where to save datasets", "./")
        if self.outputdatasetFolderPath != '':
            self.outputDatasetFolderButton.setToolTip(str(self.outputdatasetFolderPath))
        else:
            self.outputDatasetFolderButton.setToolTip("No folder selected")
        
        if (self.rawVideosFolderPath != '') and (self.trackingDataFolderPath != '') and (self.outputdatasetFolderPath !=''):
            self.foldersLoaded.emit(True)
        else:
            self.foldersLoaded.emit(False)


    # def makeProgressBar(self):
    #     self.progressBarLayout = QHBoxLayout()
    #     self.mainLayout.addLayout(self.progressBarLayout)
    #     # Progress Bar
    #     self.progressBarLabel = QLabel()
    #     self.progressBarLabel.setText("Progress:")
    #     self.progressBarLayout.addWidget(self.progressBarLabel)
    #     self.progressBar = QProgressBar()
    #     self.progressBar.setAlignment(Qt.AlignCenter)
    #     self.progressBar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
    #     self.progressBarLayout.addWidget(self.progressBar)
    #     # Stop Button
    #     self.stopButton = QPushButton("Stop")
    #     self.stopButton.setEnabled(False)
    #     self.stopButton.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
    #     self.stopButton.setIcon(QIcon(os.path.join(os.path.dirname(__file__), 'images/icons/stop.png')))
    #     self.stopButton.clicked.connect(self.stopDatasetGeneration)
    #     self.progressBarLayout.addWidget(self.stopButton)
    
    # def makeCurrentSavingAction(self):
    #     self.currentSavingActionLabel = QLabel()
    #     self.currentSavingActionLabel.setText("...")
    #     self.mainLayout.addWidget(self.currentSavingActionLabel, alignment=Qt.AlignCenter)
            

    # def imagesAnnotationsFolderSelection(self):
    #     self.progressBar.setValue(0)
    #     self.imagesAnnotationsFolderPath = QFileDialog.getExistingDirectory(self, "Select folder where images and annotations are located", "./")
    #     if self.imagesAnnotationsFolderPath != '':
    #         self.imagesAnnotationsFolderButton.setToolTip(str(self.imagesAnnotationsFolderPath))
    #         self.screenSpeciesButton.setEnabled(True)
    #     else:
    #         self.imagesAnnotationsFolderButton.setToolTip("No folder selected")
    #         self.screenSpeciesButton.setEnabled(False)
    #         self.outputDatasetFolderButton.setEnabled(False)
    #         self.generateDatasetButton.setEnabled(False)

    # def screenSpecies(self):
    #     self.progressBar.setValue(0)
    #     if self.imagesAnnotationsFolderPath != '':
    #         self.speciesLabelThread = DatasetBuilder_SpeciesThread(self.imagesAnnotationsFolderPath)
    #         self.speciesLabelThread.currentAction.connect(self.updateCurrentSavingAction)
    #         self.speciesLabelThread.totalNumberAnnotations.connect(self.updateTotalNumberAnnotations)
    #         self.speciesLabelThread.speciesLabels.connect(self.updateSpeciesLabels)
    #         self.threadIsOn.emit(True)
    #         self.imagesAnnotationsFolderButton.setEnabled(False)
    #         self.speciesLabelThread.start()
    #     else:
    #         self.outputDatasetFolderButton.setEnabled(False)
    #         self.generateDatasetButton.setEnabled(False)

    

    # def generateDataset(self):
    #     if (self.imagesAnnotationsFolderPath != '') and (len(self.speciesLabels) > 0) and (self.outputdatasetFolderPath != ''):
    #         self.datasetThread = DatasetBuilder_DatasetThread(self.imagesAnnotationsFolderPath, self.speciesLabels, self.outputdatasetFolderPath, self.imageDims)
    #         self.datasetThread.currentAnnot.connect(self.updateCurrentAnnot)
    #         self.datasetThread.currentSaving.connect(self.updateCurrentSavingAction)
    #         self.datasetThread.activateThread()
    #         self.stopButton.setEnabled(True)
    #         self.threadIsOn.emit(True)
    #         self.imagesAnnotationsFolderButton.setEnabled(False)
    #         self.screenSpeciesButton.setEnabled(False)
    #         self.outputDatasetFolderButton.setEnabled(False)
    #         self.generateDatasetButton.setEnabled(False)
    #         self.imageDims.setEnabled(False)
    #         self.datasetThread.start()
    #     else:
    #         self.stopButton.setEnabled(False)
    
    # def stopDatasetGeneration(self):
    #     try:
    #         self.datasetThread
    #     except:
    #         pass
    #     else:
    #         self.datasetThread.stopThread()
    #         self.stopButton.setEnabled(False)
    #         self.threadIsOn.emit(False)
    #         self.imagesAnnotationsFolderButton.setEnabled(True)
    #         if self.imagesAnnotationsFolderPath != '':
    #             self.screenSpeciesButton.setEnabled(True)
    #         if len(self.speciesLabels) >= 1:
    #             self.outputDatasetFolderButton.setEnabled(True)
    #         if self.outputdatasetFolderPath != '':
    #             self.generateDatasetButton.setEnabled(True)
    #             self.imageDims.setEnabled(True)
    
    # def updateTotalNumberAnnotations(self, totalNumberAnnotations): 
    #     self.totalNumberAnnotations = totalNumberAnnotations
    #     self.progressBar.setRange(0, totalNumberAnnotations)
    #     self.progressBar.setValue(0)

    # def updateSpeciesLabels(self, speciesLabels):
    #     self.speciesLabels = speciesLabels
    #     if (len(self.speciesLabels) >= 1):
    #         self.screenSpeciesButton.setToolTip(str(self.speciesLabels))
    #         self.imagesAnnotationsFolderButton.setEnabled(True)
    #         self.outputDatasetFolderButton.setEnabled(True)
    #         self.threadIsOn.emit(False)
    #     else:
    #         self.screenSpeciesButton.setToolTip("No species screened")
    #         self.imagesAnnotationsFolderButton.setEnabled(True)
    #         self.outputDatasetFolderButton.setEnabled(False)
    #         self.threadIsOn.emit(False)
    
    # def updateCurrentAnnot(self, currentAnnot):
    #     self.progressBar.setValue(currentAnnot)
    #     if currentAnnot == self.totalNumberAnnotations:
    #         self.currentSavingActionLabel.setText("All images saved")
    #         self.stopButton.setEnabled(False)
    #         self.threadIsOn.emit(False)
    #         self.imagesAnnotationsFolderButton.setEnabled(True)
    #         if self.imagesAnnotationsFolderPath != '':
    #             self.screenSpeciesButton.setEnabled(True)
    #         if len(self.speciesLabels) >= 1:
    #             self.outputDatasetFolderButton.setEnabled(True)
    #         if self.outputdatasetFolderPath != '':
    #             self.generateDatasetButton.setEnabled(True)
    #             self.imageDims.setEnabled(True)
    
    # def updateCurrentSavingAction(self, text):
    #     if text == "...":
    #         self.currentSavingActionLabel.setText("...")
    #     else:
    #         self.currentSavingActionLabel.setText(text)