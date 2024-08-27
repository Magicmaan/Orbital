from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtGui import QCursor, QIcon, QPainter, QPixmap, QTransform, QAction
from PySide6.QtWidgets import (QHBoxLayout, QLabel, QPushButton, QSizePolicy,
                               QWidget,QMenuBar,QMenu,QApplication,QDialog)

from GUI.Widgets.WidgetUtils import drawPixelBorder, removePadding
from GUI.Decorators import PixelBorder, sizePolicy
from GUI.customEvents import *
from GUI.Widgets.FileOpenWindow import FileOpenWindow


@PixelBorder

class Contextbar(QMenuBar):
    openFile_S = Signal(openFileCustEvent)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Contextbar")
        self.program = QApplication.instance().program
        self.objheight = 16
        self.icon_size = 24
        self.resize(400, self.objheight)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setLayout(QHBoxLayout())
        self.layout().setObjectName("containerLayout")
        self.layout().setAlignment(Qt.AlignmentFlag.AlignLeft)
        removePadding(self)

        
        self.setStyleSheet(
            "background:transparent;"
        )

        m = QMenu("Hi")
        m.setTitle("BOOOOOO")
        self.addMenu(m)

        self.setupUi()

    def newFile(self):
        self.openFile_S.connect(self.program.canvas.openFile)
        print("Opening File")

        self.openFileWidget = FileOpenWindow()
        result = self.openFileWidget.exec_()  # Run the dialog modally

        if result == QDialog.Accepted:
            selected_file = self.openFileWidget.selected_file
            print(f"Selected file: {selected_file}")
            # Continue with the rest of the code
            self.openFile_S.emit(openFileCustEvent(selected_file))
        else:
            print("No file selected")



    def setupUi(self):
        #self.fileMenu = QMenu("File")
        #self.addMenu(self.fileMenu)

        #openFile = QAction("Open File",self.fileMenu)
        

        #self.fileMenu.addAction(openFile)
        #openFile.triggered.connect(self.newFile)

        self.addMenuCust("File")
        self.addMenuAction("New File",self.newFile,(),self.FileMenu)
        self.addMenuAction("Open File",self.newFile,(),self.FileMenu)

        self.addMenuCust("Edit")
        self.addMenuCust("Canvas")
        self.addMenuCust("Layer")
        self.addMenuCust("Select")
        self.addMenuCust("View")
        self.addMenuCust("Help")
        self.addMenuCust("Open File")

        self.addMenuCust("Tiling",self.CanvasMenu)
        self.addMenuAction("Toggle Tiling",
                           func=self.program.canvas.toggleTiling,
                           args=(True,True),
                           menu=self.CanvasMenu.TilingMenu)
        self.addMenuAction("Toggle X",
                           func=self.program.canvas.toggleTiling,
                           args=(True,False),
                           menu=self.CanvasMenu.TilingMenu)
        self.addMenuAction("Toggle Y",
                           func=self.program.canvas.toggleTiling,
                           args=(False,True),
                           menu=self.CanvasMenu.TilingMenu)
        
        #self.CanvasMenu.TilingMenu.addAction("Toggle Tiling")


    def newMenu(self,menuName, parentMenu=None):
        if not parentMenu:
            parentMenu = self
        
        parentMenu.addMenu

    def addMenuCust(self,MenuName:str="default",parentMenu:QMenu=None,d=0):
        #if parentMenu is not specified, it will default to self
        if parentMenu==None:
            parentMenu = self
        
        #create menu with name
        menu = QMenu(MenuName)

        #assign the menu to the parent menu as attribute
        setattr(parentMenu,MenuName + "Menu",menu)
        parentMenu.addMenu(menu)
        
        #if d is less than 2, add two default menus
        #if d<2:
        #    self.addMenuCust("Default",menu,d+1)
        #    self.addMenuCust("Default2",menu,d+1)
        
        #parentMenu.addMenu(temp)
    
    def addMenuAction(self, actionName: str, func, args: list, menu: QMenu = None) -> QAction:
        if not menu:
            menu = self 
        action = QAction(QIcon("Resources/icons/plus.png").pixmap(self.icon_size,self.icon_size), 
                        actionName,
                         menu)

        menu.addAction(action)

        action.triggered.connect(lambda: func(*args))

        return action
        
    
        