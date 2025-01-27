import sys
from pathlib import Path

from PIL import Image as PILImage
from PIL.ImageQt import ImageQt
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QFileDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from Pylette import Color, extract_colors
from Pylette.gui.style import get_material_style


class MaterialCard(QFrame):
    """A card-like widget with elevation shadow."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("card")
        self.setContentsMargins(16, 16, 16, 16)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)


class ImagePreviewCard(MaterialCard):
    """A card that displays the selected image preview."""

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)

        # Add a title for the preview
        title = QLabel("Image Preview")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #202020; margin-bottom: 8px;")
        layout.addWidget(title)

        # Create a scroll area for the image
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar {
                background-color: #f5f5f5;
                border-radius: 4px;
            }
            QScrollBar::handle {
                background-color: #6200ee;
                border-radius: 2px;
            }
        """)

        # Create the image label
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        scroll.setWidget(self.image_label)

        layout.addWidget(scroll)

    def set_image(self, image_path: str):
        """Load and display an image, scaling it appropriately."""
        try:
            # Load the image using PIL first (this ensures better format support)
            pil_image = PILImage.open(image_path)

            # Convert PIL image to QImage
            qim = ImageQt(pil_image)
            pixmap = QPixmap.fromImage(qim)

            # Scale the image to fit the preview area while maintaining aspect ratio
            scaled_pixmap = pixmap.scaled(
                300,
                300,  # Target size
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )

            # Update the label with the scaled image
            self.image_label.setPixmap(scaled_pixmap)

        except Exception as e:
            print(f"Error loading image preview: {e}")
            self.image_label.setText("Error loading image preview")


class ColorButton(QPushButton):
    def __init__(self, color: Color, parent=None):
        super().__init__(parent)
        self.setObjectName("colorButton")  # For specific styling
        self.setColor(color)
        self.clicked.connect(self.copyColor)

    def setColor(self, color: Color):
        self.color = color
        r, g, b = color.rgb

        # Calculate contrasting text color for the tooltip
        luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
        text_color = "black" if luminance > 0.5 else "white"

        self.setStyleSheet(f"""
            QPushButton#colorButton {{
                background-color: rgb({r},{g},{b});
                color: {text_color};
            }}
            QPushButton#colorButton:hover {{
                border: 2px solid #6200ee;
            }}
        """)

        # Enhanced tooltip with color information
        tooltip = f"""
        <div style='font-family: Arial; padding: 8px;'>
            <div style='margin-bottom: 8px;'><b>Color Values</b></div>
            <div>RGB: {r}, {g}, {b}</div>
            <div>HEX: #{r:02x}{g:02x}{b:02x}</div>
            <div>Frequency: {color.freq:.2%}</div>
            <div style='margin-top: 8px; font-size: 0.9em;'>Click to copy</div>
        </div>
        """
        self.setToolTip(tooltip)

    def copyColor(self):
        r, g, b = self.color.rgb
        formats = {
            "RGB": f"rgb({r}, {g}, {b})",
            "HEX": f"#{r:02x}{g:02x}{b:02x}",
            "HSV": f"hsv({self.color.hsv[0]:.3f}, {self.color.hsv[1]:.3f}, {self.color.hsv[2]:.3f})",
        }

        QApplication.clipboard().setText(formats["RGB"])

        msg = QMessageBox(self)
        msg.setWindowTitle("Color Copied!")
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setText("Color values copied to clipboard")
        msg.setInformativeText("\n".join(f"{fmt}: {val}" for fmt, val in formats.items()))
        msg.setStyleSheet(get_material_style())
        msg.exec()


class PyletteGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Pylette Color Extractor")
        self.setMinimumWidth(800)  # Increased to accommodate preview
        self.setStyleSheet(get_material_style())

        # Create central widget with main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(24)
        main_layout.setContentsMargins(24, 24, 24, 24)

        # Create a horizontal layout for control panel and image preview
        top_layout = QHBoxLayout()
        top_layout.setSpacing(24)

        # Create control card
        control_card = MaterialCard()
        control_layout = QVBoxLayout(control_card)
        control_layout.setSpacing(16)

        # Title
        title = QLabel("Pylette Color Extractor")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #202020; margin-bottom: 16px;")
        control_layout.addWidget(title)

        # File selection area
        file_layout = QHBoxLayout()
        self.file_btn = QPushButton("Select Image")
        self.file_btn.clicked.connect(self.selectFile)
        file_layout.addWidget(self.file_btn)
        file_layout.addStretch()
        control_layout.addLayout(file_layout)

        # Settings grid
        settings_layout = QGridLayout()
        settings_layout.setSpacing(16)

        # Number of colors
        settings_layout.addWidget(QLabel("Number of colors:"), 0, 0)
        self.color_count = QSpinBox()
        self.color_count.setRange(1, 20)
        self.color_count.setValue(5)
        settings_layout.addWidget(self.color_count, 0, 1)

        # Algorithm selection
        settings_layout.addWidget(QLabel("Algorithm:"), 0, 2)
        self.algo_select = QComboBox()
        self.algo_select.addItems(["K-Means", "Median Cut"])
        settings_layout.addWidget(self.algo_select, 0, 3)

        # Sort mode selection
        settings_layout.addWidget(QLabel("Sort by:"), 1, 0)
        self.sort_select = QComboBox()
        self.sort_select.addItems(["Frequency", "Luminance", "None"])
        settings_layout.addWidget(self.sort_select, 1, 1)

        control_layout.addLayout(settings_layout)

        # Extract button
        self.extract_btn = QPushButton("Extract Colors")
        self.extract_btn.clicked.connect(self.extractColors)
        self.extract_btn.setEnabled(False)
        control_layout.addWidget(self.extract_btn)

        # Add control card to top layout
        top_layout.addWidget(control_card)

        # Create and add image preview card
        self.preview_card = ImagePreviewCard()
        top_layout.addWidget(self.preview_card)

        # Add top layout to main layout
        main_layout.addLayout(top_layout)

        # Create results card
        results_card = MaterialCard()
        results_layout = QVBoxLayout(results_card)

        # Results title
        results_title = QLabel("Extracted Colors")
        results_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #202020; margin-bottom: 8px;")
        results_layout.addWidget(results_title)

        # Color grid
        self.color_grid = QGridLayout()
        self.color_grid.setSpacing(8)
        results_layout.addLayout(self.color_grid)

        main_layout.addWidget(results_card)

        self.selected_file = None

    def selectFile(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, "Select Image", str(Path.home()), "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        if filename:
            self.selected_file = filename
            self.file_btn.setText(Path(filename).name)
            self.extract_btn.setEnabled(True)
            # Update the image preview
            self.preview_card.set_image(filename)

    def extractColors(self):
        if not self.selected_file:
            return

        while self.color_grid.count():
            item = self.color_grid.takeAt(0)
            if item and item.widget():
                item.widget().deleteLater()

        try:
            mode = "KM" if self.algo_select.currentText() == "K-Means" else "MC"
            sort_mode = self.sort_select.currentText().lower()
            if sort_mode == "none":
                sort_mode = None

            palette = extract_colors(
                self.selected_file, palette_size=self.color_count.value(), mode=mode, sort_mode=sort_mode
            )

            num_colors = len(palette)
            cols = min(5, num_colors)
            rows = (num_colors + cols - 1) // cols

            for i, color in enumerate(palette.colors):
                row = i // cols
                col = i % cols
                button = ColorButton(color)
                self.color_grid.addWidget(button, row, col)

        except Exception as e:
            msg = QMessageBox()
            msg.setStyleSheet(get_material_style())
            msg.critical(
                self,
                "Error",
                f"Failed to extract colors: {str(e)}\n\n" "Please make sure the selected file is a valid image.",
            )


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # Base style for consistency

    gui = PyletteGUI()
    gui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
