from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys

class ConsoleWidget(QGroupBox):

    def __init__(self):
        super().__init__()
        # sys.stdout = Stream(newText=self.onUpdateText)
        # sys.stderr = Stream(newText=self.onUpdateText)
        self.initWidget()
        self.makeConsole()
    
    def __del__(self):
        sys.stdout = sys.__stdout__

    def initWidget(self):
        self.setTitle("Console")
        self.setStyleSheet("""
                QGroupBox{font-weight: bold; border: 1px solid black; border-radius: 5px; margin-top: 0.6em;}
                QGroupBox::title{top: -0.5em; subcontrol-position: top center;}
                """)
        self.mainLayout = QVBoxLayout(self)
    
    def makeConsole(self):
        # Learning Rate
        self.console = QTextEdit()
        self.console.moveCursor(QTextCursor.Start)
        self.console.ensureCursorVisible()
        self.console.setLineWrapColumnOrWidth(int(self.width() // 1.05))
        self.console.setLineWrapMode(QTextEdit.FixedPixelWidth)
        self.mainLayout.addWidget(self.console)
    
    def onUpdateText(self, text):
        cursor = self.console.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.console.setTextCursor(cursor)
        self.console.ensureCursorVisible()


class Stream(QObject):

    newText = pyqtSignal(str)

    def write(self, text):
        self.newText.emit(str(text))
    
    def flush(self):
        pass
