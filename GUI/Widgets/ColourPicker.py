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
    def __init__(self, parent, target=None):
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

        self.target = target
        self.value = 0
        self.toAdd = 0
    def onMouseclick(self):
        QCursor.setPos(self.mapToGlobal(self.rect().center()))
        self.update()

    def onMouseMove(self):
        if self.mouseClicks.left:
            #self.setCursor(Qt.BlankCursor)
            toAdd = (self.mousePos.x() - self.mousePressPos.x()) / 40
            if self.mousePos.x() < 0 or self.mousePos.x() > self.width():
                QCursor.setPos(self.mapToGlobal(QPoint(self.width()/2,self.mousePos.y())))

            self.toAdd += toAdd 

            if self.toAdd > 255:
                self.toAdd = 255
            if self.toAdd < -255:
                self.toAdd = -255
        
        self.label.setText(f"{self.toAdd:+}")
        self.update()
    
    def onMouseRelease(self):
        self.value += int(self.toAdd)
        if self.value < 0:
            self.value = 0
        elif self.value > 255:
            self.value = 255

        self.toAdd = 0
        self.label.setText(str(self.value))
        
        #send update to colorWheel
        self.parent.colorWheel.setRGB(self.value)

        self.setCursor(Qt.ArrowCursor)
        QCursor.setPos(self.mapToGlobal(self.rect().center()))
        self.update()


class ColourPicker(QWidget):
    #TODO:
    # 1. Rework so interactions go through this widget.
    #    i.e. mouse event on spectrum -> sends event with colour to ColourPicker to update
    #         -> spectrum gets current colour from ColourPicker
    #         -> sliders get current colour from ColourPicker
    #    
    #    This way, the ColourPicker is the central hub for colour changes.
    #    The child widgets shouldn't store any information, they are only an interface.

    # 2. Add colour sliders , the R slider currently is a test.
    #    - tap will enter text entry
    #    - drag will change value by modifer, displaying it whilst dragging
    #      - will show percentage, and hue change as background
    #      - shift to step by 10?

    # 3. Improve spectrumWidget
    #    - display opacity nicely
    #    - show complementary colour on wheel
    #    - update from colour picker
    #    - shift to move radius
    #    - alt to rotate around wheel



    def __init__(self, parent=None):
        super().__init__(parent)

        self.setContentsMargins(20,20,20,20)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.colorWheel = RGBSpectrumWidget(self)
        self.colorWheel.setSize(255,160)

        self.opacitySlider = QSlider(Qt.Horizontal)
        self.opacitySlider.setContentsMargins(0,0,0,0)
        self.opacitySlider.setRange(0,255)
        self.opacitySlider.setValue(255)

        # Set background color using setStyleSheet
        self.setStyleSheet("background-color: lightblue;")
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.colorWheel)
        self.layout().addWidget(self.opacitySlider)
        self.layout().setSpacing(0)
        self.layout().setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout().setContentsMargins(10,10,10,10)
        self.opacitySlider.valueChanged.connect(self._updateAlpha)


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
        

        #self.redlabel.valueChanged.connect(self._updateColour)


    def getOpacity(self) -> int:
        
        return self.opacitySlider.value()

    def getRGB(self) -> QColor:
        return self.colorWheel.getRGB()
    
    def getRGBA(self) -> QColor:
        colour = self.getRGB()
        opacity = self.getOpacity()
        colour.setAlpha(opacity)
        return colour
    
    def setColour(self,colour:QColor):
        pass

    @Slot(QColor)
    def _updateColour(self, value):
        self.colour = value

        #self.colorWheel.setRGB(value.red(),value.green(),value.blue())
        self.redlabel.label.setText(str(value.red()))
        self.greenlabel.setText(str(value.green()))
        self.bluelabel.setText(str(value.blue()))


    
    def _updateAlpha(self, value):
        self.colorWheel.opacity = value
        self.update()




