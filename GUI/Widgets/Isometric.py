from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter,QPen,QColor,QPixmap

#TODO:
# 1. take in painter
# 2. based on line direction, rotate to align with isometric representation
# 3. draw line using linear coordinates i.e. painter + x,y,z to move it on the x axis etc in 3d coords
#    - shit, thats just matrix math
#    - test tmrw less goooo


def checkLineDirection(painter:QPainter,x1, y1, x2, y2):
    if x1 == x2:  # Vertical line
        pass
    elif y1 == y2:  # Horizontal line
        if x1 > x2:  # Going left
            return -30
        else:  # Going right
            return 30
    else:
        return None  # Line is neither vertical nor horizontal

def paintisometricCube(self,painter: QPainter):

    
    painter.save()
    painter.setPen(QPen(QColor(0, 0, 0, 255), 1))  # Set the pen color to transparent and width to 1
    painter.rotate(30)
    painter.drawLine(100, 100, 500, 100)

    
    
    painter.restore()