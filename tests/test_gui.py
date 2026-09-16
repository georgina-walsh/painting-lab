from PIL import Image
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication

from painting_lab.gui import PaintingLabWindow


def test_window_has_correct_title():
    app = QApplication.instance()

    if app is None:
        app = QApplication([])

    window = PaintingLabWindow()

    assert window.windowTitle() == "Painting Lab"


def test_window_has_open_image_button():
    app = QApplication.instance()

    if app is None:
        app = QApplication([])

    window = PaintingLabWindow()

    assert window.open_button.text() == "Open Image"


def test_window_starts_without_image():
    app = QApplication.instance()

    if app is None:
        app = QApplication([])

    window = PaintingLabWindow()

    assert window.image_label.text() == "No image selected"
    
    
def test_window_has_value_study_button():
    app = QApplication.instance()

    if app is None:
        app = QApplication([])

    window = PaintingLabWindow()

    assert window.value_button.text() == "Value Study"
    
    
def test_window_has_value_study_method():
    app = QApplication.instance()

    if app is None:
        app = QApplication([])

    window = PaintingLabWindow()

    assert callable(window.show_value_study)
    
    
def test_display_image_does_not_replace_original():
    app = QApplication.instance()

    if app is None:
        app = QApplication([])

    window = PaintingLabWindow()

    window.original_pixmap = QPixmap(100, 100)
    window.current_pixmap = QPixmap(50, 50)

    window.display_image()

    assert window.original_pixmap.size().width() == 100
    assert window.current_pixmap.size().width() == 50
    

def test_show_original_restores_original_pixmap():
    app = QApplication.instance()

    if app is None:
        app = QApplication([])

    window = PaintingLabWindow()

    window.original_pixmap = QPixmap(100, 100)
    window.current_pixmap = QPixmap(50, 50)

    window.show_original()

    assert window.current_pixmap is window.original_pixmap
    
    
def test_value_study_updates_display(tmp_path):
    app = QApplication.instance()

    if app is None:
        app = QApplication([])

    window = PaintingLabWindow()

    # Create a temporary test image.
    image_path = tmp_path / "test_image.png"

    image = Image.new(
        "RGB",
        (100, 100),
        color=(120, 150, 180),
    )

    image.save(image_path)

    # Simulate an image having been opened.
    window.image_path = str(image_path)

    # Run the actual Value Study method.
    window.show_value_study()

    # Check that an image was produced.
    assert not window.current_pixmap.isNull()
    