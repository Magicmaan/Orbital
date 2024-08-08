from PySide6.QtCore import QSize, Qt, QPoint
from PySide6.QtGui import QIcon, QPixmap, QCursor
from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QSizePolicy, QSpacerItem, QWidget

class Toolbar(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setObjectName("ToolBar")

        self.program = parent
        self.objheight = 12
        self.icon_size = 24
        self.setContentsMargins(0,0,0,0)
        self.resize(400, self.objheight)  # Adjusted size to fit the title bar
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

        self.layout = QHBoxLayout(self.inner)
        self.layout.setSpacing(0)
        
        self.containerLayout.addWidget(self.inner)
        self.inner.setContentsMargins(0,0,0,0)
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.title = QLabel(self)
        self.title.setText("Orb")
        self.layout.addWidget(self.title)

        #spacer
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.layout.addItem(self.horizontalSpacer)

        #minimise button
        self.minimiseBtn = self.addButton("MinimiseButton",self.program.showMinimized,"Resources/icons/maximise.png",self.icon_size)

        #maximise button
        self.maximiseBtn = self.addButton("MaximiseButton",lambda:self.program.setWindowState(self.program.windowState() ^ Qt.WindowFullScreen),"Resources/icons/maximise.png",self.icon_size)

        #close app
        self.exitBtn = self.addButton("ExitButton",self.program.close,"Resources/icons/exit.png",self.icon_size)
        

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

        self.layout.addWidget(btn)

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

