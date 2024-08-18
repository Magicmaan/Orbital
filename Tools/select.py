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

    def onAction(self, value: toolClickEvent):
        painter = QPainter(value.target)
        
        outline = QRect(5,5,20,20)

        pen = QPen(QColor("black"))
        pen.setStyle(Qt.DotLine)
        pen.setWidth(1)
        pen.setDashPattern([1, 1])
        pen.setDashOffset(self.offset)
        painter.setPen(pen)

        # Draw the rectangle with the dotted border
        painter.drawRect(outline)

        painter.end()
    
    @Slot(QColor)
    def _updateColour(self, value:QColor):
        pass

