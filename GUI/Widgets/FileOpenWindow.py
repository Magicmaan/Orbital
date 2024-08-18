from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QDialog
import sys

class FileOpenWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Open Example")
        self.setGeometry(100, 100, 300, 200)

        # Set window flags to prevent it from showing in the taskbar
        self.setWindowFlags(Qt.Tool)

        # Create layout
        layout = QVBoxLayout()

        # Create button to open file dialog
        self.open_button = QPushButton("Open File")
        self.open_button.clicked.connect(self.open_file_dialog)
        layout.addWidget(self.open_button)

        # Label to display selected file path
        self.file_label = QLabel("No file selected")
        layout.addWidget(self.file_label)

        self.setLayout(layout)

        self.selected_file = None

    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*);;Text Files (*.txt)")
        if file_path:
            self.file_label.setText(f"Selected file: {file_path}")
            self.selected_file = file_path
            self.accept()  # Close the dialog and return
