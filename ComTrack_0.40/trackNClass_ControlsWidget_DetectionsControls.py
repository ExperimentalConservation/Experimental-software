from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class TrackNClass_DetectionsControlsWidget(QGroupBox):

    defineObjectBB = pyqtSignal(bool)
    saveObjectBB = pyqtSignal(bool)
    cancelObjectBB = pyqtSignal(bool)
    detectionMethodSelected = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.initWidget()
        self.makeSelectDetectionMethod()
        self.makeDetectionMethodNone()
        self.makeDetectionMethodObjectBB()
        self.makeDetectionMethodThresholding()
        self.makeDetectionBackgroundSubtraction()
        self.makeBackgroundSubtractionMethodNone()
        self.makeBackgroundSubtractionMethodKNN()
        self.makeContoursDetection()
        self.makeDetectionFeatures()
        
    def initWidget(self):
        self.setTitle("Detection Controls")
        self.setCheckable(True)
        self.setChecked(False)
        self.toggled.connect(self.detectionsControlsChecked)
        self.setStyleSheet("""
                QGroupBox{font-weight: bold; border: 1px solid black; border-radius: 5px; margin-top: 0.6em;}
                QGroupBox::title{top: -0.5em; subcontrol-position: top center;}
                """)
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setAlignment(Qt.AlignTop)
    
    def makeSelectDetectionMethod(self):
        self.selectDetectionMethodLayout = QHBoxLayout()
        self.selectDetectionMethodLayout.setAlignment(Qt.AlignTop)
        self.mainLayout.addLayout(self.selectDetectionMethodLayout)

        self.selectDetectionMethodTitle = QLabel("Detection Method:")
        self.selectDetectionMethodTitle.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.selectDetectionMethodTitle.setStyleSheet("text-decoration: underline;")
        self.selectDetectionMethodLayout.addWidget(self.selectDetectionMethodTitle)

        self.selectDetectionMethod = QComboBox()
        self.selectDetectionMethod.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.selectDetectionMethod.addItems(["None", "Single Object Bounding Box", "Thresholding", "Background Subtraction"])
        self.selectDetectionMethod.setCurrentIndex(0)
        self.selectDetectionMethod.currentIndexChanged.connect(self.detectionMethodChanged)
        self.selectDetectionMethodLayout.addWidget(self.selectDetectionMethod)
    
    def makeDetectionMethodNone(self):
        self.detectionMethodNoneFrame = QFrame()
        self.detectionMethodNoneFrame.hide()
        self.detectionMethodNoneLayout = QVBoxLayout()
        self.detectionMethodNoneLayout.setAlignment(Qt.AlignTop)
        self.detectionMethodNoneFrame.setLayout(self.detectionMethodNoneLayout)
        self.detectionMethodNone = QLabel("No detection method selected")
        self.detectionMethodNone.setAlignment(Qt.AlignCenter)
        self.detectionMethodNoneLayout.addWidget(self.detectionMethodNone)

        self.mainLayout.addWidget(self.detectionMethodNoneFrame)
    
    def makeDetectionMethodObjectBB(self):
        self.detectionMethodObjectBBFrame = QFrame()
        self.detectionMethodObjectBBFrame.hide()
        self.detectionMethodObjectBBLayout = QVBoxLayout()
        self.detectionMethodObjectBBLayout.setAlignment(Qt.AlignTop)
        self.detectionMethodObjectBBFrame.setLayout(self.detectionMethodObjectBBLayout)

        self.detectionMethodDefineObjectBBButton = QPushButton("Draw")
        self.detectionMethodDefineObjectBBButton.setEnabled(True)
        self.detectionMethodDefineObjectBBButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.detectionMethodDefineObjectBBButton.clicked.connect(self.detectionMethodObjectBB_defineBB)
        self.detectionMethodObjectBBLayout.addWidget(self.detectionMethodDefineObjectBBButton)

        self.detectionMethodSaveObjectBBButton = QPushButton("Save")
        self.detectionMethodSaveObjectBBButton.setEnabled(False)
        self.detectionMethodSaveObjectBBButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.detectionMethodSaveObjectBBButton.clicked.connect(self.detectionMethodObjectBB_saveBB)
        self.detectionMethodObjectBBLayout.addWidget(self.detectionMethodSaveObjectBBButton)

        self.detectionMethodCancelObjectBBButton = QPushButton("Cancel")
        self.detectionMethodCancelObjectBBButton.setEnabled(False)
        self.detectionMethodCancelObjectBBButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.detectionMethodCancelObjectBBButton.clicked.connect(self.detectionMethodObjectBB_cancelBB)
        self.detectionMethodObjectBBLayout.addWidget(self.detectionMethodCancelObjectBBButton)

        self.mainLayout.addWidget(self.detectionMethodObjectBBFrame)
    
    def makeDetectionMethodThresholding(self):
        self.detectionMethodThreshFrame = QFrame()
        self.detectionMethodThreshFrame.hide()
        self.detectionMethodThreshLayout = QVBoxLayout()
        self.detectionMethodThreshLayout.setAlignment(Qt.AlignTop)
        self.detectionMethodThreshFrame.setLayout(self.detectionMethodThreshLayout)

        self.detectionMethodThresh_ThreshValLayout = QHBoxLayout()
        self.detectionMethodThreshLayout.addLayout(self.detectionMethodThresh_ThreshValLayout)
        self.detectionMethodThresh_ThreshValLabel = QLabel("Threshold Value:")
        self.detectionMethodThresh_ThreshValLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.detectionMethodThresh_ThreshValLayout.addWidget(self.detectionMethodThresh_ThreshValLabel)
        self.detectionMethodThresh_ThreshVal = QDoubleSpinBox()
        self.detectionMethodThresh_ThreshVal.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.detectionMethodThresh_ThreshVal.setRange(0, 255)
        self.detectionMethodThresh_ThreshVal.setSingleStep(5)
        self.detectionMethodThresh_ThreshVal.setDecimals(0)
        self.detectionMethodThresh_ThreshVal.setValue(100)
        self.detectionMethodThresh_ThreshValLayout.addWidget(self.detectionMethodThresh_ThreshVal)

        self.detectionMethodThresh_MaxValLayout = QHBoxLayout()
        self.detectionMethodThreshLayout.addLayout(self.detectionMethodThresh_MaxValLayout)
        self.detectionMethodThresh_MaxValLabel = QLabel("Maximum Value:")
        self.detectionMethodThresh_MaxValLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.detectionMethodThresh_MaxValLayout.addWidget(self.detectionMethodThresh_MaxValLabel)
        self.detectionMethodThresh_MaxVal = QDoubleSpinBox()
        self.detectionMethodThresh_MaxVal.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.detectionMethodThresh_MaxVal.setRange(0, 255)
        self.detectionMethodThresh_MaxVal.setSingleStep(5)
        self.detectionMethodThresh_MaxVal.setDecimals(0)
        self.detectionMethodThresh_MaxVal.setValue(255)
        self.detectionMethodThresh_MaxValLayout.addWidget(self.detectionMethodThresh_MaxVal)

        self.detectionMethodThresh_TypeLayout = QHBoxLayout()
        self.detectionMethodThreshLayout.addLayout(self.detectionMethodThresh_TypeLayout)
        self.detectionMethodThresh_TypeLabel = QLabel("Thresholding type:")
        self.detectionMethodThresh_TypeLabel.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.detectionMethodThresh_TypeLayout.addWidget(self.detectionMethodThresh_TypeLabel)
        self.detectionMethodThresh_Type = QComboBox()
        self.detectionMethodThresh_Type.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.detectionMethodThresh_Type.addItems(["THRESH_BINARY", "THRESH_BINARY_INV", "THRESH_TRUNC", "THRESH_TOZERO", "THRESH_TOZERO_INV", "THRESH_MASK", "THRESH_OTSU", "THRESH_TRIANGLE"])
        self.detectionMethodThresh_Type.setCurrentIndex(0)
        self.detectionMethodThresh_TypeLayout.addWidget(self.detectionMethodThresh_Type)

        self.mainLayout.addWidget(self.detectionMethodThreshFrame)

    def makeDetectionBackgroundSubtraction(self):
        self.detectionMethodBackSubFrame = QFrame()
        self.detectionMethodBackSubFrame.hide()
        self.detectionMethodBackSubLayout = QVBoxLayout()
        self.detectionMethodBackSubLayout.setAlignment(Qt.AlignTop)
        self.detectionMethodBackSubFrame.setLayout(self.detectionMethodBackSubLayout)

        self.mainLayout.addWidget(self.detectionMethodBackSubFrame)

        self.detectionMethodBackSub_BackSubMethodLayout = QHBoxLayout()
        self.detectionMethodBackSubLayout.addLayout(self.detectionMethodBackSub_BackSubMethodLayout)
        self.detectionMethodBackSub_BackSubMethodTitle = QLabel("Background Subtraction Method:")
        self.detectionMethodBackSub_BackSubMethodTitle.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.detectionMethodBackSub_BackSubMethodLayout.addWidget(self.detectionMethodBackSub_BackSubMethodTitle)
        self.detectionMethodBackSub_BackSubMethod = QComboBox()
        self.detectionMethodBackSub_BackSubMethod.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.detectionMethodBackSub_BackSubMethod.addItems(["None", "KNN"])
        self.detectionMethodBackSub_BackSubMethod.setCurrentIndex(0)
        self.detectionMethodBackSub_BackSubMethod.currentIndexChanged.connect(self.backSubMethodChanged)
        self.detectionMethodBackSub_BackSubMethodLayout.addWidget(self.detectionMethodBackSub_BackSubMethod)

    def makeBackgroundSubtractionMethodNone(self):
        self.backgroundSubtractionMethodNoneFrame = QFrame()
        self.backgroundSubtractionMethodNoneFrame.hide()
        self.backgroundSubtractionMethodNoneLayout = QVBoxLayout()
        self.backgroundSubtractionMethodNoneLayout.setAlignment(Qt.AlignTop)
        self.backgroundSubtractionMethodNoneFrame.setLayout(self.backgroundSubtractionMethodNoneLayout)
        self.backgroundSubtractionMethodNone = QLabel("No background subtraction method selected")
        self.backgroundSubtractionMethodNone.setAlignment(Qt.AlignCenter)
        self.backgroundSubtractionMethodNoneLayout.addWidget(self.backgroundSubtractionMethodNone)

        self.detectionMethodBackSubLayout.addWidget(self.backgroundSubtractionMethodNoneFrame)

    def makeBackgroundSubtractionMethodKNN(self):   
        self.backgroundSubtractionMethodKNNFrame = QFrame()
        self.backgroundSubtractionMethodKNNFrame.hide()
        self.backgroundSubtractionMethodKNNLayout = QVBoxLayout()
        self.backgroundSubtractionMethodKNNLayout.setAlignment(Qt.AlignTop)
        self.backgroundSubtractionMethodKNNFrame.setLayout(self.backgroundSubtractionMethodKNNLayout)

        self.backgroundSubtractionMethodKNNHistoryLayout = QHBoxLayout()
        self.backgroundSubtractionMethodKNNLayout.addLayout(self.backgroundSubtractionMethodKNNHistoryLayout)
        self.backgroundSubtractionMethodKNNHistoryTitle = QLabel("History")
        self.backgroundSubtractionMethodKNNHistoryTitle.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.backgroundSubtractionMethodKNNHistoryLayout.addWidget(self.backgroundSubtractionMethodKNNHistoryTitle)
        self.backgroundSubtractionMethodKNNHistory = QDoubleSpinBox()
        self.backgroundSubtractionMethodKNNHistory.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.backgroundSubtractionMethodKNNHistory.setRange(0, 999999)
        self.backgroundSubtractionMethodKNNHistory.setSingleStep(10)
        self.backgroundSubtractionMethodKNNHistory.setDecimals(0)
        self.backgroundSubtractionMethodKNNHistory.setValue(20)
        self.backgroundSubtractionMethodKNNHistoryLayout.addWidget(self.backgroundSubtractionMethodKNNHistory)

        self.backgroundSubtractionMethodKNNThresholdLayout = QHBoxLayout()
        self.backgroundSubtractionMethodKNNLayout.addLayout(self.backgroundSubtractionMethodKNNThresholdLayout)
        self.backgroundSubtractionMethodKNNThresholdTitle = QLabel("Threshold")
        self.backgroundSubtractionMethodKNNThresholdTitle.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.backgroundSubtractionMethodKNNThresholdLayout.addWidget(self.backgroundSubtractionMethodKNNThresholdTitle)
        self.backgroundSubtractionMethodKNNThreshold = QDoubleSpinBox()
        self.backgroundSubtractionMethodKNNThreshold.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.backgroundSubtractionMethodKNNThreshold.setRange(0, 999999)
        self.backgroundSubtractionMethodKNNThreshold.setSingleStep(100)
        self.backgroundSubtractionMethodKNNThreshold.setDecimals(0)
        self.backgroundSubtractionMethodKNNThreshold.setValue(2000)
        self.backgroundSubtractionMethodKNNThresholdLayout.addWidget(self.backgroundSubtractionMethodKNNThreshold)

        self.backgroundSubtractionMethodKNNShadowsLayout = QVBoxLayout()
        self.backgroundSubtractionMethodKNNLayout.addLayout(self.backgroundSubtractionMethodKNNShadowsLayout)
        self.backgroundSubtractionMethodKNNDetectShadows = QCheckBox("Detect Shadows")
        self.backgroundSubtractionMethodKNNDetectShadows.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.backgroundSubtractionMethodKNNDetectShadows.stateChanged.connect(self.backSubKNNDetectShadowsChanged)
        self.backgroundSubtractionMethodKNNShadowsLayout.addWidget(self.backgroundSubtractionMethodKNNDetectShadows)
        self.backgroundSubtractionMethodKNNShadowsValueLayout = QHBoxLayout()
        self.backgroundSubtractionMethodKNNShadowsLayout.addLayout(self.backgroundSubtractionMethodKNNShadowsValueLayout)
        self.backgroundSubtractionMethodKNNShadowsValueTitle = QLabel("Shadows Value:")
        self.backgroundSubtractionMethodKNNShadowsValueTitle.hide()
        self.backgroundSubtractionMethodKNNShadowsValueTitle.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.backgroundSubtractionMethodKNNShadowsValueLayout.addWidget(self.backgroundSubtractionMethodKNNShadowsValueTitle)
        self.backgroundSubtractionMethodKNNShadowsValue = QDoubleSpinBox()
        self.backgroundSubtractionMethodKNNShadowsValue.hide()
        self.backgroundSubtractionMethodKNNShadowsValue.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.backgroundSubtractionMethodKNNShadowsValue.setRange(0, 255)
        self.backgroundSubtractionMethodKNNShadowsValue.setSingleStep(1)
        self.backgroundSubtractionMethodKNNShadowsValue.setDecimals(0)
        self.backgroundSubtractionMethodKNNShadowsValue.setValue(127)
        self.backgroundSubtractionMethodKNNShadowsValueLayout.addWidget(self.backgroundSubtractionMethodKNNShadowsValue)
        self.backgroundSubtractionMethodKNNShadowsThreshLayout = QHBoxLayout()
        self.backgroundSubtractionMethodKNNShadowsLayout.addLayout(self.backgroundSubtractionMethodKNNShadowsThreshLayout)
        self.backgroundSubtractionMethodKNNShadowsThresholdTitle = QLabel("Shadows Threshold:")
        self.backgroundSubtractionMethodKNNShadowsThresholdTitle.hide()
        self.backgroundSubtractionMethodKNNShadowsThresholdTitle.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.backgroundSubtractionMethodKNNShadowsThreshLayout.addWidget(self.backgroundSubtractionMethodKNNShadowsThresholdTitle)
        self.backgroundSubtractionMethodKNNShadowsThreshold = QDoubleSpinBox()
        self.backgroundSubtractionMethodKNNShadowsThreshold.hide()
        self.backgroundSubtractionMethodKNNShadowsThreshold.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.backgroundSubtractionMethodKNNShadowsThreshold.setRange(0.01, 999999)
        self.backgroundSubtractionMethodKNNShadowsThreshold.setSingleStep(0.1)
        self.backgroundSubtractionMethodKNNShadowsThreshold.setDecimals(2)
        self.backgroundSubtractionMethodKNNShadowsThreshold.setValue(0.5)
        self.backgroundSubtractionMethodKNNShadowsThreshLayout.addWidget(self.backgroundSubtractionMethodKNNShadowsThreshold)

        self.detectionMethodBackSubLayout.addWidget(self.backgroundSubtractionMethodKNNFrame)
    
    def makeContoursDetection(self):
        self.contoursDetectionFrame = QFrame()
        self.contoursDetectionFrame.hide()
        self.contoursDetectionLayout = QVBoxLayout()
        self.contoursDetectionLayout.setAlignment(Qt.AlignTop)
        self.contoursDetectionFrame.setLayout(self.contoursDetectionLayout)
        self.mainLayout.addWidget(self.contoursDetectionFrame)

        self.contoursDetectionTitle = QLabel("Contour Detection Parameters:")
        self.contoursDetectionTitle.setStyleSheet("text-decoration: underline;")
        self.contoursDetectionLayout.addWidget(self.contoursDetectionTitle)

        self.contoursDetectionMethodLayout = QHBoxLayout()
        self.contoursDetectionLayout.addLayout(self.contoursDetectionMethodLayout)
        self.contoursDetectionMethodTitle = QLabel("Method:")
        self.contoursDetectionMethodTitle.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.contoursDetectionMethodLayout.addWidget(self.contoursDetectionMethodTitle)
        self.contoursDetectionMethod = QComboBox()
        self.contoursDetectionMethod.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.contoursDetectionMethod.addItems(["CHAIN_APPROX_SIMPLE", "CHAIN_APPROX_NONE"])
        self.contoursDetectionMethod.setCurrentIndex(0)
        self.contoursDetectionMethodLayout.addWidget(self.contoursDetectionMethod)

        self.contoursDetectionModeLayout = QHBoxLayout()
        self.contoursDetectionLayout.addLayout(self.contoursDetectionModeLayout)
        self.contoursDetectionModeTitle = QLabel("Mode:")
        self.contoursDetectionModeTitle.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.contoursDetectionModeLayout.addWidget(self.contoursDetectionModeTitle)
        self.contoursDetectionMode = QComboBox()
        self.contoursDetectionMode.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.contoursDetectionMode.addItems(["RETR_EXTERNAL", "RETR_TREE", "RETR_LIST", "RETR_CCOMP"])
        self.contoursDetectionMode.setCurrentIndex(0)
        self.contoursDetectionModeLayout.addWidget(self.contoursDetectionMode)

        self.contoursDetectionMinAreaLayout = QHBoxLayout()
        self.contoursDetectionLayout.addLayout(self.contoursDetectionMinAreaLayout)
        self.contoursDetectionMinAreaTitle = QLabel("Min. Area:")
        self.contoursDetectionMinAreaTitle.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.contoursDetectionMinAreaLayout.addWidget(self.contoursDetectionMinAreaTitle)
        self.contoursDetectionMinArea = QDoubleSpinBox()
        self.contoursDetectionMinArea.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.contoursDetectionMinArea.setRange(0, 999999)
        self.contoursDetectionMinArea.setSingleStep(10)
        self.contoursDetectionMinArea.setValue(15)
        self.contoursDetectionMinArea.setDecimals(0)
        self.contoursDetectionMinAreaLayout.addWidget(self.contoursDetectionMinArea)

        self.contoursDetectionMaxAreaLayout = QHBoxLayout()
        self.contoursDetectionLayout.addLayout(self.contoursDetectionMaxAreaLayout)
        self.contoursDetectionMaxAreaTitle = QLabel("Max. Area:")
        self.contoursDetectionMaxAreaTitle.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.contoursDetectionMaxAreaLayout.addWidget(self.contoursDetectionMaxAreaTitle)
        self.contoursDetectionMaxArea = QDoubleSpinBox()
        self.contoursDetectionMaxArea.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.contoursDetectionMaxArea.setRange(0, 999999)
        self.contoursDetectionMaxArea.setSingleStep(10)
        self.contoursDetectionMaxArea.setValue(5000)
        self.contoursDetectionMaxArea.setDecimals(0)
        self.contoursDetectionMaxAreaLayout.addWidget(self.contoursDetectionMaxArea)
    
    def makeDetectionFeatures(self):
        self.detectionFeaturesFrame = QFrame()
        self.detectionFeaturesFrame.hide()
        self.detectionFeaturesLayout = QVBoxLayout()
        self.detectionFeaturesLayout.setAlignment(Qt.AlignTop)
        self.detectionFeaturesFrame.setLayout(self.detectionFeaturesLayout)
        self.mainLayout.addWidget(self.detectionFeaturesFrame)

        self.detectionFeaturesTitle = QLabel("Other Detection Parameters:")
        self.detectionFeaturesTitle.setStyleSheet("text-decoration: underline;")
        self.detectionFeaturesLayout.addWidget(self.detectionFeaturesTitle)

        self.detectionFeaturesPreLabelDetectionsLayout = QHBoxLayout()
        self.detectionFeaturesLayout.addLayout(self.detectionFeaturesPreLabelDetectionsLayout)
        self.detectionFeaturesPreLabelDetections = QCheckBox("Pre-label detections")
        self.detectionFeaturesPreLabelDetections.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.detectionFeaturesPreLabelDetections.stateChanged.connect(self.preLabelDetectionsChanged)
        self.detectionFeaturesPreLabelDetectionsLayout.addWidget(self.detectionFeaturesPreLabelDetections)
        self.detectionFeaturesPreLabelDetectionsTitle = QLabel("Label:")
        self.detectionFeaturesPreLabelDetectionsTitle.hide()
        self.detectionFeaturesPreLabelDetectionsTitle.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.detectionFeaturesPreLabelDetectionsLayout.addWidget(self.detectionFeaturesPreLabelDetectionsTitle)
        self.detectionFeaturesPreLabelDetectionsEntry = QLineEdit()
        self.detectionFeaturesPreLabelDetectionsEntry.hide()
        self.detectionFeaturesPreLabelDetectionsEntry.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.detectionFeaturesPreLabelDetectionsLayout.addWidget(self.detectionFeaturesPreLabelDetectionsEntry)
        self.detectionFeaturesPreLabelDetectionsEntry.setText("Species")
        self.detectionFeaturesPreLabelDetectionsLayout.addWidget(self.detectionFeaturesPreLabelDetectionsEntry)

        self.detectionFeaturesEnlargeBBoxesLayout = QHBoxLayout()
        self.detectionFeaturesLayout.addLayout(self.detectionFeaturesEnlargeBBoxesLayout)
        self.detectionFeaturesEnlargeBBoxes = QCheckBox("Enlarge Bounding Box(es)")
        self.detectionFeaturesEnlargeBBoxes.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.detectionFeaturesEnlargeBBoxes.stateChanged.connect(self.enlargeBBoxesChanged)
        self.detectionFeaturesEnlargeBBoxesLayout.addWidget(self.detectionFeaturesEnlargeBBoxes)
        self.detectionFeaturesEnlargeBBoxesTitle = QLabel("Value:")
        self.detectionFeaturesEnlargeBBoxesTitle.hide()
        self.detectionFeaturesEnlargeBBoxesTitle.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.detectionFeaturesEnlargeBBoxesLayout.addWidget(self.detectionFeaturesEnlargeBBoxesTitle)
        self.detectionFeaturesEnlargeBBoxesEntry = QDoubleSpinBox()
        self.detectionFeaturesEnlargeBBoxesEntry.hide()
        self.detectionFeaturesEnlargeBBoxesEntry.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.detectionFeaturesEnlargeBBoxesEntry.setRange(0, 999999)
        self.detectionFeaturesEnlargeBBoxesEntry.setSingleStep(5)
        self.detectionFeaturesEnlargeBBoxesEntry.setValue(25)
        self.detectionFeaturesEnlargeBBoxesEntry.setDecimals(0)
        self.detectionFeaturesEnlargeBBoxesLayout.addWidget(self.detectionFeaturesEnlargeBBoxesEntry)

        self.detectionFeaturesIgnoreOverlappingBBoxesLayout = QHBoxLayout()
        self.detectionFeaturesLayout.addLayout(self.detectionFeaturesIgnoreOverlappingBBoxesLayout)
        self.detectionFeaturesIgnoreOverlappingBBoxes = QCheckBox("Ignore Overlapping BBoxes")
        self.detectionFeaturesIgnoreOverlappingBBoxes.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.detectionFeaturesIgnoreOverlappingBBoxes.stateChanged.connect(self.ignoreOverlappingBBoxes)
        self.detectionFeaturesIgnoreOverlappingBBoxesLayout.addWidget(self.detectionFeaturesIgnoreOverlappingBBoxes)
        self.detectionFeaturesIgnoreOverlappingBBoxesTitle = QLabel("IOU:")
        self.detectionFeaturesIgnoreOverlappingBBoxesTitle.hide()
        self.detectionFeaturesIgnoreOverlappingBBoxesTitle.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.detectionFeaturesIgnoreOverlappingBBoxesLayout.addWidget(self.detectionFeaturesIgnoreOverlappingBBoxesTitle)
        self.detectionFeaturesIgnoreOverlappingBBoxesEntry = QDoubleSpinBox()
        self.detectionFeaturesIgnoreOverlappingBBoxesEntry.hide()
        self.detectionFeaturesIgnoreOverlappingBBoxesEntry.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.detectionFeaturesIgnoreOverlappingBBoxesEntry.setRange(0, 0.99)
        self.detectionFeaturesIgnoreOverlappingBBoxesEntry.setSingleStep(0.01)
        self.detectionFeaturesIgnoreOverlappingBBoxesEntry.setValue(0)
        self.detectionFeaturesIgnoreOverlappingBBoxesEntry.setDecimals(2)
        self.detectionFeaturesIgnoreOverlappingBBoxesLayout.addWidget(self.detectionFeaturesIgnoreOverlappingBBoxesEntry)

        self.detectionFeaturesRemoveBGLayout = QHBoxLayout()
        self.detectionFeaturesLayout.addLayout(self.detectionFeaturesRemoveBGLayout)
        self.detectionFeaturesRemoveBG = QCheckBox("Remove Background")
        self.detectionFeaturesRemoveBG.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.detectionFeaturesRemoveBG.stateChanged.connect(self.removeBGChanged)
        self.detectionFeaturesRemoveBGLayout.addWidget(self.detectionFeaturesRemoveBG)

    def detectionsControlsChecked(self):
        if self.isChecked() is True:
            self.detectionMethodNoneFrame.show()
        else:
            self.restoreDefaultParameters()
            self.detectionMethodNoneFrame.hide()

    def detectionMethodChanged(self):
        self.detectionMethodSelected.emit(self.selectDetectionMethod.currentText())
        if self.selectDetectionMethod.currentText() == "None":
            self.detectionMethodNoneFrame.show()
            self.detectionMethodObjectBBFrame.hide()
            self.detectionMethodThreshFrame.hide()
            self.detectionMethodBackSub_BackSubMethod.setCurrentIndex(0)
            self.detectionMethodBackSubFrame.hide()
            self.contoursDetectionFrame.hide()
            self.detectionFeaturesFrame.hide()
        if self.selectDetectionMethod.currentText() == "Single Object Bounding Box":
            self.detectionMethodNoneFrame.hide()
            self.detectionMethodObjectBBFrame.show()
            self.detectionMethodThreshFrame.hide()
            self.detectionMethodBackSub_BackSubMethod.setCurrentIndex(0)
            self.detectionMethodBackSubFrame.hide()
            self.contoursDetectionFrame.hide()
            self.detectionFeaturesEnlargeBBoxes.setEnabled(True)
            self.detectionFeaturesIgnoreOverlappingBBoxes.setEnabled(False)
            self.detectionFeaturesRemoveBG.setEnabled(False)
            self.detectionFeaturesFrame.show()
        if self.selectDetectionMethod.currentText() == "Thresholding":
            self.detectionMethodNoneFrame.hide()
            self.detectionMethodObjectBBFrame.hide()
            self.detectionMethodThreshFrame.show()
            self.detectionMethodBackSub_BackSubMethod.setCurrentIndex(0)
            self.detectionMethodBackSubFrame.hide()
            self.contoursDetectionFrame.show()
            self.detectionFeaturesEnlargeBBoxes.setEnabled(True)
            self.detectionFeaturesIgnoreOverlappingBBoxes.setEnabled(True)
            self.detectionFeaturesRemoveBG.setEnabled(True)
            self.detectionFeaturesFrame.show()
        if self.selectDetectionMethod.currentText() == "Background Subtraction":
            self.detectionMethodNoneFrame.hide()
            self.detectionMethodObjectBBFrame.hide()
            self.detectionMethodThreshFrame.hide()
            self.detectionMethodBackSubFrame.show()
            self.backgroundSubtractionMethodNoneFrame.show()
            self.backgroundSubtractionMethodKNNFrame.hide()
            self.contoursDetectionFrame.show()
            self.detectionFeaturesEnlargeBBoxes.setEnabled(True)
            self.detectionFeaturesIgnoreOverlappingBBoxes.setEnabled(True)
            self.detectionFeaturesRemoveBG.setEnabled(True)
            self.detectionFeaturesFrame.show()
    
    def detectionMethodObjectBB_defineBB(self):
        self.defineObjectBB.emit(True)
        self.selectDetectionMethod.setEnabled(False)
        self.detectionMethodDefineObjectBBButton.setEnabled(False)
        self.detectionMethodSaveObjectBBButton.setEnabled(True)
    
    def detectionMethodObjectBB_saveBB(self):
        self.saveObjectBB.emit(True)
        self.selectDetectionMethod.setEnabled(True)
        self.detectionMethodSaveObjectBBButton.setEnabled(False)
        self.detectionMethodCancelObjectBBButton.setEnabled(True)
    
    def detectionMethodObjectBB_cancelBB(self):
        self.cancelObjectBB.emit(True)
        self.selectDetectionMethod.setEnabled(True)
        self.detectionMethodDefineObjectBBButton.setEnabled(True)
        self.detectionMethodSaveObjectBBButton.setEnabled(False)
        self.detectionMethodCancelObjectBBButton.setEnabled(False)
    
    def backSubMethodChanged(self):
        if self.detectionMethodBackSub_BackSubMethod.currentText() == "None":
            self.backgroundSubtractionMethodNoneFrame.show()
            self.backgroundSubtractionMethodKNNFrame.hide()
        if self.detectionMethodBackSub_BackSubMethod.currentText() == "KNN":
            self.backgroundSubtractionMethodNoneFrame.hide()
            self.backgroundSubtractionMethodKNNFrame.show()
    
    def backSubKNNDetectShadowsChanged(self):
        if self.backgroundSubtractionMethodKNNDetectShadows.isChecked() is True:
            self.backgroundSubtractionMethodKNNShadowsValueTitle.show()
            self.backgroundSubtractionMethodKNNShadowsValue.show()
            self.backgroundSubtractionMethodKNNShadowsThresholdTitle.show()
            self.backgroundSubtractionMethodKNNShadowsThreshold.show()
        else: 
            self.backgroundSubtractionMethodKNNShadowsValueTitle.hide()
            self.backgroundSubtractionMethodKNNShadowsValue.hide()
            self.backgroundSubtractionMethodKNNShadowsThresholdTitle.hide()
            self.backgroundSubtractionMethodKNNShadowsThreshold.hide()
    
    def preLabelDetectionsChanged(self):
        if self.detectionFeaturesPreLabelDetections.isChecked() is True:
            self.detectionFeaturesPreLabelDetectionsTitle.show()
            self.detectionFeaturesPreLabelDetectionsEntry.show()
        else:
            self.detectionFeaturesPreLabelDetectionsTitle.hide()
            self.detectionFeaturesPreLabelDetectionsEntry.hide()
    
    def enlargeBBoxesChanged(self):
        if self.detectionFeaturesEnlargeBBoxes.isChecked() is True:
            self.detectionFeaturesEnlargeBBoxesTitle.show()
            self.detectionFeaturesEnlargeBBoxesEntry.show()
        else:
            self.detectionFeaturesEnlargeBBoxesTitle.hide()
            self.detectionFeaturesEnlargeBBoxesEntry.hide()
        
    def ignoreOverlappingBBoxes(self):
        if self.detectionFeaturesIgnoreOverlappingBBoxes.isChecked() is True:
            self.detectionFeaturesIgnoreOverlappingBBoxesTitle.show()
            self.detectionFeaturesIgnoreOverlappingBBoxesEntry.show()
        else:
            self.detectionFeaturesIgnoreOverlappingBBoxesTitle.hide()
            self.detectionFeaturesIgnoreOverlappingBBoxesEntry.hide()

    def removeBGChanged(self):
        pass

    def newVideoLoaded(self):
        self.restoreDefaultParameters()
        self.detectionMethodNoneFrame.hide()
        self.detectionMethodObjectBBFrame.hide()
        self.detectionMethodThreshFrame.hide()
        self.detectionMethodBackSubFrame.hide()
        self.backgroundSubtractionMethodNoneFrame.hide()
        self.backgroundSubtractionMethodKNNFrame.hide()
        self.backgroundSubtractionMethodKNNShadowsValueTitle.hide()
        self.backgroundSubtractionMethodKNNShadowsValue.hide()
        self.backgroundSubtractionMethodKNNShadowsThresholdTitle.hide()
        self.backgroundSubtractionMethodKNNShadowsThreshold.hide()
        self.contoursDetectionFrame.hide()
        self.detectionFeaturesFrame.hide()
        self.detectionFeaturesPreLabelDetectionsTitle.hide()
        self.detectionFeaturesPreLabelDetectionsEntry.hide()
        self.detectionFeaturesEnlargeBBoxesTitle.hide()
        self.detectionFeaturesEnlargeBBoxesEntry.hide()
        self.detectionFeaturesIgnoreOverlappingBBoxesTitle.hide()
        self.detectionFeaturesIgnoreOverlappingBBoxesEntry.hide()
        self.setChecked(False)
    
    def restoreDefaultParameters(self):
        self.selectDetectionMethod.setCurrentIndex(0)
        self.detectionMethodThresh_ThreshVal.setValue(100)
        self.detectionMethodThresh_MaxVal.setValue(255)
        self.detectionMethodThresh_Type.setCurrentIndex(0)
        self.detectionMethodBackSub_BackSubMethod.setCurrentIndex(0)
        self.backgroundSubtractionMethodKNNHistory.setValue(20)
        self.backgroundSubtractionMethodKNNThreshold.setValue(2000)
        self.backgroundSubtractionMethodKNNDetectShadows.setChecked(False)
        self.backgroundSubtractionMethodKNNShadowsValue.setValue(127)
        self.backgroundSubtractionMethodKNNShadowsThreshold.setValue(0.5)
        self.contoursDetectionMethod.setCurrentIndex(0)
        self.contoursDetectionMode.setCurrentIndex(0)
        self.contoursDetectionMinArea.setValue(60)
        self.contoursDetectionMaxArea.setValue(5000)
        self.detectionFeaturesPreLabelDetections.setChecked(False)
        self.detectionFeaturesPreLabelDetectionsEntry.setText("Species")
        self.detectionFeaturesEnlargeBBoxes.setChecked(False)
        self.detectionFeaturesEnlargeBBoxesEntry.setValue(25)
        self.detectionFeaturesIgnoreOverlappingBBoxes.setChecked(False)
        self.detectionFeaturesIgnoreOverlappingBBoxesEntry.setValue(0)

    def loadDetectionParamsFromSavedControls(self, detectionSoup):
        self.setChecked(True)
        if (detectionSoup.find("detection_method").string == "Single Object Bounding Box"):
            self.selectDetectionMethod.setCurrentIndex(1)
        elif (detectionSoup.find("detection_method").string == "Thresholding"):
            self.selectDetectionMethod.setCurrentIndex(2)
            self.detectionMethodThresh_ThreshVal.setValue(int(detectionSoup.find("thresholding_threshval").string))
            self.detectionMethodThresh_MaxVal.setValue(int(detectionSoup.find("thresholding_maxval").string))
            if (str(detectionSoup.find("thresholding_type").string) == "THRESH_BINARY"):
                self.detectionMethodThresh_Type.setCurrentIndex(0)
            elif (str(detectionSoup.find("thresholding_type").string) == "THRESH_BINARY_INV"):
                self.detectionMethodThresh_Type.setCurrentIndex(1)
            elif (str(detectionSoup.find("thresholding_type").string) == "THRESH_TRUNC"):
                self.detectionMethodThresh_Type.setCurrentIndex(2)
            elif (str(detectionSoup.find("thresholding_type").string) == "THRESH_TOZERO"):
                self.detectionMethodThresh_Type.setCurrentIndex(3)
            elif (str(detectionSoup.find("thresholding_type").string) == "THRESH_TOZERO_INV"):
                self.detectionMethodThresh_Type.setCurrentIndex(4)
            elif (str(detectionSoup.find("thresholding_type").string) == "THRESH_MASK"):
                self.detectionMethodThresh_Type.setCurrentIndex(5)
            elif (str(detectionSoup.find("thresholding_type").string) == "THRESH_OTSU"):
                self.detectionMethodThresh_Type.setCurrentIndex(6)
            elif (str(detectionSoup.find("thresholding_type").string) == "THRESH_TRIANGLE"):
                self.detectionMethodThresh_Type.setCurrentIndex(7)
        elif (detectionSoup.find("detection_method").string == "Background Subtraction"):
            self.selectDetectionMethod.setCurrentIndex(3)
            if (str(detectionSoup.find("subtractmethod").string) == "None"):
                self.detectionMethodBackSub_BackSubMethod.setCurrentIndex(0)
            elif (str(detectionSoup.find("subtractmethod").string) == "KNN"):
                self.detectionMethodBackSub_BackSubMethod.setCurrentIndex(1)
                self.backgroundSubtractionMethodKNNHistory.setValue(int(detectionSoup.find("knn_history").string))
                self.backgroundSubtractionMethodKNNThreshold.setValue(int(detectionSoup.find("knn_threshold").string))
                if (str(detectionSoup.find("knn_detectshadows").string) == "True"):
                    self.backgroundSubtractionMethodKNNDetectShadows.setChecked(True)
                    self.backgroundSubtractionMethodKNNShadowsValue.setValue(int(detectionSoup.find("knn_shadowsvalue").string))
                    self.backgroundSubtractionMethodKNNShadowsThreshold.setValue(float(detectionSoup.find("knn_shadowsthreshold").string))
        
        if (detectionSoup.find("detection_method").string == "Thresholding") or (detectionSoup.find("detection_method").string == "Background Subtraction"):
            if (str(detectionSoup.find("contourdetection_method").string) == "CHAIN_APPROX_SIMPLE"):
                self.contoursDetectionMethod.setCurrentIndex(0)
            elif (str(detectionSoup.find("contourdetection_method").string) == "CHAIN_APPROX_NONE"):
                self.contoursDetectionMethod.setCurrentIndex(1)
            
            if (str(detectionSoup.find("contourdetection_mode").string) == "RETR_EXTERNAL"):
                self.contoursDetectionMode.setCurrentIndex(0)
            elif (str(detectionSoup.find("contourdetection_mode").string) == "RETR_TREE"):
                self.contoursDetectionMode.setCurrentIndex(1)
            elif (str(detectionSoup.find("contourdetection_mode").string) == "RETR_LIST"):
                self.contoursDetectionMode.setCurrentIndex(2)
            elif (str(detectionSoup.find("contourdetection_mode").string) == "RETR_CCOMP"):
                self.contoursDetectionMode.setCurrentIndex(3)
            
            self.contoursDetectionMinArea.setValue(int(detectionSoup.find("contourdetection_minarea").string))
            self.contoursDetectionMaxArea.setValue(int(detectionSoup.find("contourdetection_maxarea").string))
        
        if (detectionSoup.find("detection_method").string == "Single Object Bounding Box") or (detectionSoup.find("detection_method").string == "Thresholding") or (detectionSoup.find("detection_method").string == "Background Subtraction"):
            if (str(detectionSoup.find("prelabelling").string) == "True"):
                self.detectionFeaturesPreLabelDetections.setChecked(True)
                self.detectionFeaturesPreLabelDetectionsEntry.setText(str(detectionSoup.find("prelabel_entry").string))
            if (str(detectionSoup.find("enlargebboxes").string) == "True"):
                self.detectionFeaturesEnlargeBBoxes.setChecked(True)
                self.detectionFeaturesEnlargeBBoxesEntry.setValue(int(detectionSoup.find("enlargebboxes_entry").string))
        
        if (detectionSoup.find("detection_method").string == "Thresholding") or (detectionSoup.find("detection_method").string == "Background Subtraction"):
            if (str(detectionSoup.find("ignoreoverlappingbboxes").string) == "True"):
                self.detectionFeaturesIgnoreOverlappingBBoxes.setChecked(True)
                self.detectionFeaturesIgnoreOverlappingBBoxesEntry.setValue(float(detectionSoup.find("ignoreoverlappingbboxes_entry").string))
