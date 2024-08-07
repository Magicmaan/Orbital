from PySide6.QtCore import QSize, Qt, QPoint
from PySide6.QtGui import QIcon, QPixmap, QCursor
from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QSizePolicy, QSpacerItem, QWidget

class Toolbar(QWidget):
    def __init__(self, program,parent=None):
        super().__init__(parent)
        self.setObjectName("Titlebar2")
        self.program = program
        self.setAutoFillBackground(True)

        self.mouse_offset = QPoint(0,0)
        
        self.objheight = 12
        self.icon_size = 24
        self.setContentsMargins(0,0,0,0)
        self.resize(800, self.objheight)  # Adjusted size to fit the title bar
        
        self.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Fixed)
        self.containerLayout = QHBoxLayout(self)
        self.containerLayout.setObjectName("containerLayout")
        self.containerLayout.setSpacing(0)
        self.containerLayout.setContentsMargins(0,0,0,0)

        self.setStyleSheet(
            #titlebar background
            "QWidget#Container{background-color: rgba(0, 255, 255, 255);"
                  # Added border property
            "background: purple}"

            #buttons and labels
            "QPushButton,QLabel {"
            "background-color: transparent;"
            "margin:0px;padding:0px;}"
        )



        self.setupUi()
    
    def setupUi(self):
        self.inner = QWidget()
        self.inner.setObjectName("Container")

        self.horizontalLayout = QHBoxLayout(self.inner)
        self.horizontalLayout.setSpacing(0)
        
        self.containerLayout.addWidget(self.inner)
        self.inner.setContentsMargins(0,0,0,0)
        self.horizontalLayout.setContentsMargins(0,0,0,0)
        
        

        
        self.horizontalLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.icon = QLabel(self)
        self.icon.setObjectName("icon")
        self.icon.setPixmap(QPixmap("Resources/icons/icon.png").scaled(self.icon_size,self.icon_size, Qt.KeepAspectRatio, Qt.FastTransformation))
        self.icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.horizontalLayout.addWidget(self.icon)

        self.title = QLabel(self)
        self.title.setText("Orb")
        self.horizontalLayout.addWidget(self.title)

        #spacer
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(self.horizontalSpacer)

        #minimise button
        self.minimiseBtn = self.addButton("MinimiseButton",self.program.showMinimized,"Resources/icons/maximise.png",self.icon_size)
        self.horizontalLayout.addWidget(self.minimiseBtn)

        #maximise button
        self.maximiseBtn = self.addButton("MaximiseButton",lambda:self.program.setWindowState(self.program.windowState() ^ Qt.WindowFullScreen),"Resources/icons/maximise.png",self.icon_size)
        self.horizontalLayout.addWidget(self.maximiseBtn)

        #close app
        self.exitBtn = self.addButton("ExitButton",self.program.close,"Resources/icons/exit.png",self.icon_size)
        self.horizontalLayout.addWidget(self.exitBtn)

    #helper function to add button to it in less code
    def addButton(self,name,func,icon,size) -> QPushButton:
        btn = QPushButton(self)
        btn.setObjectName(name)
        icon = QIcon(QPixmap(icon) .scaled(size,size, Qt.KeepAspectRatio, Qt.FastTransformation))
        btn.setIcon(icon)
        btn.setText("")
        btn.setBaseSize(QSize(size,size))
        btn.setIconSize(QSize(size,size))
        btn.setContentsMargins(0,0,0,0)
        btn.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        #link button to function
        btn.clicked.connect(func)

        return btn
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mouse_pressed = True
            cpos = QCursor.pos()
            self.mouse_offset = self.program.mapFromGlobal(cpos)


    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mouse_pressed = False
    
    def mouseMoveEvent(self, event):
        if self.mouse_pressed:
            # Optionally handle mouse movement while holding    
            pos = self.program.pos()
            self.program.move(pos + event.position().toPoint() - self.mouse_offset)

