from PySide6.QtCore import QPoint, QRect, QSize, Qt
from PySide6.QtGui import QPainter, QPixmap, QWheelEvent, QColor
from PySide6.QtWidgets import QLabel, QSizePolicy, QVBoxLayout, QWidget, QHBoxLayout

class paintPixelEvent:
    def __init__(self,pixelCoord:QPoint,pixelColour:QColor,canvasImg:QPixmap) -> None:
        self.position = pixelCoord

        self.previousPixel = None
        self.pixel = pixelColour

        target = canvasImg




class History:
    def __init__(self) -> None:
        self.history = {}
        #history will be a stack

        self.history.brush
    
    def undo(self):
        #pop history, reverting change
        pass

    def logEvent(self,event):
        pass