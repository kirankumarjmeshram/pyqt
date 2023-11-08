# main_window.py

"""Main window-style application."""

import sys

from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QStatusBar,
    QToolBar,
)

class Window(QMainWindow):
    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("QMainWindow")
        self.setCentralWidget(QLabel("I'm the Central Widget"))
        self._createMenu()
        self._createToolBar()
        self._createStatusBar()

    def _createMenu(self):
        menu = self.menuBar().addMenu("&Menu")
        menu.addAction("&Exit", self.close)

    def _createToolBar(self):
        tools = QToolBar()
        tools.addAction("Exit", self.close)
        self.addToolBar(tools)

    def _createStatusBar(self):
        status = QStatusBar(self)
        status.showMessage("I'm the Status Bar")
        self.setStatusBar(status)

    # def _createStatusBar(self):
    #     self.statusbar = self.statusBar()
    #     # Adding a temporary message
    #     self.statusbar.showMessage("Ready")

    # def _createStatusBar(self):
    #     self.setStatusBar(QStatusBar(self))
    #     self.statusBar().showMessage("I'm the Status Bar")

    

if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    sys.exit(app.exec())