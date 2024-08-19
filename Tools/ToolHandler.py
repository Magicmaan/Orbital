from PySide6.QtCore import QSize, Qt, Slot, Signal, QPoint
from PySide6.QtGui import QCursor, QIcon, QPainter, QPixmap, QTransform
from PySide6.QtWidgets import (QHBoxLayout, QLabel, QPushButton, QSizePolicy,
                               QWidget, QApplication)

from GUI.Widgets.WidgetUtils import drawPixelBorder, removePadding

from GUI.customEvents import *

from GUI.Decorators import PixelBorder, sizePolicy
from Tools.brush import BrushTool
from Tools.select import SelectTool
from Utils import DotDict



@PixelBorder
class ToolHandler(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        #contains tool selection
        self.brush = BrushTool()
        self.select = SelectTool()

        #indidividual tool config (size, colour, selection etc etc)
        self.tool_config = DotDict()

        self.current_tool = self.select
    
    def onAction(self, position, painter=None):
        self.current_tool.onAction(position, painter)
    
    @Slot(toolClickEvent)
    def toolAction(self, value:toolClickEvent):
        self.current_tool.onAction(value)
    
    @Slot(toolReleaseEvent)
    def toolReleaseAction(self, value:toolReleaseEvent):
        self.current_tool.onActionRelease(value)
    
