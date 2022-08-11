from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class QHLine(QFrame):
  '''
  a horizontal seperation line\n
  '''
  def __init__(self):
    super().__init__()
    self.setMinimumWidth(1)
    self.setFixedHeight(20)
    self.setFrameShape(QFrame.HLine)
    self.setFrameShadow(QFrame.Sunken)
    self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
    return

class QVLine(QFrame):
  '''
  a vertical seperation line\n
  '''
  def __init__(self):
    super().__init__()
    self.setFixedWidth(20)
    self.setMinimumHeight(1)
    self.setFrameShape(QFrame.VLine)
    self.setFrameShadow(QFrame.Sunken)
    self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
    return