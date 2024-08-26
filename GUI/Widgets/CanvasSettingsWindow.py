from PySide6.QtWidgets import QApplication, QWidget, QSizePolicy, QVBoxLayout, QSlider, QLabel, QHBoxLayout
from PySide6.QtGui import QMouseEvent, QPainter, QColor, QPixmap, qRgb, QPen, QFont, QCursor
from PySide6.QtCore import Qt, QPoint, QRect, Signal, Slot

from math import sqrt, atan2, sin, cos, tan, degrees, radians

from GUI.Decorators import PixelBorder, sizePolicy, mouseClick


#RGBSpectrumWidget
 #multiple modes HSV,HSl etc
 #will change with opacity
 #show complementary colour on wheel


#colour sliders
 #Opacity, red, green, blue, value
 #draggable sliders to change
 #don't display value unless alt hold
 #will show percentage, and hue change as background

 #step factor to change how much sliders will change by

#colour selector
 #hold alt to choose
 #will show preview on colour picker
 
@PixelBorder
@mouseClick
class RGBSlider(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)
        self.setFixedWidth(50)
        self.setFixedHeight(20)
        self.setContentsMargins(0,0,0,0)
        
        self.setStyleSheet("background-color: none;")
        self.label = QLabel("0")
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.label)
        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0,0,0,0)
        self.layout().setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setFont(QFont("pixelated", 12))

        self.value = 0
        self.to_add = 0
    def onMouseclick(self):
        QCursor.setPos(self.mapToGlobal(self.rect().center()))
        self.update()

    def onMouseMove(self):
        if self.mouseClicks.left:
            #self.setCursor(Qt.BlankCursor)
            toAdd = (self.mousePos.x() - self.mousePressPos.x()) / 40
            if self.mousePos.x() < 0 or self.mousePos.x() > self.width():
                QCursor.setPos(self.mapToGlobal(QPoint(self.width()/2,self.mousePos.y())))

            self.to_add += toAdd 

            if self.to_add > 255:
                self.to_add = 255
            if self.to_add < -255:
                self.to_add = -255
        
        self.label.setText(f"{self.to_add:+}")
        self.update()
    
    def onMouseRelease(self):
        self.value += int(self.to_add)
        if self.value < 0:
            self.value = 0
        elif self.value > 255:
            self.value = 255

        self.to_add = 0
        self.label.setText(str(self.value))
        
        self.parent.colorWheel.setRGB(self.value)
        self.setCursor(Qt.ArrowCursor)
        QCursor.setPos(self.mapToGlobal(self.rect().center()))
        self.update()

@PixelBorder
class ViewportSettingsWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setContentsMargins(20,20,20,20)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setFixedHeight(200)


        self.opacitySlider = QSlider(Qt.Horizontal)
        self.opacitySlider.setContentsMargins(0,0,0,0)
        self.opacitySlider.setRange(0,255)
        self.opacitySlider.setValue(255)

        # Set background color using setStyleSheet
        self.setStyleSheet("background-color: lightblue;")
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.opacitySlider)
        self.layout().setSpacing(0)
        self.layout().setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout().setContentsMargins(10,10,10,10)


        sliderscontainer = QWidget()
        sliderscontainer.setLayout(QHBoxLayout())
        sliderscontainer.setFixedSize(180,30)
        self.layout().addWidget(sliderscontainer)
        sliderscontainer.layout().setSpacing(10)



        self.redlabel = RGBSlider(self)
        #self.redlabel.setRange(0,255)
        #self.redlabel.setFixedWidth(50)
        #self.redlabel.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)
        sliderscontainer.layout().addWidget(self.redlabel)
        self.greenlabel = QLabel("0")
        sliderscontainer.layout().addWidget(self.greenlabel)
        self.bluelabel = QLabel("0")
        sliderscontainer.layout().addWidget(self.bluelabel)
        
        
        self.greenlabel.setFont(QFont("pixelated", 12))
        self.bluelabel.setFont(QFont("pixelated", 12))