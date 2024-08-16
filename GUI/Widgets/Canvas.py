
import sys
from os.path import exists

from PySide6.QtCore import QPoint, QRect, QSize, Qt
from PySide6.QtGui import QPainter, QPixmap, QWheelEvent
from PySide6.QtWidgets import QLabel, QSizePolicy, QVBoxLayout, QWidget, QHBoxLayout

from DialogBox import ErrorDialog, SuccessDialog
from GUI.Widgets.WidgetUtils import removePadding

DEFAULT_IMG = "Resources/default_canvas.png"



class Canvas(QWidget):
    def __init__(self, filepath=None, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("Canvas")
        removePadding(self)
        self.setContentsMargins(0,0,0,0)
        self.image = QPixmap(filepath)
        #self.filepath = filepath
        self.scale = 1
        self._scaleImageCache = None

        self.setFixedSize(self.image.size())
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

    def drawPixel(self,pixel,position):
        pass

    def drawRect(self,rect,position):
        pass


    def scaleImageToViewport(self,scale):
        #if scale == self.scale:
        #    return self._scaleImageCache
        
        self.scale = scale

        # Get the image
        image = self.image

        #make pixmap for upscale
        scaleImage = QPixmap(image.size()*scale)

        
        # Define the source and destination rects to draw to
        sourceRect = QRect(0, 0, image.width(), image.height())
        destRect = QRect(0, 0, 
                         int(scaleImage.width()), 
                         int(scaleImage.height()))

        # Create a painter for the viewport
        painter = QPainter(scaleImage)

        # Draw the scaled image
        painter.drawPixmap(destRect, image, sourceRect)

        painter.end()


        # Cache the image
        self._scaleImageCache = scaleImage

        return self._scaleImageCache





    