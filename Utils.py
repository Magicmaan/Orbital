from PySide6.QtCore import *
from PySide6.QtGui import QFont, QFontDatabase
from PySide6.QtWidgets import *
import sys

#add font from string to application
#returns fontID 
#returns -1 if fail
def _addFont(path: str) -> int:
    font_id = QFontDatabase.addApplicationFont(path)
    if font_id == -1:
        print(f"Failed to load font {path}")
        return -1
    
    return font_id

#takes in application fontID and returns QFont
#if not valid, returns fallback Arial
def getFont(fontID: int,size: int=10) -> QFont:
    # Retrieve the family name of the loaded font
    font_families = QFontDatabase.applicationFontFamilies(fontID)
    if font_families:
        font = font_families[0]
        # Set the application-wide font using the custom font
        font = QFont(font, size)  # You can specify the size
    else: #fallback to return default font
        print(f"Failed to get font {fontID}")
        font = QFont("Arial", size)
    

    return font
    