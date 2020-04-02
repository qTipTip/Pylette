import sys

import PyQt5
from PyQt5.QtGui import QPixmap, QPainter

from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QFileDialog, QAction, QSlider, QVBoxLayout, QHBoxLayout, \
    QWidget, QPushButton, QInputDialog, QLineEdit


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

        menubar = self.menuBar()
        filemenu = menubar.addMenu('File')
        editmenu = menubar.addMenu('Edit')

        dlg = QFileDialog(self)
        openAction = QAction('Open Image', self)
        openAction.triggered.connect(self.open_image)
        filemenu.addAction(openAction)

        self.extract_button = QPushButton("Extract Colors")
        self.extract_button.setToolTip("Extracts colors using specified method")
        self.extract_button.clicked.connect(self.extract_colors)

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
        self.resize(500, 500)

    def open_image(self):
        filename = QFileDialog.getOpenFileName()
        imagePath = filename[0]
        try:
            self.image_label.setPixmap(QPixmap(imagePath))
            self.image_loaded = True

        except FileNotFoundError():
            print(f"Cannot open {imagePath}")

    def extract_colors(self):

        if not self.image_loaded:
            print("Load an Image-file first")
            return
        self.color_layout = QHBoxLayout()

        try:
            n = int(self.palette_size.text().strip())
        except:
            print("Using default of 5 colors")
            n = 5


def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec_()


if __name__ == '__main__':
    sys.exit(main())
