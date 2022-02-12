import sys

try:
    from PyQt5.QtGui import QColor, QIcon, QPainter, QPixmap
    from PyQt5.QtWidgets import (
        QAction,
        QApplication,
        QFileDialog,
        QHBoxLayout,
        QInputDialog,
        QLabel,
        QLineEdit,
        QMainWindow,
        QPushButton,
        QSlider,
        QVBoxLayout,
        QWidget,
    )
except ImportError as e:
    sys.exit(f"Unable to import PyQt: {e}")

from Pylette import extract_colors


class ResizingLabel(QWidget):
    def __init__(self, parent=None, *args, **kwargs):
        QWidget.__init__(self, parent=parent, *args, **kwargs)
        self.p = QPixmap()

    def setPixmap(self, p):
        self.p = p
        self.update()

    def paintEvent(self, event):
        if not self.p.isNull():
            painter = QPainter(self)
            painter.setRenderHint(QPainter.SmoothPixmapTransform)
            painter.drawPixmap(self.rect(), self.p)


class MainWindow(QMainWindow):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.setWindowTitle("Pylette - GUI")
        menubar = self.menuBar()
        filemenu = menubar.addMenu("File")
        option_menu = menubar.addMenu("Option")

        openAction = QAction("Open Image", self)
        openAction.triggered.connect(self.open_image)

        filemenu.addAction(openAction)

        self.extract_button = QPushButton("Extract Colors")
        self.extract_button.setToolTip("Extracts colors using specified method")
        self.extract_button.clicked.connect(self.extract_colors)
        self.extract_button.setStyleSheet("background-color: #87a0c9")

        self.image_label = ResizingLabel()
        self.image_loaded = False

        self.palette_size = QLineEdit("5")
        self.extracted_colors = QWidget()

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.extract_button)
        self.layout.addWidget(self.palette_size)
        self.layout.addWidget(self.image_label)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)

        self.setCentralWidget(self.central_widget)
        self.resize(1200, 1200)

    def open_image(self):
        filename = QFileDialog.getOpenFileName()
        image_path = filename[0]
        try:
            self.image_label.setPixmap(QPixmap(image_path))
            self.image_loaded = True
            self.image_path = image_path
        except FileNotFoundError():
            print(f"Cannot open {image_path}")

    def extract_colors(self):

        if not self.image_loaded:
            print("Load an Image-file first")
            return

        try:
            n = int(self.palette_size.text().strip())
        except:
            print("Using default of 5 colors")
            n = 5

        palette = extract_colors(
            self.image_path,
            palette_size=n,
            resize=True,
            mode="KM",
            sort_mode="luminance",
        )

        self.color_layout = QHBoxLayout()
        self.color_widget = QWidget()
        for color in palette:
            new_color_pixmap = QPixmap(10, 10)
            new_color_pixmap.fill(QColor(*color.rgb))
            new_color_container = ResizingLabel()
            new_color_container.setPixmap(new_color_pixmap)
            new_color_container.setToolTip(f"RGB: {color.rgb}")
            self.color_layout.addWidget(new_color_container)

            self.color_widget.setLayout(self.color_layout)
            self.layout.addWidget(self.color_widget)
            self.colors_extracted = True


def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec_()


if __name__ == "__main__":
    sys.exit(main())
