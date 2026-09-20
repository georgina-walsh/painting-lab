import sys

from PIL.ImageQt import ImageQt

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from painting_lab.basic_transformations import create_value_study
from painting_lab.drawing import (
    create_simple_line_drawing,
    create_detailed_line_drawing,
    create_value_based_line_drawing,
)
from painting_lab.image_io import load_image


class PaintingLabWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("PaintPal by Painting Lab")
        self.resize(900, 700)
        
        self.image_label = QLabel("No image selected")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setMinimumSize(400, 300)
        
        self.open_button = QPushButton("Open Image")
        self.open_button.clicked.connect(self.open_image)
        
        self.value_button = QPushButton("Value Study")
        self.value_button.clicked.connect(self.show_value_study)
        
        self.value_selector = QComboBox()
        self.value_selector.addItem("3 Values", 3)
        self.value_selector.addItem("5 Values", 5)
        
        self.line_selector = QComboBox()
        
        self.line_selector.addItem("Simple", "simple")
        self.line_selector.addItem("Detailed", "detailed")
        self.line_selector.addItem("Value-Based", "value_based")
        
        self.line_button = QPushButton("Generate Line Drawing")
        self.line_button.clicked.connect(self.show_line_drawing)
        
        self.original_button = QPushButton("Show Original")
        self.original_button.clicked.connect(self.show_original)
        
        # Main layout: image on the left, controls on the right
        main_layout = QHBoxLayout()


        # LEFT: Image preview
        main_layout.addWidget(self.image_label, 3)


        # RIGHT: Control panel
        controls_layout = QVBoxLayout()

        controls_layout.addWidget(self.open_button)


        # Value Study section
        value_group = QGroupBox("Value Study")

        value_layout = QVBoxLayout()

        value_layout.addWidget(self.value_selector)
        value_layout.addWidget(self.value_button)

        value_group.setLayout(value_layout)
        
        controls_layout.addWidget(value_group)
        
        # Line Drawing Section
        line_group = QGroupBox("Line Drawing")
        
        line_layout = QVBoxLayout()
        
        line_layout.addWidget(self.line_selector)
        line_layout.addWidget(self.line_button)
        
        line_group.setLayout(line_layout)

        controls_layout.addWidget(line_group)


        # Original image button
        controls_layout.addWidget(self.original_button)

        # Keep controls at the top of the panel
        controls_layout.addStretch()


        # Put the controls inside their own widget
        controls_widget = QWidget()
        controls_widget.setLayout(controls_layout)

        main_layout.addWidget(controls_widget, 1)


        # Set the main window content
        container = QWidget()
        container.setLayout(main_layout)

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
            self.current_pixmap = self.original_pixmap
            
            self.display_image()
            
            
    def display_image(self):
        if hasattr(self, "current_pixmap"):
            scaled_pixmap = self.current_pixmap.scaled(
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
        levels = self.value_selector.currentData()
        
        value_image = create_value_study(
            image,
            levels=levels,
        )
        
        qt_image = ImageQt(value_image)
        self.current_pixmap = QPixmap.fromImage(qt_image)
        
        self.display_image()
        
        
    def show_line_drawing(self):
        if not hasattr(self, "image_path"):
            return
        
        image = load_image(self.image_path)
        
        selected = self.line_selector.currentData()
        
        if selected == "simple":
            result = create_simple_line_drawing(image)
            
        elif selected == "detailed":
            result = create_detailed_line_drawing(image)
            
        elif selected == "value_based":
            result = create_value_based_line_drawing(image)
            
        else:
            return
        
        qt_image = ImageQt(result)
        
        self.current_pixmap = QPixmap.fromImage(qt_image)
        
        self.display_image()
        
        
    def show_original(self):
        if not hasattr(self, "original_pixmap"):
            return
        
        self.current_pixmap = self.original_pixmap
        self.display_image()
            
        
def run_app():
    app = QApplication(sys.argv)
        
    window = PaintingLabWindow()
    window.show()
        
    sys.exit(app.exec())
        

if __name__ == "__main__":
    run_app()
    