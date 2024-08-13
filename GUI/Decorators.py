from functools import wraps
from PySide6.QtCore import QEvent, QObject, QPoint, QSize, Qt
from PySide6.QtGui import QPainter, QPixmap, QPainter, QColor, QBitmap
from PySide6.QtWidgets import (QApplication, QGridLayout, QMainWindow,
                               QSizePolicy, QWidget)

from GUI.Widgets.WidgetUtils import drawPixelBorder,removePadding

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
