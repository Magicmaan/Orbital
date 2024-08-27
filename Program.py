from PySide6.QtCore import QSize, Qt, QPoint
from PySide6.QtGui import QFontDatabase, QIcon, QPainter, QPixmap, QRegion
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QMainWindow,
                               QSizePolicy, QVBoxLayout, QWidget)

from CustomWindow import customWindow, defaultWindow
from DiscordPresence import *
from GUI.Widgets.CanvasWindow import Viewport
from GUI.Widgets.Toolbar import Toolbar
from GUI.Widgets.Contextbar import Contextbar
from Tools.ToolHandler import ToolHandler
from GUI.Widgets.ColourPicker import ColourPicker
from GUI.Widgets.WidgetUtils import drawPixelBorder, removePadding
from Utils import getFont
from config import *
from GUI.Widgets.CanvasSettingsWindow import ViewportSettingsWindow


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
    def __init__(self, use_custom_window=False,parent=None) -> None:
        super().__init__(parent)
        #create reference accessible from program
        QApplication.instance().program = self

        self.config = loadToml("config.toml")

        use_custom_window = self.config.window["use_custom_window"]

        self.app = QApplication.instance()
        self.setMouseTracking(True)
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)

        self.min_size = QSize(800,600)

        #setup window
        self.setWindowTitle(f"{self.config.name} {self.config.version}")
        self.setMinimumSize(self.min_size)  # Minimum size for the window
        self.app.setWindowIcon(QPixmap(self.config.window["icon_path"]))
        removePadding(self)
        
        #set custom font
        font_path = "Resources/fonts/pixelated.ttf"
        self.setCustFont(font_path,8)

        #set custom font
        font_path = "Resources/fonts/mai10.ttf"
        self.setCustFont(font_path,8)
        
        
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)
        self.layout().setSpacing(0)


        #self.layout().addWidget(self.appContainer)
        #self.layout.addStretch()  # To fill the remaining space if needed
        # Custom Frame 

        if use_custom_window:
            self.window = customWindow()
            self.window_container = self.window.layout()
        else:
            self.window = defaultWindow(self)
            self.window_container = self.window.layout()

        self.tools = ToolHandler()
        self.canvas = Viewport()

        

        self.context_bar = Contextbar()
        self.window_container.addWidget(self.context_bar)

        center_container = QWidget(self.window)
        center_container.setStyleSheet("background:rgb(180,165,147);border-radius:0px;")
        center_container.resize(QSize(800,600))
        center_container.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        center_container.setLayout(QGridLayout())
        center_container.layout().setContentsMargins(2,2,2,2)
        center_container.layout().setSpacing(5)
        self.window_container.addWidget(center_container)
        #self.windowContainer.setRowStretch(0,1)
        #self.windowContainer.setColumnStretch(0,1)
        
        left_bar = pixelWidget()
        left_bar.setMaximumWidth(300)
        left_bar.setSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.Expanding)
        left_bar.setLayout(QVBoxLayout())
        left_bar.layout().setAlignment(Qt.AlignmentFlag.AlignHCenter)
        left_bar.setContentsMargins(0,0,0,0)
        left_bar.layout().setContentsMargins(0,0,0,0)
        left_bar.layout().setAlignment(Qt.AlignmentFlag.AlignTop)
        self.colourPicker = ColourPicker()
        left_bar.layout().addWidget(self.colourPicker)

        self.viewportsettings = ViewportSettingsWindow()
        left_bar.layout().addWidget(self.viewportsettings)

       
        center_container.layout().addWidget(left_bar,1,0)
        center_container.layout().addWidget(Toolbar(),0,1)
        
        
        

        #Create and configure the Canvas widget
        
        self.current_target = self.canvas
        #self.canvas.setStyleSheet("border: purple 5px solid;")
        # Add the Canvas widget to the layout
        center_container.layout().addWidget(self.canvas,1,1)
        
        center_container.layout().setAlignment(Qt.AlignmentFlag.AlignCenter)

        right_bar = pixelWidget()
        right_bar.setFixedWidth(25)
        right_bar.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Expanding)
        right_bar.setLayout(QVBoxLayout())
        removePadding(right_bar)

        #   RightBar.layout().addWidget(QLabel("Hi    "))
        center_container.layout().addWidget(right_bar,1,2)
        


        center_container.layout().setRowStretch(1,1)
        center_container.layout().setColumnStretch(1,1)
        center_container.layout().setRowStretch(0,1)
        center_container.layout().setColumnStretch(1,1)

        

        print("Program Started")


    def getConfig(self):
        return self.config


    def isCustomWindow(self) -> bool:
        if self.window.objectName() == "customWindow":
            return True
        else:
            return False

    def setCustFont(self,font_path,size) -> bool:
        #add font to application 
        fontID = QFontDatabase.addApplicationFont(font_path)
        if fontID == -1:
            print(f"failed to load font: {font_path}")
            return False 
        
        #get font from ID
        self.font = getFont(fontID,size)
        self.setFont(self.font)
        print(f"Set Font to {fontID} | {font_path}")

        return True
    





    