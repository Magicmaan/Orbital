import sys
from os.path import exists
from typing import Type

from PySide6.QtCore import QPoint, QRect, Qt
from PySide6.QtGui import QPainter, QPixmap, QTransform, QColor

from DialogBox import ErrorDialog, SuccessDialog

IMPORT_TYPES = ("PNG", "JPEG", "BMP")
EXPORT_TYPES = ("PNG","JPEG","BMP")

def exportTexture(image,path:str,format:str="png",) -> bool:
        imageTexture = image.image
        if exists(path):
            if not imageTexture.isNull():
                if format.upper() in EXPORT_TYPES:
                    saveState = imageTexture.save(f"{path}{image.name}.{format}",format)


            else:
                ErrorDialog("image is Null","Null Image")
                return False
        else:
            ErrorDialog("Invalid Filepath","Invalid Filepath")#
            return False
        
        if saveState:
            ErrorDialog("Success ig", "Buh")
            return True
        else:
            ErrorDialog("Save Error","save error")
            return False


def removePadding(object):
    object.setContentsMargins(0, 0, 0, 0)    

    if object.layout():
        layout = object.layout()  # Get the layout object
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

def drawPixelBorder(object, painter: QPainter,pmap:QPixmap,edgeSize=2,scale=2,Fill=True,FillColour=False):
    es = edgeSize  # Size of the edge sections
    w,h = pmap.width(),pmap.height()

    # Calculate the amount to shrink the rect
    shrink = es * scale
    
    # Shrink the rect
    shrunk_rect = object.rect().adjusted(
        shrink, shrink, 
        -shrink, -shrink
    )

    if Fill:
        if FillColour:
            painter.fillRect(shrunk_rect, FillColour)
        else:
            #fill in main colour
            painter.fillRect(shrunk_rect, pmap.toImage().pixelColor(pmap.width()//2, pmap.height()//2))  # Green color
    
    #sides ----------------------------------------------------------------
    top_cutout = QRect(es,0,w-es-1,2)
    _drawHorizontal(painter, pmap, top_cutout, 0, es, scale)

    bot_cutout = QRect(es,h-es,w-es-1,h)
    _drawHorizontal(painter, pmap, bot_cutout, object.height()-shrink, es, scale)

    left_cutout = QRect(0,es,es,h-es-1)
    _drawVertical(painter, pmap, left_cutout, 0, es, scale)

    right_cutout = QRect(w-es,es,w,h-es-1)
    _drawVertical(painter, pmap, right_cutout, object.width()-shrink, es, scale)


    #corners ---------------------------------------------------------------
    top_left_cutout, top_left_paste = QRect(0, 0, es, es), QPoint(0,0) # Top-left corner
    _drawCorner(painter, pmap, top_left_cutout, top_left_paste,scale) #top-Left

    bottom_left_cutout,bottom_left_paste = QRect(0, h-es, es, h), QPoint(0, object.height()-shrink)  # Bottom-left corner (adjust as needed)
    _drawCorner(painter, pmap, bottom_left_cutout, bottom_left_paste, scale)  # Draw bottom-left

    bottom_right_cutout,bottom_right_paste = QRect(w-es, h-es, w, h), QPoint(object.width()-shrink, object.height()-shrink)  # Bottom-left corner (adjust as needed)
    _drawCorner(painter, pmap, bottom_right_cutout, bottom_right_paste, scale)  # Draw bottom-right

    top_right_cutout,top_right_paste = QRect(w-es, 0, w, es), QPoint(object.width()-shrink, 0)  # Bottom-left corner (adjust as needed)
    _drawCorner(painter, pmap, top_right_cutout, top_right_paste, scale)  # Draw top-right


def _drawHorizontal(p: QPainter, pmap: QPixmap, cut: QRect, startY, cornerSize: int, scale: float):
    obj = p.device()
    # Extract and scale the pixmap region
    fpmap = pmap.copy(cut)
    fpmap = fpmap.scaled(
        fpmap.width() * scale, 
        fpmap.height() * scale, 
        Qt.AspectRatioMode.IgnoreAspectRatio, 
        Qt.TransformationMode.FastTransformation
    )
    
    # Calculate the width of the scaled pixmap
    scaled_width = fpmap.width()
    
    # Determine the starting point for tiling
    start_x = cornerSize*scale
    end_x = p.device().width() - (cornerSize*scale)
    
    # Draw the pixmap repeatedly across the side
    for x in range(start_x, end_x, scaled_width):
        if x >= obj.width() - scaled_width - (cornerSize*scale):
           p.drawPixmap(QPoint(obj.width() - scaled_width - (cornerSize*scale), startY), fpmap)
           break

        p.drawPixmap(QPoint(x, startY), fpmap)

def _drawVertical(p: QPainter, pmap: QPixmap, cut: QRect, startX, cornerSize: int, scale: float):
    obj = p.device()
    # Extract and scale the pixmap region
    fpmap = pmap.copy(cut)
    fpmap = fpmap.scaled(
        fpmap.width() * scale, 
        fpmap.height() * scale, 
        Qt.AspectRatioMode.IgnoreAspectRatio, 
        Qt.TransformationMode.FastTransformation
    )
    
    # Calculate the width of the scaled pixmap
    scaled_height = fpmap.height()
    
    # Determine the starting point for tiling
    start_y = cornerSize*scale
    end_y = p.device().height() - (cornerSize*scale)
    
    # Determine the starting point for tiling
    start_y = cornerSize * scale
    end_y = p.device().height() - (cornerSize * scale)

    # Draw the pixmap repeatedly down the side
    for y in range(start_y, end_y, scaled_height):
        if y >= obj.height() - scaled_height - (cornerSize * scale):
            p.drawPixmap(QPoint(startX, obj.height() - scaled_height - (cornerSize * scale)), fpmap)
            break

        p.drawPixmap(QPoint(startX, y), fpmap)
    
def _drawCorner(p,pmap,cut,paste,scale):
            fpmap = pmap.copy(cut)
            fpmap = fpmap.scaled(fpmap.width()*scale, fpmap.height()*scale, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.FastTransformation)

            transform = QTransform().scale(-1, -1)  # Create a transformation that flips horizontally
            #fpmap = fpmap.transformed(transform, mode=Qt.TransformationMode.FastTransformation)

            p.drawPixmap(paste, fpmap) 