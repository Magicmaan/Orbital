
import sys
from os.path import exists
from math import log, exp, floor

from PySide6.QtCore import QPoint, QRect, QSize, QTimerEvent, Signal, Slot, Qt
from PySide6.QtGui import QPainter, QPixmap, QWheelEvent, QColor, QFont, QPen
from PySide6.QtWidgets import QLabel, QSizePolicy, QVBoxLayout, QWidget, QScrollBar, QGridLayout, QSlider, QApplication

from DialogBox import ErrorDialog, SuccessDialog
from GUI.Widgets.WidgetUtils import drawPixelBorder, removePadding
from GUI.Widgets.ScrollBar import CustomScrollBar
from GUI.Widgets.Canvas import Canvas
from Utils import clamp

from GUI.customEvents import *

from GUI.Decorators import PixelBorder, sizePolicy, mouseClick
DEFAULT_IMG = "Resources/default_canvas.png"




@PixelBorder
@mouseClick
class Viewport(QWidget):
    toolClick_S = Signal(toolClickEvent)
    toolRelease_S = Signal(toolReleaseEvent)


    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        
        # Initialize variables
        self.imageScaleRange = (0.25, 50)
        self._imageScale = 1
        self._imagePosition = QPoint(0, 0)
        self.canvas = Canvas("Resources/default_canvas.png")
        self.tileCanvas = [True, True]
        self.tileCanvasRange = 2

        self._canvasSettings = {}
        self._scaleImageCache = None

        self._canvasBorder = 10
        self._canvasAxisBorder = 1
        self._canvasAxisOffset = 4


        #cursor setup for viewport
        self.cursorPos = QPoint(0, 0)
        self.lastcursorPos = QPoint(0, 0)
        

        # Set up widget properties
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMouseTracking(True)

        # Set up layout
        self.setLayout(QGridLayout())
        layout = self.layout()
        removePadding(self)
        layout.setAlignment(Qt.AlignBottom)
        layout.setRowStretch(0, 2)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(6, 6, 6, 6)

        # Connect signals
        self.program = QApplication.instance().program
        self.toolClick_S.connect(self.program.tools.toolAction)
        self.toolRelease_S.connect(self.program.tools.toolReleaseAction)

        

        # Example widget: QLabel on top of the pixmap
        # self.label = QLabel("This is a label on top of the pixmap", self)
        # self.label.setStyleSheet("color: white;")
        # self.label.setStyleSheet("background:transparent;")
        # layout.addWidget(self.label, 0, 1)

        self.update()

    def _scrollVertical(self, value: float) -> None:
        self.moveCanvas(QPoint(self._imagePosition.x(), value))

        self.update()

    def _scrollHorizontal(self, value: float) -> None:
        val = value / 100
        self.moveCanvas(QPoint(self.width() * val, self._imagePosition.y()))

        self.update()

    def getImage(self) -> QPixmap:
        return self.canvas.image

    def addImage(self,img:QPixmap) -> None:
        self.canvas.image.load(img)
        self.canvas.setFixedSize(self.canvas.image.size())

    def _styleViewport(self, image: QPixmap, scale: float) -> QPixmap:
        self._canvasAxisBorder = 1
        self._canvasAxisOffset = 4

        expandedImage = QPixmap(image.width() + self._canvasBorder * 2, image.height() + self._canvasBorder * 2)
        expandedImage.fill(QColor(0, 0, 0, 0))  # Fill with transparent color

        painter = QPainter(expandedImage)
        

        # Styling
        pen = QPen(QColor(255, 255, 255, 125))  # Set the pen color to white with transparency
        pen.setWidth(1)  # Set the pen width
        painter.setPen(pen)

        # Set font and disable aliasing
        font = QFont("pixelated", 6)
        font.setHintingPreference(QFont.PreferNoHinting)
        font.setStyleStrategy(QFont.NoAntialias)
        painter.setFont(font)

        # Draw the border
        painter.drawLine(self._canvasBorder - self._canvasAxisBorder, self._canvasBorder - self._canvasAxisOffset, 
                        expandedImage.width() - self._canvasBorder + self._canvasAxisBorder, self._canvasBorder - self._canvasAxisOffset)
        painter.drawLine(self._canvasBorder - self._canvasAxisOffset, self._canvasBorder - self._canvasAxisBorder, 
                        self._canvasBorder - self._canvasAxisOffset, expandedImage.height() - self._canvasBorder + self._canvasAxisBorder)

        # Center Y marker
        painter.drawPoint(self._canvasBorder - self._canvasAxisOffset + 1, int(expandedImage.height() / 2))
        if expandedImage.height() % 2 == 0:  # If the height is even, draw an extra line
            painter.drawPoint(self._canvasBorder - self._canvasAxisOffset + 1, int(expandedImage.height() / 2) - 1)

        # Center X marker
        painter.drawPoint(int(expandedImage.width() / 2), self._canvasBorder - self._canvasAxisOffset + 1)
        if expandedImage.width() % 2 == 0:  # If the width is even, draw an extra line
            painter.drawPoint(int(expandedImage.width() / 2) - 1, self._canvasBorder - self._canvasAxisOffset + 1)

        # Draw size
        painter.drawText(self._canvasBorder - self._canvasAxisBorder, self._canvasBorder - self._canvasAxisOffset - 1, f"{image.width()}")
        painter.drawText(self._canvasBorder - self._canvasAxisBorder - 6, self._canvasBorder - self._canvasAxisOffset - 1, "X")

        painter.rotate(-90)
        painter.drawText(-(self._canvasBorder + self._canvasAxisOffset + 5), self._canvasBorder - self._canvasAxisOffset - 1, f"{image.height()}")
        painter.rotate(90)

        # Draw the image
        painter.drawPixmap(self._canvasBorder, self._canvasBorder, image)
        painter.end()

        return expandedImage

    def _scaleImageToViewport(self, image: QPixmap, scale: float) -> QPixmap:
        # Create a pixmap for the scaled image
        scaledImage = QPixmap(image.size() * scale)
        scaledImage.fill(QColor(0, 0, 0, 0))

        # Define the source and destination rectangles
        sourceRect = QRect(0, 0, 
                           image.width(), image.height())
        destRect = QRect(0, 0, 
                         int(scaledImage.width()), int(scaledImage.height()))

        # Create a painter for the viewport and draw the scaled image
        painter = QPainter(scaledImage)
        painter.drawPixmap(destRect, image, sourceRect)
        painter.end()
        # Cache the scaled image
        self._scaleImageCache = scaledImage
        return self._scaleImageCache

    def _paintCanvasTiled(self, painter: QPainter):
        canvas = self._scaleImageToViewport(self.getImage(), self._imageScale)
        if all(self.tileCanvas): #tile diagonally
            for x in range(-self.tileCanvasRange, self.tileCanvasRange+1):
                for y in range(-self.tileCanvasRange, self.tileCanvasRange+1):
                    painter.drawPixmap(self._imagePosition.x() + (canvas.width()*x), self._imagePosition.y() + (canvas.height()*y), canvas)
        
        else:
            if self.tileCanvas[0]: #tile Horizontal 
                for x in range(-self.tileCanvasRange, self.tileCanvasRange+1):
                    painter.drawPixmap(self._imagePosition.x() + (canvas.width()*x), self._imagePosition.y(), canvas)

            if self.tileCanvas[1]: #tile Vertical
                for y in range(-self.tileCanvasRange, self.tileCanvasRange+1):
                    painter.drawPixmap(self._imagePosition.x(), self._imagePosition.y() + (canvas.height()*y), canvas)
        
        #draw outline around canvas
        pen = QPen()
        pen.setColor(QColor(0,0,0,255))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawRect(canvas.rect().adjusted(self._imagePosition.x(),self._imagePosition.y(),self._imagePosition.x(),self._imagePosition.y()))
        
    def _paintCanvas(self,painter: QPainter):
        if self.tileCanvas[0] or self.tileCanvas[1]:
            self._paintCanvasTiled(painter)
            return

        canvas = self._styleViewport(self.getImage(),self._imageScale)

        canvas = self._scaleImageToViewport(canvas,self._imageScale)

        #draw outline around canvas
        border = self._canvasBorder * self._imageScale
        c = canvas.copy()
        c = c.rect()
        c.moveTo(self._imagePosition)
        c.adjust(border-2,border-2,-border + 2,-border + 2)
        
        painter.fillRect(c,QColor(0,0,0,255))


        pen = QPen(QColor(0,0,0,55))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawLine(c.bottomLeft()+QPoint(1,2),c.bottomRight()+QPoint(0,2))
        painter.drawLine(c.topRight()+QPoint(2,1),c.bottomRight()+QPoint(2,2))
        
        #draw the canvas to Viewport
        painter.drawPixmap(self._imagePosition.x(), self._imagePosition.y(), canvas)
        
        

    def _paintPixelPosition(self, painter: QPainter):
        # Set the brush and pen for the square
        painter.setBrush(QColor(100, 200, 150))  # Fill color
        painter.setPen(QColor(50, 100, 75))  # Border color     

        img_pos = self._imagePosition
        img_scale = self._imageScale
        

        x = self._mapFromCanvas(self.cursorPos).x()
        y = self._mapFromCanvas(self.cursorPos).y()
        

        #TODO: FIX VIEWING WHEN TILED
        # Bounds check of canvas and draw the square if within bounds
        if (0 <= self.cursorPos.x() < self.canvas.width()) and (0 <= self.cursorPos.y() < self.canvas.height()):
            painter.drawRect(QRect(
                x,
                y,
                img_scale,
                img_scale
            ))

    def _paintViewport(self,painter: QPainter):
        painter.save()
        painter.setPen(QColor(255, 255, 255,125))  # Set the pen color to white

        xPos,yPos = self._imagePosition.x(), self._imagePosition.y()
        font = QFont("pixelated", 16)  # You can specify the font family, size, and weight
        painter.setFont(font)

        #draw filepath
        painter.drawText(xPos+(10*self._imageScale),yPos+20+((self.canvas.height() + 10)*self._imageScale), self.canvas.filepath)

        painter.restore()   

    def paintEvent(self, event):
        painter = QPainter(self)
        
        self._paintCanvas(painter)

        self._paintPixelPosition(painter)

        self._paintViewport(painter)
        
        

        super().paintEvent(event)

    def moveCanvas(self, position: QPoint) -> None:
        """
        Moves the canvas to the specified position.
        """
        size = self.canvas.rect()
        x = position.x()
        y = position.y()
        canvasW = size.width() * self._imageScale
        canvasH = size.height() * self._imageScale

        bSize = 10
        tempx = x
        tempy = y

        if x + (canvasW // 2) < bSize:
            tempx = bSize - (canvasW // 2)
        if x - (canvasW // 2) > self.width() - bSize:
            tempx = self.width() - bSize - canvasW

        if y + (canvasH // 2) < bSize:
            tempy = bSize - (canvasH // 2)
        if y - (canvasH // 2) > self.height() - bSize:
            tempy = self.height() - bSize - canvasH

        self._imagePosition.setX(tempx)
        self._imagePosition.setY(tempy)

    def _mapToCanvas(self, point:QPoint) -> QPoint:
        """
        Maps the viewport coordinates to canvas
        """

        img_pos = self._imagePosition
        img_scale = self._imageScale

        # Calculate position in canvas coordinates
        canvas_x = (point.x() - img_pos.x()) / img_scale - self._canvasBorder
        canvas_y = (point.y() - img_pos.y()) / img_scale - self._canvasBorder

        # Tile cursorpos if tiling is enabled
        if self.tileCanvas[0]:
            canvas_x += self._canvasBorder
            if canvas_x <= self.canvas.width()*(self.tileCanvasRange+1) and canvas_x >= -self.canvas.width()*(self.tileCanvasRange):
                canvas_x = canvas_x % self.canvas.width()
        if self.tileCanvas[1]:
            canvas_y += self._canvasBorder
            if canvas_y <= self.canvas.height()*(self.tileCanvasRange+1) and canvas_y >= -self.canvas.height()*(self.tileCanvasRange):
                canvas_y = canvas_y % self.canvas.height()

        # Return the mapped QPoint
        return QPoint(int(canvas_x), int(canvas_y))

    def _mapFromCanvas(self, point:QPoint) -> QPoint:
        """
        Map the canvas coordinates to the viewport
        """

        img_pos = self._imagePosition
        img_scale = self._imageScale

        # Calculate position in viewport coordinates
        viewport_x = point.x() * img_scale + img_pos.x() + (self._canvasBorder * img_scale)
        viewport_y = point.y() * img_scale + img_pos.y() + (self._canvasBorder * img_scale)

        # Tile cursorpos if tiling is enabled
        if self.tileCanvas[0]:
            viewport_x -= (self._canvasBorder * img_scale)
            
        if self.tileCanvas[1]:
            viewport_y -= (self._canvasBorder * img_scale)
            

        # Return the mapped QPoint
        return QPoint(int(viewport_x), int(viewport_y))

    def toolClick(self):
        custom_data = toolClickEvent(self.cursorPos,self.lastcursorPos,self.getImage())

        self.toolClick_S.emit(custom_data)
        
        #self.program.tools.onAction(self.cursorPos)

    @Slot(openFileCustEvent)
    def openFile(self, value:openFileCustEvent):
        self.addImage(value.file)

    #Mouse Events
    #--------------------------------------------------------------------------
    def onMouseClick(self):
        self.lastcursorPos = self._mapToCanvas(self.mousePos)
        self.cursorPos = self._mapToCanvas(self.mousePos) 

        if self.mouseClicks.left:
            self.toolClick()

        if self.mouseClicks.right:
            self._imageScale += 0.1
        
        if self.mouseClicks.middle:
            self.offset = self._imagePosition - self.mousePressPos
            self.moveCanvas(self.mousePos + self.offset)
        
    def onMouseMove(self):
        self.lastcursorPos = self.cursorPos
        self.cursorPos = self._mapToCanvas(self.mousePos)

        if self.mouseClicks.left:
            self.toolClick()
        
        if self.mouseClicks.middle:
            self.moveCanvas(self.mousePos + self.offset)

    def onMouseRelease(self):

        custom_data = toolClickEvent(self.cursorPos,self._mapToCanvas(self.mousePressPos),self.getImage())
        self.toolRelease_S.emit(custom_data)

    def wheelEvent(self, event: QWheelEvent):
        """
        Handles the mouse wheel event for zooming in and out.
        Adjusts the image position only if the mouse position is within the imagePixmap bounds.
        """

        min_scale, max_scale = self.imageScaleRange
        delta = event.angleDelta().y()
        zoomFactor = 1.1  # This determines how quickly the scaling changes

        log_min_scale = log(min_scale)
        log_max_scale = log(max_scale)

        if delta > 0:
            log_scale = log(self._imageScale) + log(zoomFactor)
        else:
            log_scale = log(self._imageScale) - log(zoomFactor)

        log_scale = max(log_min_scale, min(log_max_scale, log_scale))


        image_rect = self._scaleImageCache.rect().translated(self._imagePosition)
        if image_rect.contains(self.mousePos):
            image_pos_before_zoom = (self.mousePos - self._imagePosition) / self._imageScale
            self._imageScale = exp(log_scale)
            self._imagePosition = self.mousePos - image_pos_before_zoom * self._imageScale
        else:
            self._imageScale = exp(log_scale)
        
        self.update()
    