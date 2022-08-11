from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from home_VideoTrackWidget import Home_VideoTrackWidget
from home_CorrectLabelsWidget import Home_CorrectLabelsWidget
from home_DatasetBuilderWidget import Home_DatasetBuilderWidget
from home_ModelBuilderWidget import Home_ModelBuilderWidget
from home_TrackNClassWidget import Home_TrackNClassWidget

class MainWidgetHome(QWidget):

    videoTrack = pyqtSignal()
    correctLabels = pyqtSignal()
    datasetBuilder = pyqtSignal()
    modelBuilder = pyqtSignal()
    trackNClass = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initWidget()
        self.makeTrainingWidgetsSelectors()
        self.makeTrackNClassSelector()
    
    def initWidget(self):
        self.mainlayout = QGridLayout(self)

    def makeTrainingWidgetsSelectors(self):
        # VideoTrack
        self.videoTrackSelector = Home_VideoTrackWidget()
        clickable(self.videoTrackSelector).connect(self.videoTrackClicked)
        self.mainlayout.addWidget(self.videoTrackSelector, 0, 0, 1, 1)

        # Correct Labels
        self.correctLabelsSelector = Home_CorrectLabelsWidget()
        clickable(self.correctLabelsSelector).connect(self.correctLabelsClicked)
        self.mainlayout.addWidget(self.correctLabelsSelector, 0, 1, 1, 1)

        # Dataset Builder
        self.datasetBuilderSelector = Home_DatasetBuilderWidget()
        clickable(self.datasetBuilderSelector).connect(self.datasetBuilderClicked)
        self.mainlayout.addWidget(self.datasetBuilderSelector, 0, 2, 1, 1)

        # DL Model Builder
        self.modelBuilderSelector = Home_ModelBuilderWidget()
        clickable(self.modelBuilderSelector).connect(self.modelBuilderClicked)
        self.mainlayout.addWidget(self.modelBuilderSelector, 0, 3, 1, 1)

    def makeTrackNClassSelector(self):
        # TRackNClass
        self.trackNClassSelector = Home_TrackNClassWidget()
        clickable(self.trackNClassSelector).connect(self.trackNClassClicked)
        self.mainlayout.addWidget(self.trackNClassSelector, 1, 0, 1, 4)

    def videoTrackClicked(self):
        self.videoTrack.emit()
    
    def correctLabelsClicked(self):
        self.correctLabels.emit()

    def datasetBuilderClicked(self):
        self.datasetBuilder.emit()

    def modelBuilderClicked(self):
        self.modelBuilder.emit()
    
    def trackNClassClicked(self):
        self.trackNClass.emit()


def clickable(widget):
    class Filter(QObject):
        clicked = pyqtSignal()
        def eventFilter(self, obj, event):
            if obj == widget:
                if event.type() == QEvent.MouseButtonRelease:
                    if obj.rect().contains(event.pos()):
                        self.clicked.emit()
                        # The developer can opt for .emit(obj) to get the object within the slot.
                        return True
            return False
    filter = Filter(widget)
    widget.installEventFilter(filter)
    return filter.clicked