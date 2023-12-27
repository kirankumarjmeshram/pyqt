import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QTextEdit, QLineEdit, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer, Qt

class MainWindow(QWidget): # if we replace QWidget <=> QMainWindow we have to use QWidget as seen in LN 12, 13
    def __init__(self):
        super().__init__()
        self.setWindowTitle("String Printer")
        self.initUI()

    def initUI(self):
        # central_widget = QWidget(self)  # Create a central widget
        # self.setCentralWidget(central_widget)  # Set the central widget for the main window

        self.number_label = QLabel("Number:", self)
        self.number_input = QLineEdit(self)
        self.text_label = QLabel("Text:", self)
        self.text_input = QLineEdit(self)
        self.start_button = QPushButton("Start", self)
        self.start_button.clicked.connect(self.start_printing)
        self.stop_button = QPushButton("Stop", self)
        self.stop_button.clicked.connect(self.stop_printing)
        self.textbox = QTextEdit(self)

        layout = QVBoxLayout()  # Pass the central widget to the layout if we use QMainWindow like => QVBoxLayout(entral_widget)
        self.setGeometry(100, 100, 400, 400)

        layout.addWidget(self.number_label)
        layout.addWidget(self.number_input)
        layout.addWidget(self.text_label)
        layout.addWidget(self.text_input)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.textbox)  
        self.setLayout(layout)   # no need to write this when use QMainwindow
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

    # # using for loop
    # def print_hello_world(self):
    #     if self.is_printing and self.print_count > 0:
    #         text_to_print = self.text_input.text()
    #         for _ in range(self.print_count):
    #             self.textbox.append(text_to_print)
    #         self.print_count = 0
    #         self.is_printing = False
    #         self.timer.stop()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
