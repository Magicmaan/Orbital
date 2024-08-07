from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import sys

from Widgets.CanvasWindow import *
from Program import Program




class MainWindow(QMainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setWindowTitle("MagicDraw")
        self.setMinimumSize(800, 600)  # Minimum size for the window

        self.createWidgets()
        self.createMenus()

    def createWidgets(self) -> bool:
        # Create a central widget and a layout to manage it
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)

        # Create and configure the Canvas widget
        self.canvas = Canvas()
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Add the Canvas widget to the layout
        layout.addWidget(self.canvas)
        layout.addStretch()  # To fill the remaining space if needed

        # Set the central widget for the MainWindow
        self.setCentralWidget(central_widget)
        return True

    def createMenus(self) -> bool:
        toolbar = self.menuBar().addMenu("&File")

        self.newFile_action = self.createAction("New File", toolbar, self.NewFile)
        return True

    def createAction(self, text: str, menu: QMenu, slot) -> QAction:
        action = QAction(text, self)
        menu.addAction(action)
        action.triggered.connect(slot)
        return action

    def NewFile(self):
        print("New File!!")
        return True

styleSheet = """
    background-color: red;
    color: black;
    padding: 0px;
    margin: 0px;
    border: 0;  
    border-radius: 0px; 

    QWidget{
        background-color: green;
    }

"""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = Program()
    #app.setStyleSheet(styleSheet)
    window.setStyleSheet(styleSheet)
    window.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    # Set the application-wide font
    font = QFont("Minecraft", 14)  # You can specify the font family, size, and weight
    app.setFont(font)

    window.show()
    sys.exit(app.exec())
