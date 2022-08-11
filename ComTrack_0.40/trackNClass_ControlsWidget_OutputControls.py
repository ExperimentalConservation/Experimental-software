from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os

class TrackNClass_OutputControlsWidget(QGroupBox):

    def __init__(self):
        super().__init__()

        # initializing variables with random values, which will be updated when upload video
        self.videoTotalFrames = 100
        self.videoFPS = 10
        self.videoDuration = 10

        # running initialisation functions
        self.initWidget()
        self.makeOutputStartStop()
        self.makeOutputExports()
    
    def initWidget(self):
        self.setTitle("Output Controls")
        self.setCheckable(True)
        self.setChecked(False)
        self.toggled.connect(self.outputControlsChecked)
        self.setStyleSheet("""
                QGroupBox{font-weight: bold; border: 1px solid black; border-radius: 5px; margin-top: 0.6em;}
                QGroupBox::title{top: -0.5em; subcontrol-position: top center;}
                """)
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setAlignment(Qt.AlignTop)

    def makeOutputStartStop(self):
        self.outputStartStopFrame = QFrame()
        self.outputStartStopFrame.hide()
        self.outputStartStopLayout = QVBoxLayout()
        self.outputStartStopLayout.setAlignment(Qt.AlignTop)
        self.outputStartStopFrame.setLayout(self.outputStartStopLayout)
        self.mainLayout.addWidget(self.outputStartStopFrame)

        self.outputStartLayout = QHBoxLayout()
        self.outputStartStopLayout.addLayout(self.outputStartLayout)
        self.outputStartFrameTitle = QLabel("Start Tracking at Frame:")
        self.outputStartFrameTitle.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.outputStartLayout.addWidget(self.outputStartFrameTitle)
        self.outputStartFrame = QDoubleSpinBox()
        self.outputStartFrame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.outputStartFrame.setRange(1, 999999)
        self.outputStartFrame.setSingleStep(1)
        self.outputStartFrame.setValue(1)
        self.outputStartFrame.setDecimals(0)
        self.outputStartFrame.editingFinished.connect(self.updateTrackingStartTime)
        self.outputStartLayout.addWidget(self.outputStartFrame)
        self.outputStartTimeTitle = QLabel("or at Time:")
        self.outputStartTimeTitle.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.outputStartLayout.addWidget(self.outputStartTimeTitle)
        self.outputStartTime = QTimeEdit()
        self.outputStartTime.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.outputStartTime.setDisplayFormat('hh:mm:ss')
        self.outputStartTime.setTimeRange(QTime(00, 00, 00), QTime(00, 00, 1))
        self.outputStartTime.setTime(QTime(00, 00, 00))
        self.outputStartTime.editingFinished.connect(self.updateTrackingStartFrame)
        self.outputStartLayout.addWidget(self.outputStartTime)

        self.outputStopLayout = QHBoxLayout()
        self.outputStartStopLayout.addLayout(self.outputStopLayout)
        self.outputStopFrameTitle = QLabel("Stop Tracking at Frame:")
        self.outputStopFrameTitle.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.outputStopLayout.addWidget(self.outputStopFrameTitle)
        self.outputStopFrame = QDoubleSpinBox()
        self.outputStopFrame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.outputStopFrame.setRange(1, 999999)
        self.outputStopFrame.setSingleStep(1)
        self.outputStopFrame.setValue(999999)
        self.outputStopFrame.setDecimals(0)
        self.outputStopFrame.editingFinished.connect(self.updateTrackingStopTime)
        self.outputStopLayout.addWidget(self.outputStopFrame)
        self.outputStopTimeTitle = QLabel("or at Time:")
        self.outputStopTimeTitle.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.outputStopLayout.addWidget(self.outputStopTimeTitle)
        self.outputStopTime = QTimeEdit()
        self.outputStopTime.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.outputStopTime.setDisplayFormat('hh:mm:ss')
        self.outputStopTime.setTimeRange(QTime(00, 00, 00), QTime(00, 00, 1))
        self.outputStopTime.setTime(QTime(00, 00, 00))
        self.outputStopTime.editingFinished.connect(self.updateTrackingStopFrame)
        self.outputStopLayout.addWidget(self.outputStopTime)
    
    def makeOutputExports(self):
        self.outputExportsFrame = QFrame()
        self.outputExportsFrame.hide()
        self.outputExportsLayout = QVBoxLayout()
        self.outputExportsLayout.setAlignment(Qt.AlignTop)
        self.outputExportsFrame.setLayout(self.outputExportsLayout)
        self.mainLayout.addWidget(self.outputExportsFrame)

        self.outputExportDataLayout = QHBoxLayout()
        self.outputExportsLayout.addLayout(self.outputExportDataLayout)
        self.outputExportData = QCheckBox("Export Classifying Data")
        self.outputExportData.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.outputExportData.stateChanged.connect(self.exportDataStatusChanged)
        self.outputExportDataLayout.addWidget(self.outputExportData)
        self.outputExportDataFile = QPushButton("Select Data File")
        self.outputExportDataFile.setToolTip("No file selected")
        self.outputExportDataFile.setIcon(QIcon(os.path.join(os.path.dirname(__file__), 'images/icons/export.png')))
        self.outputExportDataFile.setEnabled(False)
        self.outputExportDataFile.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.outputExportDataFile.clicked.connect(self.selectOutputDataFile)
        self.outputExportDataLayout.addWidget(self.outputExportDataFile)

        self.outputExportTrackedVideoLayout = QHBoxLayout()
        self.outputExportsLayout.addLayout(self.outputExportTrackedVideoLayout)
        self.outputExportTrackedVideo = QCheckBox("Export Tracked Video")
        self.outputExportTrackedVideo.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.outputExportTrackedVideo.stateChanged.connect(self.exportTrackedVideoStatusChanged)
        self.outputExportTrackedVideoLayout.addWidget(self.outputExportTrackedVideo)
        self.outputExportTrackedVideoFile = QPushButton("Select Video File")
        self.outputExportTrackedVideoFile.setToolTip("No file selected")
        self.outputExportTrackedVideoFile.setIcon(QIcon(os.path.join(os.path.dirname(__file__), 'images/icons/export.png')))
        self.outputExportTrackedVideoFile.setEnabled(False)
        self.outputExportTrackedVideoFile.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.outputExportTrackedVideoFile.clicked.connect(self.selectOutputTrackedVideoFile)
        self.outputExportTrackedVideoLayout.addWidget(self.outputExportTrackedVideoFile)

        self.outputExportnoBGVideoLayout = QHBoxLayout()
        self.outputExportsLayout.addLayout(self.outputExportnoBGVideoLayout)
        self.outputExportnoBGVideo = QCheckBox("Export no-BG Video")
        self.outputExportnoBGVideo.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.outputExportnoBGVideo.stateChanged.connect(self.exportnoBGVideoStatusChanged)
        self.outputExportnoBGVideoLayout.addWidget(self.outputExportnoBGVideo)
        self.outputExportnoBGVideoFile = QPushButton("Select Video File")
        self.outputExportnoBGVideoFile.setToolTip("No file selected")
        self.outputExportnoBGVideoFile.setIcon(QIcon(os.path.join(os.path.dirname(__file__), 'images/icons/export.png')))
        self.outputExportnoBGVideoFile.setEnabled(False)
        self.outputExportnoBGVideoFile.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.outputExportnoBGVideoFile.clicked.connect(self.selectOutputnoBGVideoFile)
        self.outputExportnoBGVideoLayout.addWidget(self.outputExportnoBGVideoFile)

        self.outputExportTrackednoBGVideoLayout = QHBoxLayout()
        self.outputExportsLayout.addLayout(self.outputExportTrackednoBGVideoLayout)
        self.outputExportTrackednoBGVideo = QCheckBox("Export Tracked no-BG Video")
        self.outputExportTrackednoBGVideo.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.outputExportTrackednoBGVideo.stateChanged.connect(self.exportTrackednoBGVideoStatusChanged)
        self.outputExportTrackednoBGVideoLayout.addWidget(self.outputExportTrackednoBGVideo)
        self.outputExportTrackednoBGVideoFile = QPushButton("Select Video File")
        self.outputExportTrackednoBGVideoFile.setToolTip("No file selected")
        self.outputExportTrackednoBGVideoFile.setIcon(QIcon(os.path.join(os.path.dirname(__file__), 'images/icons/export.png')))
        self.outputExportTrackednoBGVideoFile.setEnabled(False)
        self.outputExportTrackednoBGVideoFile.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.outputExportTrackednoBGVideoFile.clicked.connect(self.selectOutputTrackednoBGVideoFile)
        self.outputExportTrackednoBGVideoLayout.addWidget(self.outputExportTrackednoBGVideoFile)

    # Function that triggers everytime we check/uncheck the tracking controls groupbox
    def outputControlsChecked(self):
        if self.isChecked() is True:
            self.outputStartStopFrame.show()
            self.outputExportsFrame.show()
        else:
            self.restoreDefaultParameters()  # This will already add "None" to the item list, so we don't need to add it back
            self.outputStartStopFrame.hide()
            self.outputExportsFrame.hide()
    
    # Function that triggers when we check/uncheck the export tracking data checkbox
    def exportDataStatusChanged(self):
        if self.outputExportData.isChecked() is True:
            self.outputExportDataFile.setEnabled(True)
        else:
            self.outputExportDataFile.setEnabled(False)
    
    # Function that triggers when clicking the button to select a filename for data output
    def selectOutputDataFile(self):
        self.outputDataPath = QFileDialog.getSaveFileName(self,'Select Data File', "", "Data files (*.txt)")
        if self.outputDataPath[0] != '':
            self.outputExportDataFile.setToolTip(str(self.outputDataPath[0]))
        else:
            self.outputExportDataFile.setToolTip("No file selected")
    
    # Function that triggers when we check/uncheck the export tracking video checkbox
    def exportTrackedVideoStatusChanged(self):
        if self.outputExportTrackedVideo.isChecked() is True:
            self.outputExportTrackedVideoFile.setEnabled(True)
        else:
            self.outputExportTrackedVideoFile.setEnabled(False)

    # Function that triggers when clicking the button to select a filename for tracked video output
    def selectOutputTrackedVideoFile(self):
        self.outputTrackedVideoPath = QFileDialog.getSaveFileName(self,'Select Video File', "", "Video files (*.avi)")
        if self.outputTrackedVideoPath[0] != '':
            self.outputExportTrackedVideoFile.setToolTip(str(self.outputTrackedVideoPath[0]))
        else:
            self.outputExportTrackedVideoFile.setToolTip("No file selected")
    
    # Function that triggers when we check/uncheck the export noBG video checkbox
    def exportnoBGVideoStatusChanged(self):
        if self.outputExportnoBGVideo.isChecked() is True:
            self.outputExportnoBGVideoFile.setEnabled(True)
        else:
            self.outputExportnoBGVideoFile.setEnabled(False)

    # Function that triggers when clicking the button to select a filename for noBG video output
    def selectOutputnoBGVideoFile(self):
        self.outputnoBGVideoPath = QFileDialog.getSaveFileName(self,'Select Video File', "", "Video files (*.avi)")
        if self.outputnoBGVideoPath[0] != '':
            self.outputExportnoBGVideoFile.setToolTip(str(self.outputnoBGVideoPath[0]))
        else:
            self.outputExportnoBGVideoFile.setToolTip("No file selected")
    
    # Function that triggers when we check/uncheck the export Tracked noBG tracking video checkbox
    def exportTrackednoBGVideoStatusChanged(self):
        if self.outputExportTrackednoBGVideo.isChecked() is True:
            self.outputExportTrackednoBGVideoFile.setEnabled(True)
        else:
            self.outputExportTrackednoBGVideoFile.setEnabled(False)

    # Function that triggers when clicking the button to select a filename for Tracked noBG video output
    def selectOutputTrackednoBGVideoFile(self):
        self.outputTrackednoBGVideoPath = QFileDialog.getSaveFileName(self,'Select Video File', "", "Video files (*.avi)")
        if self.outputTrackednoBGVideoPath[0] != '':
            self.outputExportTrackednoBGVideoFile.setToolTip(str(self.outputTrackednoBGVideoPath[0]))
        else:
            self.outputExportTrackednoBGVideoFile.setToolTip("No file selected")

    # Function that triggers when changing the starting frame for tracking, it translates this starting frame (int) in time (HH:MM:SS)
    def updateTrackingStartTime(self):
        selectedTime = self.outputStartFrame.value() // self.videoFPS
        selectedTimeHours = selectedTime // 3600
        selectedTimeRemainingSeconds = selectedTime % 3600
        selectedTimeMinutes = selectedTimeRemainingSeconds // 60
        selectedTimeSeconds = selectedTimeRemainingSeconds % 60
        self.outputStartTime.setTime(QTime(selectedTimeHours, selectedTimeMinutes, selectedTimeSeconds))
    
    # Function that triggers when changing the starting time for tracking, it translates this starting time (HH:MM:SS) in frame (int)
    def updateTrackingStartFrame(self):
        framenumberHours = self.outputStartTime.time().hour() * 3600 * self.videoFPS
        framenumberMinutes = self.outputStartTime.time().minute() * 60 * self.videoFPS
        framenumberSeconds = self.outputStartTime.time().second() * self.videoFPS
        framenumber = framenumberHours + framenumberMinutes + framenumberSeconds
        self.outputStartFrame.setValue(framenumber)
    
    # Same but for last tracking frame
    def updateTrackingStopTime(self):
        selectedTime = self.outputStopFrame.value() // self.videoFPS
        selectedTimeHours = selectedTime // 3600
        selectedTimeRemainingSeconds = selectedTime % 3600
        selectedTimeMinutes = selectedTimeRemainingSeconds // 60
        selectedTimeSeconds = selectedTimeRemainingSeconds % 60
        self.outputStopTime.setTime(QTime(selectedTimeHours, selectedTimeMinutes, selectedTimeSeconds))
    
    # Same but for last tracking time
    def updateTrackingStopFrame(self):
        framenumberHours = self.outputStopTime.time().hour() * 3600 * self.videoFPS
        framenumberMinutes = self.outputStopTime.time().minute() * 60 * self.videoFPS
        framenumberSeconds = self.outputStopTime.time().second() * self.videoFPS
        framenumber = framenumberHours + framenumberMinutes + framenumberSeconds
        self.outputStopFrame.setValue(framenumber)

    # Function that triggers when loading a new video
    def newVideoLoaded(self):
        self.restoreDefaultParameters()
        self.outputStartStopFrame.hide()
        self.outputExportsFrame.hide()
        self.setChecked(False)
    
    # Function restoring the tracking parameters to their default values
    def restoreDefaultParameters(self):
        self.outputExportData.setChecked(False)
        self.outputExportDataFile.setText("Select Data File")
        self.outputExportTrackedVideo.setChecked(False)
        self.outputExportTrackedVideoFile.setText("Select Video File")
        self.outputExportnoBGVideo.setChecked(False)
        self.outputExportnoBGVideoFile.setText("Select Video File")
        self.outputExportTrackednoBGVideo.setChecked(False)
        self.outputExportTrackednoBGVideoFile.setText("Select Video File")

    # Function that triggers after a video is loaded, providing an updated max number of frames on which to perform tracking
    def updateVideoTotalFrames(self, videoTotalFrames):
        self.videoTotalFrames = videoTotalFrames
        self.outputStartFrame.setRange(1, self.videoTotalFrames)
        self.outputStartFrame.setValue(1)
        self.outputStopFrame.setRange(1, self.videoTotalFrames)
        self.outputStopFrame.setValue(self.videoTotalFrames)
    
    # Function that triggers after a video is loaded, providing an updated max time on which to perform tracking
    def updateVideoDuration(self, videoDuration):
        self.videoDuration = videoDuration
        videoTotalHours = self.videoDuration // 3600
        videoTotalRemainingSeconds = self.videoDuration % 3600
        videoTotalMinutes = videoTotalRemainingSeconds // 60
        videoTotalSeconds = videoTotalRemainingSeconds % 60
        self.outputStartTime.setTimeRange(QTime(00, 00, 00), QTime(videoTotalHours, videoTotalMinutes, videoTotalSeconds))
        self.outputStartTime.setTime(QTime(00, 00, 00))
        self.outputStopTime.setTimeRange(QTime(00, 00, 00), QTime(videoTotalHours, videoTotalMinutes, videoTotalSeconds))
        self.outputStopTime.setTime(QTime(videoTotalHours, videoTotalMinutes, videoTotalSeconds))
    
    # Function that triggers after a video is loaded, given info about the video FPS, which is necessary to make the frame/time translation calculation
    def updateVideoFPS(self, videoFPS):
        self.videoFPS = videoFPS
 