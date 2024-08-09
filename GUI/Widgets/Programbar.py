from PySide6.QtGui import QAction, QColor
from PySide6.QtWidgets import QMenu

from Resources.external.Neomorphism import *


def NewFile():
    print("New File!!")
    return True

def defaultAction():
    print("Action Hit")
    return True

class Programbar():
    def __init__(self, program) -> None:
        if not program:
            return
        
        self.program = program
        self.tbar = program.menuBar()
        self.menus = {}
        self.menufuncs = {}

        # Initialize neumorphic styles (you can adjust these as needed)
        self.outside = [{"outside": True, "offset": [6, 6], "blur": 0, "color": QColor(255, 0, 0, 255)},
                        {"outside": True, "offset": [-6, -6], "blur": 0, "color": QColor(255, 58, 58, 255)}]
        self.inside = [{"inside": True, "offset": [6, 6], "blur": 8, "color": QColor(255, 0, 0, 255)},
                       {"inside": True, "offset": [-6, -6], "blur": 8, "color": QColor(255, 58, 58, 255)}]
        
        self.populate()
    
    def populate(self) -> bool:
        self.addMenu("File")
        self.addMenu("Edit")
        self.addMenu("Canvas")
        self.addMenu("Tools")
        self.addMenu("Select")
        self.addMenu("View")

        return True
    
    def addMenu(self, title, func=defaultAction, icon=False) -> bool:
        try:
            menu = self.tbar.addMenu(f"&{title}")
            self.menus[title] = menu
        except Exception as e:
            print(f"Failed to add Menu {title}: {e}")
            return False
        
        self.menufuncs[title] = self.addItem("Default", func, False, self.menus[title])
        return True

    def addItem(self, title, func, icon=False, subMenu=None) -> bool:
        if subMenu is None:
            subMenu = self.tbar
        
        action = QAction(title, subMenu)
        subMenu.addAction(action)
        action.triggered.connect(func)
        
        # Apply neumorphic style to the menu item
        self.apply_neumorphic_style(action)
        
        return action

    def apply_neumorphic_style(self, action):
        # Apply styling to the menu item if possible
        # This can be quite limited with QActions since they are not QWidget based
        # For complete neumorphic styling, consider creating a custom QWidget-based menu
        menu_widget = self.tbar.findChild(QMenu, action.text())
        if menu_widget:
            # Wrap in a neumorphic style widget (BoxShadowWrapper or similar)
            # Note: Menu widgets may need custom handling as QAction itself doesn't support complex styling
            wrapper = BoxShadowWrapper(menu_widget, self.outside, border=1, disable_margins=True)
            menu_widget.setParent(wrapper)
            wrapper.show()