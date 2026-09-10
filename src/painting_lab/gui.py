import sys

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


class PaintingLabWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Painting Lab")
        self.resize(900, 700)
        
        self.image_label = QLabel(
            "No image selected"
        )
        
        self.open_button = QPushButton(
            "Open Image"
        )
        
        self.open_button.clicked.connect(
            self.open_image
        )
        
        layout = QVBoxLayout()
        
        layout.addWidget(self.image_label)
        layout.addWidget(self.open_button)
        
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
            pixmap = QPixmap(file_path)
            
            self.image_label.setPixmap(pixmap)
            
        
def run_app():
    app = QApplication(sys.argv)
        
    window = PaintingLabWindow()
    window.show()
        
    sys.exit(app.exec())
        

if __name__ == "__main__":
    run_app()
    