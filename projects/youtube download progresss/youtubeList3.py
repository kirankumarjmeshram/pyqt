import sys
import os
from datetime import datetime
import urllib.request
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QProgressBar
from PyQt5.QtCore import QThread, pyqtSignal
from pytube import Playlist, YouTube

class DownloadThread(QThread):
    progress_signal = pyqtSignal(int)
    total_progress_signal = pyqtSignal(int, int)

    def __init__(self, url, save_folder, is_playlist=False):
        super().__init__()
        self.url = url
        self.save_folder = save_folder
        self.is_playlist = is_playlist

    def run(self):
        try:
            if self.is_playlist:
                playlist = Playlist(self.url)
                total_videos = len(playlist.video_urls)
                for index, url in enumerate(playlist.video_urls):
                    self.download_video(url)
                    total_progress = int(((index + 1) / total_videos) * 100)
                    self.total_progress_signal.emit(index + 1, total_videos)
            else:
                self.download_video(self.url)

        except Exception as e:
            print(f"Error: {e}")

    def download_video(self, url):
        yt = YouTube(url)
        video = yt.streams.filter(file_extension="mp4", progressive=True).first()
        total_bytes = video.filesize
        downloaded_bytes = 0

        # unique name to file
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        save_path = f'downloaded_video_{timestamp}.mp4'
        save_path = os.path.join(self.save_folder, save_path)

        with urllib.request.urlopen(video.url) as response:
            with open(save_path, 'wb') as file:
                chunk_size = 1024  # 1 KB
                while True:
                    chunk = response.read(chunk_size)
                    if not chunk:
                        break
                    file.write(chunk)
                    downloaded_bytes += len(chunk)
                    progress = int((downloaded_bytes / total_bytes) * 100)
                    self.progress_signal.emit(progress)

class YouTubeDownloaderApp(QWidget):
    def __init__(self):
        super().__init__()

        self.download_thread = None  # Initialize the thread as a member variable

        self.initUI()

    def initUI(self):
        self.setWindowTitle('YouTube Downloader')
        self.setGeometry(300, 300, 400, 150)

        self.url_label = QLabel('Enter YouTube Video URL:')
        self.url_input = QLineEdit()
        self.download_button = QPushButton('Download Video')
        self.download_button.clicked.connect(self.start_download)

        self.playlist_label = QLabel('Enter YouTube Playlist URL:')
        self.playlist_input = QLineEdit()
        self.download_playlist_button = QPushButton('Download Playlist')
        self.download_playlist_button.clicked.connect(self.start_playlist_download)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)

        self.total_progress_bar = QProgressBar()
        self.total_progress_bar.setValue(0)

        self.total_progress_label = QLabel()
        self.total_progress_label.setText("0/0")

        vbox = QVBoxLayout()
        vbox.addWidget(self.url_label)
        vbox.addWidget(self.url_input)
        vbox.addWidget(self.download_button)
        vbox.addWidget(self.playlist_label)
        vbox.addWidget(self.playlist_input)
        vbox.addWidget(self.download_playlist_button)
        vbox.addWidget(self.progress_bar)
        vbox.addWidget(self.total_progress_bar)
        vbox.addWidget(self.total_progress_label)
        vbox.addStretch()

        self.setLayout(vbox)

    def start_download(self):
        if self.download_thread is not None and self.download_thread.isRunning():
            # If a thread is already running, don't start a new one
            return

        url = self.url_input.text()
        save_folder = 'videos'
        os.makedirs(save_folder, exist_ok=True)  # Create the folder if it doesn't exist

        self.download_thread = DownloadThread(url, save_folder)
        self.download_thread.progress_signal.connect(self.update_progress)
        self.download_thread.start()

    def start_playlist_download(self):
        if self.download_thread is not None and self.download_thread.isRunning():
            # If a thread is already running, don't start a new one
            return

        url = self.playlist_input.text()
        save_folder = 'playlists'
        os.makedirs(save_folder, exist_ok=True)  # Create the folder if it doesn't exist

        self.download_thread = DownloadThread(url, save_folder, is_playlist=True)
        self.download_thread.progress_signal.connect(self.update_progress)
        self.download_thread.total_progress_signal.connect(self.update_total_progress)
        self.download_thread.start()

    def update_progress(self, progress):
        self.progress_bar.setValue(progress)

    def update_total_progress(self, downloaded, total):
        self.total_progress_bar.setValue(int((downloaded / total) * 100))
        self.total_progress_label.setText(f"{downloaded}/{total}")

    def closeEvent(self, event):
        # Ensure that the thread is stopped before the application exits
        if self.download_thread is not None and self.download_thread.isRunning():
            self.download_thread.quit()
            self.download_thread.wait()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = YouTubeDownloaderApp()
    window.show()
    sys.exit(app.exec_())
