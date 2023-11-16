import sys
import os
import urllib.request
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QProgressBar, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QThread, pyqtSignal, QUrl
from pytube import YouTube
from datetime import datetime

class DownloadThread(QThread):
    progress_signal = pyqtSignal(int)

    def __init__(self, url, save_path):
        super().__init__()
        self.url = url
        self.save_path = save_path

    def run(self):
        try:
            yt = YouTube(self.url)
            video = yt.streams.filter(file_extension="mp4", progressive=True).first()
            total_bytes = video.filesize
            downloaded_bytes = 0

            with urllib.request.urlopen(video.url) as response:
                with open(self.save_path, 'wb') as file:
                    chunk_size = 1024  # 1 KB
                    while True:
                        chunk = response.read(chunk_size)
                        if not chunk:
                            break
                        file.write(chunk)
                        downloaded_bytes += len(chunk)
                        progress = int((downloaded_bytes / total_bytes) * 100)
                        self.progress_signal.emit(progress)

        except Exception as e:
            print(f"Error: {e}")

class YouTubeDownloaderApp(QWidget):
    def __init__(self):
        super().__init__()

        self.download_thread = None
        self.downloaded_files = []
        self.video_player = None
        self.video_widget = None

        self.initUI()

    def initUI(self):
        self.setWindowTitle('YouTube Downloader')
        self.setGeometry(300, 300, 800, 600)

        self.url_label = QLabel('Enter YouTube Video URL:')
        self.url_input = QLineEdit()
        self.download_button = QPushButton('Download')
        self.download_button.clicked.connect(self.start_download)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)

        self.downloaded_table = QTableWidget()
        self.downloaded_table.setColumnCount(2)
        self.downloaded_table.setHorizontalHeaderLabels(['Video', 'File Name'])
        self.downloaded_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.downloaded_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.downloaded_table.itemClicked.connect(self.play_video)

        vbox = QVBoxLayout()
        vbox.addWidget(self.url_label)
        vbox.addWidget(self.url_input)
        vbox.addWidget(self.download_button)
        vbox.addWidget(self.progress_bar)
        vbox.addWidget(self.downloaded_table)
        vbox.addStretch()

        self.setLayout(vbox)

    def start_download(self):
        if self.download_thread is not None and self.download_thread.isRunning():
            return

        url = self.url_input.text()
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        save_path = f'downloaded_video_{timestamp}.mp4'

        self.download_thread = DownloadThread(url, save_path)
        self.download_thread.progress_signal.connect(self.update_progress)
        self.download_thread.finished.connect(self.add_to_downloaded_table)
        self.download_thread.start()

    def update_progress(self, progress):
        self.progress_bar.setValue(progress)

    def add_to_downloaded_table(self):
        video_name = self.url_input.text()
        file_name = os.path.basename(self.download_thread.save_path)
        self.downloaded_files.append((video_name, file_name))

        row_position = self.downloaded_table.rowCount()
        self.downloaded_table.insertRow(row_position)
        self.downloaded_table.setItem(row_position, 0, QTableWidgetItem(video_name))
        self.downloaded_table.setItem(row_position, 1, QTableWidgetItem(file_name))

    def play_video(self, item):
        video_name = item.text()
        selected_file = next((file[1] for file in self.downloaded_files if file[0] == video_name), None)
        if selected_file is not None:
            file_path = os.path.join(os.getcwd(), selected_file)

            if self.video_player is None:
                self.video_player = QMediaPlayer()
                self.video_widget = QVideoWidget()
                self.video_player.setVideoOutput(self.video_widget)

            media_content = QMediaContent(QUrl.fromLocalFile(file_path))
            self.video_player.setMedia(media_content)
            self.video_player.play()

    def closeEvent(self, event):
        if self.download_thread is not None and self.download_thread.isRunning():
            self.download_thread.quit()
            self.download_thread.wait()

        if self.video_player is not None:
            self.video_player.stop()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = YouTubeDownloaderApp()
    window.show()
    sys.exit(app.exec_())
