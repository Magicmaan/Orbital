from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QFontDatabase, QIcon, QPainter, QPixmap
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QMainWindow,
                               QSizePolicy, QVBoxLayout, QWidget)

from CustomWindow import customWindow, defaultWindow
from DiscordPresence import *
from GUI.Widgets.CanvasWindow import Viewport
from GUI.Widgets.Toolbar import Toolbar
from GUI.Widgets.Contextbar import Contextbar
from GUI.Widgets.WidgetUtils import removePadding
from GUI.Widgets.ColourPicker import RGBSpectrumWidget
from Utils import getFont

from GUI.Widgets.Decorators import PixelBorder,sizePolicy

@PixelBorder
class pixelWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.bscale = 2
    
    def paintEvent(self, event):

        super().paintEvent(event)

class mainGUIHandler:
    def __init__(self,program,parentWindow) -> None:
        self.program = program
        self.parentWindow = parentWindow
        self.parentWindowLayout = parentWindow.layout()

        


        centerContainer = QWidget(self.program)
        centerContainer.setStyleSheet("background:rgb(200,200,200);border-radius:0px;")
        centerContainer.resize(QSize(800,600))
        centerContainer.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)

        centerContainerLayout = QGridLayout(centerContainer)
        centerContainerLayout.setContentsMargins(2,2,2,2)
        centerContainerLayout.setSpacing(5)

        self.parentWindowLayout.addWidget(centerContainer,1,0)
        self.parentWindowLayout.setRowStretch(0,1)
        self.parentWindowLayout.setColumnStretch(0,1)

        leftBar = pixelWidget()
        leftBar.setFixedWidth(200)
        leftBar.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Expanding)
        leftBar.setLayout(QVBoxLayout())
        removePadding(leftBar)

       
        centerContainerLayout.addWidget(leftBar,1,0)


        centerContainerLayout.addWidget(Toolbar(self.program),0,1)
        
        
        #Create and configure the Canvas widget
        self.canvas = Viewport()
        #self.canvas.setStyleSheet("border: purple 5px solid;")
        # Add the Canvas widget to the layout
        centerContainerLayout.addWidget(self.canvas,1,1)
        
        centerContainerLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        

        RightBar = pixelWidget()
        RightBar.setFixedWidth(200)
        RightBar.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Expanding)
        RightBar.setLayout(QVBoxLayout())
        removePadding(RightBar)

        #   RightBar.layout().addWidget(QLabel("Hi    "))
        centerContainerLayout.addWidget(RightBar,1,2)
        centerContainerLayout.setRowStretch(2,1)
        
        
        cl = centerContainerLayout
        cl.setRowStretch(1,1)
        cl.setColumnStretch(1,2)

        nbar = pixelWidget()    
        nbar.resize(128,128)
        nbar.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        nbar.setLayout(QGridLayout())
        removePadding(nbar)
        #   RightBar.layout().addWidget(QLabel("Hi    "))
        centerContainerLayout.addWidget(nbar,2,0)
        centerContainerLayout.setColumnStretch(0,1)
        col = RGBSpectrumWidget()
        nbar.layout().setAlignment(Qt.AlignmentFlag.AlignCenter)
        nbar.layout().addWidget(col,0,0)
    
    def leftBarInit(self):
        pass

    def toolBarInit(self):
        pass

    def rightBarInit(self):
        pass
    