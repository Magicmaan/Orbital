from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QCursor, QIcon, QPainter, QPixmap, QTransform
from PySide6.QtWidgets import (QHBoxLayout, QLabel, QPushButton, QSizePolicy,
                               QWidget)

from GUI.Widgets.WidgetUtils import drawPixelBorder, removePadding

from GUI.Widgets.Decorators import PixelBorder, sizePolicy

@PixelBorder

class Toolbar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("ToolBar")

        self.program = parent
        self.objheight = 16
        self.icon_size = 24
        self.resize(400, self.objheight)
        self.setFixedHeight(self.objheight)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setLayout(QHBoxLayout())
        self.layout().setObjectName("containerLayout")
        self.layout().setAlignment(Qt.AlignmentFlag.AlignLeft)
        removePadding(self)

        self.setStyleSheet(
            "background:transparent;"
        )

        self.setupUi()

    def setupUi(self):
        self.title = QLabel(self)
        self.title.setText("Toolbar   ")
        self.layout().addWidget(self.title)

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
        self.layout().addWidget(btn)
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

        
    
        