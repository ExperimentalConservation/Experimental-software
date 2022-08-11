from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from mainWidget_Home import MainWidgetHome
from mainWidget_CorrectLabels import MainWidgetCorrectLabels
from mainWidget_VideoTrack import MainWidgetVideoTrack
from mainWidget_DatasetBuilder import MainWidgetDatasetBuilder
from mainWidget_DLModelBuilder import MainWidgetDLModelBuilder
from mainWidget_TrackNClass import MainWidgetTrackNClass

class CentralWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.initCentralWidget()
    
    def initCentralWidget(self):
        self.mainLayout = QGridLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        self.allMainWidgets = QStackedWidget(self)

        self.mainWidget_Home = MainWidgetHome()
        self.mainWidget_Home.videoTrack.connect(self.videoTrackClicked)
        self.mainWidget_Home.correctLabels.connect(self.correctLabelsClicked)
        self.mainWidget_Home.datasetBuilder.connect(self.datasetBuilderClicked)
        self.mainWidget_Home.modelBuilder.connect(self.modelBuilderClicked)
        self.mainWidget_Home.trackNClass.connect(self.trackNClassClicked)
        self.allMainWidgets.addWidget(self.mainWidget_Home)

        self.mainWidget_VideoTrack = MainWidgetVideoTrack()
        self.allMainWidgets.addWidget(self.mainWidget_VideoTrack)

        self.mainWidget_VideoPrepare = MainWidgetCorrectLabels()
        self.allMainWidgets.addWidget(self.mainWidget_VideoPrepare)

        self.mainWidget_DatasetBuilder = MainWidgetDatasetBuilder()
        self.allMainWidgets.addWidget(self.mainWidget_DatasetBuilder)

        self.mainWidget_DLModelBuilder = MainWidgetDLModelBuilder()
        self.allMainWidgets.addWidget(self.mainWidget_DLModelBuilder)

        self.mainWidget_TrackNClass = MainWidgetTrackNClass()
        self.allMainWidgets.addWidget(self.mainWidget_TrackNClass)

        self.allMainWidgets.setCurrentIndex(0)
        self.mainLayout.addWidget(self.allMainWidgets)
    
    def setIndex(self, index):
        if index == "Home":
            self.allMainWidgets.setCurrentIndex(0)
        elif index == "Generate Tracked Objects":
            self.allMainWidgets.setCurrentIndex(1)
        elif index == "Correct Labels":
            self.allMainWidgets.setCurrentIndex(2)
        elif index == "Generate Datasets":
            self.allMainWidgets.setCurrentIndex(3)
        elif index == "Build Model":
            self.allMainWidgets.setCurrentIndex(4)
        elif index == "Track And Class":
            self.allMainWidgets.setCurrentIndex(5)
    
    def videoTrackClicked(self):
        self.allMainWidgets.setCurrentIndex(1)
    
    def correctLabelsClicked(self):
        self.allMainWidgets.setCurrentIndex(2)
    
    def datasetBuilderClicked(self):
        self.allMainWidgets.setCurrentIndex(3)
    
    def modelBuilderClicked(self):
        self.allMainWidgets.setCurrentIndex(4)
    
    def trackNClassClicked(self):
        self.allMainWidgets.setCurrentIndex(5)
