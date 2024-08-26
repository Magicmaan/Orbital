from PySide6.QtCore import QSize, Qt, Slot, Signal, QPoint
from PySide6.QtGui import QCursor, QIcon, QPainter, QPixmap, QTransform
from PySide6.QtWidgets import (QHBoxLayout, QLabel, QPushButton, QSizePolicy,
                               QWidget, QApplication)

from GUI.Widgets.WidgetUtils import drawPixelBorder, removePadding

from GUI.customEvents import *
from GUI.Decorators import PixelBorder, sizePolicy

@PixelBorder

class Toolbar(QWidget):
    toolChange_S = Signal(toolChangeEvent)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("ToolBar")

        self.program = QApplication.instance().program

        self.objheight = 36
        self.icon_size = 24
        self.setFixedHeight(self.objheight)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setLayout(QHBoxLayout())
        self.layout().setObjectName("containerLayout")
        self.layout().setAlignment(Qt.AlignmentFlag.AlignLeft)
        removePadding(self)
        self.current_tool = None

        self.setStyleSheet(
            "background:transparent;"
        )
        
        self.toolChange_S.connect(self.program.tools.toolChangeAction)

        self.setupUi()

    def getCurrentTool(self):
        new_tool = self.program.tools.current_tool
        if self.current_tool is None:
            self.current_tool = new_tool
            return
        if new_tool != self.current_tool:
            self._removeBorder()
            self.current_tool = new_tool
    
    def _removeBorder(self):
        button = getattr(self, f"{self.current_tool.name}Btn")
        button.setFixedSize(QSize(self.icon_size, self.icon_size))
        button.setStyleSheet("")

    def _paintBorder(self, painter=None):
        border = "border:4px solid black;"
        
        button = getattr(self, f"{self.current_tool.name}Btn")
        button.setFixedSize(QSize(self.icon_size + 4, self.icon_size + 4))
        button.setStyleSheet(border)

    def paintEvent(self, event) -> None:
        self.getCurrentTool()
        self._paintBorder()
        


        return super().paintEvent(event)

    def setupUi(self):
        self.title = QLabel(self)
        self.title.setText("Toolbar   ")
        self.layout().addWidget(self.title)
        self.brushBtn = self.addButton("brushBtn", self.brush, "Resources/icons/tools/brush.png", self.icon_size)
        self.selectBtn = self.addButton("selectBtn", self.select, "Resources/icons/tools/eraser.png", self.icon_size)
        self.minimiseBtn = self.addButton("MinimiseButton", self.program.showMinimized, "Resources/icons/tools/bucket.png", self.icon_size)
        self.minimiseBtn = self.addButton("MinimiseButton", self.program.showMinimized, "Resources/icons/tools/picker.png", self.icon_size)
        self.maximiseBtn = self.addButton("MaximiseButton", lambda: self.program.setWindowState(self.program.windowState() ^ Qt.WindowFullScreen), "Resources/icons/maximise.png", self.icon_size)
        self.exitBtn = self.addButton("ExitButton", self.program.close, "Resources/icons/exit.png", self.icon_size)

    def brush(self):
        self.toolChange_S.emit(toolChangeEvent("brush"))
        #send event for tool, with config
        

    def select(self):
        self.toolChange_S.emit(toolChangeEvent("select"))
        #send event for tool, with config
        

    def selectTool(self, tool):
        pass

    def addButton(self, name, func, icon, size) -> QPushButton:
        btn = QPushButton(self)
        btn.setObjectName(name)
        icon = QIcon(QPixmap(icon).scaled(size, size, Qt.KeepAspectRatio, Qt.FastTransformation))
        btn.setIcon(icon)
        btn.setText("")

        btn.setFixedSize(QSize(size, size))
        btn.setIconSize(QSize(size, size))
        btn.setContentsMargins(0, 0, 0, 0)
        btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn.setStyleSheet(
            "background:red;"
        )
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

        
    
        