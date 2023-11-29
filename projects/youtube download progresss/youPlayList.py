import sys
import os
from datetime import datetime
import urllib.request
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QProgressBar, QCheckBox
from PyQt5.QtCore import QThread, pyqtSignal
from pytube import YouTube, Playlist

class DownloadThread(QThread):
    progress_signal = pyqtSignal(int)

    def __init__(self, url, save_path, is_playlist):
        super().__init__()
        self.url = url
        self.save_path = save_path
        self.is_playlist = is_playlist

    def run(self):
        try:
            if self.is_playlist:
                self.download_playlist()
            else:
                self.download_video_info()

        except Exception as e:
            print(f"Error: {e}")

    def download_playlist(self):
        playlist = Playlist(self.url)
        playlist_title = self.clean_filename(playlist.title())
        playlist_folder_path = os.path.join(os.getcwd(), 'downloads', playlist_title)
        os.makedirs(playlist_folder_path, exist_ok=True)

        for video_url in playlist.video_urls:
            self.url = video_url
            self.download_video_info(playlist_folder_path)

    def download_video_info(self, folder_path):
        yt = YouTube(self.url)
        total_bytes = yt.streams.filter(file_extension="mp4", progressive=True).first().filesize
        downloaded_bytes = 0

        with urllib.request.urlopen(yt.streams.filter(file_extension="mp4", progressive=True).first().url) as response:
            video_title = self.clean_filename(yt.title)
            save_path = os.path.join(folder_path, f'{video_title}.mp4')
            with open(save_path, 'ab') as file:
                chunk_size = 1024
                while True:
                    chunk = response.read(chunk_size)
                    if not chunk:
                        break
                    file.write(chunk)
                    downloaded_bytes += len(chunk)
                    progress = int((downloaded_bytes / total_bytes) * 100)
                    self.progress_signal.emit(progress)

    def clean_filename(self, name):
        return "".join(c for c in name if c.isalnum() or c in (' ', '-', '_'))

class YouTubeDownloaderApp(QWidget):
    def __init__(self):
        super().__init__()

        self.download_thread = None
        self.is_playlist = False

        self.initUI()

    def initUI(self):
        self.setWindowTitle('YouTube Downloader')
        self.setGeometry(300, 300, 400, 200)

        self.url_label = QLabel('Enter YouTube URL:')
        self.url_input = QLineEdit()
        self.download_button = QPushButton('Download')
        self.download_button.clicked.connect(self.start_download)

        self.playlist_checkbox = QCheckBox('Download Playlist')
        self.playlist_checkbox.stateChanged.connect(self.toggle_playlist_mode)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)

        vbox = QVBoxLayout()
        vbox.addWidget(self.url_label)
        vbox.addWidget(self.url_input)
        vbox.addWidget(self.playlist_checkbox)
        vbox.addWidget(self.progress_bar)
        vbox.addWidget(self.download_button)
        vbox.addStretch()

        self.setLayout(vbox)

    def start_download(self):
        if self.download_thread is not None and self.download_thread.isRunning():
            return

        url = self.url_input.text()
        save_folder = 'downloads'
        os.makedirs(save_folder, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        if self.is_playlist:
            save_path = os.path.join(save_folder, f'downloaded_playlist_{timestamp}.mp4')
        else:
            save_path = os.path.join(save_folder, f'downloaded_video_{timestamp}.mp4')

        self.download_thread = DownloadThread(url, save_path, self.is_playlist)
        self.download_thread.progress_signal.connect(self.update_progress)
        self.download_thread.start()

    def update_progress(self, progress):
        self.progress_bar.setValue(progress)

    def toggle_playlist_mode(self, state):
        self.is_playlist = state == 2

    def closeEvent(self, event):
        if self.download_thread is not None and self.download_thread.isRunning():
            self.download_thread.quit()
            self.download_thread.wait()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = YouTubeDownloaderApp()
    window.show()
    sys.exit(app.exec_())
