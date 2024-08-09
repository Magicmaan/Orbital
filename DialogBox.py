from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QDialog, QDialogButtonBox, QLabel, QVBoxLayout,
                               QWidget)


class FileSelector(QDialog):
    def __init__(self) -> None:
        super().__init__()


class SuccessDialog(QDialog):
    def __init__(self) -> None:
        super().__init__()

class ErrorDialog(QDialog):
    def __init__(self,error,title,synopsis=None,actions=None) -> None:
        super().__init__()

        self.setWindowTitle(title)

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel(error)
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

        self.exec()