import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QPushButton, QTextEdit, QLabel, QTextBrowser, QWidget, QScrollArea, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class DesktopApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Desktop App')
        self.setGeometry(100, 100, 800, 600)

        # Create a central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create layout
        layout = QVBoxLayout()

        # Create a label
        label = QLabel('Enter URL:')
        layout.addWidget(label)

        # Create a text input field
        self.url_input = QTextEdit()
        layout.addWidget(self.url_input)

        # Create a button to scrape data
        scrape_button = QPushButton('Scrape Data')
        scrape_button.clicked.connect(self.scrape_data)
        layout.addWidget(scrape_button)

        # Create a button to fetch and display data
        fetch_button = QPushButton('Fetch and Display Data')
        fetch_button.clicked.connect(self.fetch_and_display_data)
        layout.addWidget(fetch_button)

        # Create a text browser to display data
        self.text_browser = QTextBrowser()
        layout.addWidget(self.text_browser)

        # Create a scroll area for images
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        layout.addWidget(self.scroll_area)

        # Create a widget to contain the images
        self.image_widget = QWidget()
        self.scroll_area.setWidget(self.image_widget)
        self.image_layout = QHBoxLayout()
        self.image_widget.setLayout(self.image_layout)

        # Set the layout for the central widget
        central_widget.setLayout(layout)

    def scrape_data(self):
        url = self.url_input.toPlainText()
        if not url:
            self.text_browser.setPlainText("Please enter a URL to scrape.")
            return

        try:
            response = requests.post('http://127.0.0.1:5000/scrape', json={"url": url})
            if response.status_code == 200:
                self.text_browser.setPlainText("Scraping successful. Data has been collected.")
            else:
                self.text_browser.setPlainText("Scraping failed. Please check the URL.")
        except Exception as e:
            self.text_browser.setPlainText(f"Error: {str(e)}")

    def fetch_and_display_data(self):
        url = self.url_input.toPlainText()
        if not url:
            self.text_browser.setPlainText("Please enter a URL to fetch data.")
            return

        try:
            response = requests.post('http://127.0.0.1:5000/mydata', json={"url": url})
            if response.status_code == 200:
                data = response.json()
                if data is None:
                    self.text_browser.setPlainText("Data not found. Please check the URL.")
                else:
                    self.text_browser.clear()
                    self.display_data(data)
            else:
                self.text_browser.setPlainText("Data retrieval failed. Please check the URL.")
        except Exception as e:
            self.text_browser.setPlainText(f"Error: {str(e)}")

    def display_data(self, data):
        title = data.get('title', 'No Title')
        self.setWindowTitle(title)
        images = data.get('images', [])
        paragraphs = data.get('paragraphs', [])
        last_updated_date = data.get('last_updated_date')

        self.text_browser.setHtml(f"<h2>{title}</h2>")

        for img_url in images:
            try:
                # Load the image using QPixmap
                pixmap = QPixmap()
                pixmap.loadFromData(requests.get(img_url).content)
                if not pixmap.isNull():
                    image_label = QLabel()
                    image_label.setPixmap(pixmap)
                    self.image_layout.addWidget(image_label)
                else:
                    self.text_browser.setPlainText(f"Error loading image: {img_url}")
            except Exception as e:
                self.text_browser.setPlainText(f"Error loading image: {str(e)}")

        for paragraph in paragraphs:
            self.text_browser.insertPlainText(paragraph)
            self.text_browser.insertPlainText("\n\n")

        self.text_browser.insertPlainText(f'Updated on = {last_updated_date["$date"][0:10]}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DesktopApp()
    window.show()
    sys.exit(app.exec())
