from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QFontDatabase, QIcon, QPainter, QPixmap
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QMainWindow,
                               QSizePolicy, QVBoxLayout, QWidget)

from CustomWindow import customWindow, defaultWindow
from DiscordPresence import *
from GUI.Widgets.CanvasWindow import Viewport
from GUI.Widgets.Toolbar import Toolbar
from GUI.Widgets.Contextbar import Contextbar
from GUI.Widgets.ToolHandler import ToolHandler
from GUI.Widgets.ColourPicker import ColourPicker
from GUI.Widgets.WidgetUtils import drawPixelBorder, removePadding
from Utils import getFont


class pixelWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.border = "Resources/button.png"
    
    def paintEvent(self, event):
        painter = QPainter(self)
        
        # Fill the entire widget with a green color
        # Draw edges from the pixmap
        drawPixelBorder(self,painter,QPixmap(self.border))
        
        # End painting
        #painter.end()
        super().paintEvent(event)

class Program(QMainWindow):
    def __init__(self, useCustomWindow=False,parent=None) -> None:
        super().__init__(parent)
        #create reference accessible from program
        QApplication.instance().program = self

        self.app = QApplication.instance()
        self.setMouseTracking(True)
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)

        self.minSize = QSize(650,650)
        #setup window
        self.setWindowTitle("Orb")
        self.setMinimumSize(self.minSize)  # Minimum size for the window
        self.appIcon = QIcon("Resources/icons/icon.png")
        self.app.setWindowIcon(self.appIcon)
        removePadding(self)
        
        #set custom font
        font_Path = "Resources/fonts/minecraft_font.ttf"
        self.setCustFont(font_Path,8)
        
        
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)
        self.layout().setSpacing(0)


        #self.layout().addWidget(self.appContainer)
        #self.layout.addStretch()  # To fill the remaining space if needed
        # Custom Frame 

        if useCustomWindow:
            self.window = customWindow(self)
            self.windowContainer = self.window.layout()
        else:
            self.window = defaultWindow(self)
            self.windowContainer = self.window.layout()


        self.contextBar = Contextbar()
        self.windowContainer.addWidget(self.contextBar)

        centerContainer = QWidget(self.window)
        centerContainer.setStyleSheet("background:rgb(180,165,147);border-radius:0px;")
        centerContainer.resize(QSize(800,600))
        centerContainer.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        centerContainerLayout = QGridLayout(centerContainer)
        centerContainerLayout.setContentsMargins(2,2,2,2)
        centerContainerLayout.setSpacing(5)
        self.windowContainer.addWidget(centerContainer)
        #self.windowContainer.setRowStretch(0,1)
        #self.windowContainer.setColumnStretch(0,1)
        
        leftBar = pixelWidget()
        leftBar.setMaximumWidth(300)
        leftBar.setSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.Expanding)
        leftBar.setLayout(QVBoxLayout())
        leftBar.layout().setAlignment(Qt.AlignmentFlag.AlignHCenter)
        leftBar.setContentsMargins(0,0,0,0)
        leftBar.layout().setContentsMargins(0,0,0,0)
        self.colourPicker = ColourPicker()
        leftBar.layout().addWidget(self.colourPicker)

       
        centerContainerLayout.addWidget(leftBar,1,0)
        centerContainerLayout.addWidget(Toolbar(),0,1)
        
        
        #Create and configure the Canvas widget
        self.canvas = Viewport()
        self.currentTarget = self.canvas
        #self.canvas.setStyleSheet("border: purple 5px solid;")
        # Add the Canvas widget to the layout
        centerContainerLayout.addWidget(self.canvas,1,1)
        
        centerContainerLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.tools = ToolHandler()
        self.tools.current_tool.target = self.currentTarget.canvas.image

        self.colourPicker.colorWheel.colourChanged.connect(self.tools.current_tool._updateColour)

        RightBar = pixelWidget()
        RightBar.setFixedWidth(25)
        RightBar.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Expanding)
        RightBar.setLayout(QVBoxLayout())
        removePadding(RightBar)

        #   RightBar.layout().addWidget(QLabel("Hi    "))
        centerContainerLayout.addWidget(RightBar,1,2)
        

        cl = centerContainerLayout
        cl.setRowStretch(1,1)
        cl.setColumnStretch(1,1)

        cl.setRowStretch(0,1)
        cl.setColumnStretch(1,1)

        

        print("Program Started")

    def setupGUI(self):
        #self = actual program
        self.setLayout(QVBoxLayout())
        removePadding(self)

        
        # Custom Frame 
        #create custom frame for window,
        if self.isCustomWindow():
            self.window = customWindow(self)
            self.windowContainer = self.window.layout()
        else:
            self.window = defaultWindow(self)
            self.windowContainer = self.window.layout()

        
        pass

    def isCustomWindow(self) -> bool:
        if self.window.objectName() == "customWindow":
            return True
        else:
            return False

    def setCustFont(self,fontPath,size) -> bool:
        #add font to application 
        fontID = QFontDatabase.addApplicationFont(fontPath)
        if fontID == -1:
            print(f"failed to load font: {fontPath}")
            return False 
        
        #get font from ID
        self.font = getFont(fontID,size)
        self.setFont(self.font)
        print(f"Set Font to {fontID} | {fontPath}")

        return True
    





    