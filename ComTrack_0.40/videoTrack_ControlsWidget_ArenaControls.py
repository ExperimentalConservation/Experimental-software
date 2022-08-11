from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class VideoTrack_ArenaControlsWidget(QGroupBox):

    isArenaDrawed = pyqtSignal(bool)
    isArenaSaved = pyqtSignal(bool)
    isArenaCancelled = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.initWidget()
        self.makeButtons()
    
    def initWidget(self):
        self.setTitle("Arena Controls")
        self.setCheckable(True)
        self.setChecked(False)
        self.toggled.connect(self.isArenaControlsActive)
        # margin-top: 0.6em
        # top: -16px; left: 10px; 
        self.setStyleSheet("""
                QGroupBox{font-weight: bold; border: 1px solid black; border-radius: 5px; margin-top: 0.6em;}
                QGroupBox::title{top: -0.5em; subcontrol-position: top center;}
                """)
        self.mainLayout = QHBoxLayout(self)
        self.mainLayout.setAlignment(Qt.AlignTop)       
    
    def makeButtons(self):
        # Draw Arena Button
        self.drawButton = QPushButton("Draw", self)
        self.drawButton.setEnabled(False)
        self.drawButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.drawButton.clicked.connect(self.drawArena)
        self.mainLayout.addWidget(self.drawButton, alignment=Qt.AlignTop)

        # Save Arena Button
        self.saveButton = QPushButton("Save", self)
        self.saveButton.setEnabled(False)
        self.saveButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.saveButton.clicked.connect(self.saveArena)
        self.mainLayout.addWidget(self.saveButton, alignment=Qt.AlignTop)

        # Cancel Arena Button
        self.cancelButton = QPushButton("Cancel", self)
        self.cancelButton.setEnabled(False)
        self.cancelButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.cancelButton.clicked.connect(self.cancelArena)
        self.mainLayout.addWidget(self.cancelButton, alignment=Qt.AlignTop)
    
    def isArenaControlsActive(self):
        if self.isChecked() is True:
            self.drawButton.setEnabled(True)
            self.saveButton.setEnabled(False)
            self.cancelButton.setEnabled(False)
        else:
            self.drawButton.setEnabled(False)
            self.saveButton.setEnabled(False)
            self.cancelButton.setEnabled(False)

    def drawArena(self):
        self.isArenaDrawed.emit(True)
        self.drawButton.setEnabled(False)
        self.saveButton.setEnabled(True)
        self.cancelButton.setEnabled(True)

    def saveArena(self):
        self.isArenaSaved.emit(True)
        self.drawButton.setEnabled(False)
        self.saveButton.setEnabled(False)
        self.cancelButton.setEnabled(True)

    def cancelArena(self):
        self.isArenaCancelled.emit(True)
        self.drawButton.setEnabled(True)
        self.saveButton.setEnabled(False)
        self.cancelButton.setEnabled(False)

    # def enableArenaDrawing(self):
    #         self.drawButton.setEnabled(True)

    # def disableArenaDrawing(self):
    #         self.drawButton.setEnabled(False)
    
    # def enableArenaSaving(self):
    #         self.saveButton.setEnabled(True)

    # def disableArenaSaving(self):
    #         self.saveButton.setEnabled(False)
    
    # def enableArenaCancelling(self):
    #         self.cancelButton.setEnabled(True)

    # def disableArenaCancelling(self):
    #         self.cancelButton.setEnabled(False)
    
    def newVideoLoaded(self):
        self.setChecked(False)