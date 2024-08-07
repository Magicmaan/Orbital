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


class Program(QMainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        
        self.app = QApplication.instance()

        #setup window
        self.setWindowTitle("Orb")
        self.setMinimumSize(800, 600)  # Minimum size for the window
        self.appIcon = QIcon("Resources/icons/icon.png")
        self.app.setWindowIcon(self.appIcon)
        self.setWindowFlags(Qt.FramelessWindowHint) #disable window border
        self.setContentsMargins(0,0,0,0)

        #set custom font
        fontID = addFont("Resources/fonts/minecraft_font.ttf")
        self.font = getFont(fontID,8)
        self.setFont(self.font)
        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        appContainer = QWidget()
        appContainer.setObjectName("appContainer")

        
        #setup container for app
        appContainer.resize(800,600)
        appContainer.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        appContainer.setContentsMargins(0,0,0,0)
        appContainer.setStyleSheet("QWidget{border: 2px solid green}")

        #layout - vertical
        self.layout = QVBoxLayout(appContainer)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        appContainer.setAutoFillBackground(True)
        
        #titlebar init
        self.titlebar = Titlebar(self)
        self.layout.addWidget(self.titlebar)


        
        centerContainer = QWidget()
        centerContainerLayout = QHBoxLayout(centerContainer)
        self.layout.addWidget(centerContainer)

        centerContainerLayout.addWidget(Toolbar(self))

        
        
        #Create and configure the Canvas widget
        self.canvas = Canvas()

        # Add the Canvas widget to the layout
        centerContainerLayout.addWidget(self.canvas)
        self.layout.addStretch()  # To fill the remaining space if needed

        # Set the central widget for the MainWindow
        self.setCentralWidget(appContainer)


        
        

        
        #self.createWidgets()
        #self.createMenus()
    
        
    def resizeEvent(self, event):
        # Call the base class implementation
        super().resizeEvent(event)

        # Custom handling code here
        print(f"Window resized to: {event.size().width()}x{event.size().height()}")

        
        # Example: Update widget appearance based on the new size
        self.update()  # Request a repaint if necessary

    

    def canvasInit(self) -> bool:
        # Create and configure the Canvas widget
        self.canvas = Canvas(self)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Add the Canvas widget to the layout
        self.layout.addWidget(self.canvas)
        self.layout.addStretch()  # To fill the remaining space if needed

        return True



    