from PySide6.QtCore import QSize, Qt, QPoint, QRect
from PySide6.QtGui import QIcon, QPixmap, QCursor, QPainter, QColor, QTransform
from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QSizePolicy, QSpacerItem, QWidget

from GUI.Widgets.WidgetUtils import *

class Toolbar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("ToolBar")

        self.program = parent
        self.objheight = 16
        self.icon_size = 24
        self.resize(400, self.objheight)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.containerLayout = QHBoxLayout(self)
        self.containerLayout.setObjectName("containerLayout")
        removePadding(self)

        self.setStyleSheet(
            "background:transparent;"
            "QPushButton, QLabel {"
            "margin: 0px; padding: 0px; }"
        )



        self.setupUi()

    def setupUi(self):
        self.inner = QWidget()
        self.inner.setObjectName("Container")

        self.layout = QHBoxLayout(self.inner)
        self.layout.setSpacing(0)

        self.containerLayout.addWidget(self.inner)
        self.inner.setContentsMargins(0, 0, 0, 0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.title = QLabel(self)
        self.title.setText("        ")
        self.layout.addWidget(self.title)

        self.minimiseBtn = self.addButton("MinimiseButton", self.program.showMinimized, "Resources/icons/tools/brush.png", self.icon_size)
        self.minimiseBtn = self.addButton("MinimiseButton", self.program.showMinimized, "Resources/icons/tools/eraser.png", self.icon_size)
        self.minimiseBtn = self.addButton("MinimiseButton", self.program.showMinimized, "Resources/icons/tools/bucket.png", self.icon_size)
        self.minimiseBtn = self.addButton("MinimiseButton", self.program.showMinimized, "Resources/icons/tools/picker.png", self.icon_size)
        self.maximiseBtn = self.addButton("MaximiseButton", lambda: self.program.setWindowState(self.program.windowState() ^ Qt.WindowFullScreen), "Resources/icons/maximise.png", self.icon_size)
        self.exitBtn = self.addButton("ExitButton", self.program.close, "Resources/icons/exit.png", self.icon_size)

    def addButton(self, name, func, icon, size) -> QPushButton:
        btn = QPushButton(self)
        btn.setObjectName(name)
        icon = QIcon(QPixmap(icon).scaled(size, size, Qt.KeepAspectRatio, Qt.FastTransformation))
        btn.setIcon(icon)
        btn.setText("")
        btn.setBaseSize(QSize(size, size))
        btn.setIconSize(QSize(size, size))
        btn.setContentsMargins(0, 0, 0, 0)
        btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
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
            pos = self.program.pos()
            self.program.move(pos + event.position().toPoint() - self.mouse_offset)

    def paintEvent(self, event):
        painter = QPainter(self)
        
        # Fill the entire widget with a green color
        # Draw edges from the pixmap
        drawPixelBorder(self,painter,QPixmap("Resources/button.png"),2,4)
        
        # End painting
        painter.end()
        
    
        