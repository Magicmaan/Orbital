import sys

from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication

from Program import Program

#FIX SIZE POLICY
#U SET IT TO USE A DECORATOR
#REVERT IT OR FIX IDIOT


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = Program(useCustomWindow=True)

    # Set the application-wide font
    font = QFont("Minecraft", 14)  # You can specify the font family, size, and weight
    app.setFont(font)

    window.show()
    sys.exit(app.exec())
