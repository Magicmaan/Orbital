from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QCursor, QIcon, QPainter, QPixmap, QTransform, QPaintDevice, QColor
from PySide6.QtWidgets import (QHBoxLayout, QLabel, QPushButton, QSizePolicy,
                               QWidget, QApplication)

from Utils import DotDict

class Brush():
    def __init__(self) -> None:
        self.defaultProperties = DotDict(
            colour=QColor(0, 0, 0),
            size=1,
            brush=0
        )


        self.target = None
        self.properties = self.defaultProperties


    def setTarget(self,target:QPaintDevice):
        self.target = target


    def setProperties(self,properties:dict):
        self.properties = properties

    def onAction(self, position, painter=None):
        if painter==None:
            painter = QPainter(self.target)
        painter.drawPoint(position)
        painter.end()