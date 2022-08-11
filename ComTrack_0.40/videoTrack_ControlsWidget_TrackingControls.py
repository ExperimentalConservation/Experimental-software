from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class VideoTrack_TrackingControlsWidget(QGroupBox):

    def __init__(self):
        super().__init__()

        # initializing variables with random values, which will be updated when upload video
        self.videoTotalFrames = 100
        self.videoFPS = 10
        self.videoDuration = 10

        # running initialisation functions
        self.initWidget()
        self.makeSelectTrackingMethod()
        self.makeTrackingMethodNone()
        self.makeTrackingMethodKalmanFilter()
    
    def initWidget(self):
        self.setTitle("Tracking Controls")
        self.setCheckable(True)
        self.setChecked(False)
        self.toggled.connect(self.trackingControlsChecked)
        self.setStyleSheet("""
                QGroupBox{font-weight: bold; border: 1px solid black; border-radius: 5px; margin-top: 0.6em;}
                QGroupBox::title{top: -0.5em; subcontrol-position: top center;}
                """)
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setAlignment(Qt.AlignTop)
        self.potentialTrackingMethods = ["None"]
        self.detectionMethod = "None"
    
    def makeSelectTrackingMethod(self):
        self.selectTrackingMethodLayout = QHBoxLayout()
        self.selectTrackingMethodLayout.setAlignment(Qt.AlignTop)
        self.mainLayout.addLayout(self.selectTrackingMethodLayout)

        self.selectTrackingMethodTitle = QLabel("Tracking Method:")
        self.selectTrackingMethodTitle.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.selectTrackingMethodTitle.setStyleSheet("text-decoration: underline;")
        self.selectTrackingMethodLayout.addWidget(self.selectTrackingMethodTitle, alignment=Qt.AlignLeft)

        self.selectTrackingMethod = QComboBox()
        self.selectTrackingMethod.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.selectTrackingMethod.addItems(["None"])
        self.selectTrackingMethod.setCurrentIndex(0)
        self.selectTrackingMethod.currentIndexChanged.connect(self.updateTrackingParams)
        self.selectTrackingMethodLayout.addWidget(self.selectTrackingMethod)
    
    def makeTrackingMethodNone(self):
        self.trackingMethodNoneFrame = QFrame()
        self.trackingMethodNoneFrame.hide()
        self.trackingMethodNoneLayout = QVBoxLayout()
        self.trackingMethodNoneLayout.setAlignment(Qt.AlignTop)
        self.trackingMethodNoneFrame.setLayout(self.trackingMethodNoneLayout)
        self.mainLayout.addWidget(self.trackingMethodNoneFrame)

        self.trackingMethodNone = QLabel("No tracking method selected")
        self.trackingMethodNone.setAlignment(Qt.AlignCenter)
        self.trackingMethodNoneLayout.addWidget(self.trackingMethodNone)
    
    def makeTrackingMethodKalmanFilter(self):
        self.trackingMethodKalmanFilterFrame = QFrame()
        self.trackingMethodKalmanFilterFrame.hide()
        self.trackingMethodKalmanFilterLayout = QVBoxLayout()
        self.trackingMethodKalmanFilterLayout.setAlignment(Qt.AlignTop)
        self.trackingMethodKalmanFilterFrame.setLayout(self.trackingMethodKalmanFilterLayout)
        self.mainLayout.addWidget(self.trackingMethodKalmanFilterFrame)

        self.trackingMethodKalmanFilterNoiseParamLayout = QHBoxLayout()
        self.trackingMethodKalmanFilterLayout.addLayout(self.trackingMethodKalmanFilterNoiseParamLayout)
        self.trackingMethodKalmanFilterParametersNoiseTitle = QLabel("Noise:")
        self.trackingMethodKalmanFilterParametersNoiseTitle.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.trackingMethodKalmanFilterNoiseParamLayout.addWidget(self.trackingMethodKalmanFilterParametersNoiseTitle)
        self.trackingMethodKalmanFilterParametersNoise = QDoubleSpinBox()
        self.trackingMethodKalmanFilterParametersNoise.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.trackingMethodKalmanFilterParametersNoise.setRange(0, 999999)
        self.trackingMethodKalmanFilterParametersNoise.setSingleStep(0.1)
        self.trackingMethodKalmanFilterParametersNoise.setValue(1)
        self.trackingMethodKalmanFilterParametersNoise.setDecimals(5)
        self.trackingMethodKalmanFilterNoiseParamLayout.addWidget(self.trackingMethodKalmanFilterParametersNoise)
        self.trackingMethodKalmanFilterTimeStepParamLayout = QHBoxLayout()
        self.trackingMethodKalmanFilterLayout.addLayout(self.trackingMethodKalmanFilterTimeStepParamLayout)
        self.trackingMethodKalmanFilterParametersTimeStepTitle = QLabel("Time Step:")
        self.trackingMethodKalmanFilterParametersTimeStepTitle.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.trackingMethodKalmanFilterTimeStepParamLayout.addWidget(self.trackingMethodKalmanFilterParametersTimeStepTitle)
        self.trackingMethodKalmanFilterParametersTimeStep = QDoubleSpinBox()
        self.trackingMethodKalmanFilterParametersTimeStep.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.trackingMethodKalmanFilterParametersTimeStep.setRange(0, 999999)
        self.trackingMethodKalmanFilterParametersTimeStep.setSingleStep(0.01)
        self.trackingMethodKalmanFilterParametersTimeStep.setValue(0.01)
        self.trackingMethodKalmanFilterParametersTimeStep.setDecimals(3)
        self.trackingMethodKalmanFilterTimeStepParamLayout.addWidget(self.trackingMethodKalmanFilterParametersTimeStep)
        self.trackingMethodKalmanFilterMaxDistParamLayout = QHBoxLayout()
        self.trackingMethodKalmanFilterLayout.addLayout(self.trackingMethodKalmanFilterMaxDistParamLayout)
        self.trackingMethodKalmanFilterParametersMaxDistanceTitle = QLabel("Max. Distance:")
        self.trackingMethodKalmanFilterParametersMaxDistanceTitle.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.trackingMethodKalmanFilterMaxDistParamLayout.addWidget(self.trackingMethodKalmanFilterParametersMaxDistanceTitle)
        self.trackingMethodKalmanFilterParametersMaxDistance = QDoubleSpinBox()
        self.trackingMethodKalmanFilterParametersMaxDistance.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.trackingMethodKalmanFilterParametersMaxDistance.setRange(0, 999999)
        self.trackingMethodKalmanFilterParametersMaxDistance.setSingleStep(100)
        self.trackingMethodKalmanFilterParametersMaxDistance.setValue(20000)
        self.trackingMethodKalmanFilterParametersMaxDistance.setDecimals(0)
        self.trackingMethodKalmanFilterMaxDistParamLayout.addWidget(self.trackingMethodKalmanFilterParametersMaxDistance)

    # Function that triggers everytime we check/uncheck the tracking controls groupbox
    def trackingControlsChecked(self):
        if self.isChecked() is True:
            self.trackingMethodNoneFrame.show()
        else:
            self.restoreDefaultParameters()  # This will already add "None" to the item list, so we don't need to add it back
            if self.detectionMethod == "None":
                self.potentialTrackingMethods = []
            elif self.detectionMethod == "Single Object Bounding Box":
                self.potentialTrackingMethods = ["CSRT"]
            elif self.detectionMethod == "Thresholding":
                self.potentialTrackingMethods = ["Kalman Filter"]
            elif self.detectionMethod == "Background Subtraction":
                self.potentialTrackingMethods = ["Kalman Filter"]
            self.selectTrackingMethod.addItems(self.potentialTrackingMethods)
            self.trackingMethodNoneFrame.hide()
    
    # Function that triggers everytime we modify the tracking method
    def updateTrackingParams(self):
        if self.selectTrackingMethod.currentText() == "None":
            self.trackingMethodNoneFrame.show()
            self.trackingMethodKalmanFilterFrame.hide()
        elif self.selectTrackingMethod.currentText() == "Kalman Filter":
            self.trackingMethodNoneFrame.hide()
            self.trackingMethodKalmanFilterFrame.show()
        elif self.selectTrackingMethod.currentText() == "CSRT":
            self.trackingMethodNoneFrame.hide()
            self.trackingMethodKalmanFilterFrame.hide()

    # Function that triggers everytime the detection method is changed
    def updateTrackingMethods(self, method):
        self.selectTrackingMethod.clear()
        self.detectionMethod = method
        if self.detectionMethod == "None":
            self.potentialTrackingMethods = ["None"]
        elif self.detectionMethod == "Single Object Bounding Box":
            self.potentialTrackingMethods = ["None", "CSRT"]
        elif self.detectionMethod == "Thresholding":
            self.potentialTrackingMethods = ["None", "Kalman Filter"]
        elif self.detectionMethod == "Background Subtraction":
            self.potentialTrackingMethods = ["None", "Kalman Filter"]
        self.selectTrackingMethod.addItems(self.potentialTrackingMethods)
        if self.isChecked() is False:
            self.trackingMethodNoneFrame.hide()

    # Function that triggers when loading a new video
    def newVideoLoaded(self):
        self.restoreDefaultParameters()
        self.trackingMethodNoneFrame.hide()
        self.setChecked(False)
    
    # Function restoring the tracking parameters to their default values
    def restoreDefaultParameters(self):
        self.selectTrackingMethod.clear()
        self.selectTrackingMethod.addItems(["None"])
        self.selectTrackingMethod.setCurrentIndex(0)
        self.trackingMethodKalmanFilterParametersNoise.setValue(1)
        self.trackingMethodKalmanFilterParametersTimeStep.setValue(0.01)
        self.trackingMethodKalmanFilterParametersMaxDistance.setValue(20000)

    def loadTrackingParamsFromSavedControls(self, trackingSoup):
        self.setChecked(True)
        if (trackingSoup.find("tracking_method").string == "Kalman Filter"):
            self.selectTrackingMethod.clear()
            self.potentialTrackingMethods = ["None", "Kalman Filter"]
            self.selectTrackingMethod.addItems(self.potentialTrackingMethods)
            self.selectTrackingMethod.setCurrentIndex(1)
            self.trackingMethodKalmanFilterParametersNoise.setValue(float(trackingSoup.find("kfnoise").string))
            self.trackingMethodKalmanFilterParametersTimeStep.setValue(float(trackingSoup.find("kftimestep").string))
            self.trackingMethodKalmanFilterParametersMaxDistance.setValue(float(trackingSoup.find("kfmaxdistance").string))
