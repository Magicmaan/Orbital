from PySide6.QtCore import QSize, Qt, Slot, Signal, QPoint, QRect, QTimer, QObject
from PySide6.QtGui import QCursor, QIcon, QPainter, QPixmap, QTransform, QPaintDevice, QColor, QPen
from PySide6.QtWidgets import (QHBoxLayout, QLabel, QPushButton, QSizePolicy,
                               QWidget, QApplication)

from Utils import DotDict
from GUI.Decorators import PixelBorder, sizePolicy, mouseClick
from GUI.customEvents import *


class SelectTool(QObject):
    def __init__(self) -> None:
        super().__init__()
        self.defaultProperties = DotDict(
            colour=QColor(255,255,255),
            size=1,
            brush=0
        )
        self.name = "select"
        self.selectorRect = QRect(0,0,1,1)
        self.offset = 0

        self.target = None
        self.properties = self.defaultProperties

        # Set up the timer for animation
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)  # Connect the timer to the update function
        self.timer.start(50)  # Update every 50 milliseconds

    def update_animation(self):
        # Update the offset for the dotted line animation
        self.offset += 2
        if self.offset >= 10:
            self.offset = 0
        #self.update()  # Trigger a repaint

    def setTarget(self,target:QPaintDevice):
        self.target = target


    def setProperties(self,properties:dict):
        self.properties = properties

    def onClick(self, value: toolClickEvent):
        print("Selecting")
        return
        painter = QPainter(value.target)
        
        outline = self.selectorRect

        pen = QPen(QColor("black"))
        pen.setStyle(Qt.DotLine)
        pen.setWidth(1)
        pen.setDashPattern([1, 1])
        pen.setDashOffset(self.offset)
        painter.setPen(pen)

        # Draw the rectangle with the dotted border
        painter.drawRect(outline)

        painter.end()
    
    def onRelease(self, value: toolClickEvent):
        return
        self.selectorRect.adjust(value.startposition.x(),value.startposition.x(),value.position.x(),value.position.y())

        painter = QPainter(value.target)
        pen = QPen(QColor("black"))
        pen.setStyle(Qt.DotLine)
        pen.setWidth(1)
        pen.setDashPattern([1, 1])
        pen.setDashOffset(self.offset)
        painter.setPen(pen)

        # Draw the rectangle with the dotted border
        painter.drawRect(self.selectorRect)

        painter.end()
    
    @Slot(QColor)
    def _updateColour(self, value:QColor):
        pass

