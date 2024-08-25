from PySide6.QtCore import QSize, Qt, Slot, Signal, QPoint
from PySide6.QtGui import QCursor, QIcon, QPainter, QPixmap, QTransform, QPaintDevice, QColor
from PySide6.QtWidgets import (QHBoxLayout, QLabel, QPushButton, QSizePolicy,
                               QWidget, QApplication)

from Utils import DotDict
from GUI.Decorators import PixelBorder, sizePolicy, mouseClick
from GUI.customEvents import *


class BrushTool():
    def __init__(self) -> None:
        self.defaultProperties = DotDict(
            colour=QColor(255,255,255),
            size=1,
            brush=0
        )


        self.target = None
        self.properties = self.defaultProperties


    def setTarget(self,target:QPaintDevice):
        self.target = target


    def setProperties(self,properties:dict):
        self.properties = properties

    def onClick(self, value: toolClickEvent):
        painter = QPainter(value.target)
        
        painter.setPen(self.properties.colour)
        painter.drawLine(value.position, value.prevposition)

        painter.end()
    

    @Slot(QColor)
    def _updateColour(self, value:QColor):
        self.properties.colour = value
