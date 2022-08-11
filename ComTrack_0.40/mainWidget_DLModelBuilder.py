from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from modelBuilder_InputOutputWidget import ModelBuilder_InputOutputWidget
from modelBuilder_TrainingParamsWidget import ModelBuilder_TrainingParamsWidget
from modelBuilder_DataAugmentationParamsWidget import ModelBuilder_DataAugmentationParamsWidget
from modelBuilder_CompileTrainSaveWidget import ModelBuilder_CompileTrainSaveWidget
from consoleWidget import ConsoleWidget
from modelBuilder_BuilderThread import BuilderThread

class MainWidgetDLModelBuilder(QWidget):
    def __init__(self):
        super().__init__()
        self.initWidget()
        self.makeInputOutputWidget()
        self.makeTrainingParamsWidget()
        self.makeDataAugmentationParamsWidget()
        self.makeCompileTrainSaveWidget()
        self.makeConsoleWidget()
    
    def initWidget(self):
        self.modelBuilderLayout = QVBoxLayout(self)
        self.modelInputsParamsRunLayout = QHBoxLayout()
        self.modelBuilderLayout.addLayout(self.modelInputsParamsRunLayout)
        self.modelConsoleLayout = QVBoxLayout()
        self.modelBuilderLayout.addLayout(self.modelConsoleLayout)

    def makeInputOutputWidget(self):
        self.inputOutputWidget = ModelBuilder_InputOutputWidget()
        self.inputOutputWidget.datasetPath.connect(self.updateDatasetPath)
        self.inputOutputWidget.modelPath.connect(self.updateModelPath)
        self.inputOutputWidget.encoderPath.connect(self.updateEncoderPath)
        self.inputOutputWidget.plotPath.connect(self.updatePlotPath)
        self.inputOutputWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.modelInputsParamsRunLayout.addWidget(self.inputOutputWidget)
    
    def makeTrainingParamsWidget(self):
        self.trainingParamsWidget = ModelBuilder_TrainingParamsWidget()
        self.trainingParamsWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.modelInputsParamsRunLayout.addWidget(self.trainingParamsWidget)
    
    def makeDataAugmentationParamsWidget(self):
        self.dataAugmentationParamsWidget = ModelBuilder_DataAugmentationParamsWidget()
        self.dataAugmentationParamsWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.modelInputsParamsRunLayout.addWidget(self.dataAugmentationParamsWidget)
    
    def makeCompileTrainSaveWidget(self):
        self.compileTrainSaveWidget = ModelBuilder_CompileTrainSaveWidget()
        self.compileTrainSaveWidget.launchCompileTrainSave.connect(self.compileTrainSaveModel)
        self.compileTrainSaveWidget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.modelInputsParamsRunLayout.addWidget(self.compileTrainSaveWidget)
    
    def makeConsoleWidget(self):
        self.consoleWidget = ConsoleWidget()
        self.consoleWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.modelConsoleLayout.addWidget(self.consoleWidget)
    
    def updateDatasetPath(self, path):
        self.compileTrainSaveWidget.updateDatasetPath(path)
    
    def updateModelPath(self, path):
        self.compileTrainSaveWidget.updateModelPath(path)
    
    def updateEncoderPath(self, path):
        self.compileTrainSaveWidget.updateEncoderPath(path)
    
    def updatePlotPath(self, path):
        self.compileTrainSaveWidget.updatePlotPath(path)
    
    def compileTrainSaveModel(self, signal):
        if signal is True:
            self.model = BuilderThread(self.compileTrainSaveWidget, self.trainingParamsWidget, self.dataAugmentationParamsWidget)
            self.model.play()
            self.model.start()
            
