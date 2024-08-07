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