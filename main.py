from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import sys


from Widgets.CanvasWindow import *
from Program import Program

    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = Program()
    window.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    # Set the application-wide font
    font = QFont("Minecraft", 14)  # You can specify the font family, size, and weight
    app.setFont(font)

    window.show()
    sys.exit(app.exec())
