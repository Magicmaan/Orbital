from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QCursor, QIcon, QPainter, QPixmap, QTransform
from PySide6.QtWidgets import (QHBoxLayout, QLabel, QPushButton, QSizePolicy,
                               QWidget,QMenuBar,QMenu)

from GUI.Widgets.WidgetUtils import drawPixelBorder, removePadding
from GUI.Decorators import PixelBorder, sizePolicy


@PixelBorder

class Contextbar(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Contextbar")

        self.program = parent
        self.objheight = 16
        self.icon_size = 24
        self.resize(400, self.objheight)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setLayout(QHBoxLayout())
        self.layout().setObjectName("containerLayout")
        self.layout().setAlignment(Qt.AlignmentFlag.AlignLeft)
        removePadding(self)

        self.setStyleSheet(
            "background:transparent;"
        )

        m = QMenu("Hi")
        m.setTitle("BOOOOOO")
        self.addMenu(m)

        self.setupUi()



    def setupUi(self):
        self.addMenuCust("File")
        self.addMenuCust("Edit")
        self.addMenuCust("Canvas")
        self.addMenuCust("Layer")
        self.FileMenu = QMenu("Select")
        self.FileMenu = QMenu("View")
        self.FileMenu = QMenu("Help")

    def addMenuCust(self,MenuName="default",parentMenu=None,d=0):
        if parentMenu==None:
            parentMenu=self

        temp = QMenu(MenuName)
        setattr(parentMenu,MenuName + "Menu",temp)
        
        
        if d<2:
            self.addMenuCust("Default",temp,d+1)
            self.addMenuCust("Default2",temp,d+1)
        
        parentMenu.addMenu(temp)
        
    
        