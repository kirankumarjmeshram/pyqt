import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QStackedWidget, QLabel
from PyQt5.QtGui import QColor, QPalette

class SwitchScreensApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Screen Switcher App")
        self.setGeometry(100, 100, 400, 300)
        
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        
        self.stacked_widget = QStackedWidget(self)
        self.layout.addWidget(self.stacked_widget)
        
        self.screen1 = QWidget()
        self.screen2 = QWidget()
        
        self.stacked_widget.addWidget(self.screen1)
        self.stacked_widget.addWidget(self.screen2)
        
        self.init_ui()
        
    def init_ui(self):
        self.screen1_text = "Screen 1"
        self.screen2_text = "Screen 2"
        
        self.screen1_button = QPushButton("Open Screen 2", self.screen1)
        self.screen1_button.clicked.connect(self.switch_to_screen2)
        
        self.screen2_button = QPushButton("Open Screen 1", self.screen2)
        self.screen2_button.clicked.connect(self.switch_to_screen1)
        
        self.layout1 = QVBoxLayout()
        self.layout2 = QVBoxLayout()
        
        self.label1 = QLabel(self.screen1_text, self.screen1)
        self.layout1.addWidget(self.label1)
        self.layout1.addWidget(self.screen1_button)
        
        self.label2 = QLabel(self.screen2_text, self.screen2)
        self.label2.setStyleSheet("color: red;")  # Set text color to red
        self.layout2.addWidget(self.label2)
        self.layout2.addWidget(self.screen2_button)
        
        self.screen1.setLayout(self.layout1)
        self.screen2.setLayout(self.layout2)
        
    def switch_to_screen2(self):
        self.stacked_widget.setCurrentIndex(1)
        
    def switch_to_screen1(self):
        self.stacked_widget.setCurrentIndex(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SwitchScreensApp()
    window.show()
    sys.exit(app.exec_())
