from PySide6.QtCore import QEvent, QObject, QPoint, QSize, Qt
from PySide6.QtGui import QCursor, QPainter, QPixmap
from PySide6.QtWidgets import (QApplication, QGridLayout, QMainWindow,
                               QSizePolicy, QWidget)

from GUI.Widgets.titlebar import Titlebar
from GUI.Widgets.WidgetUtils import drawPixelBorder, removePadding
from Utils import *


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

class customWindow(QWidget):
    def __init__(self, parent: QMainWindow):
        super().__init__(parent)
        self.parent = parent
        self.parent.setWindowFlags(Qt.FramelessWindowHint)
        self.parent.setAttribute(Qt.WA_TranslucentBackground)  # Disable default border
        
        self.parent.appContainer.setStyleSheet("background:red;border-radius:0px;")
        self.resize(self.parent.size())
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setObjectName("customWindow")

        self.setLayout(QGridLayout())
        removePadding(self)

        self.parent.appContainer.setContentsMargins(6,8,6,6)  # Add border

        self.customTitleBar()

        # Variables for resizing
        self.dragging = False
        self.dragging_pos = QPoint()
        self.resize_edge_size = 5  # Width of the area where resizing is possible
        self.lastResize = -1

        print("Custom Window Enabled")

        # Install the global event filter
        self.mouse_event_filter = MouseEventFilter(self)
        QApplication.instance().installEventFilter(self.mouse_event_filter)

    def customTitleBar(self):
        # Titlebar init
        self.parent.titlebar = Titlebar(self)
        self.parent.layout.addWidget(self.parent.titlebar)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mouseoffset = self.parent.mapFromGlobal(event.globalPos())
            self.dragging = True

    def mouseMoveEvent(self, event):
        
        
        #if self.dragging: #check if holding down mouse to resize
            

            #return

        tbar = self.parent.titlebar
        pos = tbar.mapFromGlobal(event.globalPos())
        sideHit = self.detectEdge(pos)

        if tbar.rect().contains(pos) and self.dragging and self.lastResize == (-1) :
            self.customDrag(event)
            
        elif self.dragging:
            self.customResize(event,sideHit)
        
    def customResize(self,event,sideHit):
        self.updateCursor(sideHit)
        pos = self.parent.mapFromGlobal(event.globalPos())
        if sideHit[1] or self.lastResize==1: # Right side resize
            self.parent.setFixedWidth(max(pos.x(),self.parent.minSize.width()))
            self.lastResize = 1
        elif sideHit[0] or self.lastResize==0: # Left Side resize
            resizeTo = max(self.parent.width() - (event.globalPos().x() - self.parent.pos().x()),self.parent.minSize.width())
            if resizeTo != self.parent.minSize.width():
                self.parent.setFixedWidth(resizeTo)
                self.parent.move(event.globalPos().x() ,self.parent.pos().y())
                self.lastResize = 0

        if sideHit[3] or self.lastResize==3: # Bottom side resize
            self.parent.setFixedHeight(max(pos.y(),self.parent.minSize.height()))
            self.lastResize = 3

        elif sideHit[2] or self.lastResize==2:  # Top side resize
            resizeTo = max(self.parent.height() - (event.globalPos().y() - self.parent.pos().y()),self.parent.minSize.height())
            print(resizeTo)
            if resizeTo != self.parent.minSize.height():
                self.parent.setFixedHeight(resizeTo)
                self.parent.move(self.parent.pos().x(), event.globalPos().y())
                self.lastResize = 2


    def customDrag(self,event):
        windowPos = self.parent.pos()
        self.parent.move(event.globalPos() - self.mouseoffset)

        self.lastResize = -1

    def mouseReleaseEvent(self, event):
        self.dragging = False
        self.lastResize = -1

    def detectEdge(self,pos):
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
    
    def updateCursor(self, sideHit):
        
        # Determine the position relative to the window
        cursor = QCursor()

        if sideHit[0] or sideHit[1]:
            cursor.setShape(Qt.SizeHorCursor)

        if sideHit[2] or sideHit[3]:
            cursor.setShape(Qt.SizeVerCursor)

        self.setCursor(cursor)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.parent.isMaximized():
                self.parent.showNormal()
            else:
                self.parent.showMaximized()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        
        # Fill the entire widget with a green color
        # Draw edges from the pixmap
        #painter.fillRect(self.rect(),QColor(128,0,128))
        drawPixelBorder(self,painter,QPixmap("Resources/button.png"))
        
        # End painting
        painter.end()

    


class defaultWindow(QWidget):
    def __init__(self, parent: QMainWindow) -> None:
        super().__init__(parent)
        self.parent = parent
        self.parent.titlebar = False
        self.resize(QSize(800,600))
        self.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        self.setObjectName("defaultWindow")
        self.objectName
        self.setContentsMargins(0,0,0,0)

        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)

        print("Default Window Enabled")