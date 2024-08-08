from PySide6.QtCore import *
from PySide6.QtCore import Qt
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtWidgets import QWidget


from GUI.Widgets.titlebar import Titlebar

from Utils import *

class customWindow(QWidget):
    def __init__(self, parent: QMainWindow):
        super().__init__(parent)
        self.parent = parent
        self.parent.setWindowFlags(Qt.FramelessWindowHint)
        self.parent.setAttribute(Qt.WA_TranslucentBackground) #disable default border
        
        self.resize(self.parent.size())
        self.window.setSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.MinimumExpanding)
        self.setObjectName("customWindow")

        self.setContentsMargins(0,0,0,0)
        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)
        self.customTitleBar()

        self.setStyleSheet("background:green;")
        print("Custom Window Enabled")

    def customTitleBar(self):
        #titlebar init
        self.parent.titlebar = Titlebar(self)
        self.layout.addWidget(self.parent.titlebar,0,0)

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