from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os

class VideoTrack_VideoControlsWidget(QGroupBox):

    previousFrameClicked = pyqtSignal(bool)
    nextFrameClicked = pyqtSignal(bool)
    videoPlayClicked = pyqtSignal(bool)
    videoStopClicked = pyqtSignal(bool)
    videoResetClicked = pyqtSignal(bool)
    videoSliderValue = pyqtSignal(object)
    videoSliderReleased = pyqtSignal(bool)
    fullScreenSignal = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.fullScreen = False
        self.initWidget()
        self.makeButtons()

    def initWidget(self):
        self.setTitle("Video Controls")
        self.setStyleSheet("""
                QGroupBox{font-weight: bold; border: 1px solid black; border-radius: 5px; margin-top: 0.6em;}
                QGroupBox::title{top: -0.5em; subcontrol-position: top center;}
                """)
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setAlignment(Qt.AlignTop)
    
    def makeButtons(self):
        # Video Action Buttons
        # Horizontal Layout for the Video Actions Buttons
        self.videoControlsActionButtonsLayout = QHBoxLayout()
        self.videoControlsActionButtonsLayout.setAlignment(Qt.AlignCenter|Qt.AlignTop)
        self.mainLayout.addLayout(self.videoControlsActionButtonsLayout)

        # Previous Frame Button
        self.videoControlsPreviousFrame = QPushButton("<", self)
        self.videoControlsPreviousFrame.setEnabled(False)
        self.videoControlsPreviousFrame.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.videoControlsPreviousFrame.clicked.connect(self.videoPreviousFrame)
        self.videoControlsActionButtonsLayout.addWidget(self.videoControlsPreviousFrame, alignment=Qt.AlignCenter)

        # Play Button
        self.videoControlsPlayButton = QPushButton("Play", self)
        self.videoControlsPlayButton.setIcon(QIcon(os.path.join(os.path.dirname(__file__), 'images/icons/play.png')))
        self.videoControlsPlayButton.setEnabled(False)
        self.videoControlsPlayButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.videoControlsPlayButton.clicked.connect(self.videoPlayVideo)
        self.videoControlsActionButtonsLayout.addWidget(self.videoControlsPlayButton, alignment=Qt.AlignCenter)

        # Stop Button
        self.videoControlsStopButton = QPushButton("Stop", self)
        self.videoControlsStopButton.setIcon(QIcon(os.path.join(os.path.dirname(__file__), 'images/icons/stop.png')))
        self.videoControlsStopButton.setEnabled(False)
        self.videoControlsStopButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.videoControlsStopButton.clicked.connect(self.videoStopVideo)
        self.videoControlsActionButtonsLayout.addWidget(self.videoControlsStopButton, alignment=Qt.AlignCenter)

        # Reset Button
        self.videoControlsResetButton = QPushButton("Reset", self)
        self.videoControlsResetButton.setIcon(QIcon(os.path.join(os.path.dirname(__file__), 'images/icons/reset.png')))
        self.videoControlsResetButton.setEnabled(False)
        self.videoControlsResetButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.videoControlsResetButton.clicked.connect(self.videoResetVideo)
        self.videoControlsActionButtonsLayout.addWidget(self.videoControlsResetButton, alignment=Qt.AlignCenter)

        # Next Frame Button
        self.videoControlsNextFrame = QPushButton(">", self)
        self.videoControlsNextFrame.setEnabled(False)
        self.videoControlsNextFrame.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.videoControlsNextFrame.clicked.connect(self.videoNextFrame)
        self.videoControlsActionButtonsLayout.addWidget(self.videoControlsNextFrame, alignment=Qt.AlignCenter)

        # Full Screen Button
        self.videoDisplay_Fullscreen = QPushButton("Maximize Window")
        self.videoDisplay_Fullscreen.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.videoDisplay_Fullscreen.clicked.connect(self.goFullScreen)
        self.videoControlsActionButtonsLayout.addWidget(self.videoDisplay_Fullscreen, alignment=Qt.AlignRight)

        # Video Frame Slider
        # Horizontal Layout for the Video Frame slider
        self.videoControlsFrameSliderLayout = QHBoxLayout()
        self.videoControlsFrameSliderLayout.setAlignment(Qt.AlignCenter)
        self.mainLayout.addLayout(self.videoControlsFrameSliderLayout)

        # Frame Slider
        self.videoControlsFrameSlider = QSlider(Qt.Horizontal, self)
        self.videoControlsFrameSlider.setEnabled(False)
        self.videoControlsFrameSlider.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.videoControlsFrameSlider.setRange(0, 1)
        self.videoControlsFrameSlider.setFocusPolicy(Qt.NoFocus)
        self.videoControlsFrameSlider.setPageStep(0)
        self.videoControlsFrameSlider.valueChanged.connect(self.videoSliderValueChanged)
        self.videoControlsFrameSlider.sliderPressed.connect(self.videoStopVideo)
        self.videoControlsFrameSlider.sliderReleased.connect(self.videoReleaseSlider)
        self.videoControlsFrameSliderLayout.addWidget(self.videoControlsFrameSlider)

        # Video Time and Frame Number Labels
        # Horizontal Layout for the Time and Frame number Labels
        self.videoControlsTimeFrameNumberLabelsLayout = QHBoxLayout()
        self.videoControlsTimeFrameNumberLabelsLayout.setAlignment(Qt.AlignCenter)
        self.mainLayout.addLayout(self.videoControlsTimeFrameNumberLabelsLayout)

        # Video Time Text Widget
        self.videoControlsTimeLabelTitle = QLabel(self)
        self.videoControlsTimeLabelTitle.setText("Time: ")
        self.videoControlsTimeFrameNumberLabelsLayout.addWidget(self.videoControlsTimeLabelTitle, alignment=Qt.AlignCenter)

        self.videoControlsTimeLabel = QLabel(self)
        self.videoControlsTimeLabel.setText("00:00:00")
        self.videoControlsTimeFrameNumberLabelsLayout.addWidget(self.videoControlsTimeLabel, alignment=Qt.AlignCenter)

        # Video Time Text / Frame Number text separator
        self.videoControlsTimeFrameNumberSeparator = QLabel(self)
        self.videoControlsTimeFrameNumberSeparator.setText(" | ")
        self.videoControlsTimeFrameNumberLabelsLayout.addWidget(self.videoControlsTimeFrameNumberSeparator, alignment=Qt.AlignCenter)

        # Frame Number Text Widget
        self.videoControlsFrameNumberLabelTitle = QLabel(self)
        self.videoControlsFrameNumberLabelTitle.setText("Frame: ")
        self.videoControlsTimeFrameNumberLabelsLayout.addWidget(self.videoControlsFrameNumberLabelTitle, alignment=Qt.AlignCenter)
        
        self.videoControlsFrameNumberLabel = QLabel(self)
        self.videoControlsFrameNumberLabel.setText(str(0))
        self.videoControlsTimeFrameNumberLabelsLayout.addWidget(self.videoControlsFrameNumberLabel, alignment=Qt.AlignCenter)

    def videoPreviousFrame(self):
        self.previousFrameClicked.emit(True)
    
    def videoNextFrame(self):
        self.nextFrameClicked.emit(True)
    
    def videoPlayVideo(self):
        self.videoPlayClicked.emit(True)
    
    def videoStopVideo(self):
        self.videoStopClicked.emit(True)
    
    def videoResetVideo(self):
        self.videoResetClicked.emit(True)
    
    def videoSliderValueChanged(self, framenumber):
        self.videoSliderValue.emit(framenumber)
    
    def videoReleaseSlider(self):
        self.videoSliderReleased.emit(True)
    
    def goFullScreen(self):
        if self.fullScreen is True:
            self.videoDisplay_Fullscreen.setText("Maximize Window")
            self.fullScreenSignal.emit(0)
            self.fullScreen = False
        elif self.fullScreen is False:
            self.fullScreenSignal.emit(1)
            self.fullScreen = True
            self.videoDisplay_Fullscreen.setText("Minimize Window")
