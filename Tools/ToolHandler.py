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


#TODO: ADD tools
#TODO: link to Tool Selector Widget
#TODO: change interaction method to use signals, and have global interface
#TODO: Keybinds for tools

@PixelBorder
class ToolHandler(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        #contains tool selection
        self.brush = BrushTool()
        self.select = SelectTool()

        self.colourPicker = None #ColourPickerTool()
        self.line = None #LineTool()

        #indidividual tool config (size, colour, selection etc etc)
        self.tool_config = DotDict()
        self.tool_config.snapToEdge = False
        



        self.current_tool = self.brush
        self.shift_tool = self.line
        self.alt_tool = self.colourPicker
    

    @Slot(toolClickEvent)
    def toolAction(self, value:toolClickEvent):
        self.current_tool.onClick(value)
    
    @Slot(toolReleaseEvent)
    def toolReleaseAction(self, value:toolReleaseEvent):
        self.current_tool.onRelease(value)
    
    @Slot(toolChangeEvent)
    def toolChangeAction(self, value:toolChangeEvent):
        print(value)
        if hasattr(self,value.tool):
            self.current_tool = getattr(self,value.tool)
            #if value.config:
            #    self.tool_config = value.config
            #self.current_tool.setProperties(self.tool_config)
    
