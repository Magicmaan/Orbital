
import sys
from os.path import exists

from PySide6.QtCore import QPoint, QRect, QSize, Qt
from PySide6.QtGui import QPainter, QPixmap, QWheelEvent
from PySide6.QtWidgets import QLabel, QSizePolicy, QVBoxLayout, QWidget

from DialogBox import ErrorDialog, SuccessDialog
from GUI.Widgets.WidgetUtils import drawPixelBorder, removePadding

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
    
from GUI.Widgets.Decorators import PixelBorder, sizePolicy

@PixelBorder

class Viewport(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        sX, sY = 128, 128
        self.fixed_size = QSize(sX, sY)

        #self.resize(sX, sY)  # Minimum size to handle fixed resolution drawing
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image = Image()
        self.imageScaled = QPixmap(self.fixed_size)
        self.setStyleSheet("background:purple;")
        self.imageScale = 1
        self.imagePosition = QPoint(0, 0)

        self.shapes = []
        self.drawing = False
        self.lastPoint = QPoint()
        self.currentPoint = QPoint()
        self.dragging = False

        self.pixmap = QPixmap(self.fixed_size)
        self.RenderScaleImage()  # Draw initial content

        self.setLayout(QVBoxLayout())
        layout = self.layout()
        removePadding(self)

        self.setContentsMargins(5,5,5,5)


        # Example widget: QLabel on top of the pixmap
        self.label = QLabel("This is a label on top of the pixmap", self)
        self.label.setStyleSheet("color: white;")
        self.label.setStyleSheet("background:transparent;")
        layout.addWidget(self.label, alignment=Qt.AlignTop)

    

    def RenderScaleImage(self):
        self.imageScaled = QPixmap(self.image.image.size()*self.imageScale)

        # Get the image
        image = self.image.image

        # Define the source and destination rects to draw to
        sourceRect = QRect(0, 0, image.width(), image.height())
        destRect = QRect(0, 0, 
                         int(self.imageScaled.width()), 
                         int(self.imageScaled.height()))

        # Create a painter for the viewport
        painter = QPainter(self.imageScaled)

        # Draw the scaled image
        painter.drawPixmap(destRect, image, sourceRect)

        painter.end()

        # Copy the viewport to the main pixmap
        self.pixmap = self.imageScaled.copy()

    
    def _resizeImage(self):
        pass

    def _resizeViewport(self):
        pass

    def _mapToFixedSize(self, point):
        # Map the widget's coordinates to the fixed-size resolution
        scale_factor = self.size().width() / self.image.size().width()
        return QPoint(int(point.x() * scale_factor), int(point.y() * scale_factor))

    def _mapFromFixedSize(self, point):
        # Map the fixed-size coordinates to the widget's coordinate system
        scale_factor = self.imageScale
        return QPoint(int(point.x() * scale_factor), int(point.y() * scale_factor))

    def paintEvent(self, event):
        painter = QPainter(self)

        painter.drawPixmap(self.imagePosition.x(), self.imagePosition.y(), self.pixmap)


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.lastPoint = self._mapToFixedSize(event.position().toPoint())
            self.drawing = True
            self.imageScale = max(0.1, self.imageScale - 0.1)  # Ensure the scale is not zero or negative

        if event.button() == Qt.RightButton:
            self.imageScale += 0.1
            #exportTexture(self.image,"Resources/","png")

        if event.button() == Qt.MiddleButton:
            self.dragging = True
            self.dragging_pos = event.position().toPoint()
            self.offset = self.imagePosition - self.dragging_pos


        self.RenderScaleImage()
        self.update()

    def wheelEvent(self, event: QWheelEvent):
        # Get the amount of scrolling
        delta = event.angleDelta().y()
        # Adjust value based on scroll direction
        if delta > 0:
            self.imageScale += 0.1
        else:
            self.imageScale -= 0.1
        
        self.RenderScaleImage()
        self.update()

    def mouseMoveEvent(self, event):
        if self.drawing:
            self.currentPoint = self._mapToFixedSize(event.position().toPoint())
            self.shapes.append((self.lastPoint, self.currentPoint))
            self.RenderScaleImage()  # Re-render content with new shapes
            self.update()  # Request a repaint to finalize the line
            self.lastPoint = self.currentPoint  # Update last point for the next segment
        
        if self.dragging:
            cpos = self.imagePosition

            self.imagePosition = event.position() + self.offset

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False
        
        if event.button() == Qt.MiddleButton:
            self.dragging = False
            