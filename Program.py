from PySide6.QtCore import *
from PySide6.QtCore import Qt
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtWidgets import QWidget

from Widgets.Programbar import Programbar   
from Widgets.CanvasWindow import Canvas
from Widgets.Toolbar import Toolbar
from Widgets.titlebar import Titlebar

from Utils import *
from DiscordPresence import *

class customWindow(QWidget):
    def __init__(self, program, parent=None):
        super().__init__(parent)
        self.program = program
        program.setWindowFlags(Qt.FramelessWindowHint) #disable default border
        self.layout = QVBoxLayout(self)
        self.setObjectName("windowContainer")
        self.setContentsMargins(0,0,0,0)
        self.layout.setContentsMargins(0,0,0,0)


        self.setStyleSheet("QWidget#windowContainer{border: solid green 2px;}")

        self.layout.setSpacing(0)

         #titlebar init
        program.titlebar = Titlebar(self)
        self.layout.addWidget(program.titlebar)
        




class Program(QMainWindow):
    def __init__(self, useCustomWindow=True,parent=None) -> None:
        super().__init__(parent)
        
        self.app = QApplication.instance()
        self.setMouseTracking(True)


        #setup window
        self.setWindowTitle("Orb")
        self.setMinimumSize(800, 600)  # Minimum size for the window
        self.appIcon = QIcon("Resources/icons/icon.png")
        self.app.setWindowIcon(self.appIcon)
        self.setContentsMargins(0,0,0,0)

        
        #set custom font
        font_Path = "Resources/fonts/minecraft_font.ttf"
        self.setCustFont(font_Path,8)
    

        #Head container for app
        appContainer = QWidget()
        appContainer.setObjectName("appContainer")
        appContainer.resize(800,600)
        appContainer.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        appContainer.setContentsMargins(0,0,0,0)

        # Custom Frame 
        if useCustomWindow:
            self.window = customWindow(self)
            self.windowContainer = self.window.layout
            print("Custom Frame Enabled")
        else:
            self.window = QWidget()
            self.windowContainer = QVBoxLayout(self.window)

        self.layout = QVBoxLayout(appContainer)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.layout.addWidget(self.window)
        
       


        
        centerContainer = QWidget()
        centerContainerLayout = QHBoxLayout(centerContainer)
        self.windowContainer.addWidget(centerContainer)

        
        
        #Create and configure the Canvas widget
        self.canvas = Canvas()

        # Add the Canvas widget to the layout
        centerContainerLayout.addWidget(self.canvas)
        self.layout.addStretch()  # To fill the remaining space if needed

        # Set the central widget for the MainWindow
        self.setCentralWidget(appContainer)

        print("Program Started")
    
        
    def resizeEvent(self, event):
        # Call the base class implementation
        super().resizeEvent(event)

        # Custom handling code here
        print(f"Window resized to: {event.size().width()}x{event.size().height()}")

        # Example: Update widget appearance based on the new size
        self.update()  # Request a repaint if necessary

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
    


    def canvasInit(self) -> bool:
        # Create and configure the Canvas widget
        self.canvas = Canvas(self)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Add the Canvas widget to the layout
        self.layout.addWidget(self.canvas)
        self.layout.addStretch()  # To fill the remaining space if needed

        return True



    