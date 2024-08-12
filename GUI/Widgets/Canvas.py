
import sys
from os.path import exists

from PySide6.QtCore import QPoint, QRect, QSize, Qt
from PySide6.QtGui import QPainter, QPixmap, QWheelEvent
from PySide6.QtWidgets import QLabel, QSizePolicy, QVBoxLayout, QWidget, QGridLayout

from DialogBox import ErrorDialog, SuccessDialog
from GUI.Widgets.WidgetUtils import removePadding

DEFAULT_IMG = "Resources/default_canvas.png"



class Canvas(QWidget):
    def __init__(self, filepath=None, parent=None) -> None:
        super().__init__(parent)

        self.setObjectName("Canvas")
        self.setLayout(QGridLayout())
        layout = self.layout()
        removePadding(self)

        self.image = QPixmap()
        self.filepath = filepath
        self.focus

        self.focus = True


    def drawPixel(self,pixel,position):
        pass
    def drawRect(self,rect,position):
        pass



    

    def paintEvent(self):
        #Drawing of image
        pass


    