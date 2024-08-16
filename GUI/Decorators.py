from functools import wraps
from PySide6.QtCore import QEvent, QObject, QPoint, QSize, Qt
from PySide6.QtGui import QPainter, QPixmap, QPainter, QColor, QBitmap
from PySide6.QtWidgets import (QApplication, QGridLayout, QMainWindow,
                               QSizePolicy, QWidget)

from GUI.Widgets.WidgetUtils import drawPixelBorder,removePadding
from Utils import dictAllFalse, DotDict

def PixelBorder(cls):
    # Wrap the paintEvent method
    original_paint_event = cls.paintEvent
    original_resize_event = cls.resizeEvent

    if not hasattr(cls,"pixelBorderPath"):
        cls.pixelBorderPath = "Resources/button.png"
    
    if not hasattr(cls,"_pixelBorderCache"):
        cls._pixelBorderCache = None
    
    if not hasattr(cls,"pixelBorderFill"):
        cls.pixelBorderFill = True

    def _generatePixelBorder(self):
        width = self.width()
        height = self.height()
        pmap = QPixmap(QSize(width,height))

        painter = QPainter(pmap)

        drawPixelBorder(pmap, painter,QPixmap(self.pixelBorderPath),3,2,self.pixelBorderFill)

        self._pixelBorderCache = pmap

    def modified_paint_event(self, event):
        painter = QPainter(self)
        #if no cache, generate
        if not self._pixelBorderCache:
            self._generatePixelBorder()

        # Draw the pixmap using the mask
        painter.drawPixmap(QPoint(0, 0), self._pixelBorderCache)


        # Call the original paintEvent
        original_paint_event(self, event)

    def modified_resize_event(self, event):
        #on resize, need to remake pixel border to fit size
        #if event.oldSize() != event.size():
        self._generatePixelBorder()
        original_resize_event(self, event)



    cls.paintEvent = modified_paint_event
    cls.resizeEvent = modified_resize_event
    cls._generatePixelBorder = _generatePixelBorder

    return cls


def mouseClick(cls):

    # Add mouse tracking attributes
    if not hasattr(cls, 'mouseClicks'):
        cls.mouseClicks = DotDict(
            left=   False,
            right=  False,
            middle= False
        )
    
    if not hasattr(cls, 'mousePos'):
        cls.mousePos = QPoint(0,0)

        cls.mousePressPos = QPoint(0,0)

        cls.mouseReleasePos = QPoint(0,0)

    if not hasattr(cls, 'mouseHistory'):
        cls._mouseHistory = False
    
    #original event
    original_mouse_press_event = cls.mousePressEvent
    original_mouse_move_event = cls.mouseMoveEvent
    original_mouse_release_event = cls.mouseReleaseEvent


    def customMousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mouseClicks.left = True
        elif event.button() == Qt.RightButton:
            self.mouseClicks.right = True
        elif event.button() == Qt.MiddleButton:
            self.mouseClicks.middle = True
        
        self.mousePos = event.position().toPoint()
        self.mousePressPos = event.position().toPoint()
        
        if hasattr(self,"onMouseClick"):
            self.onMouseClick()

        original_mouse_press_event(self, event)

        self.update()

    
    def customMouseMoveEvent(self, event):
        #if self.hasMouseTracking():
        self.mousePos = event.position().toPoint()
        
        if hasattr(self,"onMouseMove"):
            self.onMouseMove()

        original_mouse_move_event(self, event)

        self.update()

    
    def customMouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mouseClicks.left = False

        elif event.button() == Qt.RightButton:
            self.mouseClicks.right = False

        elif event.button() == Qt.MiddleButton:
            self.mouseClicks.middle = False
        
        self.mousePos = event.position().toPoint()
        self.mouseReleasePos = event.position().toPoint()

        if hasattr(self,"onMouseRelease"):
            self.onMouseRelease()

        original_mouse_release_event(self, event)

        self.update()
    
    def clickHandler(self):
        #redirect to prettified stuff cus im stupid frankly
        if hasattr(self,"onMouseClick"):
            self.onMouseClick()
        
        

        
        
        self.update()

    cls.mousePressEvent = customMousePressEvent
    cls.mouseMoveEvent = customMouseMoveEvent
    cls.mouseReleaseEvent = customMouseReleaseEvent
    cls.clickHandler = clickHandler

    return cls



def sizePolicy(xPolicy, yPolicy):
    valid_Policy = {"expanding" : QSizePolicy.Expanding,
            "fixed" : QSizePolicy.Fixed,

            }
    def decorator(cls):
        original_init = cls.__init__

        @wraps(original_init)
        def new_init(self, *args, **kwargs):
            original_init(self, *args, **kwargs)

            if xPolicy in valid_Policy and yPolicy in valid_Policy:
                # Apply the size policy (Expanding by default)
                self.setSizePolicy(valid_Policy[xPolicy], valid_Policy[yPolicy])
            else:
                self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        cls.__init__ = new_init
        return cls

    return decorator
