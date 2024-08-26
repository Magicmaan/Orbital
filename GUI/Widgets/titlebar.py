from PySide6.QtCore import QPoint, QSize, Qt
from PySide6.QtGui import QColor, QIcon, QPainter, QPixmap, QFont
from PySide6.QtWidgets import (QHBoxLayout, QLabel, QPushButton, QSizePolicy,
                               QSpacerItem, QWidget, QApplication)

from GUI.Widgets.WidgetUtils import drawPixelBorder, removePadding
from GUI.Decorators import PixelBorder, sizePolicy

@PixelBorder

class Titlebar(QWidget):
    def __init__(self, app_window,parent=None):
        super().__init__(parent)
        self.program = QApplication.instance().program

        self.config = self.program.getConfig().window

        self.setObjectName("Titlebar")
        self.app_window = app_window
        self.setAutoFillBackground(True)

        self.mouse_offset = QPoint(0,0)
        
        self.fixed_height = 8
        self.icon_size = 24
        
        self.resize(800, 24)  # Adjusted size to fit the title bar
        self.setMinimumHeight(self.fixed_height)
        self.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Policy.Preferred)
        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)
        self.layout().setObjectName("containerLayout")
        self.layout().setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.layout().setSpacing(0)
        removePadding(self)
        self.setContentsMargins(5,0,5,0)

        self.setStyleSheet(
            "background: transparent;"
        )



        self.setupUi()
    
    def setupUi(self):
        self.icon = QLabel(self)
        self.icon.setObjectName("icon")
        self.icon.setPixmap(QPixmap(self.config["icon_path"]).scaled(self.icon_size,self.icon_size, Qt.KeepAspectRatio, Qt.FastTransformation))
        self.icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout().addWidget(self.icon)

        self.title = QLabel()

        font = QFont("pixelated", 12)

        self.title.setFont(self.program.font)
        self.title.setText(f"{self.config['title']} {self.program.config.version}")
        self.layout().addWidget(self.title)

        #spacer
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.layout().addItem(self.horizontalSpacer)

        #minimise button
        self.minimiseBtn = self.addButton("MinimiseButton",self.app_window.parent.showMinimized,"Resources/icons/minimise.png",self.icon_size)
        

        #maximise button
        self.maximiseBtn = self.addButton("MaximiseButton",self.app_window.parent.setWindowState(self.app_window.parent.windowState() ^ Qt.WindowFullScreen),"Resources/icons/maximise.png",self.icon_size)
        self.layout().addWidget(self.maximiseBtn)

        #close app
        self.exitBtn = self.addButton("ExitButton",self.app_window.parent.close,"Resources/icons/exit.png",self.icon_size)
        self.layout().addWidget(self.exitBtn)

    #helper function to add button to it in less code
    def addButton(self,name,func,icon,size) -> QPushButton:
        btn = QPushButton(self)
        btn.setObjectName(name)
        icon = QIcon(QPixmap(icon) .scaled(size,size, Qt.KeepAspectRatio, Qt.FastTransformation))
        btn.setIcon(icon)
        btn.setText("")
        btn.setFixedSize(QSize(size,size))
        btn.setIconSize(QSize(size,size))
        btn.setContentsMargins(0,0,0,0)
        btn.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        #link button to function
        btn.clicked.connect(func)

        self.layout().addWidget(btn)

        return btn

    
