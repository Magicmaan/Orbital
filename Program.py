from PySide6.QtCore import *
from PySide6.QtCore import Qt
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtWidgets import QWidget

from GUI.Widgets.Programbar import Programbar   
from GUI.Widgets.CanvasWindow import Viewport
from GUI.Widgets.Toolbar import Toolbar

from Utils import *
from DiscordPresence import *

from CustomWindow import customWindow,defaultWindow
        




class Program(QMainWindow):
    def __init__(self, useCustomWindow=False,parent=None) -> None:
        super().__init__(parent)
        
        self.app = QApplication.instance()
        self.setMouseTracking(True)
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)

        self.minSize = QSize(650,650)
        #setup window
        self.setWindowTitle("Orb")
        self.setMinimumSize(self.minSize)  # Minimum size for the window
        self.appIcon = QIcon("Resources/icons/icon.png")
        self.app.setWindowIcon(self.appIcon)
        self.setContentsMargins(0,0,0,0)
        
        #set custom font
        font_Path = "Resources/fonts/minecraft_font.ttf"
        self.setCustFont(font_Path,8)
        #Head container for app
        self.appContainer = QWidget(self)
        # Set the central widget for the MainWindow
        self.setCentralWidget(self.appContainer)

        self.appContainer.setObjectName("appContainer")
        self.appContainer.resize(800,600)
        self.appContainer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        

        
        
       
        
        self.layout = QVBoxLayout(self.appContainer)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        

        #self.layout.addStretch()  # To fill the remaining space if needed
        # Custom Frame 
        if useCustomWindow:
            self.window = customWindow(self)
            self.windowContainer = self.window.layout
            
        else:
            self.window = defaultWindow(self)
            self.windowContainer = self.window.layout

        
        self.window.resize(self.size())
        self.window.setStyleSheet("background:blue;border-radius:0px;")
        self.layout.addWidget(self.window)
        #self.layout.setRowStretch(0,2)
        #self.layout.setColumnStretch(0,2)

        self.windowContainer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        



        centerContainer = QWidget()
        centerContainer.setParent(self.window)
        centerContainer.setStyleSheet("background:green;border-radius:0px;")
        centerContainer.resize(QSize(800,600))
        centerContainer.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        centerContainerLayout = QGridLayout(centerContainer)
        centerContainerLayout.setContentsMargins(2,2,2,2)
        centerContainerLayout.setSpacing(5)
        self.windowContainer.addWidget(centerContainer,0,0)
        self.windowContainer.setRowStretch(0,1)
        self.windowContainer.setColumnStretch(0,1)

        leftBar = QWidget()
        leftBar.setFixedWidth(200)
        leftBar.setContentsMargins(0,0,0,0)
        leftBar.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Expanding)
        leftBar.setStyleSheet("background:purple;")
        lBarStyle = QVBoxLayout(leftBar)
        m = QLabel("Hi     ")
        m.setContentsMargins(0,0,0,0)
        m.setStyleSheet("background: purple;border: 5px solid red")
        #lBarStyle.addWidget(m)
        centerContainerLayout.addWidget(m,0,0)
        centerContainerLayout.addWidget(leftBar,1,0)


        centerContainerLayout.addWidget(Toolbar(self),0,1)
        
        
        #Create and configure the Canvas widget
        self.canvas = Viewport()
        #self.canvas.setStyleSheet("border: purple 5px solid;")
        # Add the Canvas widget to the layout
        centerContainerLayout.addWidget(self.canvas,1,1)
        
        centerContainerLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        

        RightBar = QWidget()
        RightBar.setFixedWidth(200)
        RightBar.setContentsMargins(0,0,0,0)
        RightBar.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Expanding)
        RightBar.setStyleSheet("background:blue;")
        RBarStyle = QVBoxLayout(RightBar)
        RBarStyle.addWidget(QLabel("Hi    "))
        centerContainerLayout.addWidget(RightBar,1,2)

        cl = centerContainerLayout
        cl.setRowStretch(1,1)
        cl.setColumnStretch(1,1)

        

        print("Program Started")

    

    def isCustomWindow(self) -> bool:
        if self.window.objectName() == "customWindow":
            return True
        else:
            return False
         
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
    





    