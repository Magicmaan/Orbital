import sys

from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication

from Program import Program

#TODO:
# 1. add toml file for configuration
# 2. add hot-loading of configuration + assets
# 3. Add Theme config (to make 2 more fun)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = Program()

    # Set the application-wide font
    font = QFont("mai10", 14)  # You can specify the font family, size, and weight
    app.setFont(font)

    window.show()
    sys.exit(app.exec())
