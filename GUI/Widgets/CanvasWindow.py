
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
        self.program = QApplication.instance().program

        config = self.program.getConfig().viewport
        self.config = config

        #apply config to class
        for key, value in self.config.items():
            setattr(self, key, value)

        
        self.border_color = QColor()
        self.border_color.setNamedColor(config["border_colour"])
        self.border_thickness = config["border_thickness"]


        #initalise canvas view variables
        self.image_scale = config["scale_default"]
        self.image_scale_range = (config["scale_range_min"], config["scale_range_max"])
        self.image_scale_step = config["scale_step"]
        self.image_position = QPoint(0, 0)

        self.canvas = Canvas("Resources/default_canvas.png")


        self._canvasSettings = {}
        self._scaleImageCache = None

        self._canvas_padding = 10
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
        
        self.toolClick_S.connect(self.program.tools.toolAction)
        self.toolRelease_S.connect(self.program.tools.toolReleaseAction)

        

        # Example widget: QLabel on top of the pixmap
        # self.label = QLabel("This is a label on top of the pixmap", self)
        # self.label.setStyleSheet("color: white;")
        # self.label.setStyleSheet("background:transparent;")
        # layout.addWidget(self.label, 0, 1)

        self.update()

    def _scrollVertical(self, value: float) -> None:
        self.moveCanvas(QPoint(self.image_position.x(), value))

        self.update()

    def _scrollHorizontal(self, value: float) -> None:
        val = value / 100
        self.moveCanvas(QPoint(self.width() * val, self.image_position.y()))

        self.update()

    def getImage(self) -> QPixmap:
        return self.canvas.image

    def addImage(self,img:QPixmap) -> None:
        self.canvas.image.load(img)
        self.canvas.setFixedSize(self.canvas.image.size())

    

    def _drawCanvasSize(self, image: QPixmap, painter: QPainter):
        if not self.show_size:
            return

        painter.drawText(self._canvas_padding - self._canvasAxisBorder, self._canvas_padding - self._canvasAxisOffset - 1, f"{image.width()}")
        painter.drawText(self._canvas_padding - self._canvasAxisBorder - 6, self._canvas_padding - self._canvasAxisOffset - 1, "X")
        painter.rotate(-90)
        painter.drawText(-(self._canvas_padding + self._canvasAxisOffset + 5), self._canvas_padding - self._canvasAxisOffset - 1, f"{image.height()}")
        painter.rotate(90)


    def _drawCanvasAxis(self, image, painter: QPainter):
        # Draw the border
        if not self.show_axis:
            return
        
        painter.drawLine(self._canvas_padding - self._canvasAxisBorder, self._canvas_padding - self._canvasAxisOffset, 
                        image.width() - self._canvas_padding + self._canvasAxisBorder, self._canvas_padding - self._canvasAxisOffset)
        painter.drawLine(self._canvas_padding - self._canvasAxisOffset, self._canvas_padding - self._canvasAxisBorder, 
                        self._canvas_padding - self._canvasAxisOffset, image.height() - self._canvas_padding + self._canvasAxisBorder)

        # Center Y marker
        painter.drawPoint(self._canvas_padding - self._canvasAxisOffset + 1, int(image.height() / 2))
        if image.height() % 2 == 0:  # If the height is even, draw an extra line
            painter.drawPoint(self._canvas_padding - self._canvasAxisOffset + 1, int(image.height() / 2) - 1)
        # Center X marker
        painter.drawPoint(int(image.width() / 2), self._canvas_padding - self._canvasAxisOffset + 1)
        if image.width() % 2 == 0:  # If the width is even, draw an extra line
            painter.drawPoint(int(image.width() / 2) - 1, self._canvas_padding - self._canvasAxisOffset + 1)

    def _drawCanvasFilepath(self, painter: QPainter, image:QPixmap):
        if not self.show_filepath:
            return
        painter.save()

        font = QFont("pixelated", 16)  # You can specify the font family, size, and weight
        painter.setFont(font)

        painter.setPen(QColor(255, 255, 255,125))  # Set the pen color to white
        xpos = self.image_position.x() + (10*self.image_scale)
        ypos = self.image_position.y() + 20 + ((self.canvas.height() + 10)*self.image_scale)

        
        if self.tile_x:
            xpos -= self.tiling_range * image.width()
        if self.tile_y:
            ypos += self.tiling_range * image.height()
                
        painter.drawText(xpos,
                         ypos, 
                         self.canvas.filepath)

        painter.restore()
    
    def _drawCanvasBorder(self, painter: QPainter, canvas: QPixmap):
        if not self.show_border:
            return

        offset = self._canvas_padding * self.image_scale

        rects = []

        inner_rect = canvas.rect()
        inner_rect = inner_rect.adjusted(offset, offset, -offset, -offset)
        inner_rect.adjust(self.image_position.x(), self.image_position.y(), self.image_position.x(), self.image_position.y())
        
        if self.tile_x or self.tile_y:
            inner_rect.adjust(-offset, -offset, offset, offset)
            outer_rect = inner_rect.adjusted(0,0,0,0)

            if self.tile_x:
                outer_rect.adjust(-self.tiling_range * canvas.width(), 0, self.tiling_range * canvas.width(), 0)
                
            if self.tile_y:
                outer_rect.adjust(0, -self.tiling_range * canvas.height(), 0, self.tiling_range * canvas.height())  
            
            rects.append(outer_rect)


        rects.append(inner_rect)
        # Set the pen color and width
        pen = QPen(self.border_color)
        pen.setWidth(self.border_thickness)
        painter.setPen(pen)
        # Draw the border
        painter.drawRects(rects)
    


    def _styleViewport(self, image: QPixmap, scale: float) -> QPixmap:
        """Apply styling to canvas at its scale"""
        expandedImage = QPixmap(image.width() + self._canvas_padding * 2, image.height() + self._canvas_padding * 2)
        expandedImage.fill(QColor(0, 0, 0, 0))  # Fill with transparent color
        painter = QPainter(expandedImage)

        # Set font and disable aliasing
        font = QFont("pixelated", 6)
        font.setHintingPreference(QFont.PreferNoHinting)
        font.setStyleStrategy(QFont.NoAntialias)
        painter.setFont(font)
        # Styling
        pen = QPen(QColor(255, 255, 255, 125))  # Set the pen color to white with transparency
        pen.setWidth(1)  # Set the pen width
        painter.setPen(pen)
        

        # draw the canvas Axis
        self._drawCanvasAxis(image, painter)
        # Draw the canvas size
        self._drawCanvasSize(image, painter)
        
        # Draw the image
        painter.drawPixmap(self._canvas_padding, self._canvas_padding, image)
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
        canvas = self._scaleImageToViewport(self.getImage(), self.image_scale)
        
        # draws the canvas to the viewport multiple, multiple times
        if self.tile_x and self.tile_y: #tile into a large square
            for x in range(-self.tiling_range, self.tiling_range+1):
                for y in range(-self.tiling_range, self.tiling_range+1):
                    painter.drawPixmap(self.image_position.x() + (canvas.width()*x), self.image_position.y() + (canvas.height()*y), canvas)
        
        #case for only axis tiling
        else:
            if self.tile_x: #tile Horizontal 
                for x in range(-self.tiling_range, self.tiling_range+1):
                    painter.drawPixmap(self.image_position.x() + (canvas.width()*x), self.image_position.y(), canvas)

            if self.tile_y: #tile Vertical
                for y in range(-self.tiling_range, self.tiling_range+1):
                    painter.drawPixmap(self.image_position.x(), self.image_position.y() + (canvas.height()*y), canvas)
        
        #draw border around canvas
        self._drawCanvasBorder(painter, canvas)

        #draw the filepath
        self._drawCanvasFilepath(painter, canvas)

    

    def _paintCanvas(self,painter: QPainter):
        if self.tile_x or self.tile_y:
            self._paintCanvasTiled(painter)
            return
        #style canvas at its native scale
        canvas = self._styleViewport(self.getImage(),self.image_scale) 

        canvas = self._scaleImageToViewport(canvas,self.image_scale) #scale to viewport
        
        #draw the canvas to Viewport
        painter.drawPixmap(self.image_position.x(), self.image_position.y(), canvas)

        #draw border around canvas
        self._drawCanvasBorder(painter, canvas)
        
        #draw the filepath
        self._drawCanvasFilepath(painter, canvas)
        
        

    def _paintPixelPosition(self, painter: QPainter):
        # Set the brush and pen for the square
        painter.setBrush(self.program.colourPicker.getRGBA())  # Fill color
        painter.setPen(QColor(0,0,0,0))  # Border color     

        img_pos = self.image_position
        img_scale = self.image_scale
        

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
        pass

    def paintEvent(self, event):
        painter = QPainter(self)
        
        self._paintCanvas(painter)

        self._paintPixelPosition(painter)

        self._paintViewport(painter)
        
        painter.end()

        super().paintEvent(event)

    def moveCanvas(self, position: QPoint) -> None:
        """
        Moves the canvas to the specified position.
        """
        size = self.canvas.rect()
        x = position.x()
        y = position.y()
        canvasW = size.width() * self.image_scale
        canvasH = size.height() * self.image_scale

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

        self.image_position.setX(tempx)
        self.image_position.setY(tempy)

    def _mapToCanvas(self, point:QPoint) -> QPoint:
        """
        Maps the viewport coordinates to canvas
        """

        img_pos = self.image_position
        img_scale = self.image_scale

        # Calculate position in canvas coordinates
        canvas_x = (point.x() - img_pos.x()) / img_scale - self._canvas_padding
        canvas_y = (point.y() - img_pos.y()) / img_scale - self._canvas_padding

        # Tile cursorpos if tiling is enabled
        if self.tile_x:
            canvas_x += self._canvas_padding
            if canvas_x <= self.canvas.width()*(self.tiling_range+1) and canvas_x >= -self.canvas.width()*(self.tiling_range):
                canvas_x = canvas_x % self.canvas.width()
        if self.tile_y:
            canvas_y += self._canvas_padding
            if canvas_y <= self.canvas.height()*(self.tiling_range+1) and canvas_y >= -self.canvas.height()*(self.tiling_range):
                canvas_y = canvas_y % self.canvas.height()

        # Return the mapped QPoint
        return QPoint(int(canvas_x), int(canvas_y))

    def _mapFromCanvas(self, point:QPoint) -> QPoint:
        """
        Map the canvas coordinates to the viewport
        """

        img_pos = self.image_position
        img_scale = self.image_scale

        # Calculate position in viewport coordinates
        viewport_x = point.x() * img_scale + img_pos.x() + (self._canvas_padding * img_scale)
        viewport_y = point.y() * img_scale + img_pos.y() + (self._canvas_padding * img_scale)

        # Tile cursorpos if tiling is enabled
        if self.tile_x:
            viewport_x -= (self._canvas_padding * img_scale)
            
        if self.tile_x:
            viewport_y -= (self._canvas_padding * img_scale)
            

        # Return the mapped QPoint
        return QPoint(int(viewport_x), int(viewport_y))

    def toggleTiling(self,x:bool=None,y:bool=None) -> list[bool]:
        """if x=True, will toggle x, if y=True, will toggle y
           returns the current tiling state of the canvas
        """
        if x and y: #if both, just either turn all on or off
            if self.tile_x or self.tile_y:
                self.tile_x,self.tile_y = False,False
            else:
                self.tile_x,self.tile_y = True,True
        elif x: #if toggle x
            self.tile_x = not self.tile_x
        elif y: #if toggle y
            self.tile_y = not self.tile_y

        self.update()

        return (self.tile_x,self.tile_y)

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
            self.image_scale += 0.1
        
        if self.mouseClicks.middle:
            self.offset = self.image_position - self.mousePressPos
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

        min_scale, max_scale = self.image_scale_range
        delta = event.angleDelta().y()
        zoomFactor = 1.1  # This determines how quickly the scaling changes

        log_min_scale = log(min_scale)
        log_max_scale = log(max_scale)

        if delta > 0:
            log_scale = log(self.image_scale) + log(zoomFactor)
        else:
            log_scale = log(self.image_scale) - log(zoomFactor)

        log_scale = max(log_min_scale, min(log_max_scale, log_scale))


        image_rect = self._scaleImageCache.rect().translated(self.image_position)
        if image_rect.contains(self.mousePos):
            image_pos_before_zoom = (self.mousePos - self.image_position) / self.image_scale
            self.image_scale = exp(log_scale)
            self.image_position = self.mousePos - image_pos_before_zoom * self.image_scale
        else:
            self.image_scale = exp(log_scale)
        
        self.update()
    