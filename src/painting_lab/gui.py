import sys
from PySide6.QtWidgets import (
    QApplication,
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
        
        layout = QVBoxLayout()
        
        layout.addWidget(self.image_label)
        layout.addWidget(self.open_button)
        
        container = QWidget()
        container.setLayout(layout)
        
        self.setCentralWidget(container)
        
        
def run_app():
    app = QApplication(sys.argv)
        
    window = PaintingLabWindow()
    window.show()
        
    sys.exit(app.exec())
        

if __name__ == "__main__":
    run_app()
    