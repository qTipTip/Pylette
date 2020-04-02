import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QFileDialog, QAction


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

        self.resize(500, 500)

    def open_image(self):
        label = QLabel(self)
        filename = QFileDialog.getOpenFileName()
        imagePath = filename[0]

        print(imagePath)


def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec_()


if __name__ == '__main__':
    sys.exit(main())
