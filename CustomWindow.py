from PySide6.QtCore import QEvent, QObject, QPoint, QSize, Qt
from PySide6.QtGui import QCursor, QPainter, QPixmap
from PySide6.QtWidgets import (QApplication, QGridLayout, QMainWindow,
                               QSizePolicy, QWidget, QVBoxLayout)

from GUI.Widgets.Titlebar import Titlebar
from GUI.Widgets.WidgetUtils import drawPixelBorder, removePadding
from Utils import *

from GUI.Decorators import PixelBorder, sizePolicy


#custom event filter to catch events in entire window
class MouseEventFilter(QObject):
    def __init__(self, custom_window):
        super().__init__()
        self.custom_window = custom_window

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseMove:
            # Pass the event to customWindow's updateCursor method
            self.custom_window.mouseMoveEvent(event)
        elif event.type() == QEvent.MouseButtonPress:
            self.custom_window.mousePressEvent(event)
        elif event.type() == QEvent.MouseButtonRelease:
            self.custom_window.mouseReleaseEvent(event)
        elif event.type() == QEvent.MouseButtonDblClick:
            self.custom_window.mouseDoubleClickEvent(event)

        return super().eventFilter(obj, event)


@PixelBorder
class customWindow(QWidget):
    def __init__(self, parent: QMainWindow=None):
        super().__init__(parent)
        self.parent = QApplication.instance().program
        #setup widget
        self.setObjectName("customWindow")
        self.resize(self.parent.size())
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setLayout(QVBoxLayout())
        self.layout().setAlignment(Qt.AlignmentFlag.AlignCenter)
        removePadding(self)
        self.setContentsMargins(6,6,6,6)  # Add border

        # Install the global event filter
        self.mouse_event_filter = MouseEventFilter(self)
        QApplication.instance().installEventFilter(self.mouse_event_filter)

        
        #setup custom border
        
        self.parent.setWindowFlags(Qt.FramelessWindowHint)
        #self.parent.setAttribute(Qt.WA_TranslucentBackground)  
        self.pixelBorderPath = "Resources/coloured.png"

        # Set the central widget for the MainWindow
        self.parent.setCentralWidget(self)
        

        self.customTitleBar()

        

        # Variables for resizing
        self.dragging = False
        self.mousePressPos = QPoint()
        self.resize_edge_size = 5  # Width of the area where resizing is possible
        self.last_resize = -1

        print("Custom Window Enabled")

    def customTitleBar(self):
        # Titlebar init
        self.titlebar = Titlebar(self)
        self.layout().addWidget(self.titlebar)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mousePressPos = self.parent.mapFromGlobal(event.globalPos())
            self.dragging = True

    def mouseMoveEvent(self, event):
        tbar = self.titlebar
        pos = tbar.mapFromGlobal(event.globalPos())
        sideHit = self._detectEdge(pos)
        if tbar.rect().contains(pos) and tbar.rect().contains(self.mousePressPos) and self.dragging and self.last_resize == (-1):
            self.customDrag(event,sideHit)
            
        elif self.dragging and (any(self._detectEdge(self.mousePressPos)) or self.last_resize!=-1):
            self.customResize(event,sideHit)
        
    def customResize(self,event,sideHit):
        if self.isMaximised():
            return

        self._updateCursor(sideHit)

        pos = self.parent.mapFromGlobal(event.globalPos())
        if sideHit[1] or self.last_resize==1: # Right side resize
            self.parent.setFixedWidth(max(pos.x(),self.parent.min_size.width()))
            self.last_resize = 1
        elif sideHit[0] or self.last_resize==0: # Left Side resize
            resizeTo = max(self.parent.width() - (event.globalPos().x() - self.parent.pos().x()),self.parent.min_size.width())
            if resizeTo != self.parent.min_size.width():
                self.parent.setFixedWidth(resizeTo)
                self.parent.move(event.globalPos().x() ,self.parent.pos().y())
                self.last_resize = 0

        if sideHit[3] or self.last_resize==3: # Bottom side resize
            self.parent.setFixedHeight(max(pos.y(),self.parent.min_size.height()))
            self.last_resize = 3

        elif sideHit[2] or self.last_resize==2:  # Top side resize
            resizeTo = max(self.parent.height() - (event.globalPos().y() - self.parent.pos().y()),self.parent.min_size.height())
            print(resizeTo)
            if resizeTo != self.parent.min_size.height():
                self.parent.setFixedHeight(resizeTo)
                self.parent.move(self.parent.pos().x(), event.globalPos().y())
                self.last_resize = 2

    def customDrag(self,event,sideHit):
        if self.isMaximised():
            self.toggleMaximiseWindow()

        self._updateCursor(sideHit)
        self.parent.move(event.globalPos() - self.mousePressPos)

        self.last_resize = -1

    def toggleMaximiseWindow(self):
        if self.isMaximised():
            self.parent.setWindowState(self.parent.windowState() ^ Qt.WindowState.WindowNoState)
            self.parent.setFixedSize(QSize(500,500))
        else:
            self.parent.setWindowState(self.parent.windowState() ^ Qt.WindowState.WindowMaximized)
    
    def isMaximised(self):
        if self.parent.windowState() == Qt.WindowState.WindowMaximized:
            return True
        return False

    def mouseReleaseEvent(self, event):
        self.dragging = False
        self.last_resize = -1

    def _detectEdge(self,pos):
        Left,Right,Top,Bot = False,False,False,False
        #edge detection for resize app
        if pos.x() <= self.resize_edge_size: #left edge
            Left = True
        if pos.x() >= self.parent.width() - self.resize_edge_size:
            Right = True
        if pos.y() <= self.resize_edge_size:
            Top = True
        if pos.y() >= self.parent.height() - self.resize_edge_size:
            Bot = True

        return Left,Right,Top,Bot
    
    def _updateCursor(self, sideHit):
        # Determine the position relative to the window
        cursor = QCursor()
        cursor.setShape(Qt.CursorShape.CrossCursor)

        if sideHit[0] or sideHit[1]:
            cursor.setShape(Qt.SizeHorCursor)

        if sideHit[2] or sideHit[3]:
            cursor.setShape(Qt.SizeVerCursor)

        self.setCursor(cursor)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            tbar = self.titlebar
            pos = tbar.mapFromGlobal(event.globalPos())
            if tbar.rect().contains(pos)and self.last_resize == (-1):
                if self.parent.isMaximized():
                    self.parent.showNormal()
                else:
                    self.parent.showMaximized()
    
    
class defaultWindow(QWidget):
    def __init__(self, parent: QMainWindow) -> None:
        super().__init__(parent)
        self.parent = parent
        config = parent.config
        self.setObjectName("defaultWindow")

        self.parent.titlebar = False
        self.resize(self.parent.size())
        self.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        

        self.setLayout(QVBoxLayout())

        #setup window
        self.setWindowTitle(f"{config.window['title']} {config.version}")
        self.parent.setWindowIcon(QPixmap(config.window["icon_path"]))
        removePadding(self)

        print("Default Window Enabled")