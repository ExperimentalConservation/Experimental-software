from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os

class ModelBuilder_InputOutputWidget(QGroupBox):

    datasetPath = pyqtSignal(object)
    modelPath = pyqtSignal(object)
    encoderPath = pyqtSignal(object)
    plotPath = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.initWidget()
        self.makeButtons()

    def initWidget(self):
        self.imageDatasetsFolderPath = []
        self.modelOutputPath = []
        self.labelEncoderOutputPath = []
        self.plotOutputPath = []
        self.setTitle("Input/Output Folders && Files")
        self.setStyleSheet("""
                QGroupBox{font-weight: bold; border: 1px solid black; border-radius: 5px; margin-top: 0.6em;}
                QGroupBox::title{top: -0.5em; subcontrol-position: top center;}
                """)
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setAlignment(Qt.AlignCenter)
    
    def makeButtons(self):
        # Image Datasets Folder Selector
        self.imageDatasetsFolderButton = QPushButton("Image Datasets Input Folder")
        self.imageDatasetsFolderButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.imageDatasetsFolderButton.setIcon(QIcon(os.path.join(os.path.dirname(__file__), 'images/icons/load.png')))
        self.imageDatasetsFolderButton.clicked.connect(self.imageDatasetsFolderSelection)
        self.mainLayout.addWidget(self.imageDatasetsFolderButton)
        # Image Dataset Folder Label
        self.imageDatasetsFolderLabel = QLabel()
        self.imageDatasetsFolderLabel.setText("No folder selected")
        self.mainLayout.addWidget(self.imageDatasetsFolderLabel, alignment=Qt.AlignCenter)

        # Model Output Filepath Selector
        self.modelOutputPathButton = QPushButton("Model Output File")
        self.modelOutputPathButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.modelOutputPathButton.setIcon(QIcon(os.path.join(os.path.dirname(__file__), 'images/icons/export.png')))
        self.modelOutputPathButton.clicked.connect(self.modelOutputPathSelection)
        self.mainLayout.addWidget(self.modelOutputPathButton)
        # Model Output Filepath Label
        self.modelOutputPathLabel = QLabel()
        self.modelOutputPathLabel.setText("No filepath provided")
        self.mainLayout.addWidget(self.modelOutputPathLabel, alignment=Qt.AlignCenter)

        # Label Encoder Output Filepath Selector
        self.labelEncoderOutputPathButton = QPushButton("Label Encoder Output File")
        self.labelEncoderOutputPathButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.labelEncoderOutputPathButton.setIcon(QIcon(os.path.join(os.path.dirname(__file__), 'images/icons/export.png')))
        self.labelEncoderOutputPathButton.clicked.connect(self.labelEncoderPathSelection)
        self.mainLayout.addWidget(self.labelEncoderOutputPathButton)
        # Label Encoder Output Filepath Label
        self.labelEncoderOutputPathLabel = QLabel()
        self.labelEncoderOutputPathLabel.setText("No filepath provided")
        self.mainLayout.addWidget(self.labelEncoderOutputPathLabel, alignment=Qt.AlignCenter)

        # Plot Output Filepath Selector
        self.plotOutputPathButton = QPushButton("Plot Output File")
        self.plotOutputPathButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.plotOutputPathButton.setIcon(QIcon(os.path.join(os.path.dirname(__file__), 'images/icons/export.png')))
        self.plotOutputPathButton.clicked.connect(self.plotOutputPathSelection)
        self.mainLayout.addWidget(self.plotOutputPathButton)
        # Plot Output Filepath Label
        self.plotOutputPathLabel = QLabel()
        self.plotOutputPathLabel.setText("No filepath provided")
        self.mainLayout.addWidget(self.plotOutputPathLabel, alignment=Qt.AlignCenter)
    
    def imageDatasetsFolderSelection(self):
        self.imageDatasetsFolderPath = QFileDialog.getExistingDirectory(self, "Select folder where image datasets are located", "./")
        if self.imageDatasetsFolderPath != '':
            self.imageDatasetsFolderLabel.setText(self.imageDatasetsFolderPath)
            self.datasetPath.emit(self.imageDatasetsFolderPath)
        else:
            self.imageDatasetsFolderLabel.setText("No folder selected")
            self.imageDatasetsFolderPath = []
            self.datasetPath.emit(self.imageDatasetsFolderPath)

    def modelOutputPathSelection(self):
        self.modelOutputPath = QFileDialog.getSaveFileName(self,'Save model as', "", "h5 files (*.h5)")
        if self.modelOutputPath[0] != '':
            self.modelOutputPathLabel.setText(self.modelOutputPath[0])
            self.modelPath.emit(self.modelOutputPath[0])
        else:
            self.modelOutputPathLabel.setText("No folder selected")
            self.modelOutputPath = []
            self.modelPath.emit(self.modelOutputPath)

    def labelEncoderPathSelection(self):
        self.labelEncoderOutoutPath = QFileDialog.getSaveFileName(self,'Save label encoder as', "", "pickle files (*.pickle)")
        if self.labelEncoderOutoutPath[0] != '':
            self.labelEncoderOutputPathLabel.setText(self.labelEncoderOutoutPath[0])
            self.encoderPath.emit(self.labelEncoderOutoutPath[0])
        else:
            self.labelEncoderOutputPathLabel.setText("No folder selected")
            self.labelEncoderOutoutPath = []
            self.encoderPath.emit(self.labelEncoderOutoutPath)

    def plotOutputPathSelection(self):
        self.plotOutputPath = QFileDialog.getSaveFileName(self,'Save plot as', "", "png files (*.png)")
        if self.plotOutputPath[0] != '':
            self.plotOutputPathLabel.setText(self.plotOutputPath[0])
            self.plotPath.emit(self.plotOutputPath[0])
        else:
            self.plotOutputPathLabel.setText("No folder selected")
            self.plotOutputPath = []
            self.plotPath.emit(self.plotOutputPath)
