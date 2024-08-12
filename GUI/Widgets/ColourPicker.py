from PySide6.QtWidgets import QApplication, QWidget, QSizePolicy
from PySide6.QtGui import QPainter, QColor, QPixmap
from PySide6.QtCore import Qt

from GUI.Decorators import PixelBorder, sizePolicy


class RGBSpectrumWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("RGB Spectrum")
        self.setFixedSize(255, 255)
        self.setContentsMargins(0,0,0,0)
        self.spectrum_pixmap = None  # Cache for the spectrum pixmap
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    def generateSpectrum(self):
        width = 128
        height = 128

        # Create a QPixmap to cache the RGB spectrum
        pixmap = QPixmap(width, height)
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)

        # Draw the RGB spectrum onto the pixmap
        for x in range(width):
            for y in range(height):
                r = int(255 * (x / width))   # Red increases along the X-axis
                g = int(255 * (y / height))  # Green increases along the Y-axis
                b = 128  # Fixed blue component

                color = QColor(r, g, b)
                painter.setPen(color)
                painter.drawPoint(x, y)

        painter.end()
        self.spectrum_pixmap = pixmap

    def paintEvent(self, event):
        if self.spectrum_pixmap is None or self.spectrum_pixmap.size() != self.size():
            self.generateSpectrum()

        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.spectrum_pixmap)
        painter.end()