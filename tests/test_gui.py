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
    