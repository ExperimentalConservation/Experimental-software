from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class TrackNClass_ImageSmoothingControlsWidget(QGroupBox):

    def __init__(self):
        super().__init__()
        self.availableCounters = [1, 2, 3, 4]
        self.smoothingItemWidgets = []
        self.initWidget()
        self.makeAddSmoothingButton()
        self.makeSmoothingItemsLayout()
    
    def initWidget(self):
        self.setTitle("Smoothing Controls")
        self.setCheckable(True)
        self.setChecked(False)
        self.setStyleSheet("""
                QGroupBox{font-weight: bold; border: 1px solid black; border-radius: 5px; margin-top: 0.6em;}
                QGroupBox::title{top: -0.5em; subcontrol-position: top center;}
                """)
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setAlignment(Qt.AlignTop)
    
    def makeAddSmoothingButton(self):
        self.addSmoothingButton = QPushButton("Add a smoothing function")
        self.addSmoothingButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.addSmoothingButton.clicked.connect(self.addSmoothing)
        self.mainLayout.addWidget(self.addSmoothingButton, alignment = Qt.AlignTop)
    
    def makeSmoothingItemsLayout(self):
        self.smoothingItemsLayout = QVBoxLayout()
        self.smoothingItemsLayout.setAlignment(Qt.AlignTop)
        self.mainLayout.addLayout(self.smoothingItemsLayout)
    
    def addSmoothing(self):
        if len(self.availableCounters) > 0:
            smoothingID = self.availableCounters[0]
            self.availableCounters.remove(smoothingID)

            self.smoothingItemWidget = SmoothingItem(self, smoothingID)
            self.smoothingItemWidgets.append([smoothingID, self.smoothingItemWidget])
            self.smoothingItemWidgets = sorted(self.smoothingItemWidgets, key = lambda x: x[0])
            self.smoothingItemsLayout.insertWidget(smoothingID, self.smoothingItemWidget, alignment=Qt.AlignTop)

            self.smoothingItemWidget.smoothingRemoved.connect(self.removeSmoothing)
    
    def removeSmoothing(self, ID):
        self.availableCounters.append(ID)
        self.availableCounters = sorted(self.availableCounters)
        self.smoothingItemWidgets = [item for item in self.smoothingItemWidgets if item[0] != ID]
        self.smoothingItemWidgets = sorted(self.smoothingItemWidgets, key = lambda x: x[0])
    
    def newVideoLoaded(self):
        self.setChecked(False)
        self.smoothingItemWidgets = []
        if len(self.availableCounters) < 4:
            self.availableCounters = [1, 2, 3, 4]
            items = self.findChildren(QFrame)
            for i in items:
                if i.objectName in self.availableCounters:
                    i.deleteLater()


    def loadSmoothingParamsFromSavedControls(self, smoothingSoup):
        self.setChecked(True)
        self.smoothingID = self.availableCounters[0]
        self.availableCounters.remove(self.smoothingID)

        self.smoothingItemWidget = SmoothingItem(self, self.smoothingID)
        if (smoothingSoup.find("smoothingname").string == "Averaging"):
            self.smoothingItemWidget.smoothingItem.setCurrentIndex(1)
            if (str(smoothingSoup.find("averageblurbordertype").string) == "BORDER_DEFAULT"):
                self.smoothingItemWidget.smoothingAverageBlurBorderTypeEntry.setCurrentIndex(0)
            elif (str(smoothingSoup.find("averageblurbordertype").string) == "BORDER_CONSTANT"):
                self.smoothingItemWidget.smoothingAverageBlurBorderTypeEntry.setCurrentIndex(1)
            elif (str(smoothingSoup.find("averageblurbordertype").string) == "BORDER_REPLICATE"):
                self.smoothingItemWidget.smoothingAverageBlurBorderTypeEntry.setCurrentIndex(2)
            elif (str(smoothingSoup.find("averageblurbordertype").string) == "BORDER_REFLECT"):
                self.smoothingItemWidget.smoothingAverageBlurBorderTypeEntry.setCurrentIndex(3)
            elif (str(smoothingSoup.find("averageblurbordertype").string) == "BORDER_TRANSPARENT"):
                self.smoothingItemWidget.smoothingAverageBlurBorderTypeEntry.setCurrentIndex(4)
            elif (str(smoothingSoup.find("averageblurbordertype").string) == "BORDER_ISOLATED"):
                self.smoothingItemWidget.smoothingAverageBlurBorderTypeEntry.setCurrentIndex(5)
        elif (smoothingSoup.find("smoothingname").string == "Median Blurring"):
            self.smoothingItemWidget.smoothingItem.setCurrentIndex(2)
            self.smoothingItemWidget.smoothingMedianBlurKernelEntry.setValue(int(smoothingSoup.find("medianblurkernel").string))
        elif (smoothingSoup.find("smoothingname").string == "Gaussian Blurring"):
            self.smoothingItemWidget.smoothingItem.setCurrentIndex(3)
            self.smoothingItemWidget.smoothingGaussianBlurKernelEntry.setValue(int(smoothingSoup.find("gaussianblurkernel").string))
            self.smoothingItemWidget.smoothingGaussianBlurSigmaXEntry.setValue(float(smoothingSoup.find("gaussianblursigmax").string))
            self.smoothingItemWidget.smoothingGaussianBlurSigmaYEntry.setValue(float(smoothingSoup.find("gaussianblursigmay").string))
            if (str(smoothingSoup.find("gaussianblurbordertype").string) == "BORDER_DEFAULT"):
                self.smoothingItemWidget.smoothingGaussianBlurBorderTypeEntry.setCurrentIndex(0)
            elif (str(smoothingSoup.find("gaussianblurbordertype").string) == "BORDER_CONSTANT"):
                self.smoothingItemWidget.smoothingGaussianBlurBorderTypeEntry.setCurrentIndex(1)
            elif (str(smoothingSoup.find("gaussianblurbordertype").string) == "BORDER_REPLICATE"):
                self.smoothingItemWidget.smoothingGaussianBlurBorderTypeEntry.setCurrentIndex(2)
            elif (str(smoothingSoup.find("gaussianblurbordertype").string) == "BORDER_REFLECT"):
                self.smoothingItemWidget.smoothingGaussianBlurBorderTypeEntry.setCurrentIndex(3)
            elif (str(smoothingSoup.find("gaussianblurbordertype").string) == "BORDER_TRANSPARENT"):
                self.smoothingItemWidget.smoothingGaussianBlurBorderTypeEntry.setCurrentIndex(4)
            elif (str(smoothingSoup.find("gaussianblurbordertype").string) == "BORDER_ISOLATED"):
                self.smoothingItemWidget.smoothingGaussianBlurBorderTypeEntry.setCurrentIndex(5)
        elif (smoothingSoup.find("smoothingname").string == "Bilateral Filtering"):
            self.smoothingItemWidget.smoothingItem.setCurrentIndex(4)
            self.smoothingItemWidget.smoothingBilateralFilterFilterSizeEntry.setValue(int(smoothingSoup.find("bilateralfiltersize").string))
            self.smoothingItemWidget.smoothingBilateralFilterSigmaColorEntry.setValue(int(smoothingSoup.find("bilateralfiltersigmacolor").string))
            self.smoothingItemWidget.smoothingBilateralFilterSigmaSpaceEntry.setValue(int(smoothingSoup.find("bilateralfiltersigmaspace").string))
            if (str(smoothingSoup.find("bilateralfilterbordertype").string) == "BORDER_DEFAULT"):
                self.smoothingItemWidget.smoothingBilateralFilterBorderTypeEntry.setCurrentIndex(0)
            elif (str(smoothingSoup.find("bilateralfilterbordertype").string) == "BORDER_CONSTANT"):
                self.smoothingItemWidget.smoothingBilateralFilterBorderTypeEntry.setCurrentIndex(1)
            if (str(smoothingSoup.find("bilateralfilterbordertype").string) == "BORDER_REPLICATE"):
                self.smoothingItemWidget.smoothingBilateralFilterBorderTypeEntry.setCurrentIndex(2)
            if (str(smoothingSoup.find("bilateralfilterbordertype").string) == "BORDER_REFLECT"):
                self.smoothingItemWidget.smoothingBilateralFilterBorderTypeEntry.setCurrentIndex(3)
            if (str(smoothingSoup.find("bilateralfilterbordertype").string) == "BORDER_TRANSPARENT"):
                self.smoothingItemWidget.smoothingBilateralFilterBorderTypeEntry.setCurrentIndex(4)
            if (str(smoothingSoup.find("bilateralfilterbordertype").string) == "BORDER_ISOLATED"):
                self.smoothingItemWidget.smoothingBilateralFilterBorderTypeEntry.setCurrentIndex(5)
        self.smoothingItemWidget.smoothingRemoved.connect(self.removeSmoothing)
        self.smoothingItemWidgets.append([self.smoothingID, self.smoothingItemWidget])
        self.smoothingItemWidgets = sorted(self.smoothingItemWidgets, key = lambda x: x[0])
        self.smoothingItemsLayout.insertWidget(self.smoothingID, self.smoothingItemWidget, alignment=Qt.AlignTop)
            

