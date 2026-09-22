from painting_lab.gui import PaintingLabWindow

from PIL import Image

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QGroupBox, QScrollArea

from unittest.mock import patch


def test_window_has_correct_title():
    app = QApplication.instance()

    if app is None:
        app = QApplication([])

    window = PaintingLabWindow()

    assert window.windowTitle() == "PaintPal by Painting Lab"


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
    
    
def test_value_selector_has_correct_options():
    app = QApplication.instance()

    if app is None:
        app = QApplication([])

    window = PaintingLabWindow()

    assert window.value_selector.count() == 2

    assert window.value_selector.itemData(0) == 3
    assert window.value_selector.itemData(1) == 5
    
    
def test_value_study_uses_selected_levels(tmp_path):
    app = QApplication.instance()

    if app is None:
        app = QApplication([])

    window = PaintingLabWindow()

    image_path = tmp_path / "test.png"

    Image.new(
        "RGB",
        (50, 50),
        color=(120, 150, 180),
    ).save(image_path)

    window.image_path = str(image_path)

    window.value_selector.setCurrentIndex(0)

    with patch(
        "painting_lab.gui.create_value_study",
        return_value=Image.new("RGB", (50, 50)),
    ) as mock_transform:

        window.show_value_study()

        assert mock_transform.call_args.kwargs["levels"] == 3

    window.value_selector.setCurrentIndex(1)

    with patch(
        "painting_lab.gui.create_value_study",
        return_value=Image.new("RGB", (50, 50)),
    ) as mock_transform:

        window.show_value_study()

        assert mock_transform.call_args.kwargs["levels"] == 5
        
        
def test_gui_has_value_study_group():
    app = QApplication.instance()

    if app is None:
        app = QApplication([])

    window = PaintingLabWindow()

    groups = window.findChildren(QGroupBox)

    assert any(
        group.title() == "Value Study"
        for group in groups
    )
    

def test_line_drawing_controls_exist():
    app = QApplication.instance()

    if app is None:
        app = QApplication([])

    window = PaintingLabWindow()

    assert window.line_selector.count() == 3
    assert window.line_button.text() == "Generate Line Drawing"

    assert window.line_selector.itemData(0) == "simple"
    assert window.line_selector.itemData(1) == "detailed"
    assert window.line_selector.itemData(2) == "value_based"
    
    
def test_line_drawing_uses_selected_algorithm(tmp_path):
    app = QApplication.instance()

    if app is None:
        app = QApplication([])

    window = PaintingLabWindow()

    image_path = tmp_path / "test.png"

    Image.new(
        "RGB",
        (50, 50),
        color=(120, 150, 180),
    ).save(image_path)

    window.image_path = str(image_path)

    algorithms = [
        ("simple", "create_simple_line_drawing"),
        ("detailed", "create_detailed_line_drawing"),
        ("value_based", "create_value_based_line_drawing"),
    ]

    for selection, function_name in algorithms:

        index = window.line_selector.findData(selection)
        window.line_selector.setCurrentIndex(index)

        with patch(
            f"painting_lab.gui.{function_name}",
            return_value=Image.new("RGB", (50, 50)),
        ) as mock_algorithm:

            window.line_button.click()

            mock_algorithm.assert_called_once()

            assert not window.current_pixmap.isNull()
            
            
def test_line_drawing_without_image_does_nothing():
    app = QApplication.instance()

    if app is None:
        app = QApplication([])

    window = PaintingLabWindow()

    window.line_button.click()

    assert window.image_label.text() == "No image selected"
    assert not hasattr(window, "current_pixmap")
    
    
def test_grisaille_controls_exist():
    app = QApplication.instance()

    if app is None:
        app = QApplication([])

    window = PaintingLabWindow()

    assert window.grisaille_selector.count() == 2

    assert window.grisaille_selector.itemData(0) == 8
    assert window.grisaille_selector.itemData(1) == 16

    assert window.grisaille_button.text() == "Generate Grisaille"
    
    
def test_grisaille_uses_selected_tones(tmp_path):
    app = QApplication.instance()

    if app is None:
        app = QApplication([])

    window = PaintingLabWindow()

    # Create a temporary photograph.
    image_path = tmp_path / "test.png"

    Image.new(
        "RGB",
        (50, 50),
        color=(120, 150, 180),
    ).save(image_path)

    window.image_path = str(image_path)

    # Test both dropdown options.
    for tones in (8, 16):

        index = window.grisaille_selector.findData(
            tones
        )

        window.grisaille_selector.setCurrentIndex(
            index
        )

        with patch(
            "painting_lab.gui.create_grisaille",
            return_value=Image.new("RGB", (50, 50)),
        ) as mock_grisaille:

            window.grisaille_button.click()

            # Check that the correct number of tones
            # was passed to the algorithm.
            assert mock_grisaille.call_args.kwargs["tones"] == tones

            # Check that the preview contains an image.
            assert not window.current_pixmap.isNull()
            
            
