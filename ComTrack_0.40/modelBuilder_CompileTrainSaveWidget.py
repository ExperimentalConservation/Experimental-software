from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os

class ModelBuilder_CompileTrainSaveWidget(QGroupBox):

    launchCompileTrainSave = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.datasetPath = []
        self.modelPath = []
        self.encoderPath = []
        self.plotPath = []
        self.initWidget()
        self.makeButton()

    def initWidget(self):
        self.setTitle("Compile, Train && Save Model")
        self.setStyleSheet("""
                QGroupBox{font-weight: bold; border: 1px solid black; border-radius: 5px; margin-top: 0.6em;}
                QGroupBox::title{top: -0.5em; subcontrol-position: top center;}
                """)
        self.mainLayout = QVBoxLayout(self)
    
    def makeButton(self):
        # Learning Rate
        self.compileTrainSaveButton = QPushButton()
        self.compileTrainSaveButton.setEnabled(False)
        self.compileTrainSaveButton.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.compileTrainSaveButton.setIcon(QIcon(os.path.join(os.path.dirname(__file__), 'images/icons/play.png')))
        self.compileTrainSaveButton.setText("GO")
        self.compileTrainSaveButton.clicked.connect(self.compileTrainSaveModel)
        self.mainLayout.addWidget(self.compileTrainSaveButton)
    
    def compileTrainSaveModel(self):
        self.launchCompileTrainSave.emit(True)
    
    def updateDatasetPath(self, path):
        self.datasetPath = path
        if (len(self.datasetPath) > 0) and (len(self.modelPath) > 0) and (len(self.encoderPath) > 0) and (len(self.plotPath) > 0):
            self.compileTrainSaveButton.setEnabled(True)
        else:
            self.compileTrainSaveButton.setEnabled(False)
    
    def updateModelPath(self, path):
        self.modelPath = path
        if (len(self.datasetPath) > 0) and (len(self.modelPath) > 0) and (len(self.encoderPath) > 0) and (len(self.plotPath) > 0):
            self.compileTrainSaveButton.setEnabled(True)
        else:
            self.compileTrainSaveButton.setEnabled(False)
    
    def updateEncoderPath(self, path):
        self.encoderPath = path
        if (len(self.datasetPath) > 0) and (len(self.modelPath) > 0) and (len(self.encoderPath) > 0) and (len(self.plotPath) > 0):
            self.compileTrainSaveButton.setEnabled(True)
        else:
            self.compileTrainSaveButton.setEnabled(False)
    
    def updatePlotPath(self, path):
        self.plotPath = path
        if (len(self.datasetPath) > 0) and (len(self.modelPath) > 0) and (len(self.encoderPath) > 0) and (len(self.plotPath) > 0):
            self.compileTrainSaveButton.setEnabled(True)
        else:
            self.compileTrainSaveButton.setEnabled(False)
