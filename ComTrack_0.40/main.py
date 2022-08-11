from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os
import sys

from mainSetCentralWidget import CentralWidget

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()       
        self.setGeometry(100, 100, 1500, 1500)
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), 'images/icons/logo256x256.png')))
        self.setWindowTitle('ComTrack - Detecting, Tracking, and Classifying Multiple Species')
        self.initMenu()
        self.initCentralWidget()

    def initMenu(self):
        # CREATING THE MENU
        mainMenu = self.menuBar()

        # # File subMenu
        # fileMenu = mainMenu.addMenu('File')
        # fileMenu_OpenVideo = QAction('Open Video', self)
        # fileMenu_OpenVideo.triggered.connect(self.openVideo)
        # fileMenu.addAction(fileMenu_OpenVideo)

        # # Edit subMenu
        # editMenu = mainMenu.addMenu('Edit')

        # Apps subMenu
        appsMenu = mainMenu.addMenu('Apps')

        appsMenu_Home = QAction('Home', self)
        appsMenu_Home.triggered.connect(self.goToHome)
        appsMenu.addAction(appsMenu_Home)

        appsMenu_VideoTrack = QAction("Training Step 1: Generate Tracked Objects", self)
        appsMenu_VideoTrack.triggered.connect(self.goToVideoTrack)
        appsMenu.addAction(appsMenu_VideoTrack)

        appsMenu_DataPrepare = QAction('Training Step 2: Add/Correct Labels on Tracked Objects', self)
        appsMenu_DataPrepare.triggered.connect(self.goToCorrectLabels)
        appsMenu.addAction(appsMenu_DataPrepare)

        appsMenu_DatasetGenerate = QAction('Training Step 3: Generate Image Datasets', self)
        appsMenu_DatasetGenerate.triggered.connect(self.goToGenerateDatasets)
        appsMenu.addAction(appsMenu_DatasetGenerate)

        appsMenu_ModelBuild = QAction('Training Step 4: Build Deep-Learning Classifier', self)
        appsMenu_ModelBuild.triggered.connect(self.goToBuildModel)
        appsMenu.addAction(appsMenu_ModelBuild)

        appsMenu_TrackNClass = QAction('Track And Classify', self)
        appsMenu_TrackNClass.triggered.connect(self.goToTrackNClass)
        appsMenu.addAction(appsMenu_TrackNClass)

        # Help subMenu
        helpMenu = mainMenu.addMenu('Help')

        helpMenu_About = QAction('About', self)
        helpMenu_About.triggered.connect(self.openAbout)
        helpMenu.addAction(helpMenu_About)


    def initCentralWidget(self):
        self.myCentralWidget = CentralWidget()
        self.setCentralWidget(self.myCentralWidget)

    # def openVideo(self):
    #     self.myCentralWidget.mainWidget_VideoTrack.controlsWidget.fileControlsWidget.loadVideo()

    def openAbout(self):
        QMessageBox.about(self, "About", "ComTrack version 0.40")

    def goToHome(self):
        self.myCentralWidget.setIndex("Home")

    def goToVideoTrack(self):
        self.myCentralWidget.setIndex("Generate Tracked Objects")

    def goToCorrectLabels(self):
        self.myCentralWidget.setIndex("Correct Labels")

    def goToGenerateDatasets(self):
        self.myCentralWidget.setIndex("Generate Datasets")

    def goToBuildModel(self):
        self.myCentralWidget.setIndex("Build Model")

    def goToTrackNClass(self):
        self.myCentralWidget.setIndex("Track And Class")
    

    def closeEvent(self, event):
            close = QMessageBox.question(self,
                                         "Close",
                                         "Are you sure you want to close ComTrack?",
                                         QMessageBox.Yes | QMessageBox.No)
            if close == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()
    

# Main Function of the GUI
def main():
    global rect
    app = QApplication(sys.argv)
    # screen = app.primaryScreen()
    # screen = app.screens()[2]
    screen = app.screens()[0]
    rect = screen.availableGeometry()
    window = MyMainWindow()
    window.showMaximized()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
