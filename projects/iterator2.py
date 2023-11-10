import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QLineEdit
from PyQt5.QtCore import QTimer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 400, 400)
        self.setWindowTitle("Hello World Printer")

        self.textbox = QTextEdit(self)
        self.textbox.setGeometry(50, 50, 300, 200)

        self.start_button = QPushButton("Start", self)
        self.start_button.setGeometry(50, 300, 100, 50)
        self.start_button.clicked.connect(self.start_printing)

        self.stop_button = QPushButton("Stop", self)
        self.stop_button.setGeometry(250, 300, 100, 50)
        self.stop_button.clicked.connect(self.stop_printing)

        self.number_input = QLineEdit(self)
        self.number_input.setGeometry(50, 260, 100, 30)

        self.text_input = QLineEdit(self)
        self.text_input.setGeometry(250, 260, 100, 30)

        self.timer = QTimer()
        self.timer.timeout.connect(self.print_hello_world)
        self.timer.setInterval(300)

        self.is_printing = False
        self.print_count = 0

    def start_printing(self):
        self.is_printing = True
        self.print_count = int(self.number_input.text())
        self.timer.start()

    def stop_printing(self):
        self.is_printing = False
        self.timer.stop()

    def print_hello_world(self):
        if self.is_printing and self.print_count > 0:
            self.textbox.append(self.text_input.text())
            self.print_count -= 1
        elif self.print_count == 0:
            self.is_printing = False
            self.timer.stop()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
