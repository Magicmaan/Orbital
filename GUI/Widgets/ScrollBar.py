from PySide6.QtCore import Qt, QRect, QSize, QPoint
from PySide6.QtGui import QPainter, QColor, QPixmap
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit, QScrollBar
from GUI.Widgets.WidgetUtils import drawPixelBorder

class CustomScrollBar(QScrollBar):
    def __init__(self, orientation=Qt.Vertical, parent=None):
        super().__init__(orientation, parent)
        self.setOrientation(orientation)
        self.setFixedWidth(24)  # Set the width of the scroll bar

    def paintEvent(self, event):
        painter = QPainter(self)

        # Draw background
        painter.fillRect(self.rect(), QColor(51, 51, 51))  # Dark gray background

        # Determine the position and size of the handle
        handle_rect = self._handle_rect()

        # Draw the handle
        painter.setBrush(QColor(102, 102, 102))  # Light gray handle
        painter.setPen(Qt.NoPen)
        size = 24

        path = "Resources/icons/scrollbar.png"
        drawPixelBorder(self,painter,QPixmap(path))
        #painter.drawPixmap(QPoint(0,0),QPixmap("Resources/icons/scrollbar.png").scaled(size, size, Qt.KeepAspectRatio, Qt.FastTransformation))

        # Optionally, draw top and bottom arrow buttons
        self._draw_arrows(painter)

    def _handle_rect(self):
        """Calculate the rectangle representing the handle position and size."""
        total_length = self.height() if self.orientation() == Qt.Vertical else self.width()
        handle_length = self.pageStep() / self.maximum() * total_length

        # Calculate the start position of the handle
        pos = self.sliderPosition() / self.maximum() * total_length
        if self.orientation() == Qt.Vertical:
            return QRect(0, pos, self.width(), handle_length)
        else:
            return QRect(pos, 0, handle_length, self.height())

    def _draw_arrows(self, painter):
        """Optional method to draw custom arrows on the scroll bar."""
        arrow_color = QColor(136, 136, 136)  # Gray arrows

        # Top arrow
        painter.setBrush(arrow_color)
        painter.setPen(Qt.NoPen)
        top_arrow = QRect(0, 0, self.width(), 20)
        painter.drawPolygon([
            top_arrow.topLeft(),
            top_arrow.topRight(),
            top_arrow.center()
        ])

        # Bottom arrow
        bottom_arrow = QRect(0, self.height() - 20, self.width(), 20)
        painter.drawPolygon([
            bottom_arrow.bottomLeft(),
            bottom_arrow.bottomRight(),
            bottom_arrow.center()
        ])

    def sizeHint(self):
        return QSize(20, 100)