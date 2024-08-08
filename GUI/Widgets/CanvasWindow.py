
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import sys
from os.path import exists




import CanvasUtils
from DialogBox import ErrorDialog,SuccessDialog
from CanvasUtils import *

DEFAULT_IMG = "Resources/default_canvas.png"



class Image(QWidget):
    def __init__(self, texturepath=DEFAULT_IMG, parent=None) -> None:
        super().__init__(parent)
        self.image = QPixmap()
        self.texturepath = texturepath
        self.loadTexture()
        self.name = "LOLL"
        

    def loadTexture(self, texturepath=None) -> bool:
        if texturepath:
            self.texturepath = texturepath

        if exists(self.texturepath):
            self.image.load(self.texturepath)
            self.update()
            return True
        else:
            return False
    
    


class Canvas(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        sX, sY = 256, 256
        self.fixed_size = QSize(sX, sY)

        self.resize(sX, sY)  # Minimum size to handle fixed resolution drawing
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.viewport = QPixmap(self.fixed_size)
        self.image = Image()

        self.imageScale = 1
        self.imagePosition = (0, 0)

        self.shapes = []
        self.drawing = False
        self.lastPoint = QPoint()
        self.currentPoint = QPoint()

        self.pixmap = QPixmap(self.fixed_size)
        self.render_content()  # Draw initial content

    

    def render_content(self):
        self.viewport = QPixmap(self.size())
        # Clear the viewport before drawing
        self.viewport.fill(QColor('red'))  # Clear background with white

        # Create a painter for the viewport
        painter = QPainter(self.viewport)
        painter.setPen(QPen(QColor('black'), 1))

        # Get the image
        image = self.image.image

        # Define the source and destination rectangles
        sourceRect = QRect(0, 0, image.width(), image.height())
        destRect = QRect(self.imagePosition[0], self.imagePosition[1], 
                         int(image.width() * self.imageScale), 
                         int(image.height() * self.imageScale))

        # Draw the scaled image onto the viewport
        painter.drawPixmap(destRect, image, sourceRect)

        # Draw any shapes on the viewport
        for shape in self.shapes:
            painter.drawLine(shape[0], shape[1])

        painter.end()

        # Copy the viewport to the main pixmap
        self.pixmap = self.viewport.copy()

    
    def _resizeImage(self):
        pass

    def _resizeViewport(self):
        pass

    def _mapToFixedSize(self, point):
        # Map the widget's coordinates to the fixed-size resolution
        scale_factor = self.fixed_size.width() / self.width()
        return QPoint(int(point.x() * scale_factor), int(point.y() * scale_factor))

    def _mapFromFixedSize(self, point):
        # Map the fixed-size coordinates to the widget's coordinate system
        scale_factor = self.width() / self.fixed_size.width()
        return QPoint(int(point.x() * scale_factor), int(point.y() * scale_factor))

    def paintEvent(self, event):
            painter = QPainter(self)
            # Scale the fixed-size pixmap to fit the widget's size using nearest neighbor scaling
            scaled_pixmap = self.pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.FastTransformation)
            painter.drawPixmap(0, 0, scaled_pixmap)
            painter.end()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.lastPoint = self._mapToFixedSize(event.position().toPoint())
            self.drawing = True
            self.imageScale = max(0.1, self.imageScale - 0.1)  # Ensure the scale is not zero or negative

        if event.button() == Qt.RightButton:
            self.imageScale += 0.1
            #exportTexture(self.image,"Resources/","png")

        self.render_content()
        self.update()
    def mouseMoveEvent(self, event):
        if self.drawing:
            self.currentPoint = self._mapToFixedSize(event.position().toPoint())
            self.shapes.append((self.lastPoint, self.currentPoint))
            self.render_content()  # Re-render content with new shapes
            self.update()  # Request a repaint to finalize the line
            self.lastPoint = self.currentPoint  # Update last point for the next segment
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False