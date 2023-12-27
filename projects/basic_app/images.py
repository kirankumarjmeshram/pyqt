import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class ImageArrayApp(QMainWindow):
    def __init__(self, image_urls):
        super().__init__()
        self.image_urls = image_urls
        self.initUI()

    def initUI(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        for image_url in self.image_urls:
            label = QLabel(self)
            pixmap = QPixmap()

            # Fetch the image from the URL and load it into the QPixmap
            response = requests.get(image_url)
            if response.status_code == 200:
                pixmap.loadFromData(response.content)
                label.setPixmap(pixmap)
                layout.addWidget(label)
            else:
                print(f"Failed to fetch image from {image_url}")

        central_widget.setLayout(layout)

        self.setWindowTitle("Image Array Viewer")
        self.setGeometry(100, 100, 800, 600)

def main(image_urls):
    app = QApplication(sys.argv)
    window = ImageArrayApp(image_urls)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    # Make a request to the API endpoint to get the list of image URLs
    api_endpoint = "http://127.0.0.1:5000/mydata/imges"  # Corrected URL
    response = requests.get(api_endpoint)

    if response.status_code == 200:
        image_urls = response.json()  # Assuming the API returns a JSON array of image URLs
        main(image_urls)
    else:
        print("Failed to fetch image URLs from the API.")
