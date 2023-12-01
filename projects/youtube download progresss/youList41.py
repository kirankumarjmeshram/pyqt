import sys
import os
import urllib.request
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QProgressBar, QComboBox
from PyQt5.QtCore import QThread, pyqtSignal
from pytube import YouTube, Playlist

class DownloadThread(QThread):
    progress_signal = pyqtSignal(int, str)  # Updated signal to include the video title

    def __init__(self, playlist_url, resolution, save_folder):
        super().__init__()
        self.playlist_url = playlist_url
        self.resolution = resolution
        self.save_folder = save_folder

    def run(self):
        try:
            playlist = Playlist(self.playlist_url)
            videos = playlist.video_urls

            for video_url in videos:
                yt = YouTube(video_url)
                video = yt.streams.filter(file_extension="mp4", resolution=self.resolution).first()

                save_path = os.path.join(self.save_folder, f'{yt.title}.mp4')

                with urllib.request.urlopen(video.url) as response:
                    with open(save_path, 'wb') as file:
                        total_bytes = int(response.info()['Content-Length'])
                        downloaded_bytes = 0
                        chunk_size = 1024  # 1 KB
                        while True:
                            chunk = response.read(chunk_size)
                            if not chunk:
                                break
                            file.write(chunk)
                            downloaded_bytes += len(chunk)
                            progress = int((downloaded_bytes / total_bytes) * 100)
                            # Emit both progress and video title
                            self.progress_signal.emit(progress, yt.title)

        except Exception as e:
            print(f"Error: {e}")

class YouTubeDownloaderApp(QWidget):
    def __init__(self):
        super().__init__()

        self.download_thread = None  # Initialize the thread as a member variable

        self.initUI()

    def initUI(self):
        self.setWindowTitle('YouTube Playlist Downloader')
        self.setGeometry(300, 300, 500, 200)

        self.playlist_label = QLabel('Enter YouTube Playlist URL:')
        self.playlist_input = QLineEdit()

        self.resolution_label = QLabel('Select Resolution:')
        self.resolution_combo = QComboBox()
        self.resolution_combo.addItems(['720p', '480p', '360p', '240p'])

        self.download_button = QPushButton('Download Playlist')
        self.download_button.clicked.connect(self.start_download)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)

        self.current_video_label = QLabel('Current Video: ')

        vbox = QVBoxLayout()
        vbox.addWidget(self.playlist_label)
        vbox.addWidget(self.playlist_input)
        vbox.addWidget(self.resolution_label)
        vbox.addWidget(self.resolution_combo)
        vbox.addWidget(self.current_video_label)
        vbox.addWidget(self.progress_bar)
        vbox.addWidget(self.download_button)
        vbox.addStretch()

        self.setLayout(vbox)

    def start_download(self):
        if self.download_thread is not None and self.download_thread.isRunning():
            # If a thread is already running, don't start a new one
            return

        playlist_url = self.playlist_input.text()
        resolution = self.resolution_combo.currentText()
        save_folder = 'playlist_videos'

        os.makedirs(save_folder, exist_ok=True)  # Create the folder if it doesn't exist

        self.download_thread = DownloadThread(playlist_url, resolution, save_folder)
        self.download_thread.progress_signal.connect(self.update_progress)
        self.download_thread.start()

    def update_progress(self, progress, video_title):
        self.progress_bar.setValue(progress)
        self.current_video_label.setText(f'Current Video: {video_title} downloading')

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
