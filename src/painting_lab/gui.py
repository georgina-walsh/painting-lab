import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from painting_lab.basic_transformations import create_value_study
from painting_lab.image_io import load_image


class PaintingLabWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Painting Lab")
        self.resize(900, 700)
        
        self.image_label = QLabel("No image selected")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setMinimumSize(400, 300)
        
        self.open_button = QPushButton("Open Image")
        self.open_button.clicked.connect(self.open_image)
        
        self.value_button = QPushButton("Value Study")
        self.value_button.clicked.connect(self.show_value_study)
        
        layout = QVBoxLayout()
        
        layout.addWidget(self.image_label)
        layout.addWidget(self.open_button)
        layout.addWidget(self.value_button)
        
        container = QWidget()
        container.setLayout(layout)
        
        self.setCentralWidget(container)
        
        
    def open_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Image",
            "",
            "Images (*.png *.jpg *.jpeg)",
        )
    
        if file_path:
            self.image_path = file_path
            self.original_pixmap = QPixmap(file_path)
            
            self.display_image()
            
            
    def display_image(self):
        if hasattr(self, "original_pixmap"):
            scaled_pixmap = self.original_pixmap.scaled(
                self.image_label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
                )

            self.image_label.setPixmap(scaled_pixmap)
        
            
    def resizeEvent(self, event):
        self.display_image()

        super().resizeEvent(event)
        
    
    def show_value_study(self):
        if not hasattr(self, "image_path"):
            return
        
        image = load_image(self.image_path)
        value_image = create_value_study(image)
        qt_image = ImageQt(value_image)
        
        self.original_pixmap = QPixmap.fromImage(qt_image)
        self.display_image()
            
        
def run_app():
    app = QApplication(sys.argv)
        
    window = PaintingLabWindow()
    window.show()
        
    sys.exit(app.exec())
        

if __name__ == "__main__":
    run_app()
    