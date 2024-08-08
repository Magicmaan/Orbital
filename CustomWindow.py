from PySide6.QtCore import *
from PySide6.QtCore import Qt
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtWidgets import QWidget


from GUI.Widgets.titlebar import Titlebar

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
        self.parent.appContainer.setContentsMargins(2, 2, 2, 2)  # Add border
        self.parent.appContainer.setStyleSheet("background:red;border-radius:0px;")

        self.resize(self.parent.size())
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setObjectName("customWindow")

        self.setContentsMargins(0, 0, 0, 0)
        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.customTitleBar()

        # Variables for resizing
        self.dragging = False
        self.dragging_pos = QPoint()
        self.resize_edge_size = 5  # Width of the area where resizing is possible

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
            self.dragging_pos = event.globalPos()
            self.dragging = True

    def mouseMoveEvent(self, event):
        pos = self.parent.mapFromGlobal(event.globalPos())
        sideHit = self.detectEdge(pos)
        print(sideHit)
        if self.dragging: #check if holding down mouse
            if sideHit[1] or self.lastResize==1:
                self.parent.setFixedWidth(pos.x())
                self.lastResize = 1
            elif sideHit[0] or self.lastResize==0:
                self.parent.setFixedWidth(self.parent.width() - (event.globalPos().x() - self.parent.pos().x()))
                self.parent.move(event.globalPos().x() ,self.parent.pos().y())
                self.lastResize = 0
            if sideHit[3] or self.lastResize==3:
                self.parent.setFixedHeight(pos.y())
                self.lastResize = 3
            elif sideHit[2] or self.lastResize==2:  # Assuming sideHit[2] now indicates a hit on the top side
                self.parent.setFixedHeight(self.parent.height() - (event.globalPos().y() - self.parent.pos().y()))
                self.parent.move(self.parent.pos().x(), event.globalPos().y())
                self.lastResize = 2

        self.updateCursor(sideHit)

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