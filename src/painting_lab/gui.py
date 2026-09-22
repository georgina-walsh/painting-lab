import sys

from PIL.ImageQt import ImageQt

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPalette, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QScrollArea,
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

from painting_lab.painting_stages import (
    create_colour_block_in,
    create_grisaille,
    create_imprimatura,
    create_verdaccio,
    extract_palette,
)


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
        
        self.grisaille_selector = QComboBox()
        
        self.grisaille_selector.addItem("8 Tones", 8)
        self.grisaille_selector.addItem("16 Tones", 16)
        
        self.grisaille_button = QPushButton("Generate Grisaille")
        self.grisaille_button.clicked.connect(self.show_grisaille)
        
        self.imprimatura_selector = QComboBox()
        
        self.imprimatura_selector.addItem("Burnt Sienna", "burnt_sienna")
        self.imprimatura_selector.addItem("Raw Umber", "raw_umber")
        
        self.imprimatura_button = QPushButton("Generate Imprimatura")
        self.imprimatura_button.clicked.connect(self.show_imprimatura)
        
        self.verdaccio_selector = QComboBox()
        
        self.verdaccio_selector.addItem("8 Tones", 8)
        self.verdaccio_selector.addItem("16 Tones", 16)
        
        self.verdaccio_button = QPushButton("Generate Verdaccio")
        self.verdaccio_button.clicked.connect(self.show_verdaccio)
        
        self.colour_selector = QComboBox()
        
        self.colour_selector.addItem("5 Colours", 5)
        self.colour_selector.addItem("8 Colours", 8)
        self.colour_selector.addItem("12 Colours", 12)
        
        self.colour_selector.setCurrentIndex(1)
        
        self.colour_button = QPushButton("Generate Colour Block-In")
        self.colour_button.clicked.connect(self.show_colour_block)
        
        self.palette_selector = QComboBox()
        
        self.palette_selector.addItem("5 Colours", 5)
        self.palette_selector.addItem("8 Colours", 8)
        self.palette_selector.addItem("12 Colours", 12)
        
        self.palette_selector.setCurrentIndex(1)
        
        self.palette_button = QPushButton("Extract Palette")
        self.palette_button.clicked.connect(self.show_palette)
        self.palette_layout = QHBoxLayout()
        
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
        
        # Grisaille Section
        grisaille_group = QGroupBox("Grisaille")
         
        grisaille_layout = QVBoxLayout()
         
        grisaille_layout.addWidget(self.grisaille_selector)
        grisaille_layout.addWidget(self.grisaille_button)
         
        grisaille_group.setLayout(grisaille_layout)
        
        controls_layout.addWidget(grisaille_group)
        
        # Imprimatura Section
        imprimatura_group = QGroupBox("Imprimatura")
        
        imprimatura_layout = QVBoxLayout()
        
        imprimatura_layout.addWidget(self.imprimatura_selector)
        imprimatura_layout.addWidget(self.imprimatura_button)
        
        imprimatura_group.setLayout(imprimatura_layout)
        
        controls_layout.addWidget(imprimatura_group)
        
        # Verdaccio Section
        verdaccio_group = QGroupBox("Verdaccio")
        
        verdaccio_layout = QVBoxLayout()
        
        verdaccio_layout.addWidget(self.verdaccio_selector)
        verdaccio_layout.addWidget(self.verdaccio_button)
        
        verdaccio_group.setLayout(verdaccio_layout)
        
        controls_layout.addWidget(verdaccio_group)
        
        # Colour Block-In Section
        colour_group = QGroupBox("Colour Block-In")
        
        colour_layout = QVBoxLayout()
        
        colour_layout.addWidget(self.colour_selector)
        colour_layout.addWidget(self.colour_button)
        
        colour_group.setLayout(colour_layout)
        
        controls_layout.addWidget(colour_group)
        
        # Palette Extraction section
        palette_group = QGroupBox("Palette Extraction")
        
        palette_layout = QVBoxLayout()
        
        palette_layout.addWidget(self.palette_selector)
        palette_layout.addWidget(self.palette_button)
        
        palette_layout.addLayout(self.palette_layout)
        
        palette_group.setLayout(palette_layout)
        
        controls_layout.addWidget(palette_group)

        # Original image button
        controls_layout.addWidget(self.original_button)

        # Keep controls at the top of the panel
        controls_layout.addStretch()


        # Put the controls inside their own widget
        controls_widget = QWidget()
        controls_widget.setLayout(controls_layout)

        # Scrollable area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(controls_widget)
        
        main_layout.addWidget(scroll_area, 1)

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
        
    
    def show_grisaille(self):
        if not hasattr(self, "image_path"):
            return
        
        image = load_image(self.image_path)
        
        tones = self.grisaille_selector.currentData()
        
        grisaille_image = create_grisaille(image, tones=tones)
        
        qt_image = ImageQt(grisaille_image)
        
        self.current_pixmap = QPixmap.fromImage(qt_image)
        
        self.display_image()
        
        
    def show_imprimatura(self):
        if not hasattr(self, "image_path"):
            return
        
        image = load_image(self.image_path)
        
        tone = self.imprimatura_selector.currentData()
        
        imprimatura_image = create_imprimatura(image, tone=tone)
        
        qt_image = ImageQt(imprimatura_image)
        
        self.current_pixmap = QPixmap.fromImage(qt_image)
        
        self.display_image()
        
        
    def show_verdaccio(self):
        if not hasattr(self, "image_path"):
            return
        
        image = load_image(self.image_path)
        
        tones = self.verdaccio_selector.currentData()
        
        verdaccio_image = create_verdaccio(image, tones=tones)
        
        qt_image = ImageQt(verdaccio_image)
        
        self.current_pixmap = QPixmap.fromImage(qt_image)
        
        self.display_image()
        
        
    def show_colour_block(self):
        if not hasattr(self, "image_path"):
            return

        image = load_image(self.image_path)
        
        colours = self.colour_selector.currentData()
        
        block_image = create_colour_block_in(image, colours=colours)
        
        qt_image = ImageQt(block_image)
        
        self.current_pixmap = QPixmap.fromImage(qt_image)
        
        self.display_image()
        
        
    def show_palette(self):
        if not hasattr(self, "image_path"):
            return
        
        image = load_image(self.image_path)
        
        colours = self.palette_selector.currentData()
        
        palette = extract_palette(image, colours=colours)
        
        # Remove existing swatches
        while self.palette_layout.count():
            item = self.palette_layout.takeAt(0)
            
            widget = item.widget()
            
            if widget is not None:
                widget.deleteLater()
                
        # Display new palette
        for colour in palette:
            swatch = QWidget()
            
            swatch.setFixedSize(35, 35)
            
            red, green, blue = colour
            
            qt_colour = QColor(
                int(red),
                int(green),
                int(blue),
            )
            
            swatch_palette = swatch.palette()
            
            swatch_palette.setColor(
                QPalette.ColorRole.Window,
                qt_colour,
            )
            
            swatch.setPalette(swatch_palette)
            
            swatch.setAutoFillBackground(True)
            
            self.palette_layout.addWidget(swatch)
                  
        
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
    