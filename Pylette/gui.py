import sys

import PyQt5
from PyQt5.QtGui import QPixmap, QPainter

from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QFileDialog, QAction, QSlider, QVBoxLayout, QHBoxLayout, \
    QWidget


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

        self.image_label = ResizingLabel()
        self.palette_size = QSlider(PyQt5.QtCore.Qt.Horizontal)

        layout = QVBoxLayout()
        layout.addWidget(self.palette_size)
        layout.addWidget(self.image_label)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)
        self.resize(500, 500)

    def open_image(self):
        label = QLabel(self)
        filename = QFileDialog.getOpenFileName()
        imagePath = filename[0]

        self.image_label.setPixmap(QPixmap(imagePath))


def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec_()


if __name__ == '__main__':
    sys.exit(main())
