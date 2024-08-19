from PySide6.QtCore import QSize, Qt, Slot, Signal, QPoint
from PySide6.QtGui import QCursor, QIcon, QPainter, QPixmap, QTransform
from PySide6.QtWidgets import (QHBoxLayout, QLabel, QPushButton, QSizePolicy,
                               QWidget, QApplication)

class toolClickEvent:
    def __init__(self,position:QPoint,prevposition:QPoint,targetImage:QPixmap) -> None:
        self.position = position
        self.prevposition = prevposition
        self.target = targetImage
    
    def __str__(self):
        return f"ToolClickEvent: (pos={self.position.x(), self.position.y()},pre={self.prevposition.x(), self.prevposition.y()})"

class toolReleaseEvent:
    def __init__(self,position,startposition,targetImage) -> None:
        self.position = position
        self.startposition = startposition
        self.target = targetImage
    
    def __str__(self) -> str:
        return f"ToolReleaseEvent: (pos={self.position.x(), self.position.y()},start={self.startposition.x(), self.startposition.y()})"

class toolReleaseEvent:
    def __init__(self,position:QPoint,prevposition:QPoint,targetImage:QPixmap) -> None:
        self.position = position
        self.target = targetImage
    
    def __str__(self):
        return f"ToolClickEvent: (pos={self.position.x(), self.position.y()},pre={self.prevposition.x(), self.prevposition.y()})"

class openFileCustEvent:
    def __init__(self,filepath:str) -> None:
        self.file = filepath
    
    def __str__(self):
        return f"openFileEvent: (file={self.file})"