@PixelBorder
@mouseClick
class RGBSpectrumWidget(QWidget):
    #TODO: Fix coordinate out of range on mouse move
    #      to do with centering, ur not correcting for offset
    #      - fix by getting the center of the widget and then calculating the distance from the center


    colourChanged_S = Signal(QColor)

    def __init__(self, parent=None):
        """
        Initializes the ColourPicker widget.
        """
        super().__init__(parent)
        
        # Set window title
        self.setWindowTitle("RGB Spectrum")
        # Enable mouse tracking
        self.setMouseTracking(True)
        self.parent = parent

        # Set margins and fixed size
        self.setContentsMargins(5, 5, 5, 5)
        self.resize(160, 160)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Cache for the spectrum pixmap
        self._PixmapSpectrum = None
        # Display modes for the spectrum
        self._spectrumModes = (self._RGBSpectrum, self._HSVSpectrum, self._HSLSpectrum, self._CMYKSpectrum)
        self.currentSpectrum = self._spectrumModes[1]  # Default to HSV Spectrum
        
        # Background fill color
        self.backgroundFill = QColor(255, 255, 255, 255)
        self.mousePos = self.rect().center()

        self.colour = QColor(255, 0, 0, 255)
        self.opacity = 255

        
        self.colourChanged_S.connect(self.parent._updateColour)
        # Connect colour changed signal to the current tool's update colour method
        self.colourChanged_S.connect(QApplication.instance().program.tools.current_tool._updateColour)

        

        
        
        

    def _RGBSpectrum(self):
        pass

    def _HSVSpectrum(self,width,height):

        radius = min(width, height) // 2

        # Create a QPixmap to cache the HSV color wheel
        pixmap = QPixmap(width, height)
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)

        center_x = width // 2
        center_y = height // 2

        for x in range(width):
            for y in range(height):
                dx = x - center_x
                dy = y - center_y
                distance = sqrt(dx*dx + dy*dy)
                
                if distance <= radius:
                    # Calculate the hue based on the angle from the center
                    hue = (degrees(atan2(dy, dx)) + 360) % 360

                    # Saturation is based on the distance from the center
                    saturation = distance / radius

                    # Fixed value (brightness)
                    value = 1.0

                    # Convert HSV to QColor
                    color = QColor()
                    color.setHsvF(hue / 360, saturation, value)
                    painter.setPen(color)
                    painter.drawPoint(x, y)
        painter.end()

        return pixmap

    def _HSLSpectrum(self):
        pass

    def _CMYKSpectrum(self):
        pass

    def OpacitySpectrum(self):
        pass
    
    def getComplement(self):
        pass

    def getAnalogous(self,offset):
        pass

    def generateSpectrum(self):
        width,height = 160,160  
        self._PixmapSpectrum = self.currentSpectrum(width,height)

    def paintEvent(self, event):
        if self._PixmapSpectrum is None or self._PixmapSpectrum.size() != self.size():
            self.generateSpectrum()

        painter = QPainter(self)

        #draw spectrum
        painter.setOpacity(self.opacity/255)
        
        x = (self.width() - self._PixmapSpectrum.width()) // 2
        y = (self.height() - self._PixmapSpectrum.height()) // 2
        
        # Draw the pixmap centered in the widget
        painter.drawPixmap(x, y, self._PixmapSpectrum)
        painter.setOpacity(1)

        if self.mouseClicks.left:
            x = self.mousePos.x()
            y = self.mousePos.y()
        else:
            x = self.mouseReleasePos.x()
            y = self.mouseReleasePos.y()
        
        selectorSize = 6
        
        #draw selector
        painter.setPen(QColor(255,0,255))
        pen = QPen()
        pen.setWidth(2)
        painter.setPen(pen)
        pos = QRect(x-selectorSize/2,y-selectorSize/2,selectorSize,selectorSize)
        painter.drawRoundedRect(pos,2,2)

    def snaptoCircle(self):
         # Get the center of the widget
        center = QPoint(self.width() // 2, self.height() // 2)
        
        # Calculate the radius of the circle (assuming a square widget)
        radius = min(self.width(), self.height()) // 2
        # Calculate the distance from the center to the position
        dx = self.mousePos.x() - center.x()
        dy = self.mousePos.y() - center.y()

        distance_squared = dx ** 2 + dy ** 2

        # If outside the circle, calculate the closest point on the edge of the circle
        distance = sqrt(distance_squared)
        scale = radius / distance
        
        if distance_squared <= radius ** 2:
            return
        
        # Calculate the closest point on the circle's edge
        closest_x = center.x() + int(dx * scale)
        closest_y = center.y() + int(dy * scale)
        closest_point = QPoint(closest_x, closest_y)
        
        self.mousePos = closest_point

    def _getColourAtPoint(self,position:QPoint) -> QColor:
        # Get the center of the widget
        center = QPoint(self.width() // 2, self.height() // 2)
        
        # Calculate the radius of the circle (assuming a square widget)
        radius = min(self.width(), self.height()) // 2
        # Calculate the distance from the center to the position
        dx = position.x() - center.x()
        dy = position.y() - center.y()
        distance_squared = dx ** 2 + dy ** 2
        
        pos = position
        # Check if the position is within the circle
        if distance_squared <= radius ** 2:
            pos = position
        else:
            pos = self.snaptoCircle()
        
        pmap = self._PixmapSpectrum
        colour = pmap.toImage().pixelColor(pos)
        colour.setAlpha(self.opacity)
        return colour

    def onMouseClick(self):
        self.snaptoCircle()

    def onMouseMove(self):
        self.snaptoCircle()

        if self.mouseClicks.left:
            self.getRGB()
            self.update()
        
    def setRGB(self,red:int=None,green:int=None,blue:int=None) -> None:
        if red:
            if 0 <= red <= 255:
                self.colour.setRed(red)
        if green:
            if 0 <= green <= 255:
                self.colour.setGreen(green)
        if blue:
            if 0 <= blue <= 255:
                self.colour.setBlue(blue)
        
        self.colourChanged_S.emit(self.colour)

    @Slot()
    def getRGB(self) -> QColor:
        if not self.colour or self.mousePos != self.lastMousePos:
            colour = self._getColourAtPoint(self.mousePos)

            self.setRGB(colour.red(),colour.green(),colour.blue())

            self.backgroundFill = self.colour
            
        return self.colour
        
    def setSize(self,xSize:int,ySize:int):   
        if xSize > 25 and ySize > 25:
            self.setFixedSize(xSize,ySize)

        return


