from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import sys
from os.path import exists
from DialogBox import ErrorDialog,SuccessDialog
from typing import Type

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

def drawPixelBorder(object, painter: QPainter,pmap,edgeSize,scale):

        # Define the size for scaling
        es = edgeSize  # Size of the edge sections


        # Calculate the amount to shrink the rect
        shrink_amount = es * scale
        
        # Shrink the rect
        shrunk_rect = object.rect().adjusted(
            shrink_amount, shrink_amount, 
            -shrink_amount, -shrink_amount
        )

        painter.fillRect(shrunk_rect, pmap.toImage().pixelColor(6, 6))  # Green color

        w,h = pmap.width(),pmap.height()

        top_cutout = QRect(es,0,es+2,2)
        drawHorizontal(painter, pmap, top_cutout, 0, es, scale)

        bot_cutout = QRect(es,h-es,es+2,h)
        drawHorizontal(painter, pmap, bot_cutout, object.height()-(es*scale), es, scale)

        left_cutout = QRect(0,es,es,es+1)
        drawVertical(painter, pmap, left_cutout, 0, es, scale)

        right_cutout = QRect(w-es,es,w,es+1)
        drawVertical(painter, pmap, right_cutout, object.width()-(es*scale), es, scale)


        top_left_cutout, top_left_paste = QRect(0, 0, es, es), QPoint(0,0) # Top-left corner
        drawCorner(painter, pmap, top_left_cutout, top_left_paste,scale) #top-Left

        bottom_left_cutout,bottom_left_paste = QRect(0, h-es, es, h), QPoint(0, object.height()-(es*scale))  # Bottom-left corner (adjust as needed)
        drawCorner(painter, pmap, bottom_left_cutout, bottom_left_paste, scale)  # Draw bottom-left

        bottom_right_cutout,bottom_right_paste = QRect(w-es, h-es, w, h), QPoint(object.width()-(es*scale), object.height()-(es*scale))  # Bottom-left corner (adjust as needed)
        drawCorner(painter, pmap, bottom_right_cutout, bottom_right_paste, scale)  # Draw bottom-right

        top_right_cutout,top_right_paste = QRect(w-es, 0, w, es), QPoint(object.width()-(es*scale), 0)  # Bottom-left corner (adjust as needed)
        drawCorner(painter, pmap, top_right_cutout, top_right_paste, scale)  # Draw top-right


        

def drawHorizontal(p: QPainter, pmap: QPixmap, cut: QRect, startY, cornerSize: int, scale: float):
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

def drawVertical(p: QPainter, pmap: QPixmap, cut: QRect, startX, cornerSize: int, scale: float):
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
        


def drawCorner(p,pmap,cut,paste,scale):
            fpmap = pmap.copy(cut)
            fpmap = fpmap.scaled(fpmap.width()*scale, fpmap.height()*scale, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.FastTransformation)

            transform = QTransform().scale(-1, -1)  # Create a transformation that flips horizontally
            #fpmap = fpmap.transformed(transform, mode=Qt.TransformationMode.FastTransformation)

            p.drawPixmap(paste, fpmap) 