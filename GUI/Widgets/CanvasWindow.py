
import sys
from os.path import exists
from math import log, exp

from PySide6.QtCore import QPoint, QRect, QSize, Qt
from PySide6.QtGui import QPainter, QPixmap, QWheelEvent, QColor
from PySide6.QtWidgets import QLabel, QSizePolicy, QVBoxLayout, QWidget, QScrollBar, QGridLayout, QSlider, QApplication

from DialogBox import ErrorDialog, SuccessDialog
from GUI.Widgets.WidgetUtils import drawPixelBorder, removePadding
from GUI.Widgets.ScrollBar import CustomScrollBar
from GUI.Widgets.Canvas import Canvas
from Utils import clamp

from GUI.Decorators import PixelBorder, sizePolicy, mouseClick
DEFAULT_IMG = "Resources/default_canvas.png"




@PixelBorder
@mouseClick
class Viewport(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        
        sX, sY = 128, 128
        self.fixed_size = QSize(sX, sY)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.program = QApplication.instance().program

        #image scaling and position
        self.imageScaleRange = (0.25, 50)
        self._imageScale = 1
        self._imagePosition = QPoint(0, 0)


        self.canvas = Canvas("Resources/default_canvas.png")
        #["canvas_name"] : (canvas, scale, etc)
        self._canvasSettings = {    }

        
        self.setMouseTracking(True)
        self.shapes = []
        self.drawing = False
        self.lastPoint = QPoint()
        self.currentPoint = QPoint()
        self.dragging = False

        self.cursorPos = QPoint(0,0)
        self.snapCursor = False

        self.pixmap = QPixmap(self.fixed_size)
        

        self.setLayout(QGridLayout())
        layout = self.layout()
        removePadding(self)
        layout.setAlignment(Qt.AlignBottom)
        layout.setRowStretch(0, 2)
        layout.setSpacing(0)
        layout.setContentsMargins(0,0,0,0)
        self.setContentsMargins(6,6,6,6)


        # Example widget: QLabel on top of the pixmap
        self.label = QLabel("This is a label on top of the pixmap", self)
        self.label.setStyleSheet("color: white;")
        self.label.setStyleSheet("background:transparent;")
        layout.addWidget(self.label,0,1)
        self.update()

    def scrollVertical(self, value):
        # Update the label with the current scroll value
        self.label.setText(f"Scroll Value: {value}")

        val = 1
        self.moveCanvas(QPoint(self._imagePosition.x(), value))

        self.update()
    def scrollHorizontal(self, value):
        # Update the label with the current scroll value
        self.label.setText(f"Scroll Value: {value}")

        val = value / 100
        self.moveCanvas(QPoint(self.width() * val, self._imagePosition.y()))

        self.update()

    def getImage(self):
        return self.canvas.image

    def addImage(self,img):
        self.canvas.image.load(img)
        self.canvas.setFixedSize(self.image.size())

    def paintCanvas(self,painter):
        canvas = self.canvas.scaleImageToViewport(self._imageScale)
        #draw the canvas to Viewport
        painter.drawPixmap(self._imagePosition.x(), self._imagePosition.y(), canvas)

    def paintPixelPosition(self, painter):
        # Set the brush and pen for the square
        painter.setBrush(QColor(100, 200, 150))  # Fill color
        painter.setPen(QColor(50, 100, 75))  # Border color     

        img_pos = self._imagePosition
        img_scale = self._imageScale

        self.cursorPos = self._mapToCanvas(self.mousePos)
        # Bounds check of canvas and draw the square if within bounds
        if (0 <= self.cursorPos.x() < self.canvas.width()) and (0 <= self.cursorPos.y() < self.canvas.height()):

            painter.drawRect(QRect(
                self.cursorPos.x() * img_scale + img_pos.x(),
                self.cursorPos.y() * img_scale + img_pos.y(),
                img_scale,
                img_scale
            ))

    def paintViewport(self,painter):
        pass

    def paintEvent(self, event):
        painter = QPainter(self)

        self.paintCanvas(painter)

        self.paintPixelPosition(painter)

        super().paintEvent(event)

    def moveCanvas(self,position:QPoint,add=False):
        size = self.canvas.rect()
        x = position.x()
        y = position.y()
        canvasW = size.width() * self._imageScale
        canvasH = size.height() * self._imageScale

        bSize = 10
        tempx = x
        tempy = y

        if x+(canvasW//2) < bSize: tempx= bSize - (canvasW//2)
        if x-(canvasW//2) > self.width()-bSize: tempx=self.width() - bSize - canvasW

        if y+(canvasH//2) < bSize: tempx= bSize - (canvasW//2)
        if y-(canvasH//2) > self.height()-bSize: tempy=self.height() - bSize - canvasW

        
        self._imagePosition.setX(tempx)
        self._imagePosition.setY(tempy)

    def _mapToCanvas(self, point:QPoint):
        """
        Maps the viewport coordinates to canvas
        """
        img_pos = self._imagePosition
        img_scale = self._imageScale

        # Calculate position in canvas coordinates
        canvas_x = (point.x() - img_pos.x()) / img_scale
        canvas_y = (point.y() - img_pos.y()) / img_scale

        # Return the mapped QPoint
        return QPoint(int(canvas_x), int(canvas_y))

    def _mapFromCanvas(self, point:QPoint):
        """
        Map the canvas coordinates to the viewport
        """

        img_pos = self._imagePosition
        img_scale = self._imageScale

        # Calculate position in viewport coordinates
        viewport_x = point.x() * img_scale + img_pos.x()
        viewport_y = point.y() * img_scale + img_pos.y()

        # Return the mapped QPoint
        return QPoint(int(viewport_x), int(viewport_y))

    def paintpix(self):
        self.program.tools.onAction(self.cursorPos)

    def onMouseClick(self):
        if self.mouseClicks.left:
            self.paintpix()

        if self.mouseClicks.right:
            self._imageScale += 0.1
        
        if self.mouseClicks.middle:
            self.offset = self._imagePosition - self.mousePressPos
            self.moveCanvas(self.mousePos + self.offset)

    def onMouseMove(self):
        if self.mouseClicks.left:
            self.paintpix()
        
        if self.mouseClicks.middle:
            self.moveCanvas(self.mousePos + self.offset)

        self.update()
        print("Buh")

    '''def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.lastPoint = self._mapToCanvas(event.position().toPoint())
            self.drawing = True
            #self._imageScale = max(0.1, self._imageScale - 0.1)  # Ensure the scale is not zero or negative

            self.program.tools.onAction(self.cursorPos)

        if event.button() == Qt.RightButton:
            self._imageScale += 0.1
            #exportTexture(self.image,"Resources/","png")

        if event.button() == Qt.MiddleButton:
            self.dragging = True
            self.dragging_pos = event.position().toPoint()
            self.offset = self._imagePosition - self.mousePressPos


        self.update()'''

    def wheelEvent(self, event: QWheelEvent):
        min_scale,max_scale = self.imageScaleRange
        # Get the amount of scrolling
        delta = event.angleDelta().y()
        # Adjust value based on scroll direction
        scale_factor = 1.1  # This determines how quickly the scaling changes
    
        # Logarithmically transform the scale to maintain uniform zoom behavior
        log_min_scale = log(min_scale)
        log_max_scale = log(max_scale)
        
        # Get the amount of scrolling
        delta = event.angleDelta().y()
        
        # Adjust the logarithmic scale factor based on scroll direction
        if delta > 0:
            log_scale = log(self._imageScale) + log(scale_factor)
        else:
            log_scale = log(self._imageScale) - log(scale_factor)
        
        # Clamp the logarithmic scale to the specified range
        log_scale = max(log_min_scale, min(log_max_scale, log_scale))
        
        # Convert back from logarithmic to linear scale
        self._imageScale = exp(log_scale)
        
        self.update()

    """def mouseMoveEvent(self, event):
        self.currentPoint = event.position().toPoint()
        self.lastPoint = self.currentPoint  # Update last point for the next segment

        if self.drawing:
            self.update()
            #self.shapes.append((self._mapToFixedSize(self.lastPoint), self._mapToFixedSize(self.currentPoint)))
            
            
        
        if self.dragging:
            cpos = self._imagePosition
            self.moveCanvas(event.position() + self.offset)

        self.update()  # Request a repaint to finalize the line"""

    """def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False
        
        if event.button() == Qt.MiddleButton:
            self.dragging = False
        
        self.update()"""
    
    