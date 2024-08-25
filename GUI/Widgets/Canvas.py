
import sys
from os.path import exists

from math import ceil, floor
from PySide6.QtCore import QPoint, QRect, QSize, Qt
from PySide6.QtGui import QPainter, QPixmap, QWheelEvent, QPen, QFont, QColor
from PySide6.QtWidgets import QLabel, QSizePolicy, QVBoxLayout, QWidget, QHBoxLayout

from DialogBox import ErrorDialog, SuccessDialog
from GUI.Widgets.WidgetUtils import removePadding
from Utils import clamp
DEFAULT_IMG = "Resources/default_canvas.png"



class Canvas(QWidget):
    def __init__(self, filepath=None, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("Canvas")
        removePadding(self)
        self.setContentsMargins(0,0,0,0)

        self.filepath = filepath

        if type(filepath) == str:
            self.image = QPixmap(filepath)
        elif type(filepath) == QPixmap:
            self.image = filepath

        #self.filepath = filepath
        self.scale = 1
        self._scaleImageCache = None

        self.setFixedSize(self.image.size())
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

    def drawPixel(self,position,prevposition,colour):
        painter = QPainter(self.image)
        
        painter.setPen(self.colour)
        painter.drawLine(position,prevposition)
        painter.end()

    def drawRect(self,rect,position):
        pass

    def ViewportStyling(self,image:QPixmap) -> QPixmap:
        
        scale = self.scale
        border = 10

        print(f"Scale: {scale}")
        

        expandedImage = QPixmap(image.width() + border * 2, image.height() + border * 2)
        expandedImage.fill(QColor(0, 0, 0, 0))  # Fill with transparent color
        #draw image to expanded image
        painter = QPainter(expandedImage)
        #painter.fillRect(expandedImage.rect(), Qt.black)

        print(f"hasAlpha: {expandedImage.hasAlphaChannel()}")
        

        #styling
        # Styling
        pen = QPen(QColor(255,255,255,125))  # Set the pen color to red
        pen.setWidth(1)  # Set the pen width
        painter.setPen(pen)

        #set font + no aliasing
        font = QFont("pixelated", 6)
        font.setHintingPreference(QFont.PreferNoHinting)
        font.setStyleStrategy(QFont.NoAntialias)
        painter.setFont(font)
        

        # Draw the border
        AxisBorder = 1
        AxisOffset = 4
        # Draw line on top border
        painter.drawLine(border -AxisBorder, border -AxisOffset, 
                         expandedImage.width() -border +AxisBorder, border -AxisOffset)
        # Draw line on left border
        painter.drawLine(border -AxisOffset, border -AxisBorder, 
                         border -AxisOffset, expandedImage.height() -border +AxisBorder)  

        #centre y marker
        painter.drawPoint(border -AxisOffset +1, int(expandedImage.height()/2))
        if expandedImage.height() % 2 == 0: #if the width is even, draw an extra line
            painter.drawPoint(border - AxisOffset +1, int(expandedImage.height()/2)-1)
        
        #centre x marker
        painter.drawPoint(int(expandedImage.width()/2), border - AxisOffset +1)
        if expandedImage.width() % 2 == 0: #if the width is even, draw an extra line
            painter.drawPoint(int(expandedImage.width()/2)-1, border - AxisOffset +1)

        # draw size
        painter.drawText(border - AxisBorder, border - AxisOffset -1, f"{image.width()}")

        painter.drawText(border - AxisBorder -6, border - AxisOffset -1, "X")

        painter.rotate(-90)
        painter.drawText(-(border + AxisOffset +5), border - AxisOffset -1, f"{image.height()}")
        painter.rotate(90)

        
           
        # Draw the image
        painter.drawPixmap(border, border, image)

        
        painter.end()

        return expandedImage

    def scaleImageToViewport(self, scale):
        # if scale == self.scale:
        #    return self._scaleImageCache
        border = 2
        # Get the image
        image = self.image.copy()
        self.scale = scale
        # draw border + details stuff
        imageStyled = self.ViewportStyling(image)

        # Make pixmap for upscale
        scaledImage = QPixmap(imageStyled.size() * scale)
        scaledImage.fill(QColor(0, 0, 0, 0))

        # Define the source and destination rects to draw to
        sourceRect = QRect(0, 0, imageStyled.width(), imageStyled.height())
        destRect = QRect(0, 0, int(scaledImage.width()), int(scaledImage.height()))

        # Create a painter for the viewport
        painter = QPainter(scaledImage)
        # Draw the scaled image
        painter.drawPixmap(destRect, imageStyled, sourceRect)
        painter.end()

        # Cache the image
        self._scaleImageCache = scaledImage

        return self._scaleImageCache
    





    