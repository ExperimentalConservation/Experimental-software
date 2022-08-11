from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class VideoTrack_VideoObjectBB(QWidget):

    def __init__(self, parent=None):
        super(VideoTrack_VideoObjectBB, self).__init__(parent)
        self.setWindowFlags(Qt.SubWindow)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(QSizeGrip(self), 0, Qt.AlignLeft | Qt.AlignTop)
        layout.addWidget(QSizeGrip(self), 0, Qt.AlignRight | Qt.AlignBottom)
        self._band = QRubberBand(QRubberBand.Rectangle, self)
        self._band.show()
        self.show()
    
    def parentWidgetDims(self, parentWidth, parentHeight):
        self.parentWidth = parentWidth
        self.parentHeight = parentHeight

    def mousePressEvent(self, event):
        self._mousePressPos = None
        self._mouseMovePos = None
        if event.button() == Qt.LeftButton:
            self._mousePressPos = event.globalPos()
            self._mouseMovePos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            # adjust offset from clicked point to origin of widget
            currPos = self.mapToGlobal(self.pos())
            globalPos = event.globalPos()
            diff = globalPos - self._mouseMovePos
            newPos = self.mapFromGlobal(currPos + diff)
            localCoords = self.contentsRect()
            if newPos.x() < 0:
                newPos.setX(0)
            if newPos.y() < 0:
                newPos.setY(0)
            if newPos.x() + localCoords.width() > self.parentWidth:
                newPos.setX(self.parentWidth - localCoords.width())
            if newPos.y() + localCoords.height() > self.parentHeight:
                newPos.setY(self.parentHeight - localCoords.height())
            self.move(newPos)
            self._mouseMovePos = globalPos

    def mouseReleaseEvent(self, event):
        if self._mousePressPos:
            moved = event.globalPos() - self._mousePressPos
            if moved.manhattanLength() > 3:
                event.ignore()
                return

    def resizeEvent(self, event):
        self._band.resize(self.size())
    
    def getObjectBBCoords(self):
        localCoords = self.contentsRect()
        self.videoBB_x = self.pos().x()
        self.videoBB_y = self.pos().y()
        self.videoBB_width = localCoords.width()
        self.videoBB_height = localCoords.height()
        videoObjectBBCoords = [self.videoBB_x, self.videoBB_y, self.videoBB_width, self.videoBB_height]
        return videoObjectBBCoords