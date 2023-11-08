import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QGridLayout, QLineEdit, QMainWindow, QPushButton, QVBoxLayout, QWidget

WINDOW_SIZE = 235
DISPLAY_HEIGHT = 35
BUTTON_SIZE = 40
ERROR_MSG = "ERROR"

class PyCalcWindow(QMainWindow):
    """PyCalc's main window (GUI or view)."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyCalc")
        self.setFixedSize(WINDOW_SIZE, WINDOW_SIZE)
        self.generalLayout = QVBoxLayout()
        centralWidget = QWidget(self)
        centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(centralWidget)
        self._createDisplay()
        self._createButtons()

    def _createDisplay(self):
        self.display = QLineEdit()
        self.display.setFixedHeight(DISPLAY_HEIGHT)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)
        self.generalLayout.addWidget(self.display)

    def _createButtons(self):
        buttonsLayout = QGridLayout()
        keyBoard = [
            ["7", "8", "9", "/", "C"],
            ["4", "5", "6", "*", "("],
            ["1", "2", "3", "-", ")"],
            ["0", "00", ".", "+", "="],
        ]

        for row, keys in enumerate(keyBoard):
            for col, key in enumerate(keys):
                button = QPushButton(key)
                button.setFixedSize(BUTTON_SIZE, BUTTON_SIZE)
                buttonsLayout.addWidget(button, row, col)
                button.clicked.connect(self._buttonClicked)

        self.generalLayout.addLayout(buttonsLayout)

    def _buttonClicked(self):
        clickedButton = self.sender()
        text = clickedButton.text()

        if text == "=":
            self._calculateResult()
        elif text == "C":
            self.clearDisplay()
        else:
            self.display.setText(self.display.text() + text)

    def _calculateResult(self):
        expression = self.display.text()
        try:
            result = str(eval(expression))
        except Exception:
            result = ERROR_MSG
        self.display.setText(result)

    def clearDisplay(self):
        self.display.clear()

def main():
    """PyCalc's main function."""
    pycalcApp = QApplication([])
    pycalcWindow = PyCalcWindow()
    pycalcWindow.show()
    sys.exit(pycalcApp.exec())

if __name__ == "__main__":
    main()
