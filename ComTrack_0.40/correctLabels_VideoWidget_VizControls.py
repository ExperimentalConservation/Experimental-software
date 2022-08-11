from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import cv2

from aesthetics import QHLine, QVLine

class CorrectLabels_VizControlsWidget(QGroupBox):

    visualizationParams = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.vizParams = [
            False,  # 0
            255,  # 1
            255,  # 2
            255,  # 3
            0,  # 4
            0,  # 5
            False,  # 6
            255,  # 7
            255,  # 8
            255,  # 9
            0,  # 10
            False,  # 11
            255,  # 12
            255,  # 13
            255,  # 14
            0,  # 15
            False,  # 16
            255,  # 17
            255,  # 18
            255,  # 19
            0,  # 20
            False,  # 21
            False,  # 22
            255,  # 23
            255,  # 24
            255,  # 25
            cv2.FONT_HERSHEY_PLAIN,  # 26
            0,  # 27
            0  # 28
        ]
        self.visualizationParams.emit(self.vizParams)
        self.initWidget()
        self.makeScrollArea()
        self.makeInsideWidget()
        self.makeVizParams()

    def initWidget(self):
        self.setTitle("Visualization Controls")
        self.setStyleSheet("""
                QGroupBox{font-weight: bold; border: 1px solid black; border-radius: 5px; margin-top: 0.6em;}
                QGroupBox::title{top: -0.5em; subcontrol-position: top center;}
                """)
        self.mainLayout = QHBoxLayout(self)
        self.mainLayout.setAlignment(Qt.AlignBottom)
    
    def makeScrollArea(self):
        self.vizControlsScrollArea = QScrollArea()
        self.vizControlsScrollArea.setFrameShape(QFrame.NoFrame)
        self.vizControlsScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        # self.vizControlsScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.vizControlsScrollArea.setWidgetResizable(True)  
        self.mainLayout.addWidget(self.vizControlsScrollArea)
    
    def makeInsideWidget(self):
        self.insideWidget = QWidget()
        self.insideWidgetLayout = QHBoxLayout(self.insideWidget)
        self.insideWidgetLayout.setAlignment(Qt.AlignBottom)
        self.vizControlsScrollArea.setWidget(self.insideWidget)
    
    def makeVizParams(self):
        # Layouts
        self.centroidParamsLayout = QVBoxLayout()
        self.insideWidgetLayout.addLayout(self.centroidParamsLayout)
        separatorV1 = QVLine()
        self.insideWidgetLayout.addWidget(separatorV1)
        self.nBBoxParamsLayout = QVBoxLayout()
        self.insideWidgetLayout.addLayout(self.nBBoxParamsLayout)
        separatorV2 = QVLine()
        self.insideWidgetLayout.addWidget(separatorV2)
        self.lBBoxParamsLayout = QVBoxLayout()
        self.insideWidgetLayout.addLayout(self.lBBoxParamsLayout)
        separatorV3 = QVLine()
        self.insideWidgetLayout.addWidget(separatorV3)
        self.rBBoxParamsLayout = QVBoxLayout()
        self.insideWidgetLayout.addLayout(self.rBBoxParamsLayout)
        separatorV4 = QVLine()
        self.insideWidgetLayout.addWidget(separatorV4)
        self.trackingIDAndClassificationParamsLayout = QVBoxLayout()
        self.insideWidgetLayout.addLayout(self.trackingIDAndClassificationParamsLayout)
        self.trackingIDAndClassificationCheckboxesLayout = QHBoxLayout()
        self.trackingIDAndClassificationParamsLayout.addLayout(self.trackingIDAndClassificationCheckboxesLayout)
        self.trackingIDFontAndThicknessParamsLayout = QHBoxLayout()
        self.trackingIDAndClassificationParamsLayout.addLayout(self.trackingIDFontAndThicknessParamsLayout)
        self.trackingIDColorParamsLayout = QHBoxLayout()
        self.trackingIDAndClassificationParamsLayout.addLayout(self.trackingIDColorParamsLayout)
        separatorV5 = QVLine()
        self.insideWidgetLayout.addWidget(separatorV5)
        self.contourParamsLayout = QVBoxLayout()
        self.insideWidgetLayout.addLayout(self.contourParamsLayout)

        # Centroid viz parameters
        self.showCentroids = QCheckBox("Draw Centroids")
        self.showCentroids.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.showCentroids.stateChanged.connect(self.updateVizParams)
        self.centroidParamsLayout.addWidget(self.showCentroids, alignment=Qt.AlignCenter)
        self.showCentroidsColorsLayout = QHBoxLayout()
        self.centroidParamsLayout.addLayout(self.showCentroidsColorsLayout)
        self.showCentroidsRedLabel = QLabel("R:")
        self.showCentroidsRedLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.showCentroidsColorsLayout.addWidget(self.showCentroidsRedLabel)
        self.showCentroidsRed = QDoubleSpinBox()
        self.showCentroidsRed.setEnabled(False)
        self.showCentroidsRed.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.showCentroidsRed.setRange(0, 255)
        self.showCentroidsRed.setSingleStep(1)
        self.showCentroidsRed.setValue(255)
        self.showCentroidsRed.setDecimals(0)
        self.showCentroidsRed.editingFinished.connect(self.updateVizParams)
        self.showCentroidsColorsLayout.addWidget(self.showCentroidsRed)
        self.showCentroidsGreenLabel = QLabel("G:")
        self.showCentroidsGreenLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.showCentroidsColorsLayout.addWidget(self.showCentroidsGreenLabel)
        self.showCentroidsGreen = QDoubleSpinBox()
        self.showCentroidsGreen.setEnabled(False)
        self.showCentroidsGreen.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.showCentroidsGreen.setRange(0, 255)
        self.showCentroidsGreen.setSingleStep(1)
        self.showCentroidsGreen.setValue(255)
        self.showCentroidsGreen.setDecimals(0)
        self.showCentroidsGreen.editingFinished.connect(self.updateVizParams)
        self.showCentroidsColorsLayout.addWidget(self.showCentroidsGreen)
        self.showCentroidsBlueLabel = QLabel("B:")
        self.showCentroidsBlueLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.showCentroidsColorsLayout.addWidget(self.showCentroidsBlueLabel)
        self.showCentroidsBlue = QDoubleSpinBox()
        self.showCentroidsBlue.setEnabled(False)
        self.showCentroidsBlue.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.showCentroidsBlue.setRange(0, 255)
        self.showCentroidsBlue.setSingleStep(1)
        self.showCentroidsBlue.setValue(255)
        self.showCentroidsBlue.setDecimals(0)
        self.showCentroidsBlue.editingFinished.connect(self.updateVizParams)
        self.showCentroidsColorsLayout.addWidget(self.showCentroidsBlue)

        self.showCentroidsRadiusThicknessLayout = QHBoxLayout()
        self.centroidParamsLayout.addLayout(self.showCentroidsRadiusThicknessLayout)
        self.showCentroidsRadiusLabel = QLabel("Radius:")
        self.showCentroidsRadiusLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.showCentroidsRadiusThicknessLayout.addWidget(self.showCentroidsRadiusLabel)
        self.showCentroidsRadius = QDoubleSpinBox()
        self.showCentroidsRadius.setEnabled(False)
        self.showCentroidsRadius.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.showCentroidsRadius.setRange(1, 999)
        self.showCentroidsRadius.setSingleStep(1)
        self.showCentroidsRadius.setValue(2)
        self.showCentroidsRadius.setDecimals(0)
        self.showCentroidsRadius.editingFinished.connect(self.updateVizParams)
        self.showCentroidsRadiusThicknessLayout.addWidget(self.showCentroidsRadius)
        self.showCentroidsThicknessLabel = QLabel("Thickness:")
        self.showCentroidsThicknessLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.showCentroidsRadiusThicknessLayout.addWidget(self.showCentroidsThicknessLabel)
        self.showCentroidsThickness = QDoubleSpinBox()
        self.showCentroidsThickness.setEnabled(False)
        self.showCentroidsThickness.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.showCentroidsThickness.setRange(1, 99)
        self.showCentroidsThickness.setSingleStep(1)
        self.showCentroidsThickness.setValue(6)
        self.showCentroidsThickness.setDecimals(0)
        self.showCentroidsThickness.editingFinished.connect(self.updateVizParams)
        self.showCentroidsRadiusThicknessLayout.addWidget(self.showCentroidsThickness)

        # Normal Bounding Box viz parameters
        self.showNormalBBoxes = QCheckBox("Draw nBBox")
        self.showNormalBBoxes.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.showNormalBBoxes.stateChanged.connect(self.updateVizParams)
        self.nBBoxParamsLayout.addWidget(self.showNormalBBoxes, alignment=Qt.AlignCenter)
        self.showNormalBBoxesColorsLayout = QHBoxLayout()
        self.nBBoxParamsLayout.addLayout(self.showNormalBBoxesColorsLayout)
        self.showNormalBBoxesRedLabel = QLabel("R:")
        self.showNormalBBoxesRedLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.showNormalBBoxesColorsLayout.addWidget(self.showNormalBBoxesRedLabel)
        self.showNormalBBoxesRed = QDoubleSpinBox()
        self.showNormalBBoxesRed.setEnabled(False)
        self.showNormalBBoxesRed.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.showNormalBBoxesRed.setRange(0, 255)
        self.showNormalBBoxesRed.setSingleStep(1)
        self.showNormalBBoxesRed.setValue(255)
        self.showNormalBBoxesRed.setDecimals(0)
        self.showNormalBBoxesRed.editingFinished.connect(self.updateVizParams)
        self.showNormalBBoxesColorsLayout.addWidget(self.showNormalBBoxesRed)
        self.showNormalBBoxesGreenLabel = QLabel("G:")
        self.showNormalBBoxesGreenLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.showNormalBBoxesColorsLayout.addWidget(self.showNormalBBoxesGreenLabel)
        self.showNormalBBoxesGreen = QDoubleSpinBox()
        self.showNormalBBoxesGreen.setEnabled(False)
        self.showNormalBBoxesGreen.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.showNormalBBoxesGreen.setRange(0, 255)
        self.showNormalBBoxesGreen.setSingleStep(1)
        self.showNormalBBoxesGreen.setValue(255)
        self.showNormalBBoxesGreen.setDecimals(0)
        self.showNormalBBoxesGreen.editingFinished.connect(self.updateVizParams)
        self.showNormalBBoxesColorsLayout.addWidget(self.showNormalBBoxesGreen)
        self.showNormalBBoxesBlueLabel = QLabel("B:")
        self.showNormalBBoxesBlueLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.showNormalBBoxesColorsLayout.addWidget(self.showNormalBBoxesBlueLabel)
        self.showNormalBBoxesBlue = QDoubleSpinBox()
        self.showNormalBBoxesBlue.setEnabled(False)
        self.showNormalBBoxesBlue.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.showNormalBBoxesBlue.setRange(0, 255)
        self.showNormalBBoxesBlue.setSingleStep(1)
        self.showNormalBBoxesBlue.setValue(255)
        self.showNormalBBoxesBlue.setDecimals(0)
        self.showNormalBBoxesBlue.editingFinished.connect(self.updateVizParams)
        self.showNormalBBoxesColorsLayout.addWidget(self.showNormalBBoxesBlue)

        self.showNormalBBoxesThicknessLayout = QHBoxLayout()
        self.nBBoxParamsLayout.addLayout(self.showNormalBBoxesThicknessLayout)
        self.showNormalBBoxesThicknessLabel = QLabel("Thickness:")
        self.showNormalBBoxesThicknessLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.showNormalBBoxesThicknessLayout.addWidget(self.showNormalBBoxesThicknessLabel)
        self.showNormalBBoxesThickness = QDoubleSpinBox()
        self.showNormalBBoxesThickness.setEnabled(False)
        self.showNormalBBoxesThickness.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.showNormalBBoxesThickness.setRange(1, 99)
        self.showNormalBBoxesThickness.setSingleStep(1)
        self.showNormalBBoxesThickness.setValue(6)
        self.showNormalBBoxesThickness.setDecimals(0)
        self.showNormalBBoxesThickness.editingFinished.connect(self.updateVizParams)
        self.showNormalBBoxesThicknessLayout.addWidget(self.showNormalBBoxesThickness)

        # Large Bounding Box viz parameters
        self.showLargeBBoxes = QCheckBox("Draw lBBox")
        self.showLargeBBoxes.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.showLargeBBoxes.stateChanged.connect(self.updateVizParams)
        self.lBBoxParamsLayout.addWidget(self.showLargeBBoxes, alignment=Qt.AlignCenter)
        self.showLargeBBoxesColorsLayout = QHBoxLayout()
        self.lBBoxParamsLayout.addLayout(self.showLargeBBoxesColorsLayout)
        self.showLargeBBoxesRedLabel = QLabel("R:")
        self.showLargeBBoxesRedLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.showLargeBBoxesColorsLayout.addWidget(self.showLargeBBoxesRedLabel)
        self.showLargeBBoxesRed = QDoubleSpinBox()
        self.showLargeBBoxesRed.setEnabled(False)
        self.showLargeBBoxesRed.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.showLargeBBoxesRed.setRange(0, 255)
        self.showLargeBBoxesRed.setSingleStep(1)
        self.showLargeBBoxesRed.setValue(255)
        self.showLargeBBoxesRed.setDecimals(0)
        self.showLargeBBoxesRed.editingFinished.connect(self.updateVizParams)
        self.showLargeBBoxesColorsLayout.addWidget(self.showLargeBBoxesRed)
        self.showLargeBBoxesGreenLabel = QLabel("G:")
        self.showLargeBBoxesGreenLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.showLargeBBoxesColorsLayout.addWidget(self.showLargeBBoxesGreenLabel)
        self.showLargeBBoxesGreen = QDoubleSpinBox()
        self.showLargeBBoxesGreen.setEnabled(False)
        self.showLargeBBoxesGreen.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.showLargeBBoxesGreen.setRange(0, 255)
        self.showLargeBBoxesGreen.setSingleStep(1)
        self.showLargeBBoxesGreen.setValue(255)
        self.showLargeBBoxesGreen.setDecimals(0)
        self.showLargeBBoxesGreen.editingFinished.connect(self.updateVizParams)
        self.showLargeBBoxesColorsLayout.addWidget(self.showLargeBBoxesGreen)
        self.showLargeBBoxesBlueLabel = QLabel("B:")
        self.showLargeBBoxesBlueLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.showLargeBBoxesColorsLayout.addWidget(self.showLargeBBoxesBlueLabel)
        self.showLargeBBoxesBlue = QDoubleSpinBox()
        self.showLargeBBoxesBlue.setEnabled(False)
        self.showLargeBBoxesBlue.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.showLargeBBoxesBlue.setRange(0, 255)
        self.showLargeBBoxesBlue.setSingleStep(1)
        self.showLargeBBoxesBlue.setValue(255)
        self.showLargeBBoxesBlue.setDecimals(0)
        self.showLargeBBoxesBlue.editingFinished.connect(self.updateVizParams)
        self.showLargeBBoxesColorsLayout.addWidget(self.showLargeBBoxesBlue)

        self.showLargeBBoxesThicknessLayout = QHBoxLayout()
        self.lBBoxParamsLayout.addLayout(self.showLargeBBoxesThicknessLayout)
        self.showLargeBBoxesThicknessLabel = QLabel("Thickness:")
        self.showLargeBBoxesThicknessLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.showLargeBBoxesThicknessLayout.addWidget(self.showLargeBBoxesThicknessLabel)
        self.showLargeBBoxesThickness = QDoubleSpinBox()
        self.showLargeBBoxesThickness.setEnabled(False)
        self.showLargeBBoxesThickness.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.showLargeBBoxesThickness.setRange(1, 99)
        self.showLargeBBoxesThickness.setSingleStep(1)
        self.showLargeBBoxesThickness.setValue(6)
        self.showLargeBBoxesThickness.setDecimals(0)
        self.showLargeBBoxesThickness.editingFinished.connect(self.updateVizParams)
        self.showLargeBBoxesThicknessLayout.addWidget(self.showLargeBBoxesThickness)

        # Rotated Bounding Box viz parameters
        self.showRotatedBBoxes = QCheckBox("Draw rBBox")
        self.showRotatedBBoxes.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.showRotatedBBoxes.stateChanged.connect(self.updateVizParams)
        self.rBBoxParamsLayout.addWidget(self.showRotatedBBoxes, alignment=Qt.AlignCenter)
        self.showRotatedBBoxesColorsLayout = QHBoxLayout()
        self.rBBoxParamsLayout.addLayout(self.showRotatedBBoxesColorsLayout)
        self.showRotatedBBoxesRedLabel = QLabel("R:")
        self.showRotatedBBoxesRedLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.showRotatedBBoxesColorsLayout.addWidget(self.showRotatedBBoxesRedLabel)
        self.showRotatedBBoxesRed = QDoubleSpinBox()
        self.showRotatedBBoxesRed.setEnabled(False)
        self.showRotatedBBoxesRed.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.showRotatedBBoxesRed.setRange(0, 255)
        self.showRotatedBBoxesRed.setSingleStep(1)
        self.showRotatedBBoxesRed.setValue(255)
        self.showRotatedBBoxesRed.setDecimals(0)
        self.showRotatedBBoxesRed.editingFinished.connect(self.updateVizParams)
        self.showRotatedBBoxesColorsLayout.addWidget(self.showRotatedBBoxesRed)
        self.showRotatedBBoxesGreenLabel = QLabel("G:")
        self.showRotatedBBoxesGreenLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.showRotatedBBoxesColorsLayout.addWidget(self.showRotatedBBoxesGreenLabel)
        self.showRotatedBBoxesGreen = QDoubleSpinBox()
        self.showRotatedBBoxesGreen.setEnabled(False)
        self.showRotatedBBoxesGreen.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.showRotatedBBoxesGreen.setRange(0, 255)
        self.showRotatedBBoxesGreen.setSingleStep(1)
        self.showRotatedBBoxesGreen.setValue(255)
        self.showRotatedBBoxesGreen.setDecimals(0)
        self.showRotatedBBoxesGreen.editingFinished.connect(self.updateVizParams)
        self.showRotatedBBoxesColorsLayout.addWidget(self.showRotatedBBoxesGreen)
        self.showRotatedBBoxesBlueLabel = QLabel("B:")
        self.showRotatedBBoxesBlueLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.showRotatedBBoxesColorsLayout.addWidget(self.showRotatedBBoxesBlueLabel)
        self.showRotatedBBoxesBlue = QDoubleSpinBox()
        self.showRotatedBBoxesBlue.setEnabled(False)
        self.showRotatedBBoxesBlue.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.showRotatedBBoxesBlue.setRange(0, 255)
        self.showRotatedBBoxesBlue.setSingleStep(1)
        self.showRotatedBBoxesBlue.setValue(255)
        self.showRotatedBBoxesBlue.setDecimals(0)
        self.showRotatedBBoxesBlue.editingFinished.connect(self.updateVizParams)
        self.showRotatedBBoxesColorsLayout.addWidget(self.showRotatedBBoxesBlue)

        self.showRotatedBBoxesThicknessLayout = QHBoxLayout()
        self.rBBoxParamsLayout.addLayout(self.showRotatedBBoxesThicknessLayout)
        self.showRotatedBBoxesThicknessLabel = QLabel("Thickness:")
        self.showRotatedBBoxesThicknessLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.showRotatedBBoxesThicknessLayout.addWidget(self.showRotatedBBoxesThicknessLabel)
        self.showRotatedBBoxesThickness = QDoubleSpinBox()
        self.showRotatedBBoxesThickness.setEnabled(False)
        self.showRotatedBBoxesThickness.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.showRotatedBBoxesThickness.setRange(1, 99)
        self.showRotatedBBoxesThickness.setSingleStep(1)
        self.showRotatedBBoxesThickness.setValue(6)
        self.showRotatedBBoxesThickness.setDecimals(0)
        self.showRotatedBBoxesThickness.editingFinished.connect(self.updateVizParams)
        self.showRotatedBBoxesThicknessLayout.addWidget(self.showRotatedBBoxesThickness)

        # Tracking ID & Classification viz parameters
        self.showTrackingIDs = QCheckBox("Draw Tracking IDs")
        self.showTrackingIDs.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.showTrackingIDs.stateChanged.connect(self.updateVizParams)
        self.trackingIDAndClassificationCheckboxesLayout.addWidget(self.showTrackingIDs, alignment=Qt.AlignCenter|Qt.AlignTop)

        self.showClassViz = QCheckBox("Draw Classification")
        self.showClassViz.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.showClassViz.stateChanged.connect(self.updateVizParams)
        self.trackingIDAndClassificationCheckboxesLayout.addWidget(self.showClassViz, alignment=Qt.AlignCenter|Qt.AlignTop)

        self.trackingIDRedColorLabel = QLabel("R:")
        self.trackingIDRedColorLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.trackingIDColorParamsLayout.addWidget(self.trackingIDRedColorLabel)
        self.trackingIDRedColor = QDoubleSpinBox()
        self.trackingIDRedColor.setEnabled(False)
        self.trackingIDRedColor.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.trackingIDRedColor.setRange(0, 255)
        self.trackingIDRedColor.setSingleStep(1)
        self.trackingIDRedColor.setValue(255)
        self.trackingIDRedColor.setDecimals(0)
        self.trackingIDRedColor.editingFinished.connect(self.updateVizParams)
        self.trackingIDColorParamsLayout.addWidget(self.trackingIDRedColor)
        self.trackingIDGreenColorLabel = QLabel("G:")
        self.trackingIDGreenColorLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.trackingIDColorParamsLayout.addWidget(self.trackingIDGreenColorLabel)
        self.trackingIDGreenColor = QDoubleSpinBox()
        self.trackingIDGreenColor.setEnabled(False)
        self.trackingIDGreenColor.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.trackingIDGreenColor.setRange(0, 255)
        self.trackingIDGreenColor.setSingleStep(1)
        self.trackingIDGreenColor.setValue(255)
        self.trackingIDGreenColor.setDecimals(0)
        self.trackingIDGreenColor.editingFinished.connect(self.updateVizParams)
        self.trackingIDColorParamsLayout.addWidget(self.trackingIDGreenColor)
        self.trackingIDBlueColorLabel = QLabel("B:")
        self.trackingIDBlueColorLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.trackingIDColorParamsLayout.addWidget(self.trackingIDBlueColorLabel)
        self.trackingIDBlueColor = QDoubleSpinBox()
        self.trackingIDBlueColor.setEnabled(False)
        self.trackingIDBlueColor.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.trackingIDBlueColor.setRange(0, 255)
        self.trackingIDBlueColor.setSingleStep(1)
        self.trackingIDBlueColor.setValue(255)
        self.trackingIDBlueColor.setDecimals(0)
        self.trackingIDBlueColor.editingFinished.connect(self.updateVizParams)
        self.trackingIDColorParamsLayout.addWidget(self.trackingIDBlueColor)

        self.trackingIDFontFaceLabel = QLabel("Font Face:")
        self.trackingIDFontFaceLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.trackingIDFontAndThicknessParamsLayout.addWidget(self.trackingIDFontFaceLabel)
        self.trackingIDFontFace = QComboBox()
        self.trackingIDFontFace.setEnabled(False)
        self.trackingIDFontFace.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.trackingIDFontFace.addItems(["Simplex", "Plain", "Duplex", "Complex", "Triplex", "Complex Small", "Script Simplex", "Script Complex"])
        self.trackingIDFontFace.setCurrentIndex(1)
        self.trackingIDFontFace.currentIndexChanged.connect(self.updateVizParams)
        self.trackingIDFontAndThicknessParamsLayout.addWidget(self.trackingIDFontFace)

        self.trackingIDFontScaleLabel = QLabel("Font Scale:")
        self.trackingIDFontScaleLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.trackingIDFontAndThicknessParamsLayout.addWidget(self.trackingIDFontScaleLabel)
        self.trackingIDFontScale = QDoubleSpinBox()
        self.trackingIDFontScale.setEnabled(False)
        self.trackingIDFontScale.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.trackingIDFontScale.setRange(1, 99)
        self.trackingIDFontScale.setSingleStep(1)
        self.trackingIDFontScale.setValue(4)
        self.trackingIDFontScale.setDecimals(0)
        self.trackingIDFontScale.editingFinished.connect(self.updateVizParams)
        self.trackingIDFontAndThicknessParamsLayout.addWidget(self.trackingIDFontScale)

        self.trackingIDThicknessLabel = QLabel("Thickness:")
        self.trackingIDThicknessLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.trackingIDFontAndThicknessParamsLayout.addWidget(self.trackingIDThicknessLabel)
        self.trackingIDThickness = QDoubleSpinBox()
        self.trackingIDThickness.setEnabled(False)
        self.trackingIDThickness.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.trackingIDThickness.setRange(1, 99)
        self.trackingIDThickness.setSingleStep(1)
        self.trackingIDThickness.setValue(6)
        self.trackingIDThickness.setDecimals(0)
        self.trackingIDThickness.editingFinished.connect(self.updateVizParams)
        self.trackingIDFontAndThicknessParamsLayout.addWidget(self.trackingIDThickness)

        # Contour viz parameters
        self.showContours = QCheckBox("Draw Contours")
        self.showContours.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.showContours.stateChanged.connect(self.updateVizParams)
        self.contourParamsLayout.addWidget(self.showContours, alignment=Qt.AlignCenter)
        self.showContoursColorsLayout = QHBoxLayout()
        self.contourParamsLayout.addLayout(self.showContoursColorsLayout)
        self.showContoursRedLabel = QLabel("R:")
        self.showContoursRedLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.showContoursColorsLayout.addWidget(self.showContoursRedLabel)
        self.showContoursRed = QDoubleSpinBox()
        self.showContoursRed.setEnabled(False)
        self.showContoursRed.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.showContoursRed.setRange(0, 255)
        self.showContoursRed.setSingleStep(1)
        self.showContoursRed.setValue(255)
        self.showContoursRed.setDecimals(0)
        self.showContoursRed.editingFinished.connect(self.updateVizParams)
        self.showContoursColorsLayout.addWidget(self.showContoursRed)
        self.showContoursGreenLabel = QLabel("G:")
        self.showContoursGreenLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.showContoursColorsLayout.addWidget(self.showContoursGreenLabel)
        self.showContoursGreen = QDoubleSpinBox()
        self.showContoursGreen.setEnabled(False)
        self.showContoursGreen.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.showContoursGreen.setRange(0, 255)
        self.showContoursGreen.setSingleStep(1)
        self.showContoursGreen.setValue(255)
        self.showContoursGreen.setDecimals(0)
        self.showContoursGreen.editingFinished.connect(self.updateVizParams)
        self.showContoursColorsLayout.addWidget(self.showContoursGreen)
        self.showContoursBlueLabel = QLabel("B:")
        self.showContoursBlueLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.showContoursColorsLayout.addWidget(self.showContoursBlueLabel)
        self.showContoursBlue = QDoubleSpinBox()
        self.showContoursBlue.setEnabled(False)
        self.showContoursBlue.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.showContoursBlue.setRange(0, 255)
        self.showContoursBlue.setSingleStep(1)
        self.showContoursBlue.setValue(255)
        self.showContoursBlue.setDecimals(0)
        self.showContoursBlue.editingFinished.connect(self.updateVizParams)
        self.showContoursColorsLayout.addWidget(self.showContoursBlue)

        self.showContoursThicknessLayout = QHBoxLayout()
        self.contourParamsLayout.addLayout(self.showContoursThicknessLayout)
        self.showContoursThicknessLabel = QLabel("Thickness:")
        self.showContoursThicknessLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.showContoursThicknessLayout.addWidget(self.showContoursThicknessLabel)
        self.showContoursThickness = QDoubleSpinBox()
        self.showContoursThickness.setEnabled(False)
        self.showContoursThickness.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.showContoursThickness.setRange(1, 99)
        self.showContoursThickness.setSingleStep(1)
        self.showContoursThickness.setValue(6)
        self.showContoursThickness.setDecimals(0)
        self.showContoursThickness.editingFinished.connect(self.updateVizParams)
        self.showContoursThicknessLayout.addWidget(self.showContoursThickness)         


    def updateVizParams(self):
        if self.showCentroids.isChecked() is True:
            self.showCentroidsRed.setEnabled(True)
            self.showCentroidsGreen.setEnabled(True)
            self.showCentroidsBlue.setEnabled(True)
            self.showCentroidsRadius.setEnabled(True)
            self.showCentroidsThickness.setEnabled(True)
        elif self.showNormalBBoxes.isChecked() is False:
            self.showCentroidsRed.setEnabled(False)
            self.showCentroidsGreen.setEnabled(False)
            self.showCentroidsBlue.setEnabled(False)
            self.showCentroidsRadius.setEnabled(False)
            self.showCentroidsThickness.setEnabled(False)
        
        if self.showNormalBBoxes.isChecked() is True:
            self.showNormalBBoxesRed.setEnabled(True)
            self.showNormalBBoxesGreen.setEnabled(True)
            self.showNormalBBoxesBlue.setEnabled(True)
            self.showNormalBBoxesThickness.setEnabled(True)
        elif self.showNormalBBoxes.isChecked() is False:
            self.showNormalBBoxesRed.setEnabled(False)
            self.showNormalBBoxesGreen.setEnabled(False)
            self.showNormalBBoxesBlue.setEnabled(False)
            self.showNormalBBoxesThickness.setEnabled(False)
        
        if self.showLargeBBoxes.isChecked() is True:
            self.showLargeBBoxesRed.setEnabled(True)
            self.showLargeBBoxesGreen.setEnabled(True)
            self.showLargeBBoxesBlue.setEnabled(True)
            self.showLargeBBoxesThickness.setEnabled(True)
        elif self.showLargeBBoxes.isChecked() is False:
            self.showLargeBBoxesRed.setEnabled(False)
            self.showLargeBBoxesGreen.setEnabled(False)
            self.showLargeBBoxesBlue.setEnabled(False)
            self.showLargeBBoxesThickness.setEnabled(False)
        
        if self.showRotatedBBoxes.isChecked() is True:
            self.showRotatedBBoxesRed.setEnabled(True)
            self.showRotatedBBoxesGreen.setEnabled(True)
            self.showRotatedBBoxesBlue.setEnabled(True)
            self.showRotatedBBoxesThickness.setEnabled(True)
        elif self.showRotatedBBoxes.isChecked() is False:
            self.showRotatedBBoxesRed.setEnabled(False)
            self.showRotatedBBoxesGreen.setEnabled(False)
            self.showRotatedBBoxesBlue.setEnabled(False)
            self.showRotatedBBoxesThickness.setEnabled(False)
        
        if (self.showTrackingIDs.isChecked() is True) or (self.showClassViz.isChecked() is True):
            self.trackingIDRedColor.setEnabled(True)
            self.trackingIDGreenColor.setEnabled(True)
            self.trackingIDBlueColor.setEnabled(True)
            self.trackingIDFontFace.setEnabled(True)
            self.trackingIDFontScale.setEnabled(True)
            self.trackingIDThickness.setEnabled(True)
        elif (self.showTrackingIDs.isChecked() is False) and (self.showClassViz.isChecked() is False):
            self.trackingIDRedColor.setEnabled(False)
            self.trackingIDGreenColor.setEnabled(False)
            self.trackingIDBlueColor.setEnabled(False)
            self.trackingIDFontFace.setEnabled(False)
            self.trackingIDFontScale.setEnabled(False)
            self.trackingIDThickness.setEnabled(False)
        
        if self.showContours.isChecked() is True:
            self.showContoursRed.setEnabled(True)
            self.showContoursGreen.setEnabled(True)
            self.showContoursBlue.setEnabled(True)
            self.showContoursThickness.setEnabled(True)
        elif self.showNormalBBoxes.isChecked() is False:
            self.showContoursRed.setEnabled(False)
            self.showContoursGreen.setEnabled(False)
            self.showContoursBlue.setEnabled(False)
            self.showContoursThickness.setEnabled(False)
        
        drawCentroid = self.showCentroids.isChecked()
        centroidRed = self.showCentroidsRed.value()
        centroidGreen = self.showCentroidsGreen.value()
        centroidBlue = self.showCentroidsBlue.value()
        centroidRadius = int(self.showCentroidsRadius.value())
        centroidThickness = int(self.showCentroidsThickness.value())
        drawNBBox = self.showNormalBBoxes.isChecked()
        nBBoxRed = self.showNormalBBoxesRed.value()
        nBBoxGreen = self.showNormalBBoxesGreen.value()
        nBBoxBlue = self.showNormalBBoxesBlue.value()
        nBBoxThickness = int(self.showNormalBBoxesThickness.value())
        drawLBBox = self.showLargeBBoxes.isChecked()
        lBBoxRed = self.showLargeBBoxesRed.value()
        lBBoxGreen = self.showLargeBBoxesGreen.value()
        lBBoxBlue = self.showLargeBBoxesBlue.value()
        lBBoxThickness = int(self.showLargeBBoxesThickness.value())
        drawRBBox = self.showRotatedBBoxes.isChecked()
        rBBoxRed = self.showRotatedBBoxesRed.value()
        rBBoxGreen = self.showRotatedBBoxesGreen.value()
        rBBoxBlue = self.showRotatedBBoxesBlue.value()
        rBBoxThickness = int(self.showRotatedBBoxesThickness.value())
        drawTrackingIDs = self.showTrackingIDs.isChecked()
        drawClassification = self.showClassViz.isChecked()
        trackingIDsRed = self.trackingIDRedColor.value()
        trackingIDsGreen = self.trackingIDGreenColor.value()
        trackingIDsBlue = self.trackingIDBlueColor.value()
        if self.trackingIDFontFace.currentText() == "Simplex": trackingIDsFontFace = cv2.FONT_HERSHEY_SIMPLEX
        elif self.trackingIDFontFace.currentText() == "Plain": trackingIDsFontFace = cv2.FONT_HERSHEY_PLAIN
        elif self.trackingIDFontFace.currentText() == "Duplex": trackingIDsFontFace = cv2.FONT_HERSHEY_DUPLEX
        elif self.trackingIDFontFace.currentText() == "Complex": trackingIDsFontFace = cv2.FONT_HERSHEY_COMPLEX
        elif self.trackingIDFontFace.currentText() == "Triplex": trackingIDsFontFace = cv2.FONT_HERSHEY_TRIPLEX
        elif self.trackingIDFontFace.currentText() == "Complex Small": trackingIDsFontFace = cv2.FONT_HERSHEY_COMPLEX_SMALL
        elif self.trackingIDFontFace.currentText() == "Script Simplex": trackingIDsFontFace = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
        elif self.trackingIDFontFace.currentText() == "Script Complex": trackingIDsFontFace = cv2.FONT_HERSHEY_SCRIPT_COMPLEX
        trackingIDsFontScale = int(self.trackingIDFontScale.value())
        trackingIDsThickness = int(self.trackingIDThickness.value())
        drawContours = self.showContours.isChecked()
        contoursRed = self.showContoursRed.value()
        contoursGreen = self.showContoursGreen.value()
        contoursBlue = self.showContoursBlue.value()
        contoursThickness = int(self.showContoursThickness.value())

        self.vizParams = [
            drawCentroid,  # 0
            centroidRed,  # 1
            centroidGreen,  # 2
            centroidBlue,  # 3
            centroidRadius,  # 4
            centroidThickness,  # 5
            drawNBBox,  # 6
            nBBoxRed,  # 7
            nBBoxGreen,  # 8
            nBBoxBlue,  # 9
            nBBoxThickness,  # 10
            drawLBBox,  # 11
            lBBoxRed,  # 12
            lBBoxGreen,  # 13
            lBBoxBlue,  # 14
            lBBoxThickness,  # 15
            drawRBBox,  # 16
            rBBoxRed,  # 17
            rBBoxGreen,  # 18
            rBBoxBlue,  # 19
            rBBoxThickness,  # 20
            drawTrackingIDs, # 21
            drawClassification,  # 22
            trackingIDsRed,  # 23
            trackingIDsGreen,  # 24
            trackingIDsBlue,  # 25
            trackingIDsFontFace,  # 26
            trackingIDsFontScale,  # 27
            trackingIDsThickness,  # 28
            drawContours,  # 29
            contoursRed,  # 30
            contoursGreen,  # 31
            contoursBlue,  # 32
            contoursThickness,  # 33
        ]
        self.visualizationParams.emit(self.vizParams)
    
    def resetVizParams(self, signal):
        if signal is True:
            self.showCentroids.setChecked(False)
            self.showNormalBBoxes.setChecked(False)
            self.showLargeBBoxes.setChecked(False)
            self.showRotatedBBoxes.setChecked(False)
            self.showTrackingIDs.setChecked(False)
            self.showClassViz.setChecked(False)
            self.showContours.setChecked(False)