def test_grisaille_without_image_does_nothing():
    app = QApplication.instance()

    if app is None:
        app = QApplication([])

    window = PaintingLabWindow()

    window.grisaille_button.click()

    assert window.image_label.text() == "No image selected"
    assert not hasattr(window, "current_pixmap")
    

def test_imprimatura_controls_exist():
    app = QApplication.instance()

    if app is None:
        app = QApplication([])

    window = PaintingLabWindow()

    assert window.imprimatura_selector.count() == 2

    assert window.imprimatura_selector.itemData(0) == "burnt_sienna"
    assert window.imprimatura_selector.itemData(1) == "raw_umber"

    assert window.imprimatura_button.text() == "Generate Imprimatura"
    
    
def test_imprimatura_uses_selected_tone(tmp_path):
    app = QApplication.instance()

    if app is None:
        app = QApplication([])

    window = PaintingLabWindow()

    image_path = tmp_path / "test.png"

    Image.new(
        "RGB",
        (50, 50),
        color=(120, 150, 180),
    ).save(image_path)

    window.image_path = str(image_path)

    for tone in ("burnt_sienna", "raw_umber"):

        index = window.imprimatura_selector.findData(tone)
        window.imprimatura_selector.setCurrentIndex(index)

        with patch(
            "painting_lab.gui.create_imprimatura",
            return_value=Image.new("RGB", (50, 50)),
        ) as mock_imprimatura:

            window.imprimatura_button.click()

            assert mock_imprimatura.call_args.kwargs["tone"] == tone
            assert not window.current_pixmap.isNull()
            
            
def test_verdaccio_controls_exist():
    app = QApplication.instance()

    if app is None:
        app = QApplication([])

    window = PaintingLabWindow()

    assert window.verdaccio_selector.count() == 2

    assert window.verdaccio_selector.itemData(0) == 8
    assert window.verdaccio_selector.itemData(1) == 16

    assert window.verdaccio_button.text() == "Generate Verdaccio"
    
    
def test_verdaccio_uses_selected_tones(tmp_path):
    app = QApplication.instance()

    if app is None:
        app = QApplication([])

    window = PaintingLabWindow()

    image_path = tmp_path / "test.png"

    Image.new(
        "RGB",
        (50, 50),
        color=(120, 150, 180),
    ).save(image_path)

    window.image_path = str(image_path)

    for tones in (8, 16):
        index = window.verdaccio_selector.findData(tones)
        window.verdaccio_selector.setCurrentIndex(index)

        with patch(
            "painting_lab.gui.create_verdaccio",
            return_value=Image.new("RGB", (50, 50)),
        ) as mock_verdaccio:

            window.verdaccio_button.click()

            assert mock_verdaccio.call_args.kwargs["tones"] == tones
            assert not window.current_pixmap.isNull()
            
            
def test_control_panel_is_scrollable():
    app = QApplication.instance()

    if app is None:
        app = QApplication([])

    window = PaintingLabWindow()

    scroll_areas = window.findChildren(QScrollArea)

    assert len(scroll_areas) == 1

    assert scroll_areas[0].widgetResizable()
    
    
def test_colour_block_controls_exist():
    app = QApplication.instance()

    if app is None:
        app = QApplication([])

    window = PaintingLabWindow()

    assert window.colour_selector.count() == 3

    assert window.colour_selector.itemData(0) == 5
    assert window.colour_selector.itemData(1) == 8
    assert window.colour_selector.itemData(2) == 12

    assert window.colour_button.text() == "Generate Colour Block-In"
    
    
def test_colour_block_uses_selected_colours(tmp_path):
    app = QApplication.instance()

    if app is None:
        app = QApplication([])

    window = PaintingLabWindow()

    image_path = tmp_path / "test.png"

    Image.new(
        "RGB",
        (50, 50),
        color=(120, 150, 180),
    ).save(image_path)

    window.image_path = str(image_path)

    for colours in (5, 8, 12):

        index = window.colour_selector.findData(colours)

        window.colour_selector.setCurrentIndex(index)

        with patch(
            "painting_lab.gui.create_colour_block_in",
            return_value=Image.new("RGB", (50, 50)),
        ) as mock_block:

            window.colour_button.click()

            assert mock_block.call_args.kwargs["colours"] == colours

            assert not window.current_pixmap.isNull()
            
            
def test_colour_block_without_image_does_nothing():
    app = QApplication.instance()

    if app is None:
        app = QApplication([])

    window = PaintingLabWindow()

    window.colour_button.click()

    assert window.image_label.text() == "No image selected"
    assert not hasattr(window, "current_pixmap")
    