class SmoothingItem(QFrame):
    smoothingRemoved = pyqtSignal(int)
    def __init__(self, parent, ID):
        super(SmoothingItem, self).__init__(parent)
        self.ID = ID
        self.objectName = self.ID
        self.setFrameStyle(QFrame.StyledPanel)
        self.setStyleSheet("""
                QFrame{border-left: 1px solid black;}
                """)
        self.initWidget()
        self.makeSmoothingSelector()
        self.makeSmoothingAveraging()
        self.makeSmoothingMedianBlurring()
        self.makeSmoothingGaussianBlurring()
        self.makeSmoothingBilateralFiltering()
    
    def initWidget(self):
        self.smoothingItemLayout = QVBoxLayout(self)
        self.smoothingItemLayout.setAlignment(Qt.AlignTop)
    
    def makeSmoothingSelector(self):
        self.smoothingSelectorLayout = QHBoxLayout()
        self.smoothingItemLayout.addLayout(self.smoothingSelectorLayout)

        self.smoothingItemTitle = QLabel("Smoothing {0}".format(self.ID))
        self.smoothingItemTitle.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.smoothingItemTitle.setStyleSheet("text-decoration: underline;")
        self.smoothingSelectorLayout.addWidget(self.smoothingItemTitle)

        self.smoothingItem = QComboBox()
        self.smoothingItem.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.smoothingItem.addItems(["None", "Averaging", "Median Blurring", "Gaussian Blurring", "Bilateral Filtering"])
        self.smoothingItem.setCurrentIndex(0)
        self.smoothingItem.currentIndexChanged.connect(self.smoothingItemChanged)
        self.smoothingSelectorLayout.addWidget(self.smoothingItem)

        self.removeSmoothingItem = QPushButton("X")
        self.removeSmoothingItem.setStyleSheet("""
                QPushButton{color: red;}
                """)
        self.removeSmoothingItem.setFixedWidth(50)
        self.removeSmoothingItem.clicked.connect(self.deleteSmoothing)
        self.smoothingSelectorLayout.addWidget(self.removeSmoothingItem)

        self.smoothingNone = QLabel()
        self.smoothingNone.setText("No smoothing selected")
        self.smoothingNone.setAlignment(Qt.AlignCenter)
        self.smoothingItemLayout.addWidget(self.smoothingNone)
        
    def makeSmoothingAveraging(self):
        self.smoothingAverageBlurFrame = QFrame()
        self.smoothingAverageBlurFrame.hide()
        self.smoothingAverageBlurLayout = QVBoxLayout()
        self.smoothingAverageBlurFrame.setLayout(self.smoothingAverageBlurLayout)
        self.smoothingItemLayout.addWidget(self.smoothingAverageBlurFrame)

        self.smoothingAverageBlurFirstRowLayout = QHBoxLayout()
        self.smoothingAverageBlurLayout.addLayout(self.smoothingAverageBlurFirstRowLayout)
        self.smoothingAverageBlurKernelTitle = QLabel("Kernel:")
        self.smoothingAverageBlurKernelTitle.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.smoothingAverageBlurFirstRowLayout.addWidget(self.smoothingAverageBlurKernelTitle)
        self.smoothingAverageBlurKernelEntry = QDoubleSpinBox(self)
        self.smoothingAverageBlurKernelEntry.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.smoothingAverageBlurKernelEntry.setRange(1, 999999)
        self.smoothingAverageBlurKernelEntry.setSingleStep(2)
        self.smoothingAverageBlurKernelEntry.setValue(7)
        self.smoothingAverageBlurKernelEntry.setDecimals(0)
        self.smoothingAverageBlurFirstRowLayout.addWidget(self.smoothingAverageBlurKernelEntry)

        self.smoothingAverageBlurSecondRowLayout = QHBoxLayout()
        self.smoothingAverageBlurLayout.addLayout(self.smoothingAverageBlurSecondRowLayout)
        self.smoothingAverageBlurBorderTypeTitle = QLabel("Border Type:")
        self.smoothingAverageBlurBorderTypeTitle.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.smoothingAverageBlurSecondRowLayout.addWidget(self.smoothingAverageBlurBorderTypeTitle)
        self.smoothingAverageBlurBorderTypeEntry = QComboBox()
        self.smoothingAverageBlurBorderTypeEntry.addItems(["BORDER_DEFAULT", "BORDER_CONSTANT", "BORDER_REPLICATE", "BORDER_REFLECT", "BORDER_TRANSPARENT", "BORDER_ISOLATED"])
        self.smoothingAverageBlurBorderTypeEntry.setCurrentIndex(0)
        self.smoothingAverageBlurBorderTypeEntry.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.smoothingAverageBlurSecondRowLayout.addWidget(self.smoothingAverageBlurBorderTypeEntry)

    def makeSmoothingMedianBlurring(self):
        self.smoothingMedianBlurFrame = QFrame()
        self.smoothingMedianBlurFrame.hide()
        self.smoothingMedianBlurLayout = QVBoxLayout()
        self.smoothingMedianBlurFrame.setLayout(self.smoothingMedianBlurLayout)
        self.smoothingItemLayout.addWidget(self.smoothingMedianBlurFrame)

        self.smoothingMedianBlurFirstRowLayout = QHBoxLayout()
        self.smoothingMedianBlurLayout.addLayout(self.smoothingMedianBlurFirstRowLayout)
        self.smoothingMedianBlurKernelTitle = QLabel("Kernel:")
        self.smoothingMedianBlurKernelTitle.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.smoothingMedianBlurFirstRowLayout.addWidget(self.smoothingMedianBlurKernelTitle)
        self.smoothingMedianBlurKernelEntry = QDoubleSpinBox(self)
        self.smoothingMedianBlurKernelEntry.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.smoothingMedianBlurKernelEntry.setRange(1, 999999)
        self.smoothingMedianBlurKernelEntry.setSingleStep(2)
        self.smoothingMedianBlurKernelEntry.setValue(7)
        self.smoothingMedianBlurKernelEntry.setDecimals(0)
        self.smoothingMedianBlurFirstRowLayout.addWidget(self.smoothingMedianBlurKernelEntry)
    
    def makeSmoothingGaussianBlurring(self):
        self.smoothingGaussianBlurFrame = QFrame()
        self.smoothingGaussianBlurFrame.hide()
        self.smoothingGaussianBlurLayout = QVBoxLayout()
        self.smoothingGaussianBlurFrame.setLayout(self.smoothingGaussianBlurLayout)
        self.smoothingItemLayout.addWidget(self.smoothingGaussianBlurFrame)
        
        self.smoothingGaussianBlurFirstRowLayout = QHBoxLayout()
        self.smoothingGaussianBlurLayout.addLayout(self.smoothingGaussianBlurFirstRowLayout)
        self.smoothingGaussianBlurKernelTitle = QLabel("Gaussian Kernel:")
        self.smoothingGaussianBlurKernelTitle.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.smoothingGaussianBlurFirstRowLayout.addWidget(self.smoothingGaussianBlurKernelTitle)
        self.smoothingGaussianBlurKernelEntry = QDoubleSpinBox(self)
        self.smoothingGaussianBlurKernelEntry.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.smoothingGaussianBlurKernelEntry.setRange(1, 999999)
        self.smoothingGaussianBlurKernelEntry.setSingleStep(2)
        self.smoothingGaussianBlurKernelEntry.setValue(7)
        self.smoothingGaussianBlurKernelEntry.setDecimals(0)
        self.smoothingGaussianBlurFirstRowLayout.addWidget(self.smoothingGaussianBlurKernelEntry)

        self.smoothingGaussianBlurSecondRowLayout = QHBoxLayout()
        self.smoothingGaussianBlurLayout.addLayout(self.smoothingGaussianBlurSecondRowLayout)
        self.smoothingGaussianBlurSigmaXTitle = QLabel("Sigma X:")
        self.smoothingGaussianBlurSigmaXTitle.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.smoothingGaussianBlurSecondRowLayout.addWidget(self.smoothingGaussianBlurSigmaXTitle)
        self.smoothingGaussianBlurSigmaXEntry = QDoubleSpinBox(self)
        self.smoothingGaussianBlurSigmaXEntry.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.smoothingGaussianBlurSigmaXEntry.setRange(0, 999999)
        self.smoothingGaussianBlurSigmaXEntry.setSingleStep(5)
        self.smoothingGaussianBlurSigmaXEntry.setValue(0)
        self.smoothingGaussianBlurSigmaXEntry.setDecimals(3)
        self.smoothingGaussianBlurSecondRowLayout.addWidget(self.smoothingGaussianBlurSigmaXEntry)

        self.smoothingGaussianBlurThirdRowLayout = QHBoxLayout()
        self.smoothingGaussianBlurLayout.addLayout(self.smoothingGaussianBlurThirdRowLayout)
        self.smoothingGaussianBlurSigmaYTitle = QLabel("Sigma Y:")
        self.smoothingGaussianBlurSigmaYTitle.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.smoothingGaussianBlurThirdRowLayout.addWidget(self.smoothingGaussianBlurSigmaYTitle)
        self.smoothingGaussianBlurSigmaYEntry = QDoubleSpinBox(self)
        self.smoothingGaussianBlurSigmaYEntry.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.smoothingGaussianBlurSigmaYEntry.setRange(0, 999999)
        self.smoothingGaussianBlurSigmaYEntry.setSingleStep(5)
        self.smoothingGaussianBlurSigmaYEntry.setValue(0)
        self.smoothingGaussianBlurSigmaYEntry.setDecimals(3)
        self.smoothingGaussianBlurThirdRowLayout.addWidget(self.smoothingGaussianBlurSigmaYEntry)

        self.smoothingGaussianBlurFourthRowLayout = QHBoxLayout()
        self.smoothingGaussianBlurLayout.addLayout(self.smoothingGaussianBlurFourthRowLayout)
        self.smoothingGaussianBlurBorderTypeTitle = QLabel("Border Type:")
        self.smoothingGaussianBlurBorderTypeTitle.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.smoothingGaussianBlurFourthRowLayout.addWidget(self.smoothingGaussianBlurBorderTypeTitle)
        self.smoothingGaussianBlurBorderTypeEntry = QComboBox()
        self.smoothingGaussianBlurBorderTypeEntry.addItems(["BORDER_DEFAULT", "BORDER_CONSTANT", "BORDER_REPLICATE", "BORDER_REFLECT", "BORDER_TRANSPARENT", "BORDER_ISOLATED"])
        self.smoothingGaussianBlurBorderTypeEntry.setCurrentIndex(0)
        self.smoothingGaussianBlurBorderTypeEntry.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.smoothingGaussianBlurFourthRowLayout.addWidget(self.smoothingGaussianBlurBorderTypeEntry)
    
    def makeSmoothingBilateralFiltering(self):
        self.smoothingBilateralFilterFrame = QFrame()
        self.smoothingBilateralFilterFrame.hide()
        self.smoothingBilateralFilterLayout = QVBoxLayout()
        self.smoothingBilateralFilterFrame.setLayout(self.smoothingBilateralFilterLayout)
        self.smoothingItemLayout.addWidget(self.smoothingBilateralFilterFrame)

        self.smoothingBilateralFilterFirstRowLayout = QHBoxLayout()
        self.smoothingBilateralFilterLayout.addLayout(self.smoothingBilateralFilterFirstRowLayout)
        self.smoothingBilateralFilterFilterSizeTitle = QLabel("Filter Size:")
        self.smoothingBilateralFilterFilterSizeTitle.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.smoothingBilateralFilterFirstRowLayout.addWidget(self.smoothingBilateralFilterFilterSizeTitle)
        self.smoothingBilateralFilterFilterSizeEntry = QDoubleSpinBox(self)
        self.smoothingBilateralFilterFilterSizeEntry.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.smoothingBilateralFilterFilterSizeEntry.setRange(-1, 9)
        self.smoothingBilateralFilterFilterSizeEntry.setSingleStep(2)
        self.smoothingBilateralFilterFilterSizeEntry.setValue(5)
        self.smoothingBilateralFilterFilterSizeEntry.setDecimals(0)
        self.smoothingBilateralFilterFirstRowLayout.addWidget(self.smoothingBilateralFilterFilterSizeEntry)

        self.smoothingBilateralFilterSecondRowLayout = QHBoxLayout()
        self.smoothingBilateralFilterLayout.addLayout(self.smoothingBilateralFilterSecondRowLayout)
        self.smoothingBilateralFilterSigmaColorTitle = QLabel("Sigma Color:")
        self.smoothingBilateralFilterSigmaColorTitle.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.smoothingBilateralFilterSecondRowLayout.addWidget(self.smoothingBilateralFilterSigmaColorTitle)
        self.smoothingBilateralFilterSigmaColorEntry = QDoubleSpinBox(self)
        self.smoothingBilateralFilterSigmaColorEntry.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.smoothingBilateralFilterSigmaColorEntry.setRange(0, 300)
        self.smoothingBilateralFilterSigmaColorEntry.setSingleStep(5)
        self.smoothingBilateralFilterSigmaColorEntry.setValue(150)
        self.smoothingBilateralFilterSigmaColorEntry.setDecimals(0)
        self.smoothingBilateralFilterSecondRowLayout.addWidget(self.smoothingBilateralFilterSigmaColorEntry)

        self.smoothingBilateralFilterThirdRowLayout = QHBoxLayout()
        self.smoothingBilateralFilterLayout.addLayout(self.smoothingBilateralFilterThirdRowLayout)
        self.smoothingBilateralFilterSigmaSpaceTitle = QLabel("Sigma Space:")
        self.smoothingBilateralFilterSigmaSpaceTitle.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.smoothingBilateralFilterThirdRowLayout.addWidget(self.smoothingBilateralFilterSigmaSpaceTitle)
        self.smoothingBilateralFilterSigmaSpaceEntry = QDoubleSpinBox(self)
        self.smoothingBilateralFilterSigmaSpaceEntry.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.smoothingBilateralFilterSigmaSpaceEntry.setRange(0, 300)
        self.smoothingBilateralFilterSigmaSpaceEntry.setSingleStep(5)
        self.smoothingBilateralFilterSigmaSpaceEntry.setValue(150)
        self.smoothingBilateralFilterSigmaSpaceEntry.setDecimals(0)
        self.smoothingBilateralFilterThirdRowLayout.addWidget(self.smoothingBilateralFilterSigmaSpaceEntry)

        self.smoothingBilateralFilterFourthRowLayout = QHBoxLayout()
        self.smoothingBilateralFilterLayout.addLayout(self.smoothingBilateralFilterFourthRowLayout)
        self.smoothingBilateralFilterBorderTypeTitle = QLabel("Border Type:")
        self.smoothingBilateralFilterBorderTypeTitle.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.smoothingBilateralFilterFourthRowLayout.addWidget(self.smoothingBilateralFilterBorderTypeTitle)
        self.smoothingBilateralFilterBorderTypeEntry = QComboBox()
        self.smoothingBilateralFilterBorderTypeEntry.addItems(["BORDER_DEFAULT", "BORDER_CONSTANT", "BORDER_REPLICATE", "BORDER_REFLECT", "BORDER_TRANSPARENT", "BORDER_ISOLATED"])
        self.smoothingBilateralFilterBorderTypeEntry.setCurrentIndex(0)
        self.smoothingBilateralFilterBorderTypeEntry.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.smoothingBilateralFilterFourthRowLayout.addWidget(self.smoothingBilateralFilterBorderTypeEntry)

    def smoothingItemChanged(self):
        if self.smoothingItem.currentText() == "None":
            self.smoothingNone.show()
            self.smoothingAverageBlurFrame.hide()
            self.smoothingMedianBlurFrame.hide()
            self.smoothingGaussianBlurFrame.hide()
            self.smoothingBilateralFilterFrame.hide()
        if self.smoothingItem.currentText() == "Averaging":
            self.smoothingNone.hide()
            self.smoothingAverageBlurFrame.show()
            self.smoothingMedianBlurFrame.hide()
            self.smoothingGaussianBlurFrame.hide()
            self.smoothingBilateralFilterFrame.hide()
        if self.smoothingItem.currentText() == "Median Blurring":
            self.smoothingNone.hide()
            self.smoothingAverageBlurFrame.hide()
            self.smoothingMedianBlurFrame.show()
            self.smoothingGaussianBlurFrame.hide()
            self.smoothingBilateralFilterFrame.hide()
        if self.smoothingItem.currentText() == "Gaussian Blurring":
            self.smoothingNone.hide()
            self.smoothingAverageBlurFrame.hide()
            self.smoothingMedianBlurFrame.hide()
            self.smoothingGaussianBlurFrame.show()
            self.smoothingBilateralFilterFrame.hide()
        if self.smoothingItem.currentText() == "Bilateral Filtering":
            self.smoothingNone.hide()
            self.smoothingAverageBlurFrame.hide()
            self.smoothingMedianBlurFrame.hide()
            self.smoothingGaussianBlurFrame.hide()
            self.smoothingBilateralFilterFrame.show()
    
    def deleteSmoothing(self):
        self.smoothingRemoved.emit(self.ID)
        self.deleteLater()
