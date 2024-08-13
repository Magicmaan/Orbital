
import sys
from os.path import exists
from math import log, exp

from PySide6.QtCore import QPoint, QRect, QSize, Qt
from PySide6.QtGui import QPainter, QPixmap, QWheelEvent, QColor
from PySide6.QtWidgets import QLabel, QSizePolicy, QVBoxLayout, QWidget, QScrollBar

from DialogBox import ErrorDialog, SuccessDialog
from GUI.Widgets.WidgetUtils import drawPixelBorder, removePadding
from GUI.Widgets.ScrollBar import CustomScrollBar
from GUI.Widgets.Canvas import Canvas
from Utils import clamp
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
    
from GUI.Decorators import PixelBorder, sizePolicy



@PixelBorder
class Viewport(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setMouseTracking(True)
        sX, sY = 128, 128
        self.fixed_size = QSize(sX, sY)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
       
        self.imageScaleRange = (0.25, 50)
        self._imageScale = 1
        self._imagePosition = QPoint(0, 0)
        #self.canvas = 
        self.canvas = Canvas("Resources/default_canvas.png")
        #["canvas_name"] : (canvas, scale, etc)
        self._canvasSettings = {    }
        self._canvasCache = {}
        


        self.shapes = []
        self.drawing = False
        self.lastPoint = QPoint()
        self.currentPoint = QPoint()
        self.dragging = False
        
        self.cursorPos = QPoint(0,0)
        self.snapCursor = False

        self.pixmap = QPixmap(self.fixed_size)
        

        self.setLayout(QVBoxLayout())
        layout = self.layout()
        removePadding(self)

        self.setContentsMargins(2,2,2,2)


        # Example widget: QLabel on top of the pixmap
        self.label = QLabel("This is a label on top of the pixmap", self)
        self.label.setStyleSheet("color: white;")
        self.label.setStyleSheet("background:transparent;")
        layout.addWidget(self.label, alignment=Qt.AlignTop)

        # Create a vertical QScrollBar
        scroll_vert = CustomScrollBar(Qt.Vertical)
        scroll_vert.setRange(0, self.height())
        scroll_vert.setValue(0)
        scroll_vert.valueChanged.connect(self.scrollVertical)
        layout.addWidget(scroll_vert)

        # Create a vertical QScrollBar
        scroll_horiz = QScrollBar(self)
        scroll_horiz.setOrientation(Qt.Horizontal)
        scroll_horiz.setRange(0, self.width())
        scroll_horiz.setValue(0)
        scroll_horiz.valueChanged.connect(self.scrollHorizontal)
        layout.addWidget(scroll_horiz)

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


    def addLayer(self):
        pass


    def paintCanvas(self,painter):
        canvas = self.canvas.scaleImageToViewport(self._imageScale)
        #draw the canvas to Viewport
        painter.drawPixmap(self._imagePosition.x(), self._imagePosition.y(), canvas)

    def paintPixelPosition(self,painter):
        # Set the brush and pen for the square
        painter.setBrush(QColor(100, 200, 150))  # Fill color
        painter.setPen(QColor(50, 100, 75))  # Border color     

        imgPos = self._imagePosition
        imgscale = self._imageScale

        # Get the current position in the local coordinate system
        local_pos = self.currentPoint + imgPos
        square_top_left_x = (local_pos.x()-1 - imgPos.x()) // imgscale
        square_top_left_y = (local_pos.y()-1 - imgPos.y()) // imgscale

        cPosX = square_top_left_x-(imgPos.x() // imgscale)
        cPosY = square_top_left_y-(imgPos.y() // imgscale)
        
        

        self.cursorPos = QPoint(cPosX,cPosY)

        # Update label with current square's top-left x-coordinate
        self.label.setText(f"X: {self.cursorPos.x()} \nY: {self.cursorPos.y()}")

        if self.snapCursor:
            cPosX = clamp(cPosX,0,self.canvas.width()-1)
            cPosY = clamp(cPosY,0,self.canvas.height()-1)

        #bounds check of canvas
        if (cPosX >= 0 and cPosX <= self.canvas.width()-1) and (cPosY >= 0 and cPosY <= self.canvas.height()-1):
            painter.drawRect(QRect( (0.5+cPosX *imgscale) +imgPos.x(),
                                    (0.5+cPosY *imgscale) +imgPos.y(),
                                    imgscale,
                                    imgscale))

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


    def _mapToFixedSize(self, point):
        # Map the widget's coordinates to the fixed-size resolution

        return QPoint(int(point.x() * self._imageScale), int(point.y() * self._imageScale))

    def _mapFromFixedSize(self, point):
        # Map the fixed-size coordinates to the widget's coordinate system
        return QPoint(int(point.x() * self._imageScale), int(point.y() * self._imageScale))

    


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.lastPoint = self._mapToFixedSize(event.position().toPoint())
            self.drawing = True
            self._imageScale = max(0.1, self._imageScale - 0.1)  # Ensure the scale is not zero or negative

        if event.button() == Qt.RightButton:
            self._imageScale += 0.1
            #exportTexture(self.image,"Resources/","png")

        if event.button() == Qt.MiddleButton:
            self.dragging = True
            self.dragging_pos = event.position().toPoint()
            self.offset = self._imagePosition - self.dragging_pos


        self.update()

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

    def mouseMoveEvent(self, event):
        self.currentPoint = event.position().toPoint()
        self.lastPoint = self.currentPoint  # Update last point for the next segment

        if self.drawing:
            self.shapes.append((self._mapToFixedSize(self.lastPoint), self._mapToFixedSize(self.currentPoint)))
            
            
        
        if self.dragging:
            cpos = self._imagePosition
            self.moveCanvas(event.position() + self.offset)

        self.update()  # Request a repaint to finalize the line

    

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False
        
        if event.button() == Qt.MiddleButton:
            self.dragging = False
    
    