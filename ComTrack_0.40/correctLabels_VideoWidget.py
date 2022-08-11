from ctypes import alignment
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import cv2
import pandas as pd

from correctLabels_VideoWidget_VideoControls import CorrectLabels_VideoControlsWidget
from correctLabels_VideoWidget_VideoDisplay import CorrectLabels_VideoDisplayWidget
from correctLabels_VideoWidget_VizControls import CorrectLabels_VizControlsWidget
from correctLabels_VideoWidget_VideoThread import CorrectLabels_VideoThread
from aesthetics import QHLine, QVLine

class CorrectLabels_VideoWidget(QWidget):
    videoPlayStatus = pyqtSignal(bool)

    signalVideoTotalFrames = pyqtSignal(int)
    signalVideoFPS = pyqtSignal(float)
    signalVideoDuration = pyqtSignal(int)

    fullScreenSignal = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.minimizedSize = False
        self.maximizedSize = False
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.initWidget()
        self.makeVideoControls()
        self.makeVideoDisplay()
        self.makeVideoViz()
    
    def initWidget(self):
        self.dataframe = []
        self.videoWidgetLayout = QGridLayout(self)
        self.videoWidgetLayout.setContentsMargins(5, 5, 5, 5)
        self.videoWidgetLayout.setAlignment(Qt.AlignCenter)
        self.videoWidgetLayout.setRowStretch(0, 0)
        self.videoWidgetLayout.setRowStretch(1, 1)
        self.videoWidgetLayout.setRowStretch(2, 0)
    # Creating the Video Controls (slider and play/pause/stop buttons) Widget
    def makeVideoControls(self):
        self.videoControlsWidget = CorrectLabels_VideoControlsWidget()
        self.videoControlsWidget.setEnabled(False)
        self.videoControlsWidget.previousFrameClicked.connect(self.videoPreviousFrame)
        self.videoControlsWidget.nextFrameClicked.connect(self.videoNextFrame)
        self.videoControlsWidget.videoPlayClicked.connect(self.videoPlayVideo)
        self.videoControlsWidget.videoStopClicked.connect(self.videoStopVideo)
        self.videoControlsWidget.videoResetClicked.connect(self.videoResetVideo)
        self.videoControlsWidget.videoSliderValue.connect(self.videoSliderValueChanged)
        self.videoControlsWidget.videoSliderReleased.connect(self.videoReleaseSlider)
        self.videoControlsWidget.fullScreenSignal.connect(self.updateFullScreen)
        self.videoControlsWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.videoWidgetLayout.addWidget(self.videoControlsWidget, 0, 0, 1, 1)

    # Creating the Video Image Panel Widget
    def makeVideoDisplay(self):
        self.videoDisplayWidget = CorrectLabels_VideoDisplayWidget()
        self.videoDisplayWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.videoWidgetLayout.addWidget(self.videoDisplayWidget, 1, 0, 1, 1)

    # Creating the Centroid/BBox/ID Visualisations Widget
    def makeVideoViz(self):
        self.vizControlsWidget = CorrectLabels_VizControlsWidget()
        self.vizControlsWidget.setEnabled(False)
        self.vizControlsWidget.visualizationParams.connect(self.updateVizParams)
        self.vizControlsWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.videoWidgetLayout.addWidget(self.vizControlsWidget, 2, 0, 1, 1)
    
    def loadData(self, dataframe):
        if isinstance(dataframe, pd.DataFrame):
            self.dataframe = dataframe
        else:
            self.dataframe = []


    # BELOW are functions that are triggered by the different buttons (in this widget and from other widgets using signal connexions)

    # Function that runs when pressing the Load Video Button to load the video and display its first frame
    def loadVideo(self, videoPath):
        self.videoPath = videoPath
        
        self.playingStatus = False
        self.videoPlayStatus.emit(self.playingStatus)

        self.vizControlsWidget.resetVizParams(True)

        if self.videoPath[0] == '':
            self.videoControlsWidget.setEnabled(False)
            self.videoDisplayWidget.videoDisplayImageLabel.setPixmap(QPixmap())
            self.videoDisplayWidget.videoDisplayImageLabel.setText("No video loaded")
            self.vizControlsWidget.setEnabled(False)
        elif self.videoPath[0] != '':
            self.videoControlsWidget.setEnabled(True)
            self.vizControlsWidget.setEnabled(True)
            self.videoCapture = cv2.VideoCapture(self.videoPath[0])
            self.videoTotalFrames = int(self.videoCapture.get(cv2.CAP_PROP_FRAME_COUNT))
            self.signalVideoTotalFrames.emit(self.videoTotalFrames)
            self.videoFPS = self.videoCapture.get(cv2.CAP_PROP_FPS)
            self.signalVideoFPS.emit(self.videoFPS)
            self.videoDuration = self.videoTotalFrames // self.videoFPS
            self.signalVideoDuration.emit(self.videoDuration)
            self.videoCapture.release()

            self.frameNumber = 1
            self.videoControlsWidget.videoControlsFrameSlider.setValue(self.frameNumber)
            self.videoControlsWidget.videoControlsFrameSlider.setRange(self.frameNumber, self.videoTotalFrames)
            
            self.videoFrame = CorrectLabels_VideoThread(self.videoPath, self.videoDisplayWidget.width(), self.videoDisplayWidget.height(), self.dataframe)
            self.videoRunThread(self.frameNumber, self.playingStatus)
            self.updateVideoFPS(self.videoFPS)
            self.vizControlsWidget.setEnabled(True)
            self.videoFrame.frameDims.connect(self.videoUpdateVideoLabelDims)
            self.videoFrame.frameImageUpdate.connect(self.videoFrameImageUpdate)
            self.videoFrame.frameNumberUpdate.connect(self.videoFrameNumberUpdate)
            self.videoFrame.scaleRatio.connect(self.videoUpdateScaleRatio)
            self.videoFrame.videoEnded.connect(self.videoEnded)


    # Function that runs after pressing the Load, Play, Reset and Slider buttons to update the Video thread.
    def videoRunThread(self, framenumber, playingStatus):
        self.videoFrame.updateFrameNumber(framenumber)
        self.videoFrame.updatePlayingStatus(playingStatus)
        self.videoFrame.activateThread()
        self.videoFrame.start()


    # Function that updates the Image Label size to match with the loaded video size
    def videoUpdateVideoLabelDims(self, dims):
        width = dims[0]
        height = dims[1]
        self.videoDisplayWidget.videoDisplayImageLabel.setFixedSize(int(width), int(height))
        self.videoControlsWidget.videoControlsFrameSlider.setFixedWidth(int(self.width()*0.95))
    

    # Function that updates the displayed video frame in the Image Label
    def videoFrameImageUpdate(self, image):
        self.videoDisplayWidget.videoDisplayImageLabel.setPixmap(QPixmap.fromImage(image))

    # Function that updates the displayed video frame number
    def videoFrameNumberUpdate(self, value):
        self.videoControlsWidget.videoControlsFrameSlider.setValue(value)
        self.videoControlsWidget.videoControlsFrameNumberLabel.setText(str(value))


    # Function that runs after the video is loaded, to store the ratio between the real video size and the displayed video size, to later match the drawed BB onto the real video
    def videoUpdateScaleRatio(self, scaleRatio):
        self.videoScaleRatio = scaleRatio


    # Function that runs when pressing the Play Button to run the video Thread and play the video
    def videoPlayVideo(self, signal):
        if signal is True:
            self.playingStatus = True
            self.videoPlayStatus.emit(self.playingStatus)
            self.videoControlsWidget.videoControlsPreviousFrame.setEnabled(False)
            self.videoControlsWidget.videoControlsPlayButton.setEnabled(False)
            self.videoControlsWidget.videoControlsResetButton.setEnabled(False)
            self.videoControlsWidget.videoControlsNextFrame.setEnabled(False)
            self.videoControlsWidget.videoControlsFrameSlider.setEnabled(False)
            self.videoControlsWidget.videoControlsStopButton.setEnabled(True)
            self.vizControlsWidget.setEnabled(False)
            self.videoRunThread(self.videoControlsWidget.videoControlsFrameSlider.value(), self.playingStatus)
    

    # Function that runs when pressing the Stop Button to stop the video Thread
    def videoStopVideo(self, signal):
        if signal is True:
            self.playingStatus = False
            self.videoPlayStatus.emit(self.playingStatus)
            self.videoControlsWidget.videoControlsPlayButton.setEnabled(True)
            self.videoControlsWidget.videoControlsResetButton.setEnabled(True)
            self.videoControlsWidget.videoControlsFrameSlider.setEnabled(True)
            self.videoControlsWidget.videoControlsStopButton.setEnabled(False)
            self.vizControlsWidget.setEnabled(True)
            self.videoFrame.stopThread()

            if self.frameNumber > 1:
                self.videoControlsWidget.videoControlsPreviousFrame.setEnabled(True)
            if self.frameNumber < self.videoTotalFrames:
                self.videoControlsWidget.videoControlsNextFrame.setEnabled(True)


    # Function that runs when pressing the Reset Button to reset the video to its first frame
    def videoResetVideo(self, signal):
        if signal is True:
            self.frameNumber = 1
            self.videoControlsWidget.videoControlsFrameSlider.setValue(self.frameNumber)
            self.videoControlsWidget.videoControlsPlayButton.setEnabled(True)
            self.videoControlsWidget.videoControlsResetButton.setEnabled(False)
            self.videoRunThread(self.frameNumber, self.playingStatus)


    # Function that runs when pressing the "<" button to go to previous frame
    def videoPreviousFrame(self, signal):
        if signal is True:
            self.videoRunThread(self.videoControlsWidget.videoControlsFrameSlider.value() - 1, self.playingStatus)


    # Function that runs when pressing the ">" button to go to next frame
    def videoNextFrame(self, signal):
        if signal is True:
            self.videoRunThread(self.videoControlsWidget.videoControlsFrameSlider.value() + 1, self.playingStatus)


    # Function that runs when the video frame/time slider is released
    def videoReleaseSlider(self, signal):
        if signal is True:
            if self.videoControlsWidget.videoControlsFrameSlider.value() > 1:
                self.videoControlsWidget.videoControlsResetButton.setEnabled(True)
            else:
                self.videoControlsWidget.videoControlsResetButton.setEnabled(False)
            
            if self.videoControlsWidget.videoControlsFrameSlider.value() < self.videoTotalFrames:
                self.videoControlsWidget.videoControlsPlayButton.setEnabled(True)
            else:
                self.videoControlsWidget.videoControlsPlayButton.setEnabled(False)

            self.videoRunThread(self.videoControlsWidget.videoControlsFrameSlider.value(), self.playingStatus)


    # Function that updates the displayed frame number and stop the video Thread when reaching the last frame of the video
    def videoSliderValueChanged(self, framenumber):
        self.frameNumber = framenumber
        self.videoControlsWidget.videoControlsFrameNumberLabel.setText(str(self.frameNumber))
        if self.frameNumber == self.videoTotalFrames:
            self.playingStatus = False
            self.videoPlayStatus.emit(self.playingStatus)
            self.videoFrame.stopThread()
            self.videoControlsWidget.videoControlsPlayButton.setEnabled(False)
            self.videoControlsWidget.videoControlsStopButton.setEnabled(False)
            self.videoControlsWidget.videoControlsResetButton.setEnabled(True)
            self.videoControlsWidget.videoControlsFrameSlider.setEnabled(True)

        if self.playingStatus is False:
            if self.frameNumber > 1:
                self.videoControlsWidget.videoControlsPreviousFrame.setEnabled(True)
            else:
                self.videoControlsWidget.videoControlsPreviousFrame.setEnabled(False)
            
            if self.frameNumber < self.videoTotalFrames:
                self.videoControlsWidget.videoControlsNextFrame.setEnabled(True)
            else:
                self.videoControlsWidget.videoControlsNextFrame.setEnabled(False)

        self.videoTimeUpdate(self.frameNumber)


    # Function that updates the displayed video time based on video frame
    def videoTimeUpdate(self, framenumber):
        videoTime = framenumber // self.videoFPS
        videoTimeHours = int(videoTime / 3600)
        videoRemainingMinutes = int(videoTime % 3600)
        videoTimeMinutes = int(videoRemainingMinutes / 60)
        videoTimeSeconds = int(videoRemainingMinutes % 60)
        self.videoTime = str(videoTimeHours).zfill(2) + ":" + str(videoTimeMinutes).zfill(2) + ":" + str(videoTimeSeconds).zfill(2)
        self.videoControlsWidget.videoControlsTimeLabel.setText(self.videoTime)


    # Function that run when the video naturally ends (last frame reached)
    def videoEnded(self, signal):
        if signal is True:
            self.playingStatus = False
            self.videoPlayStatus.emit(self.playingStatus)
            self.videoControlsWidget.videoControlsPlayButton.setEnabled(True)
            self.videoControlsWidget.videoControlsResetButton.setEnabled(True)
            self.videoControlsWidget.videoControlsFrameSlider.setEnabled(True)
            self.videoControlsWidget.videoControlsStopButton.setEnabled(False)
            self.vizControlsWidget.setEnabled(True)
            if self.frameNumber > 1:
                self.videoControlsWidget.videoControlsPreviousFrame.setEnabled(True)


    # Functions that update the videoThread with the fps and viz parameters before processing the video
    def updateVideoFPS(self, fps):
        self.videoFrame.updateVideoFPS(fps)
    

    def updateVizParams(self, params):
        self.videoFrame.updateVizParams(params)


    # Function that triggers when exporting the tracked video
    def exportVideo(self, videoPath):
        self.videoResetVideo(True)
        self.videoFrame.updateExportVideo(videoPath)
        if videoPath[0] != '':
            self.videoPlayVideo(True)


    # Function to switch between maximized and minimized viewing of the video
    def updateFullScreen(self, signal):
        if signal == 0:
            self.vizControlsWidget.show()
            self.videoWidgetLayout.addWidget(self.videoDisplayWidget, 1, 0, 1, 1)
            self.fullScreenSignal.emit(0)
        elif signal == 1:
            self.vizControlsWidget.hide()
            self.videoWidgetLayout.addWidget(self.videoDisplayWidget, 1, 0, 2, 1)
            self.fullScreenSignal.emit(1)

        self.videoDisplayWidget.hide()
        self.videoDisplayWidget.show()
        try:
            self.videoFrame
        except:
            pass
        else:
            self.videoFrame.updateVideoResize(self.videoDisplayWidget.width(), self.videoDisplayWidget.height())
