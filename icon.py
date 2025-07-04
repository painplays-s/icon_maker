import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QLabel, QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt
from PIL import Image

class IconMaker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PNG to ICO Converter")
        self.setMinimumSize(400, 200)
        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.info_label = QLabel("Select a PNG file to convert to .ICO")
        self.info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.info_label)

        self.select_button = QPushButton("Select PNG File")
        self.select_button.clicked.connect(self.select_png)
        layout.addWidget(self.select_button)

    def select_png(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select PNG Image", "", "PNG Files (*.png)"
        )
        if not file_path:
            return

        try:
            img = Image.open(file_path)
            if img.size[0] != img.size[1]:
                raise ValueError("Image must be square (e.g. 512x512)")
            
            # Ask user where to save the ICO file
            default_name = "icon.ico"
            default_dir = os.path.dirname(file_path)
            save_path, _ = QFileDialog.getSaveFileName(
                self, "Save ICO File", 
                os.path.join(default_dir, default_name),
                "ICO Files (*.ico)"
            )
            
            if not save_path:
                return  # User canceled the save dialog
                
            img.save(save_path, format='ICO', sizes=[
                (16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)
            ])

            QMessageBox.information(self, "Success", f"ICO file saved at:\n{save_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to convert icon:\n{str(e)}")

def main():
    app = QApplication(sys.argv)
    window = IconMaker()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
