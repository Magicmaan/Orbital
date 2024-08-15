from PySide6.QtWidgets import QApplication, QWidget, QSizePolicy, QVBoxLayout, QSlider, QLabel
from PySide6.QtGui import QMouseEvent, QPainter, QColor, QPixmap, qRgb
from PySide6.QtCore import Qt, QPoint, QRect, Signal, Slot

from math import sqrt, atan2, sin, cos, tan, degrees, radians

from GUI.Decorators import PixelBorder, sizePolicy


from GUI.Decorators import PixelBorder, sizePolicy




class ColourPicker(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setContentsMargins(20,20,20,20)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.colorWheel = RGBSpectrumWidget()
        self.colorWheel.setSize(128)
        self.opacitySlider = QSlider(Qt.Horizontal)
        self.opacitySlider.setContentsMargins(0,0,0,0)
        self.opacitySlider.setRange(0,255)
        # Set background color using setStyleSheet
        self.setStyleSheet("background-color: lightblue;")
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.colorWheel)
        self.layout().addWidget(self.opacitySlider)

        self.opacitySlider.valueChanged.connect(self._updateAlpha)
        self.redlabel = QLabel("0")
        self.layout().addWidget(self.redlabel)

        self.greenlabel = QLabel("0")
        self.layout().addWidget(self.greenlabel)

        self.bluelabel = QLabel("0")
        self.layout().addWidget(self.bluelabel)

        self.colorWheel.colourChanged.connect(self._updateColour)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        print(f"Colour at: {self.getRGBA()}")
        self.update()
        super().mousePressEvent(event)

    def getOpacity(self) -> int:
        
        return self.opacitySlider.value()

    def getRGB(self) -> QColor:
        return self.colorWheel.getRGB()
    
    def getRGBA(self) -> QColor:
        colour = self.getRGB()
        opacity = self.getOpacity()
        print(type(colour))
        print(opacity)
        colour.setAlpha(opacity)
        return colour
    
    def setColour(self,colour:QColor):
        pass

    @Slot(QColor)
    def _updateColour(self, value):
        self.colour = value

        self.redlabel.setText(str(value.red()))
        self.greenlabel.setText(str(value.green()))
        self.bluelabel.setText(str(value.blue()))
    
    def _updateAlpha(self, value):
        self.colorWheel.opacity = value




@PixelBorder
class RGBSpectrumWidget(QWidget):
    colourChanged = Signal(QColor)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("RGB Spectrum")
        self.setContentsMargins(0,0,0,0)
        self.setFixedSize(255,160)
        self._PixmapSpectrum = None  # Cache for the spectrum pixmap
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.backgroundFill = QColor(255,255,255,255)
        self._displayModes = (self._RGBSpectrum, self._HSVSpectrum, self._HSLSpectrum, self._CMYKSpectrum)#
        self.currentDisplayMode = self._displayModes[1]

        self.colour = None
        self.opacity = 255
        self.mousePos = QPoint(0,0)
        self.lastMousePos = QPoint(0,0)

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
        width,height = 128,128
        self._PixmapSpectrum = self.currentDisplayMode(width,height)

    def paintEvent(self, event):
        if self._PixmapSpectrum is None or self._PixmapSpectrum.size() != self.size():
            self.generateSpectrum()

        painter = QPainter(self)

        if self.backgroundFill:
            painter.fillRect(self.rect(),self.backgroundFill)

        #draw spectrum
        painter.setOpacity(self.opacity/255)
        painter.drawPixmap(0, 0, self._PixmapSpectrum)
        painter.setOpacity(1)

        painter.setPen(QColor(255,255,255))
        pos = QRect(self.mousePos.x(),self.mousePos.y(),5,5)
        painter.drawRect(pos)

        painter.end()

        self.getRGB()
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton: 
            
            self.mousePos = event.localPos().toPoint()
            #print(f"Clicked color: {self.getRGB()} at: {self.mousePos}")  # Prints the color in hex format

        self.update()
    
    def mouseMoveEvent(self, event):
        if event.button() == Qt.LeftButton: 
            
            self.mousePos = event.localPos().toPoint()
        self.update()
        #return super().mouseMoveEvent(event)

    def _getColourAtPoint(self,position:QPoint) -> QColor:
        if (position.x() >= 0 and position.x() <= self.width()) and (position.y() >= 0 and position.y() <= self.height()):
            pmap = self._PixmapSpectrum
            colour = pmap.toImage().pixelColor(position)
            colour.setAlpha(self.opacity)
            return colour

    @Slot()
    def getRGB(self) -> QColor:
        if not self.colour or self.mousePos != self.lastMousePos:
            self.colour = self._getColourAtPoint(self.mousePos)
            #print("COLOUR IS:" + str(self.colour.getRgb()))
            self.colourChanged.emit(self.colour)
            self.backgroundFill = self.colour
        return self.colour
        
    def setSize(self,squareSize:int):   
        if squareSize > 25:
            self.setFixedSize(squareSize,squareSize)

        return


