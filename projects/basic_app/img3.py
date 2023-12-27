import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QTextBrowser
from urllib.parse import urlparse
import base64
import warnings

# Suppress DeprecationWarning
warnings.filterwarnings("ignore", category=DeprecationWarning)

class Abc(QWidget):
    def __init__(self):
        super().__init__()

        self.url = ''
        self.data = None

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.setWindowTitle('Scrape and View Data')
        self.setGeometry(100, 100, 400, 400)

        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText('Enter URL')
        self.url_input.textChanged.connect(self.updateUrl)

        self.scrape_button = QPushButton('Scrape', self)
        self.scrape_button.clicked.connect(self.fetchData)

        self.show_info_button = QPushButton('Show Info', self)
        self.show_info_button.clicked.connect(self.showInfo)

        self.image_view = QTextBrowser(self)
        self.image_view.setOpenExternalLinks(True)

        layout.addWidget(self.url_input)
        layout.addWidget(self.scrape_button)
        layout.addWidget(self.show_info_button)
        layout.addWidget(self.image_view)

        self.setLayout(layout)

    def updateUrl(self, text):
        self.url = text

    def is_valid_url(self, url):
        parsed_url = urlparse(url)
        return parsed_url.scheme in ('http', 'https') and parsed_url.netloc

    def fetchData(self):
        if not self.is_valid_url(self.url):
            print("Invalid URL. Please enter a valid URL with 'http://' or 'https://'.")
            return

        try:
            response = requests.post('http://127.0.0.1:5000/scrape', json={'url': self.url})
            response.raise_for_status()
        except requests.exceptions.RequestException as error:
            print(error)
        else:
            print(response.text)

    def showInfo(self):
        if not self.is_valid_url(self.url):
            print("Invalid URL. Please enter a valid URL with 'http://' or 'https'.")
            return

        try:
            response = requests.post('http://127.0.0.1:5000/mydata', json={'url': self.url})
            response.raise_for_status()

            if response.json() is None:
                print("Data not found. Please scrape the data.")
            else:
                self.data = response.json()
                self.displayImages()

        except requests.exceptions.RequestException as error:
            print(error)

    def displayImages(self):
        if self.data:
            self.image_view.clear()

            for index, img_url in enumerate(self.data.get('images', [])):
                if img_url.startswith("data:image"):
                    # Data URL format
                    img_html = f'<img src="{img_url}" alt="Img {index}" style="max-width:100%; max-height:100%;"/>'
                elif img_url.startswith("/"):
                    # Relative path
                    # You may need to construct the full URL based on your application's logic
                    img_html = f'<img src="https://your_base_url{img_url}" alt="Img {index}" style="max-width:100%; max-height:100%;"/>'
                else:
                    # Assume it's a valid URL (http or https)
                    img_html = f'<img src="{img_url}" alt="Img {index}" style="max-width:100%; max-height:100%;"/>'

                self.image_view.insertHtml(img_html)

def main():
    app = QApplication(sys.argv)
    window = Abc()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
