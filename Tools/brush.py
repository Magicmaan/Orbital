from PySide6.QtCore import QSize, Qt, Slot, Signal, QPoint
from PySide6.QtGui import QCursor, QIcon, QPainter, QPixmap, QTransform, QPaintDevice, QColor
from PySide6.QtWidgets import (QHBoxLayout, QLabel, QPushButton, QSizePolicy,
                               QWidget, QApplication)

from Utils import DotDict
from GUI.Decorators import PixelBorder, sizePolicy, mouseClick
from GUI.customEvents import *

#TODO: fix transparency so when holding down can't overlap
#TODO: fix when drawing across tiling mode
#TODO: Draw line tool


class BrushTool():
    def __init__(self) -> None:
        self.defaultProperties = DotDict(
            colour=QColor(255,255,255),
            size=1,
            brush=0
        )
        self.name = "brush"
        self.pmap = None
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

        return
        painter = QPainter(self.pmap)
        colour = self.properties.colour
        colour.setAlpha(255)
        painter.setPen(colour)
        painter.drawLine(value.position, value.prevposition)

        painter.end()
    
    def onRelease(self, value: toolClickEvent):
        # Ensure the pixmap is properly initialized
        if self.pmap is None:
            return

        # Create a temporary pixmap with an alpha channel
        temp_pixmap = QPixmap(self.pmap.size())
        temp_pixmap.fillRect(temp_pixmap.rect(), Qt.transparent)

        # Use a QPainter to draw the original pixmap onto the temporary pixmap with transparency
        temp_painter = QPainter(temp_pixmap)
        #temp_painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_DestinationAtop)
        temp_painter.drawPixmap(0, 0, self.pmap)
        temp_painter.setCompositionMode(QPainter.CompositionMode_DestinationOver)
        #temp_painter.fillRect(temp_pixmap.rect(), QColor(0, 0, 0, 127))  # 127 for 50% transparency
        temp_painter.end()

        # Draw the temporary pixmap onto the target
        painter = QPainter(value.target)
        painter.drawPixmap(QPoint(0, 0), temp_pixmap)
        painter.end()
        self.pmap = QPixmap(128,128)

    @Slot(QColor)
    def _updateColour(self, value:QColor):
        self.properties.colour = value
