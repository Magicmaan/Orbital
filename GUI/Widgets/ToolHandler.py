from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QCursor, QIcon, QPainter, QPixmap, QTransform
from PySide6.QtWidgets import (QHBoxLayout, QLabel, QPushButton, QSizePolicy,
                               QWidget, QApplication)

from GUI.Widgets.WidgetUtils import drawPixelBorder, removePadding

from GUI.Decorators import PixelBorder, sizePolicy

@PixelBorder
class ToolHandler(QWidget):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)

        #contains tool selection
        self.tools = []
        #indidividual tool config (size, colour, selection etc etc)
        self.tool_settings = []

        self.current_tool = None