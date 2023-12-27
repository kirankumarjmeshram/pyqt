import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class ImageDisplayApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Image Display App')
        self.setGeometry(100, 100, 600, 400)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)

        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText("Enter Image URL")

        self.load_button = QPushButton('Load Image', self)
        self.load_button.clicked.connect(self.load_image)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.url_input)
        input_layout.addWidget(self.load_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(input_layout)
        main_layout.addWidget(self.image_label)

        self.setLayout(main_layout)

    def load_image(self):
        url = self.url_input.text()
        if not url:
            return

        try:
            response = requests.get(url)
            if response.status_code == 200:
                pixmap = QPixmap()
                pixmap.loadFromData(response.content)
                self.image_label.setPixmap(pixmap)
                self.image_label.setScaledContents(True)
            else:
                self.image_label.clear()
        except Exception as e:
            print(f"Error loading image: {str(e)}")
            self.image_label.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageDisplayApp()
    window.show()
    sys.exit(app.exec_())
